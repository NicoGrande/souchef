import Foundation
import FirebaseFirestore
import FirebaseAuth

struct UserProfile: Codable {
    let userId: String
    let email: String
    let fullName: String
    let dateOfBirth: Date
    let location: String
    var createdAt: Date
}

class UserManager: ObservableObject {
    @Published var currentUserProfile: UserProfile?
    private let db = Firestore.firestore()
    
    func createUserProfile(userId: String, email: String, fullName: String, dateOfBirth: Date, location: String) async throws {
        let profile = UserProfile(
            userId: userId,
            email: email,
            fullName: fullName,
            dateOfBirth: dateOfBirth,
            location: location,
            createdAt: Date()
        )
        
        try await db.collection("users").document(userId).setData([
            "userId": profile.userId,
            "email": profile.email,
            "fullName": profile.fullName,
            "dateOfBirth": Timestamp(date: profile.dateOfBirth),
            "location": profile.location,
            "createdAt": Timestamp(date: profile.createdAt)
        ])
        
        DispatchQueue.main.async {
            self.currentUserProfile = profile
        }
    }
    
    func fetchUserProfile() async throws {
        guard let userId = Auth.auth().currentUser?.uid else { 
            DispatchQueue.main.async {
                self.currentUserProfile = nil
            }
            return 
        }
        
        let document = try await db.collection("users").document(userId).getDocument()
        
        if !document.exists {
            DispatchQueue.main.async {
                self.currentUserProfile = nil
            }
            return
        }
        
        guard let data = document.data() else { 
            DispatchQueue.main.async {
                self.currentUserProfile = nil
            }
            return 
        }
        
        let userProfile = UserProfile(
            userId: data["userId"] as? String ?? "",
            email: data["email"] as? String ?? "",
            fullName: data["fullName"] as? String ?? "",
            dateOfBirth: (data["dateOfBirth"] as? Timestamp)?.dateValue() ?? Date(),
            location: data["location"] as? String ?? "",
            createdAt: (data["createdAt"] as? Timestamp)?.dateValue() ?? Date()
        )
        
        DispatchQueue.main.async {
            self.currentUserProfile = userProfile
        }
    }
    
    func deleteUserProfile() async throws {
        guard let userId = Auth.auth().currentUser?.uid else { return }
        try await db.collection("users").document(userId).delete()
        DispatchQueue.main.async {
            self.currentUserProfile = nil
        }
    }
} 