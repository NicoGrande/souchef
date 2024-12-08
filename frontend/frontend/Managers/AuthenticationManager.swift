import Foundation
import FirebaseAuth

enum AuthError: Error {
    case signInError
    case signUpError
    case signOutError
    case unknownError
}

class AuthenticationManager: ObservableObject {
    @Published var user: User?
    private var stateListener: AuthStateDidChangeListenerHandle?
    
    init() {
        user = Auth.auth().currentUser
        
        stateListener = Auth.auth().addStateDidChangeListener { [weak self] _, user in
            DispatchQueue.main.async {
                self?.user = user
            }
        }
    }
    
    deinit {
        // Remove the listener when the manager is deallocated
        if let handle = stateListener {
            Auth.auth().removeStateDidChangeListener(handle)
        }
    }
    
    func signIn(email: String, password: String) async throws {
        do {
            let result = try await Auth.auth().signIn(withEmail: email, password: password)
            DispatchQueue.main.async {
                self.user = result.user
            }
        } catch {
            print("Sign in error: \(error)")
            throw AuthError.signInError
        }
    }
    
    func signUp(email: String, password: String) async throws {
        do {
            let result = try await Auth.auth().createUser(withEmail: email, password: password)
            DispatchQueue.main.async {
                self.user = result.user
            }
        } catch {
            print("Sign up error: \(error)")
            throw AuthError.signUpError
        }
    }
    
    func signOut() throws {
        do {
            try Auth.auth().signOut()
            DispatchQueue.main.async {
                self.user = nil
            }
        } catch {
            print("Sign out error: \(error)")
            throw AuthError.signOutError
        }
    }
    
    func deleteAccount() async throws {
        try await Auth.auth().currentUser?.delete()
        DispatchQueue.main.async {
            self.user = nil
        }
    }
} 