from dataclasses import dataclass
from uuid import UUID
from item import Item


@dataclass
class ItemStorage:
    """Class representing food stored. This includes items, components and meals."""

    storage_id: UUID
    pantry_items: dict[UUID, Item]
    refrigerated_items: dict[UUID, Item]
    frozen_items: dict[UUID, Item]

    def update_pantry_item(self, item: Item):
        if item.item_id in self.pantry_items:
            self.pantry_items.update(item.item_id, item)
        else:
            self.pantry_items[item.item_id] = item

    def remove_pantry_item(self, item_id: UUID):
        del self.pantry_items[item_id]

    def update_refrigerated_item(self, item: Item):
        if item.item_id in self.refrigerated_items:
            self.refrigerated_items.update(item.item_id, item)
        else:
            self.refrigerated_items[item.item_id] = item

    def remove_refrigerated_item(self, item_id: UUID):
        del self.refrigerated_items[item_id]

    def update_frozen_item(self, item: Item):
        if item.item_id in self.frozen_items:
            self.frozen_items.update(item.item_id, item)
        else:
            self.frozen_items[item.item_id] = item

    def remove_frozen_item(self, item_id: UUID):
        del self.frozen_items[item_id]
