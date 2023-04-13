from abc import ABC, abstractmethod
from service.entities import (
    DeliveryData,
    DeliveryResult,
    PostcodeInput,
    PostcodeOutput,
    PostcodeOutputTest
)
from service.enums import Delivery
from service.keys import API_KEY, SECRET_KEY
from service import exceptions

class BaseDeliveryService(ABC):

    @abstractmethod
    def calc_delivery(self, data: DeliveryData) -> DeliveryResult:
        pass

class InternationalService(BaseDeliveryService):

    def calc_delivery(self, data: DeliveryData) -> DeliveryResult:
        
        h: float = data["height"]
        w: float = data["width"]
        d: float = data["depth"]
        weight: int = data["weight"]
        is_safe: bool = data["is_safe"]

        price = h * w * d * weight * 0.5
        if (is_safe):
            return DeliveryResult(
                price = price * 2,
                is_safe = "Застраховано"
            )
            return DeliveryResult(
                    price = price,
                    is_safe = "Нет страховки"
                )

class DomesticService(BaseDeliveryService):

    def calc_delivery(self, data: DeliveryData) -> DeliveryResult:
        
        h: float = data["height"]
        w: float = data["width"]
        d: float = data["depth"]
        weight: int = data["weight"]
        is_safe: bool = data["is_safe"]

        price = h * w * d * weight * 0.5
        if (is_safe):
            return DeliveryResult(
                price = price * 4,
                is_safe = "Застраховано"
            )
            return DeliveryResult(
                    price = price,
                    is_safe = "Нет страховки"
                )

class DeliveryService:

    def calc(self, data: DeliveryData):

        name: str = data["name"]

        if name in Delivery.INTERNATIONAL:
            service = InternationalService()
        elif name in Delivery.DOMESTIC:
            service = DomesticService()
        else:
            raise exceptions.DeliveryException(details = "123456")
        return service.calc_delivery(data)

    def postcode(self, data: PostcodeInput):

        address: str = data["address"]
        dadata = Dadata(API_KEY, SECRET_KEY)
        try:
            result = dadata.clean(name ="address", source = address)
        except (httpx.ConnectError) as ex:
            raise exceptions.DadataException(details = str(ex))
        else:
            return PostcodeOutput(
                full_address = result["result"],
                postcode = result["postal_code"],
                timezone = result["timezone"]
        )

    def testcode(self, data: PostcodeOutputTest):

        address: str = data["address"]
        dadata = Dadata(API_KEY, SECRET_KEY)
        result = dadata.clean(name = "address", source = address)
        return PostcodeOutputTest(
            result = result["result"],
            region = result["region"],
            city_dist = result["city_district"]
        )