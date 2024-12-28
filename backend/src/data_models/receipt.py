import pydantic
import datetime
import uuid

import src.data_models.item as sc_item


class ReceiptItem(pydantic.BaseModel):
    """A class representing an item on a receipt.

    This class models an item on a receipt with a name, price, and quantity.

    Attributes:
        price (float): The price of the item.
        item (sc_item.Item): The item on the receipt.
    """

    price: float
    item: sc_item.Item


class Receipt(pydantic.BaseModel):
    """A class representing a receipt with date and items.

    This class models a receipt that contains a date and a list of purchased items.

    Attributes:
        merchant (str): The name of the merchant of the reciept.
        merchant (str): The name of the merchant of the reciept.
        receipt_id (uuid.UUID): The unique identifier for the receipt.
        date (datetime.date): The date when the receipt was issued.
        items (list[ReceiptItem]): A list of items purchased, where each item is an instance
            of the ReceiptItem class.
    """

    merchant: str
    items: list[ReceiptItem]
    _receipt_id: uuid.UUID = pydantic.PrivateAttr(default_factory=uuid.uuid4)
    _date: datetime.date = pydantic.PrivateAttr(default_factory=datetime.date.today)

    @property
    def receipt_id(self) -> uuid.UUID:
        return self._receipt_id

    @property
    def date(self) -> datetime.date:
        return self._date

    @pydantic.field_validator("merchant", mode="before")
    def validate_merchant(cls, v):
        if not isinstance(v, str):
            raise ValueError("Merchant must be a string")
        return v

    @pydantic.field_validator("items", mode="before")
    def validate_items(cls, v):
        if not isinstance(v, list):
            raise ValueError("Items must be a list")
        return v
