from src.PersonalAccount import PersonalAccount as p_acc
from src.BusinessAccount import BusinessAccount as b_acc
from src.modules.Account import Account
from src.smtp.smtp import SMTPClient as smtp
from pytest_mock import MockFixture
from datetime import datetime
import pytest


class TestEmail:
    todays_date = datetime.today().strftime("%Y-%m-%d")
    email_adress = "test@email.com"

    def test_p_acc_email(self, mocker: MockFixture):
        account = p_acc("John", "Doe", "12345678901")
        account.history = [150.0, -50.0]
        mock_send = mocker.patch("src.smtp.smtp.SMTPClient.send", return_value=True)

        result = account.send_history_via_email(self.email_adress)

        assert result is True
        mock_send.assert_called_once_with(
            "Account Transfer History " + self.todays_date,
            "Personal Account History: " + account.history.__str__(),
            self.email_adress,
        )

    def test_p_acc_email_false(self, mocker: MockFixture):
        account = p_acc("John", "Doe", "12345678901")
        account.history = [150.0, -50.0]
        mock_send = mocker.patch("src.smtp.smtp.SMTPClient.send", return_value=False)
        result = account.send_history_via_email(self.email_adress)

        assert result is False

    @pytest.fixture(autouse=True)
    def setup_mock(self, mocker: MockFixture):
        mocker.patch.object(b_acc, "validateNIP", return_value=True)

    def test_b_acc_email(self, mocker: MockFixture):
        account = b_acc("Nazwa", "8461627563")
        account.history = [150.0, -50.0]
        mock_send = mocker.patch("src.smtp.smtp.SMTPClient.send", return_value=True)

        result = account.send_history_via_email(self.email_adress)

        assert result is True
        mock_send.assert_called_once_with(
            "Account Transfer History " + self.todays_date,
            "Business Account History: " + account.history.__str__(),
            self.email_adress,
        )

    def test_b_acc_email_false(self, mocker: MockFixture):
        account = b_acc("Nazwa", "8461627563")
        account.history = [150.0, -50.0]
        mock_send = mocker.patch("src.smtp.smtp.SMTPClient.send", return_value=False)

        result = account.send_history_via_email(self.email_adress)

        assert result is False


    def test_base_account_email(self, mocker: MockFixture):
        account = Account()
        account.history = [100]
        mock_send = mocker.patch("src.smtp.smtp.SMTPClient.send", return_value=True)
        result = account.send_history_via_email("test@email.com")
        assert result is False

    def test_smtp_client_send(self):
        assert smtp.send("subject", "text", "email@gmail.com") == False