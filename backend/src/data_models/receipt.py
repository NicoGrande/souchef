import pydantic
import datetime
import uuid
import backend.src.data_models.item as sc_item


class Receipt(pydantic.BaseModel):
    """A class representing a receipt with date and items.

    This class models a receipt that contains a date and a list of purchased items.

    Attributes:
        receipt_id (uuid.UUID): The unique identifier for the receipt.
        date (datetime.date): The date when the receipt was issued.
        items (list[Item]): A list of items purchased, where each item is an instance
            of the Item class.
    """

    receipt_id: uuid.UUID = pydantic.Field(default_factory=uuid.uuid4)
    date: datetime.date = pydantic.Field(default_factory=datetime.date.today)
    items: list[sc_item.Item]
