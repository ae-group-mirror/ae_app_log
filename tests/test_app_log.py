""" logging unit tests. """
from unittest.mock import patch

from tests.conftest import skip_gitlab_ci


from ae.app_log import ErrorMsgMixin


class TestErrorMsgMixin:
    def test_instantiation(self):
        ins = ErrorMsgMixin()
        assert ins
        assert ins.main_app is None     # in test env is no console/gui app available
        assert ins.po is ins.dpo is ins.vpo is print

    @skip_gitlab_ci
    def test_instantiation_locally(self):
        with patch('ae.core.main_app_instance', lambda: None):  # ae.core not available on CI(removed pjm from tst_reqs)
            ins = ErrorMsgMixin()
            assert ins
            assert ins.main_app is None
            assert ins.po is ins.dpo is ins.vpo is print

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

        err_msg = "error message with the word warning"
        ins.error_message = err_msg
        ins.error_message = "another message"
        assert err_msg in ins.error_message
