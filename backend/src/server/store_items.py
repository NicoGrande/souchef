import firebase_admin
from firebase_admin import credentials, firestore
import src.data_models.item as sc_item


class ItemFireStore:
    """A class to store items.

    This class interfaces with Cloud Firestore to store and retrieve items.
    """

    def __init__(self, user_id: str, db: firestore.Client | None = None):
        """Initialize the ItemStore with a Firestore client.

        Args:
            db: Optional Firestore client. If not provided, creates a new client.
        """
        self.user_id = user_id
        if db is None:
            if not firebase_admin._apps:
                # Initialize Firebase Admin SDK if not already initialized
                cred = credentials.ApplicationDefault()
                firebase_admin.initialize_app(cred)
            self.db = firestore.client(database="souschet-items")
        else:
            self.db = db

        self.collection = self.db.collection("items")

    def add_items(self, items: list[sc_item.Item]):
        """Add multiple items to Firestore.

        Args:
            items: List of Item objects to store
        """
        batch = self.db.batch()

        for item in items:
            doc_ref = self.collection.document(f"{self.user_id}/{item.name}")
            batch.set(doc_ref, item.to_dict(), merge=True)
        batch.commit()

    def get_items(self) -> list[sc_item.Item]:
        """Retrieve all items from Firestore.

        Returns:
            List of Item objects
        """
        docs = self.collection.where("user_id", "==", self.user_id).stream()
        return [sc_item.Item.from_dict(doc.to_dict()) for doc in docs]

    def get_item(self, item_name: str) -> sc_item.Item:
        """Retrieve a specific item by name.

        Args:
            item_name: Name of the item to retrieve

        Returns:
            Item object if found

        Raises:
            KeyError: If item is not found
        """
        doc_ref = self.collection.document(f"{self.user_id}/{item_name}")
        doc = doc_ref.get()

        if not doc.exists:
            raise KeyError(f"Item '{item_name}' not found")

        return sc_item.Item.from_dict(doc.to_dict())

    def update_item(self, item: sc_item.Item):
        """Update an item in Firestore.

        Args:
            item: Item object to update
        """
        doc_ref = self.collection.document(f"{self.user_id}/{item.name}")
        doc_ref.set(item.model_dump_json(), merge=True)

    def delete_item(self, item_name: str):
        """Delete an item from Firestore.

        Args:
            item_name: Name of the item to delete
        """
        doc_ref = self.collection.document(f"{self.user_id}/{item_name}")
        doc_ref.delete()
