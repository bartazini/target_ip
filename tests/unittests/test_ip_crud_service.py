import pytest
from mock import Mock, patch
from unittest.mock import AsyncMock

from fastapi.responses import JSONResponse

from domain.services.ip_crud.ip_crud_service import (
    get_ip_location,
    add_ip_location,
    delete_ip_location,
    _get_ip_address_geolocation_details,
)

ip_crud_service_path = "domain.services.ip_crud.ip_crud_service"


@pytest.mark.asyncio
async def test_get_ip_location_should_return_response_with_geolocation_details():
    get_ip_address_geo_details_mock = AsyncMock(return_value={"data": "some_data"})
    ip_address = "178.0.1.44"
    expected_response_class = JSONResponse
    expected_content = b'{"data":"some_data"}'

    with patch(ip_crud_service_path + "._get_ip_address_geolocation_details", get_ip_address_geo_details_mock):
        result = await get_ip_location(ip_address=ip_address)

    assert isinstance(result, expected_response_class)
    assert result.body == expected_content
    get_ip_address_geo_details_mock.assert_called_once_with(ip_address=ip_address)


@pytest.mark.asyncio
async def test_get_ip_location_should_raise_exception_when_ip_stuck_service_issue():
    get_ip_address_geo_details_mock = AsyncMock(side_effect=Exception)
    ip_address = "178.0.1.44"
    expected_response_class = JSONResponse
    expected_content = b'{"status":"Could not get geolocation data for: 178.0.1.44 due to: Exception"}'

    with patch(ip_crud_service_path + "._get_ip_address_geolocation_details", get_ip_address_geo_details_mock):
        result = await get_ip_location(ip_address=ip_address)

    assert isinstance(result, expected_response_class)
    assert result.body == expected_content
    get_ip_address_geo_details_mock.assert_called_once_with(ip_address=ip_address)


@pytest.mark.asyncio
async def test_get_ip_address_geolocation_details_should_call_on_instance():
    ip_stack = Mock()
    ip_stack_instance = Mock()
    ip_stack.from_ip_stack = Mock(return_value=ip_stack_instance)
    ip_stack_instance.get_ip_location_details = Mock(return_value=b"{'data'}:'some_data'")
    ip_address = "10.1.0.10"
    expected = b"{'data'}:'some_data'"

    with patch(ip_crud_service_path + ".IpStack", ip_stack):
        result = await _get_ip_address_geolocation_details(ip_address=ip_address)

    assert result == expected
    ip_stack.from_ip_stack.assert_called_once()
    ip_stack_instance.get_ip_location_details.assert_called_once_with(ip_address=ip_address)
