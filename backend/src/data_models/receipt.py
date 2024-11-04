import pydantic
import datetime
import uuid
import backend.src.data_models.item as sc_item


class Receipt(pydantic.BaseModel):
    """A class representing a receipt with date and items.

    This class models a receipt that contains a date and a list of purchased items.

    Attributes:
        merchant (str): The name of the merchant of the reciept.
        receipt_id (uuid.UUID): The unique identifier for the receipt.
        date (datetime.date): The date when the receipt was issued.
        items (list[Item]): A list of items purchased, where each item is an instance
            of the Item class.
    """

    merchant: str
    items: list[sc_item.Item]
    _receipt_id: uuid.UUID = pydantic.PrivateAttr(default_factory=uuid.uuid4)
    _date: datetime.date = pydantic.PrivateAttr(default_factory=datetime.date.today)

