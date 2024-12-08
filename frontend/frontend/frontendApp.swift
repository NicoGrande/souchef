//
//  frontendApp.swift
//  frontend
//
//  Created by Nicolas Grande on 11/13/24.
//

import SwiftUI
import Firebase
import FirebaseCore
import FirebaseAuth

class AppDelegate: NSObject, UIApplicationDelegate {
    func application(_ application: UIApplication, didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey : Any]? = nil) -> Bool {
        FirebaseApp.configure()
        
        // Connect to Firebase emulators
        Auth.auth().useEmulator(withHost: "127.0.0.1", port: 9099)
        
        let settings = Firestore.firestore().settings
        settings.host = "127.0.0.1:8080"
        settings.isSSLEnabled = false
        settings.cacheSettings = MemoryCacheSettings()
        Firestore.firestore().settings = settings
        
        // Set the Firestore emulator
        Firestore.firestore().useEmulator(withHost: "127.0.0.1", port: 8080)
        
        print("Debug: Firebase configured with emulators")
        return true
    }
}

@main
struct frontendApp: App {
    @UIApplicationDelegateAdaptor(AppDelegate.self) var delegate
    @StateObject private var authManager = AuthenticationManager()
    @StateObject private var userManager = UserManager()
    
    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(authManager)
                .environmentObject(userManager)
        }
    }
}
