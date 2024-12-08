import Foundation

enum Unit: String, CaseIterable {
    case pounds = "lb"
    case kilos = "kg"
    case grams = "g"
    case kcal = "kcal"
    case gallons = "gal"
    case liter = "L"
    case milliliter = "ml"
    case ounces = "oz"
    case none = "none"
    
    var displayName: String {
        switch self {
        case .pounds: return "Pounds (lb)"
        case .kilos: return "Kilograms (kg)"
        case .grams: return "Grams (g)"
        case .kcal: return "Kilocalories (kcal)"
        case .gallons: return "Gallons (gal)"
        case .liter: return "Liters (L)"
        case .milliliter: return "Milliliters (ml)"
        case .ounces: return "Ounces (oz)"
        case .none: return "Count"
        }
    }
}

enum UnitType: String {
    case weight = "weight"
    case volume = "volume"
    case energy = "energy"
    case none = "none"
}

// Mapping units to their types
let unitTypeMapping: [Unit: UnitType] = [
    .grams: .weight,
    .kilos: .weight,
    .pounds: .weight,
    .ounces: .weight,
    .gallons: .volume,
    .liter: .volume,
    .milliliter: .volume,
    .kcal: .energy,
    .none: .none
] 