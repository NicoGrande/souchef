import Foundation
import FirebaseFirestore
import FirebaseAuth

class ItemManager: ObservableObject {
    @Published var userItems: [Item] = []
    private let db = Firestore.firestore()
    
    func createItem(_ item: Item) async throws {
        guard let userId = Auth.auth().currentUser?.uid else {
            throw ItemError.userNotFound
        }
        
        let macrosData: [String: [String: Any]] = [
            "calories": [
                "value": item.perServingMacros["calories"]?.value as Any,
                "unit": "kcal"
            ],
            "protein": [
                "value": item.perServingMacros["protein"]?.value as Any,
                "unit": "g"
            ],
            "carbs": [
                "value": item.perServingMacros["carbs"]?.value as Any,
                "unit": "g"
            ],
            "fat": [
                "value": item.perServingMacros["fat"]?.value as Any,
                "unit": "g"
            ]
        ]
        
        let itemData: [String: Any] = [
            "name": item.name,
            "quantity": [
                "value": item.quantity.value,
                "unit": item.quantity.unit
            ],
            "price": item.price,
            "perServingMacros": macrosData,
            "servingSize": [
                "value": item.servingSize.value,
                "unit": item.servingSize.unit
            ],
            "shelfLife": item.shelfLife,
            "storage": item.storage.rawValue,
            "expirationDate": Timestamp(date: item.expirationDate),
            "createdAt": Timestamp(date: Date())
        ]
        
        try await db.collection("users").document(userId).collection("items").document(item.id).setData(itemData)
    }
    
    func fetchUserItems() async throws {
        guard let userId = Auth.auth().currentUser?.uid else {
            throw ItemError.userNotFound
        }
        
        let snapshot = try await db.collection("users").document(userId).collection("items").getDocuments()
        
        let items = snapshot.documents.compactMap { document -> Item? in
            let data = document.data()
            guard let name = data["name"] as? String,
                  let quantityData = data["quantity"] as? [String: Any],
                  let quantityValue = quantityData["value"] as? Double,
                  let quantityUnit = quantityData["unit"] as? String,
                  let price = data["price"] as? Double,
                  let servingSizeData = data["servingSize"] as? [String: Any],
                  let servingSizeValue = servingSizeData["value"] as? Double,
                  let servingSizeUnit = servingSizeData["unit"] as? String,
                  let storageString = data["storage"] as? String,
                  let storage = StorageType(rawValue: storageString),
                  let expirationTimestamp = data["expirationDate"] as? Timestamp,
                  let macrosData = data["perServingMacros"] as? [String: [String: Any]] else {
                return nil
            }
            
            var macros: [String: Item.Quantity] = [:]
            for (key, value) in macrosData {
                if let quantity = value["value"] as? Double,
                   let unit = value["unit"] as? String {
                    macros[key] = Item.Quantity(value: quantity, unit: unit)
                }
            }
            
            return Item(
                id: document.documentID,
                name: name,
                quantity: Item.Quantity(value: quantityValue, unit: quantityUnit),
                price: price,
                perServingMacros: macros,
                servingSize: Item.Quantity(value: servingSizeValue, unit: servingSizeUnit),
                shelfLife: data["shelfLife"] as? Int ?? 0,
                storage: storage,
                expirationDate: expirationTimestamp.dateValue()
            )
        }
        
        DispatchQueue.main.async {
            self.userItems = items
        }
    }
}

enum ItemError: Error {
    case userNotFound
    case saveFailed
    case fetchFailed
} 
