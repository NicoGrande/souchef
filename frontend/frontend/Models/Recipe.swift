import Foundation

struct Recipe: Identifiable, Codable {
    let id: String
    let name: String
    let description: String
    let instructions: [Int: String]
    let nutritionalFacts: NutritionalFacts
    let imageUrl: String?
    
    struct NutritionalFacts: Codable {
        let calories: Double
        let protein: Double
        let carbs: Double
        let sugars: Double
    }
} 