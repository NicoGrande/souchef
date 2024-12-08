import Foundation

enum StorageType: String, Codable, CaseIterable {
    case pantry = "PANTRY"
    case refrigerator = "REFRIGERATOR"
    case freezer = "FREEZER"
}

struct Item: Identifiable, Codable {
    let id: String
    var name: String
    var quantity: Quantity
    var price: Double
    var perServingMacros: [String: Quantity]
    var servingSize: Quantity
    var shelfLife: Int // in days
    var storage: StorageType
    var expirationDate: Date
    
    struct Quantity: Codable {
        var value: Double
        var unit: String
    }
} 