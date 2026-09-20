""" logging unit tests. """
import sys
import types
from unittest.mock import patch, MagicMock

from tests.conftest import skip_gitlab_ci


from ae.app_log import ErrorMsgMixin


class TestErrorMsgMixin:
    def test_instantiation(self):
        ins = ErrorMsgMixin()

        assert ins
        assert ins.main_app is None     # in test env is no console/gui app available
        assert ins.po is ins.dpo is ins.vpo is print

    def test_instantiation_with_mocked_main_app(self, monkeypatch):
        fake_ae_core = types.ModuleType('ae.core')
        fake_ae_core.main_app_instance = MagicMock()
        mocked_main_app_instance = fake_ae_core.main_app_instance.return_value
        monkeypatch.setitem(sys.modules, 'ae.core', fake_ae_core)

        ins = ErrorMsgMixin()

        assert ins
        assert ins.main_app is mocked_main_app_instance
        assert ins.po is mocked_main_app_instance.po
        assert ins.dpo is mocked_main_app_instance.dpo
        assert ins.vpo is mocked_main_app_instance.vpo

    @skip_gitlab_ci
    def test_integration_if_ae_core_installed(self):
        with patch('ae.core.main_app_instance', lambda: None):  # ae.core not available on CI(removed pjm from tst_reqs)
            ins = ErrorMsgMixin()

        assert ins
        assert ins.main_app is None
        assert ins.po is ins.dpo is ins.vpo is print

    @skip_gitlab_ci
    def test_integration_with_mocked_app_class_and_if_ae_core_installed(self):
        class _AppMock(ErrorMsgMixin):
            main_app = None

            @staticmethod
            def po():
                """ po() mock """
                return "po"

            @staticmethod
            def dpo():
                """ dpo() mock """
                return "dpo"

            @staticmethod
            def vpo():
                """ vpo() mock """
                return "vpo"

        app_ins = _AppMock()

        with patch('ae.core.main_app_instance', lambda: app_ins):
            ins = ErrorMsgMixin()

        assert ins.main_app is app_ins
        assert ins.po is not print
        assert ins.po() == "po"
        assert ins.dpo is not print
        assert ins.dpo() == "dpo"
        assert ins.vpo is not print
        assert ins.vpo() == "vpo"

    def test_error_message_property(self):
        ins = ErrorMsgMixin()

        assert ins.error_message == ""

        err_msg = "set new error message"
        ins.error_message = err_msg

        assert ins.error_message == err_msg

        err_msg2 = "added error message"
        ins.error_message = err_msg2

        assert err_msg in ins.error_message
        assert err_msg2 in ins.error_message

        ins.error_message = ""

        assert ins.error_message == ""

    def test_error_message_property_for_warnings(self):
        ins = ErrorMsgMixin()
        ins.dpo = MagicMock()
        ins.vpo = MagicMock()
        debug_msg = "any other message without this w-word"
        verbose_msg = "error message with the word warning"
        ins.error_message = verbose_msg
        ins.error_message = debug_msg

        assert debug_msg in ins.error_message
        assert verbose_msg in ins.error_message
        ins.dpo.assert_called_once_with(f" .::. {debug_msg}")
        ins.vpo.assert_called_once_with(f"  .:. {verbose_msg}")
