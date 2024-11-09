import pytest
from unittest.mock import Mock, patch
from firebase_admin import firestore
from src.server.store_items import ItemFireStore
from src.data_models.item import Item


@pytest.fixture
def mock_firestore():
    """Create a mock Firestore client."""
    mock_db = Mock(spec=firestore.Client)
    mock_collection = Mock(spec=firestore.CollectionReference)
    mock_db.collection.return_value = mock_collection
    return mock_db


@pytest.fixture
def mock_batch():
    """Create a mock batch object."""
    return Mock(spec=firestore.WriteBatch)


@pytest.fixture
def store(mock_firestore):
    """Create an ItemFireStore instance with a mock db."""
    return ItemFireStore(user_id="test_user", db=mock_firestore)


@pytest.fixture
def sample_item():
    """Create a sample Item for testing."""
    return Item(name="test_item", user_id="test_user", quantity=1.0, unit="kg")


def test_add_items(store, mock_firestore, mock_batch, sample_item):
    """Test adding items to Firestore."""
    # Setup
    mock_firestore.batch.return_value = mock_batch
    items = [sample_item]

    # Execute
    store.add_items(items)

    # Verify
    assert mock_firestore.batch.called
    assert mock_batch.set.called
    mock_batch.commit.assert_called_once()


def test_get_items(store, mock_firestore):
    """Test retrieving all items from Firestore."""
    # Setup
    mock_doc = Mock()
    mock_doc.to_dict.return_value = {
        "name": "test_item",
        "user_id": "test_user",
        "quantity": 1.0,
        "unit": "kg",
    }
    mock_firestore.collection().where().stream.return_value = [mock_doc]

    # Execute
    items = store.get_items()

    # Verify
    assert len(items) == 1
    assert isinstance(items[0], Item)
    assert items[0].name == "test_item"
    mock_firestore.collection().where.assert_called_with("user_id", "==", "test_user")


def test_get_item_exists(store, mock_firestore, sample_item):
    """Test retrieving a specific item that exists."""
    # Setup
    mock_doc = Mock()
    mock_doc.exists = True
    mock_doc.to_dict.return_value = sample_item.model_dump()
    mock_firestore.collection().document().get.return_value = mock_doc

    # Execute
    item = store.get_item("test_item")

    # Verify
    assert isinstance(item, Item)
    assert item.name == "test_item"


def test_get_item_not_exists(store, mock_firestore):
    """Test retrieving a non-existent item."""
    # Setup
    mock_doc = Mock()
    mock_doc.exists = False
    mock_firestore.collection().document().get.return_value = mock_doc

    # Execute and verify
    with pytest.raises(KeyError):
        store.get_item("nonexistent_item")


def test_update_item(store, mock_firestore, sample_item):
    """Test updating an item."""
    # Execute
    store.update_item(sample_item)

    # Verify
    mock_firestore.collection().document().set.assert_called_once()


def test_delete_item(store, mock_firestore):
    """Test deleting an item."""
    # Execute
    store.delete_item("test_item")

    # Verify
    mock_firestore.collection().document().delete.assert_called_once()


@patch("firebase_admin.credentials.ApplicationDefault")
@patch("firebase_admin.initialize_app")
def test_init_without_db(mock_init_app, mock_cred):
    """Test initialization without providing a db instance."""
    # Setup
    mock_cred.return_value = Mock()

    # Execute
    store = ItemFireStore(user_id="test_user")

    # Verify
    assert mock_cred.called
    assert mock_init_app.called
