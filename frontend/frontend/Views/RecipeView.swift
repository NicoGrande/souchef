import SwiftUI

struct RecipeView: View {
    @EnvironmentObject var authManager: AuthenticationManager
    @EnvironmentObject var userManager: UserManager
    @StateObject private var recipeManager = RecipeManager()
    @State private var showSettings = false
    
    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 20) {
                // Welcome Message
                if let firstName = userManager.currentUserProfile?.fullName.components(separatedBy: " ").first {
                    Text("Welcome, \(firstName)!")
                        .font(.system(size: 28, weight: .bold))
                        .foregroundColor(Theme.textColor)
                        .padding(.horizontal)
                }
                
                // Today's Recipes Section
                VStack(alignment: .leading, spacing: 15) {
                    Text("Today's Recipes")
                        .font(.system(size: 24, weight: .bold))
                        .foregroundColor(Theme.textColor)
                        .padding(.horizontal)
                    
                    ScrollView(.horizontal, showsIndicators: false) {
                        HStack(spacing: 20) {
                            ForEach(recipeManager.recipes) { recipe in
                                RecipeCard(recipe: recipe)
                            }
                        }
                        .padding(.horizontal)
                    }
                }
            }
            .padding(.vertical)
        }
        .background(Theme.backgroundGreen.opacity(0.1))
        .navigationBarTitleDisplayMode(.inline)
        .toolbar {
            ToolbarItem(placement: .navigationBarLeading) {
                Button(action: { showSettings = true }) {
                    Image(systemName: "gearshape.fill")
                        .foregroundColor(Theme.primaryGreen)
                }
            }
        }
        .sheet(isPresented: $showSettings) {
            SettingsView()
        }
        .task {
            await recipeManager.fetchTodaysRecipes()
        }
    }
}

struct RecipeCard: View {
    let recipe: Recipe
    
    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            // Recipe Image
            if let imageUrl = recipe.imageUrl {
                AsyncImage(url: URL(string: imageUrl)) { image in
                    image
                        .resizable()
                        .aspectRatio(contentMode: .fill)
                } placeholder: {
                    Rectangle()
                        .fill(Theme.secondaryGreen.opacity(0.3))
                }
                .frame(height: 150)
                .clipShape(RoundedRectangle(cornerRadius: 12))
            }
            
            // Recipe Name
            Text(recipe.name)
                .font(.system(size: 18, weight: .bold))
                .foregroundColor(Theme.textColor)
            
            // Nutritional Facts
            HStack(spacing: 15) {
                NutritionBadge(
                    value: recipe.nutritionalFacts.calories,
                    unit: "kcal",
                    name: "Calories"
                )
                NutritionBadge(
                    value: recipe.nutritionalFacts.protein,
                    unit: "g",
                    name: "Protein"
                )
                NutritionBadge(
                    value: recipe.nutritionalFacts.carbs,
                    unit: "g",
                    name: "Carbs"
                )
                NutritionBadge(
                    value: recipe.nutritionalFacts.sugars,
                    unit: "g",
                    name: "Sugars"
                )
            }
        }
        .padding()
        .background(Color.white)
        .cornerRadius(16)
        .shadow(color: Color.black.opacity(0.1), radius: 5, y: 2)
        .frame(width: 300)
    }
}

struct NutritionBadge: View {
    let value: Double
    let unit: String
    let name: String
    
    var body: some View {
        VStack(spacing: 4) {
            Text(String(format: "%.0f", value))
                .font(.system(size: 16, weight: .bold))
            Text(unit)
                .font(.system(size: 12))
            Text(name)
                .font(.system(size: 12))
        }
        .foregroundColor(Theme.textColor)
    }
} 