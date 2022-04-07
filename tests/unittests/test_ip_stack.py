import pytest
from mock import Mock, patch

from ip_stack.IpStack import IpStack


ip_stack_path = "ip_stack.IpStack"


@pytest.mark.asyncio
async def test_ip_stack_should_assign_base_api_url_correctly():
    ip_stack = IpStack()

    assert hasattr(ip_stack, "_base_api_url")


@pytest.mark.asyncio
async def test_from_ip_stack_should_return_instance_of_ip_stack():
    ip_stack = IpStack.from_ip_stack()

    assert isinstance(ip_stack, IpStack)


@pytest.mark.asyncio
async def test_ip_location_details_should_return_response_correctly():
    response_mock = Mock()
    response_mock.json = Mock(return_value="some_json_content")
    requests_mock = Mock()
    requests_mock.get = Mock(return_value=response_mock)
    ip_stack = IpStack()
    ip_address = "192.168.255.1"
    access_key = "11b99a9b1c0a3b3ac981cca0b896697f"
    expected_requests_get_call = ip_stack._base_api_url.format(ip_address, access_key)
    expected = "some_json_content"

    with patch(ip_stack_path + ".requests", requests_mock):
        result = ip_stack.get_ip_location_details(ip_address=ip_address)

    assert result == expected
    requests_mock.get.assert_called_once_with(url=expected_requests_get_call)
    response_mock.json.assert_called()
