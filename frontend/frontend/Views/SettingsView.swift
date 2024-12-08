import SwiftUI

struct SettingsView: View {
    @Environment(\.dismiss) var dismiss
    @EnvironmentObject var authManager: AuthenticationManager
    @EnvironmentObject var userManager: UserManager
    @State private var showDeleteAccountAlert = false
    
    var body: some View {
        NavigationView {
            List {
                Section {
                    Button(action: {
                        try? authManager.signOut()
                        dismiss()
                    }) {
                        HStack {
                            Label("Sign Out", systemImage: "rectangle.portrait.and.arrow.right")
                            Spacer()
                        }
                        .foregroundColor(.red)
                    }
                    
                    Button(action: {
                        showDeleteAccountAlert = true
                    }) {
                        HStack {
                            Label("Delete Account", systemImage: "person.crop.circle.badge.minus")
                            Spacer()
                        }
                        .foregroundColor(.red)
                    }
                } header: {
                    Text("Account")
                }
            }
            .navigationTitle("Settings")
            .navigationBarTitleDisplayMode(.large)
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button("Done") {
                        dismiss()
                    }
                    .foregroundColor(Theme.primaryGreen)
                }
            }
            .alert("Delete Account", isPresented: $showDeleteAccountAlert) {
                Button("Cancel", role: .cancel) { }
                Button("Delete", role: .destructive) {
                    Task {
                        do {
                            // Delete user profile first
                            try await userManager.deleteUserProfile()
                            // Then delete authentication account
                            try await authManager.deleteAccount()
                            dismiss()
                        } catch {
                            print("Error deleting account: \(error)")
                        }
                    }
                }
            } message: {
                Text("Are you sure you want to delete your account? This action cannot be undone.")
            }
        }
    }
} 