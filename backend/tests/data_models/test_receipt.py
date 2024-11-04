import datetime
import pytest
import sys
import uuid

from backend.src.data_models.receipt import Receipt
from backend.src.data_models.item import Item
from backend.src.data_models import quantity as sc_quantity
from backend.src.utils import types as sc_types


def test_receipt_init():
    # Create test items
    test_item1 = Item(
        name="Test Item 1",
        quantity=sc_quantity.Quantity(
            quantity=1,
            unit=sc_types.Unit.NONE,
            type=sc_types.UnitType.NONE,
        ),
        price=1.0,
        merchant="Test Merchant",
        per_serving_macros={},
        serving_size=sc_quantity.Quantity(
            quantity=1,
            unit=sc_types.Unit.NONE,
            type=sc_types.UnitType.NONE,
        ),
        shelf_life=datetime.timedelta(days=1),
        storage=sc_types.StorageType.PANTRY,
    )
    
    test_item2 = Item(
        name="Test Item 2",
        quantity=sc_quantity.Quantity(
            quantity=2,
            unit=sc_types.Unit.NONE,
            type=sc_types.UnitType.NONE,
        ),
        price=2.0,
        merchant="Test Merchant",
        per_serving_macros={},
        serving_size=sc_quantity.Quantity(
            quantity=1,
            unit=sc_types.Unit.NONE,
            type=sc_types.UnitType.NONE,
        ),
        shelf_life=datetime.timedelta(days=1),
        storage=sc_types.StorageType.PANTRY,
    )

    # Create receipt
    receipt = Receipt(
        merchant="Test Merchant",
        items=[test_item1, test_item2]
    )

    # Test attributes
    assert receipt.merchant == "Test Merchant"
    assert len(receipt.items) == 2
    assert isinstance(receipt._receipt_id, uuid.UUID)
    assert isinstance(receipt._date, datetime.date)
    assert receipt._date == datetime.date.today()


def test_receipt_validation():
    # Test validation with invalid merchant type
    with pytest.raises(ValueError):
        Receipt(
            merchant=123,  # Invalid merchant type (should be string)
            items=[]
        )

    # Test validation with invalid items type
    with pytest.raises(ValueError):
        Receipt(
            merchant="Test Merchant",
            items="not a list"  # Invalid items type (should be list)
        )


if __name__ == "__main__":
    sys.exit(pytest.main()) 