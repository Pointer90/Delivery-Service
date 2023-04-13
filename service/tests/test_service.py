import pytest
from service.main import (
    BaseDeliveryService,
    InternationalService,
    DomesticService,
    DeliveryService
)

from service.enums import Delivery
from service.entities import (
    DeliveryData,
    DeliveryResult,
    PostcodeInput,
    PostcodeOutput
)
from service.exceptions import DeliveryException
from service import messages

class TestDeliveryService:
    
	@pytest.mark.parametrize('name', Delivery.INTERNATIONAL)
	def test_calc__call_international_service__ok(
		self,
		name,
		mocker):

		#arrange
		chek_input = DeliveryData(
			name = name,
			height = 123.1,
			width = 234.2,
			depth = 345.3,
			weight = 456,
			is_safe = True
		)

		chek_result = DeliveryResult(
			price = 567.4,
			safe = 'some code'
		)

		calc_delivery_mock = mocker.patch(
			'service.main.InternationalService.calc_delivery',
			return_value = chek_result
		)

		service = DeliveryService()

		#act
		result = service.calc(data = chek_input)

		#assert
		calc_delivery_mock.assert_called_once_with(chek_input)
		assert result == chek_result

	@pytest.mark.parametrize('name', Delivery.DOMESTIC)
	def test_calc__call_domestic_service__ok(
		self,
		name,
		mocker):

		#arrange
		chek_input = DeliveryData(
			name = name,
			height = 123.1,
			width = 234.2,
			depth = 345.3,
			weight = 456,
			is_safe = True
		)

		chek_result = DeliveryResult(
			price = 567.4,
			safe = 'some code'
		)

		calc_delivery_mock = mocker.patch(
			'service.main.DomesticService.calc_delivery',
			return_value = chek_result
		)

		service = DeliveryService()

		#act
		result = service.calc(data = chek_input)

		#assert
		calc_delivery_mock.assert_called_once_with(chek_input)
		assert result == chek_result

	def test_calc__invalid_delivery__raise_exception(self):

		#arrange
		check_input = DeliveryData(
			name = 'WB',
			height= 123.1,
			width=234.2,
			depth=345.3,
			weight=456,
			is_safe=True
		)

		#act
		with pytest.raises(DeliveryException) as ex:
			DeliveryService().calc(data = check_input)

		#assert
		assert ex.value.message == messages.MSG_1