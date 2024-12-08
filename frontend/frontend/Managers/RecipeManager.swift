import Foundation
import FirebaseFirestore

class RecipeManager: ObservableObject {
    @Published var recipes: [Recipe] = []
    private let db = Firestore.firestore()
    
    func fetchTodaysRecipes() async {
        do {
            let snapshot = try await db.collection("recipes").limit(to: 5).getDocuments()
            let fetchedRecipes = snapshot.documents.compactMap { document -> Recipe? in
                let data = document.data()
                guard let name = data["recipe_name"] as? String,
                      let description = data["recipe_description"] as? String,
                      let instructions = data["recipe_instructions"] as? [String: String],
                      let nutritionalFacts = data["nutritional_facts"] as? [String: Double] else {
                    return nil
                }
                
                let sortedInstructions = instructions.reduce(into: [Int: String]()) { result, pair in
                    if let key = Int(pair.key) {
                        result[key] = pair.value
                    }
                }
                
                return Recipe(
                    id: document.documentID,
                    name: name,
                    description: description,
                    instructions: sortedInstructions,
                    nutritionalFacts: Recipe.NutritionalFacts(
                        calories: nutritionalFacts["calories"] ?? 0,
                        protein: nutritionalFacts["protein"] ?? 0,
                        carbs: nutritionalFacts["carbs"] ?? 0,
                        sugars: nutritionalFacts["sugars"] ?? 0
                    ),
                    imageUrl: data["image_url"] as? String
                )
            }
            
            DispatchQueue.main.async {
                self.recipes = fetchedRecipes
            }
        } catch {
            print("Error fetching recipes: \(error)")
        }
    }
}