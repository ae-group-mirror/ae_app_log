"""
runtime logging helpers
=======================

* :class:`ErrorMsgMixin`: a mixin class that extends any class with a sophisticated error message handling and
  logging.
"""


__version__ = '0.3.2'


class ErrorMsgMixin:                                                # pylint: disable=too-few-public-methods
    """ mixin class providing sophisticated error message handling and logging. """
    error_sep = "\n\n"          #: error messages separator (reading the :attr:`~ErrorMsgMixin.error_message` property)
    main_app = None             #: main :class:`ae.core.AppBase` instance
    po = dpo = vpo = print      #: default print functions for normal/debug/verbose console output

    def __init__(self):
        """ try to initialize and use app environment logging output methods from the main app instance. """
        self._errors: list[str] = []
        try:                                            # pragma: no cover
            from ae.core import main_app_instance       # type: ignore # pylint: disable=import-outside-toplevel

            self.main_app = main_app = main_app_instance()
            assert main_app is not None, f"{self.__class__.__name__}.__init__() called too early; main app instance not"

            self.po = main_app.po
            self.dpo = main_app.dpo
            self.vpo = main_app.vpo

        except (ImportError, AssertionError, Exception) as exc:                 # pylint: disable=broad-except
            print(f"{self.__class__.__name__}.__init__() raised {exc}; using print() instead of main app error loggers")
            # fallbacks assigned as/in class attributes: self.main_app = None; self.po = self.dpo = self.vpo = print

    @property
    def error_message(self) -> str:
        """ error message string if an error occurred or an empty string if not.

        :getter:                return the accumulated error message of the recently occurred error(s).
        :setter:                any assigned error message will be accumulated/added to recent error messages.
                                assign an empty string to reset all the previously accumulated error messages.
        """
        return self.error_sep.join(self._errors)

    @error_message.setter
    def error_message(self, next_err_msg: str):
        if next_err_msg:
            if "WARNING" in next_err_msg.upper():
                self.vpo(f" .::. {next_err_msg}")
            else:
                self.dpo(f" .::. {next_err_msg}")
            self._errors.append(next_err_msg)
        else:
            self._errors = []

    # def flush_error_lines_to(self, callee: Callable[[str], None]):
    #     """ pass all the collected error message lines
    #
    #     :param callee:          will be called with
    #     :return:
    #     """
    #     for err_msg in self._errors:
    #         callee(err_msg)
    #     self._errors = []
