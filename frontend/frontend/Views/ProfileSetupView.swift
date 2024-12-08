import SwiftUI

struct ProfileSetupView: View {
    @Environment(\.dismiss) var dismiss
    @EnvironmentObject var authManager: AuthenticationManager
    @EnvironmentObject var userManager: UserManager
    
    @State private var fullName = ""
    @State private var dateOfBirth = Date()
    @State private var location = ""
    @State private var showError = false
    @State private var errorMessage = ""
    @State private var isLoading = false
    @State private var showCancelAlert = false
    
    // Date formatter for validation
    private let minimumAge = Calendar.current.date(byAdding: .year, value: -13, to: Date()) ?? Date()
    
    var isFormValid: Bool {
        !fullName.trimmingCharacters(in: .whitespaces).isEmpty &&
        !location.trimmingCharacters(in: .whitespaces).isEmpty &&
        dateOfBirth <= minimumAge
    }
    
    var body: some View {
        ScrollView {
            VStack(spacing: 25) {
                // Header
                VStack(spacing: 10) {
                    Image(systemName: "person.crop.circle.badge.plus")
                        .font(.system(size: 70))
                        .foregroundColor(Theme.primaryGreen)
                    
                    Text("Tell us a bit about yourself")
                        .font(.system(size: 18))
                        .foregroundColor(Theme.textColor.opacity(0.7))
                }
                .padding(.top, 40)
                
                // Form Fields
                VStack(spacing: 20) {
                    CustomTextField(
                        icon: "person",
                        placeholder: "Full Name",
                        text: $fullName
                    )
                    
                    // Custom Date Picker
                    HStack(spacing: 15) {
                        Image(systemName: "calendar")
                            .foregroundColor(Theme.primaryGreen)
                            .frame(width: 20)
                        
                        DatePicker(
                            "Date of Birth",
                            selection: $dateOfBirth,
                            in: ...minimumAge,
                            displayedComponents: .date
                        )
                        .accentColor(Theme.primaryGreen)
                    }
                    .padding()
                    .background(Color.white)
                    .cornerRadius(12)
                    .shadow(color: .black.opacity(0.05), radius: 5, y: 2)
                    
                    CustomTextField(
                        icon: "location",
                        placeholder: "Location",
                        text: $location
                    )
                }
                .padding(.horizontal)
                
                // Submit Button
                Button(action: submitProfile) {
                    ZStack {
                        Text("Complete Setup")
                            .font(.system(size: 18, weight: .bold))
                            .foregroundColor(.white)
                            .opacity(isLoading ? 0 : 1)
                        
                        if isLoading {
                            ProgressView()
                                .tint(.white)
                        }
                    }
                    .frame(maxWidth: .infinity)
                    .frame(height: 56)
                    .background(isFormValid ? Theme.primaryGreen : Theme.primaryGreen.opacity(0.5))
                    .cornerRadius(16)
                    .shadow(color: Theme.primaryGreen.opacity(0.3), radius: 8, y: 4)
                }
                .disabled(!isFormValid || isLoading)
                .padding(.horizontal)
                .padding(.top, 20)
            }
        }
        .background(Theme.backgroundGreen.opacity(0.1))
        .navigationTitle("Complete Profile")
        .navigationBarTitleDisplayMode(.inline)
        .toolbar {
            ToolbarItem(placement: .principal) {
                Text("Complete Profile")
                    .font(.system(size: 24, weight: .bold))
                    .foregroundColor(Theme.textColor)
            }
            ToolbarItem(placement: .navigationBarLeading) {
                Button("Cancel") {
                    showCancelAlert = true
                }
                .foregroundColor(Theme.primaryGreen)
            }
        }
        .alert("Cancel Setup", isPresented: $showCancelAlert) {
            Button("Continue Setup", role: .cancel) { }
            Button("Cancel", role: .destructive) {
                Task {
                    do {
                        // Delete the user profile if it exists
                        try await userManager.deleteUserProfile()
                        // Delete the authentication account
                        try await authManager.deleteAccount()
                    } catch {
                        print("Error during cancellation: \(error)")
                    }
                }
            }
        } message: {
            Text("Are you sure you want to cancel? Your account will be deleted if setup is not completed.")
        }
        .alert("Error", isPresented: $showError) {
            Button("OK", role: .cancel) { }
        } message: {
            Text(errorMessage)
        }
        .navigationBarBackButtonHidden(true)
        .onAppear {
            print("Debug: ProfileSetupView appeared") // Add debug print
        }
    }
    
    private func submitProfile() {
        guard let userId = authManager.user?.uid,
              let email = authManager.user?.email else {
            return
        }
        
        isLoading = true
        
        Task {
            do {
                try await userManager.createUserProfile(
                    userId: userId,
                    email: email,
                    fullName: fullName.trimmingCharacters(in: .whitespaces),
                    dateOfBirth: dateOfBirth,
                    location: location.trimmingCharacters(in: .whitespaces)
                )
                isLoading = false
            } catch {
                isLoading = false
                errorMessage = "Failed to save profile. Please try again."
                showError = true
            }
        }
    }
} 