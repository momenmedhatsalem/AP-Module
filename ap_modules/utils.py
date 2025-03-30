"""
The goal of this file is to add some methods from requests and base64 libs to Server Script NameSpaces
"""

import frappe

from frappe.model.document import Document
from frappe import _
import json
import mimetypes
import inspect
import base64
import requests

from frappe.utils.safe_exec import (
    get_safe_globals,
    is_safe_exec_enabled,
    safe_exec,
    ServerScriptNotEnabled,
    SERVER_SCRIPT_FILE_PREFIX,
    safe_exec_flags,
    patched_qb,
    FrappeTransformer,
    call_whitelisted_function,
    FrappePrintCollector,
    NamespaceDict,
    add_data_utils,
    add_module_properties,
    get_hooks,
    safe_enqueue,
    read_sql,
    _write,
    run_script,
    is_job_queued,
    _getitem,
    _getattr_for_safe_exec,
    get_python_builtins
)


import RestrictedPython.Guards
from RestrictedPython import compile_restricted, safe_globals


from frappe.core.utils import html2text
from frappe.frappeclient import FrappeClient
from frappe.model.delete_doc import delete_doc
from frappe.model.mapper import get_mapped_doc
from frappe.model.rename_doc import rename_doc
from frappe.modules import scrub
from frappe.website.utils import get_next_link, get_toc
from frappe.www.printview import get_visible_columns


def safe_exec(
        script: str,
        _globals: dict | None = None,
        _locals: dict | None = None,
        *,
        restrict_commit_rollback: bool = False,
        script_filename: str | None = None,
):
    if not is_safe_exec_enabled():
        msg = _(
            "Server Scripts are disabled. Please enable server scripts from bench configuration.")
        docs_cta = _("Read the documentation to know more")
        msg += f"<br><a href='https://frappeframework.com/docs/user/en/desk/scripting/server-script'>{docs_cta}</a>"
        frappe.throw(msg, ServerScriptNotEnabled,
                     title="Server Scripts Disabled")

    # build globals
    exec_globals = get_safe_globals()
    if _globals:
        exec_globals.update(_globals)

    if restrict_commit_rollback:
        # prevent user from using these in docevents
        exec_globals.frappe.db.pop("commit", None)
        exec_globals.frappe.db.pop("rollback", None)
        exec_globals.frappe.db.pop("add_index", None)

    filename = SERVER_SCRIPT_FILE_PREFIX
    if script_filename:
        filename += f": {frappe.scrub(script_filename)}"

    with safe_exec_flags(), patched_qb():
        # execute script compiled by RestrictedPython
        exec(
            compile_restricted(script, filename=filename,
                               policy=FrappeTransformer),
            exec_globals,
            _locals,
        )

    return exec_globals, _locals


def encode_base64(data):
    return base64.b64encode(data.encode()).decode()


def decode_base64(data):
    return base64.b64decode(data).decode()


def requests_get(url, **kwargs):
    return requests.get(url, **kwargs)


def requests_post(url, data=None, json=None, **kwargs):
    return requests.post(url, data=data, json=json, **kwargs)


def requests_put(url, data=None, json=None, **kwargs):
    return requests.put(url, data=data, json=json, **kwargs)


def requests_session():
    return requests.Session()


def get_safe_globals():
    datautils = frappe._dict()

    if frappe.db:
        date_format = frappe.db.get_default("date_format") or "yyyy-mm-dd"
        time_format = frappe.db.get_default("time_format") or "HH:mm:ss"
    else:
        date_format = "yyyy-mm-dd"
        time_format = "HH:mm:ss"

    add_data_utils(datautils)

    form_dict = getattr(frappe.local, "form_dict", frappe._dict())

    if "_" in form_dict:
        del frappe.local.form_dict["_"]

    user = getattr(frappe.local, "session",
                   None) and frappe.local.session.user or "Guest"

    out = NamespaceDict(
        # make available limited methods of frappe
        json=NamespaceDict(loads=json.loads, dumps=json.dumps),
        as_json=frappe.as_json,
        dict=dict,
        log=frappe.log,
        _dict=frappe._dict,
        args=form_dict,
        frappe=NamespaceDict(
            call=call_whitelisted_function,
            flags=frappe._dict(),
            format=frappe.format_value,
            format_value=frappe.format_value,
            date_format=date_format,
            time_format=time_format,
            format_date=frappe.utils.data.global_date_format,
            form_dict=form_dict,
            bold=frappe.bold,
            copy_doc=frappe.copy_doc,
            errprint=frappe.errprint,
            qb=frappe.qb,
            get_meta=frappe.get_meta,
            new_doc=frappe.new_doc,
            get_doc=frappe.get_doc,
            get_mapped_doc=get_mapped_doc,
            get_last_doc=frappe.get_last_doc,
            get_cached_doc=frappe.get_cached_doc,
            get_list=frappe.get_list,
            get_all=frappe.get_all,
            get_system_settings=frappe.get_system_settings,
            rename_doc=rename_doc,
            delete_doc=delete_doc,
            utils=datautils,
            get_url=frappe.utils.get_url,
            render_template=frappe.render_template,
            msgprint=frappe.msgprint,
            throw=frappe.throw,
            sendmail=frappe.sendmail,
            get_print=frappe.get_print,
            attach_print=frappe.attach_print,
            user=user,
            get_fullname=frappe.utils.get_fullname,
            get_gravatar=frappe.utils.get_gravatar_url,
            full_name=frappe.local.session.data.full_name
            if getattr(frappe.local, "session", None)
            else "Guest",
            request=getattr(frappe.local, "request", {}),
            session=frappe._dict(
                user=user,
                csrf_token=frappe.local.session.data.csrf_token
                if getattr(frappe.local, "session", None)
                else "",
            ),

            # The necessary methods to be added to the NameSpace
            encode_base64=encode_base64,
            decode_base64=decode_base64,
            requests_get=requests_get,
            post=requests_post,
            put=requests_put,
            requests_session=requests_session,


            make_get_request=frappe.integrations.utils.make_get_request,
            make_post_request=frappe.integrations.utils.make_post_request,
            make_put_request=frappe.integrations.utils.make_put_request,
            make_patch_request=frappe.integrations.utils.make_patch_request,
            make_delete_request=frappe.integrations.utils.make_delete_request,
            socketio_port=frappe.conf.socketio_port,
            get_hooks=get_hooks,
            enqueue=safe_enqueue,
            sanitize_html=frappe.utils.sanitize_html,
            log_error=frappe.log_error,
            log=frappe.log,
            db=NamespaceDict(
                get_list=frappe.get_list,
                get_all=frappe.get_all,
                get_value=frappe.db.get_value,
                set_value=frappe.db.set_value,
                get_single_value=frappe.db.get_single_value,
                get_default=frappe.db.get_default,
                exists=frappe.db.exists,
                count=frappe.db.count,
                escape=frappe.db.escape,
                sql=read_sql,
                commit=frappe.db.commit,
                rollback=frappe.db.rollback,
                after_commit=frappe.db.after_commit,
                before_commit=frappe.db.before_commit,
                after_rollback=frappe.db.after_rollback,
                before_rollback=frappe.db.before_rollback,
                add_index=frappe.db.add_index,
            ),
            lang=getattr(frappe.local, "lang", "en"),
        ),
        FrappeClient=FrappeClient,
        style=frappe._dict(border_color="#d1d8dd"),
        get_toc=get_toc,
        get_next_link=get_next_link,
        _=frappe._,
        scrub=scrub,
        guess_mimetype=mimetypes.guess_type,
        html2text=html2text,
        dev_server=frappe.local.dev_server,
        run_script=run_script,
        is_job_queued=is_job_queued,
        get_visible_columns=get_visible_columns,
    )

    add_module_properties(
        frappe.exceptions, out.frappe, lambda obj: inspect.isclass(
            obj) and issubclass(obj, Exception)
    )

    if frappe.response:
        out.frappe.response = frappe.response

    out.update(safe_globals)

    # default writer allows write access
    out._write_ = _write
    out._getitem_ = _getitem
    out._getattr_ = _getattr_for_safe_exec

    # Allow using `print()` calls with `safe_exec()`
    out._print_ = FrappePrintCollector

    # allow iterators and list comprehension
    out._getiter_ = iter
    out._iter_unpack_sequence_ = RestrictedPython.Guards.guarded_iter_unpack_sequence

    # add common python builtins
    out.update(get_python_builtins())

    return out
