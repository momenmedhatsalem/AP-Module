import frappe
from itertools import chain
from frappe.core.doctype.server_script.server_script import ServerScript
from frappe.model.document import Document
from frappe import _
from functools import partial
from frappe.rate_limiter import rate_limit

from frappe.utils.safe_exec import (
    get_keys_for_autocomplete
)

from ..utils import safe_exec, get_safe_globals


class CustomServerScript(ServerScript):

    def execute_doc(self, doc: Document):
        """Specific to Document Event triggered Server Scripts

        Args:
                doc (Document): Executes script with for a certain document's events
        """
        safe_exec(
            self.script,
            _locals={"doc": doc},
            restrict_commit_rollback=True,
            script_filename=self.name,
        )

    @frappe.whitelist()
    def get_autocompletion_items(self):
        """Generates a list of a autocompletion strings from the context dict
        that is used while executing a Server Script.

        Returns:
                list: Returns list of autocompletion items.
                For e.g., ["frappe.utils.cint", "frappe.get_all", ...]
        """

        return frappe.cache.get_value(
            "server_script_autocompletion_items",
            generator=lambda: list(
                chain.from_iterable(
                    get_keys_for_autocomplete(key, value, meta="utils")
                    for key, value in get_safe_globals().items()
                ),
            ),
        )

    def execute_method(self) -> dict:
        """Specific to API endpoint Server Scripts

        Raises:
                frappe.DoesNotExistError: If self.script_type is not API
                frappe.PermissionError: If self.allow_guest is unset for API accessed by Guest user

        Returns:
                dict: Evaluates self.script with frappe.utils.safe_exec.safe_exec and returns the flags set in it's safe globals
        """

        if self.enable_rate_limit:
            # Wrap in rate limiter, required for specifying custom limits for each script
            # Note that rate limiter works on `cmd` which is script name
            limit = self.rate_limit_count or 5
            seconds = self.rate_limit_seconds or 24 * 60 * 60

            _fn = partial(execute_api_server_script, script=self)
            return rate_limit(limit=limit, seconds=seconds)(_fn)()
        else:
            return execute_api_server_script(self)

    def execute_scheduled_method(self):
        """Specific to Scheduled Jobs via Server Scripts

        Raises:
                frappe.DoesNotExistError: If script type is not a scheduler event
        """
        if self.script_type != "Scheduler Event":
            raise frappe.DoesNotExistError

        safe_exec(self.script, script_filename=self.name)

    def get_permission_query_conditions(self, user: str) -> list[str]:
        """Specific to Permission Query Server Scripts

        Args:
                user (str): Takes user email to execute script and return list of conditions

        Returns:
                list: Returns list of conditions defined by rules in self.script
        """
        locals = {"user": user, "conditions": ""}
        safe_exec(self.script, None, locals, script_filename=self.name)
        if locals["conditions"]:
            return locals["conditions"]


def execute_api_server_script(script=None, *args, **kwargs):
    # These are only added for compatibility with rate limiter.
    del args
    del kwargs

    if script.script_type != "API":
        raise frappe.DoesNotExistError

    # validate if guest is allowed
    if frappe.session.user == "Guest" and not script.allow_guest:
        raise frappe.PermissionError

    # output can be stored in flags
    _globals, _locals = safe_exec(script.script, script_filename=script.name)

    return _globals.frappe.flags
