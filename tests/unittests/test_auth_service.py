import pytest
from _pytest.python_api import raises
from fastapi.responses import JSONResponse
from fastapi import HTTPException

from domain.services.auth.auth_service import login
from core.schemas import AuthDetails

from mock import Mock, patch


auth_service_path = "domain.services.auth.auth_service"


@pytest.mark.asyncio
async def test_auth_login_should_return_correct_json_respon_when_autorized():
    auth_handler_mock = Mock()
    auth_handler_mock.encode_token = Mock(return_value="example_jwt_token")
    auth_handler_mock.verify_password = Mock(return_value=True)
    auth_login_details = AuthDetails(
        username="admin",
        password="admin"
    )
    expected_class = JSONResponse
    expected_content = b'{"access_token":"example_jwt_token"}'

    with patch(auth_service_path + ".AuthHandler", Mock(return_value=auth_handler_mock)):
        result = await login(auth_details=auth_login_details)

    assert isinstance(result, expected_class)
    assert result.body == expected_content
    auth_handler_mock.verify_password.assert_called_once_with("admin", "admin")
    auth_handler_mock.encode_token.assert_called_once_with("admin")


@pytest.mark.asyncio
async def test_auth_login_should_raise_exception_when_user_not_autorized():
    auth_handler_mock = Mock()
    auth_handler_mock.encode_token = Mock(return_value="example_jwt_token")
    auth_handler_mock.verify_password = Mock(return_value=False)
    auth_login_details = AuthDetails(
        username="admin",
        password="bad_password"
    )
    expected_exception = HTTPException
    expected_details = 'Invalid username and/or password'
    expected_status_code = 401

    with patch(auth_service_path + ".AuthHandler", Mock(return_value=auth_handler_mock)), \
         raises(expected_exception) as ex:
        await login(auth_details=auth_login_details)

    assert ex.value.detail == expected_details
    assert ex.value.status_code == expected_status_code
    auth_handler_mock.encode_token.assert_not_called()
    auth_handler_mock.verify_password.assert_called_once_with("bad_password", "admin")
