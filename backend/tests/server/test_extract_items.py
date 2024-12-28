import pytest
import sys
import os
from src.server.extract_items import ExtractItemsAgent
from src.data_models.receipt import Receipt, ReceiptItem


class TestExtractItems:
    # Test URLs
    RECEIPT_URL = "https://i.redd.it/4r55c4845kvc1.jpg"
    IMAGE_URL = "https://i.redd.it/5dmd65845kvc1.jpg"

    @pytest.fixture(autouse=True)
    def setup_api_keys(self):
        """Fixture to set up required API keys for tests."""
        assert os.getenv("OPENAI_API_KEY") is not None
        assert os.getenv("GOOGLE_API_KEY") is not None
        assert os.getenv("GOOGLE_CSE_ID") is not None

    @pytest.fixture
    def extract_items_agent(self):
        """Fixture to create an ExtractItemsAgent instance."""
        return ExtractItemsAgent(verbose=True)

    def test_extract_items_from_receipt(self, extract_items_agent):
        """Test that items can be extracted from a receipt."""
        receipt = extract_items_agent.extract_items_from_receipt(
            receipt_url=self.RECEIPT_URL, image_url=self.IMAGE_URL
        )

        # Verify the receipt object
        assert isinstance(receipt, Receipt)
        assert receipt.merchant is not None
        assert len(receipt.items) > 0

        # Verify each item in the receipt
        for receipt_item in receipt.items:
            assert isinstance(receipt_item, ReceiptItem)
            assert receipt_item.item is not None
            assert receipt_item.price is not None

    def test_invalid_receipt_url(self, extract_items_agent):
        """Test that appropriate error is raised for invalid receipt URL."""
        with pytest.raises(Exception):
            extract_items_agent.extract_items_from_receipt(
                receipt_url="invalid-url.com/receipt.jpg", image_url=self.IMAGE_URL
            )

    def test_invalid_image_url(self, extract_items_agent):
        """Test that appropriate error is raised for invalid image URL."""
        with pytest.raises(Exception):
            extract_items_agent.extract_items_from_receipt(
                receipt_url=self.RECEIPT_URL, image_url="invalid-url.com/image.jpg"
            )


if __name__ == "__main__":
    sys.exit(pytest.main())
