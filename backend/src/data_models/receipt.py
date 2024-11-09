import pydantic
import datetime
import uuid

import src.data_models.quantity as sc_quantity


class ReceiptItem(pydantic.BaseModel):
    """A class representing an item on a receipt.

    This class models an item on a receipt with a name, price, and quantity.

    Attributes:
        name (str): The name of the item.
        price (float): The price of the item.
        quantity (sc_quantity.Quantity): The quantity of the item.
    """

    name: str
    price: float
    quantity: sc_quantity.Quantity


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
    merchant: str
    items: list[ReceiptItem]
    _receipt_id: uuid.UUID = pydantic.PrivateAttr(default_factory=uuid.uuid4)
    _date: datetime.date = pydantic.PrivateAttr(default_factory=datetime.date.today)
