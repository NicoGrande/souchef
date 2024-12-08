//
//  ContentView.swift
//  frontend
//
//  Created by Nicolas Grande on 11/13/24.
//

import SwiftUI
import FirebaseAuth
import FirebaseCore

struct ContentView: View {
    @EnvironmentObject var authManager: AuthenticationManager
    @EnvironmentObject var userManager: UserManager
    
    var body: some View {
        Group {
            if authManager.user != nil {
                if userManager.currentUserProfile != nil {
                    MainAppView()
                } else {
                    NavigationView {
                        ProfileSetupView()
                    }
                }
            } else {
                LandingView()
            }
        }
        .task {
            if authManager.user != nil {
                do {
                    try await userManager.fetchUserProfile()
                } catch {
                    print("Error fetching user profile: \(error)")
                }
            }
        }
    }
}

struct MainAppView: View {
    @State private var showCreateItem = false
    
    var body: some View {
        NavigationView {
            RecipeView()
                .toolbar {
                    ToolbarItem(placement: .navigationBarTrailing) {
                        Button(action: { showCreateItem = true }) {
                            Image(systemName: "plus.circle.fill")
                                .foregroundColor(Theme.primaryGreen)
                        }
                    }
                }
                .sheet(isPresented: $showCreateItem) {
                    CreateItemView()
                }
        }
    }
}

struct LandingView: View {
    var body: some View {
        NavigationView {
            ZStack {
                LinearGradient(
                    gradient: Gradient(colors: [
                        Theme.backgroundGreen.opacity(0.9),
                        Theme.backgroundGreen
                    ]),
                    startPoint: .top,
                    endPoint: .bottom
                )
                .ignoresSafeArea()
                
                VStack(spacing: 30) {
                    VStack(spacing: 20) {
                        Image(systemName: "fork.knife.circle.fill")
                            .resizable()
                            .scaledToFit()
                            .frame(width: 100, height: 100)
                            .foregroundColor(Theme.primaryGreen)
                            .background(
                                Circle()
                                    .fill(.white)
                                    .frame(width: 120, height: 120)
                                    .shadow(color: .black.opacity(0.1), radius: 10)
                            )
                            .padding(.top, 60)
                        
                        VStack(spacing: 8) {
                            Text("Souschef.ai")
                                .font(.system(size: 40, weight: .bold))
                                .foregroundColor(Theme.textColor)
                                .multilineTextAlignment(.center)
                            
                            Text("Your smart kitchen assistant")
                                .font(.system(size: 18, weight: .medium))
                                .foregroundColor(Theme.textColor.opacity(0.8))
                                .multilineTextAlignment(.center)
                        }
                    }
                    .frame(maxWidth: .infinity)
                    
                    Spacer()
                    
                    VStack(spacing: 25) {
                        FeatureRow(icon: "wand.and.stars", title: "AI-Powered Recipes", description: "Get personalized recipe recommendations")
                        FeatureRow(icon: "timer", title: "Smart Scheduling", description: "Perfect recipes for your busy schedule")
                        FeatureRow(icon: "list.bullet.clipboard", title: "Shopping Lists", description: "Automated grocery planning and analytics")
                    }
                    .padding(.horizontal, 30)
                    
                    Spacer()
                    
                    NavigationLink(destination: LoginView()) {
                        Text("Get Started")
                            .font(.system(size: 18, weight: .bold))
                            .foregroundColor(.white)
                            .frame(maxWidth: .infinity)
                            .frame(height: 56)
                            .background(Theme.primaryGreen)
                            .cornerRadius(16)
                            .shadow(color: Theme.primaryGreen.opacity(0.3), radius: 8, y: 4)
                    }
                    .padding(.horizontal, 30)
                    .padding(.bottom, 40)
                }
            }
            .navigationBarHidden(true)
        }
    }
}

struct FeatureRow: View {
    let icon: String
    let title: String
    let description: String
    
    var body: some View {
        HStack(spacing: 15) {
            Image(systemName: icon)
                .font(.system(size: 24))
                .foregroundColor(Theme.primaryGreen)
                .frame(width: 50)
            
            VStack(alignment: .leading, spacing: 4) {
                Text(title)
                    .font(.system(size: 16, weight: .semibold))
                    .foregroundColor(Theme.textColor)
                
                Text(description)
                    .font(.system(size: 14))
                    .foregroundColor(Theme.textColor.opacity(0.7))
            }
            Spacer()
        }
    }
}

struct LoginView: View {
    @Environment(\.dismiss) var dismiss
    @EnvironmentObject var authManager: AuthenticationManager
    @EnvironmentObject var userManager: UserManager
    @State private var email = ""
    @State private var password = ""
    @State private var isSignUp = false
    @State private var showError = false
    @State private var errorMessage = ""
    
    // Password validation
    private var isPasswordValid: Bool {
        password.count >= 8 &&
        password.contains(where: { $0.isNumber }) &&
        password.contains(where: { $0.isUppercase }) &&
        password.contains(where: { $0.isLowercase })
    }
    
    var body: some View {
        ScrollView {
            VStack(spacing: 25) {
                VStack(spacing: 20) {
                    CustomTextField(
                        icon: "envelope",
                        placeholder: "Email",
                        text: $email
                    )
                    
                    CustomTextField(
                        icon: "lock",
                        placeholder: "Password",
                        text: $password,
                        isSecure: true
                    )
                    
                    if isSignUp {
                        VStack(alignment: .leading, spacing: 5) {
                            Text("Password requirements:")
                                .font(.caption)
                                .foregroundColor(.gray)
                            
                            PasswordRequirementRow(
                                isValid: password.count >= 8,
                                text: "At least 8 characters"
                            )
                            PasswordRequirementRow(
                                isValid: password.contains(where: { $0.isNumber }),
                                text: "At least one number"
                            )
                            PasswordRequirementRow(
                                isValid: password.contains(where: { $0.isUppercase }),
                                text: "At least one uppercase letter"
                            )
                            PasswordRequirementRow(
                                isValid: password.contains(where: { $0.isLowercase }),
                                text: "At least one lowercase letter"
                            )
                        }
                        .padding(.vertical, 5)
                    }
                }
                .padding(.horizontal)
                
                Button(action: {
                    Task {
                        do {
                            if isSignUp {
                                guard isPasswordValid else {
                                    errorMessage = "Password does not meet requirements"
                                    showError = true
                                    return
                                }
                                print("Debug: Attempting signup...")
                                try await authManager.signUp(email: email, password: password)
                                print("Debug: Signup successful")
                            } else {
                                try await authManager.signIn(email: email, password: password)
                            }
                        } catch {
                            print("Debug: Error during signup: \(error)")
                            errorMessage = isSignUp ? "Failed to create account" : "Invalid credentials"
                            showError = true
                        }
                    }
                }) {
                    Text(isSignUp ? "Sign Up" : "Login")
                        .font(.system(size: 18, weight: .bold))
                        .foregroundColor(.white)
                        .frame(maxWidth: .infinity)
                        .frame(height: 56)
                        .background(Theme.primaryGreen)
                        .cornerRadius(16)
                        .shadow(color: Theme.primaryGreen.opacity(0.3), radius: 8, y: 4)
                }
                .padding(.horizontal)
                
                Button(action: {
                    isSignUp.toggle()
                }) {
                    Text(isSignUp ? "Already have an account? Login" : "Don't have an account? Sign Up")
                        .foregroundColor(Theme.primaryGreen)
                }
                
                Spacer()
            }
            .padding(.top, 40)
        }
        .background(Theme.backgroundGreen.opacity(0.1))
        .navigationTitle(isSignUp ? "Sign Up" : "Login")
        .navigationBarTitleDisplayMode(.inline)
        .toolbar {
            ToolbarItem(placement: .principal) {
                Text(isSignUp ? "Sign Up" : "Login")
                    .font(.system(size: 24, weight: .bold))
                    .foregroundColor(Theme.textColor)
            }
        }
        .alert("Error", isPresented: $showError) {
            Button("OK", role: .cancel) { }
        } message: {
            Text(errorMessage)
        }
    }
}

struct CustomTextField: View {
    let icon: String
    let placeholder: String
    @Binding var text: String
    var isSecure: Bool = false
    
    var body: some View {
        HStack(spacing: 15) {
            Image(systemName: icon)
                .foregroundColor(Theme.primaryGreen)
                .frame(width: 20)
            
            if isSecure {
                SecureField(placeholder, text: $text)
            } else {
                TextField(placeholder, text: $text)
            }
        }
        .padding()
        .background(Color.white)
        .cornerRadius(12)
        .shadow(color: .black.opacity(0.05), radius: 5, y: 2)
    }
}

// Add this new view for password requirements
struct PasswordRequirementRow: View {
    let isValid: Bool
    let text: String
    
    var body: some View {
        HStack {
            Image(systemName: isValid ? "checkmark.circle.fill" : "circle")
                .foregroundColor(isValid ? .green : .gray)
            Text(text)
                .font(.caption)
                .foregroundColor(.gray)
        }
    }
}

// Keep all the existing view code, but replace the preview at the bottom with:

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        let authManager = AuthenticationManager()
        let userManager = UserManager()
        
        return Group {
            // Preview the landing view
            LandingView()
                .environmentObject(authManager)
                .environmentObject(userManager)
            
            // Preview the login view
            LoginView()
                .environmentObject(authManager)
                .environmentObject(userManager)
            
            // Preview the main app view
            MainAppView()
                .environmentObject(authManager)
                .environmentObject(userManager)
        }
    }
}
