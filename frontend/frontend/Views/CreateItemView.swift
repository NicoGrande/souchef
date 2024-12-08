import SwiftUI
import AVFoundation

enum ActiveSheet: Identifiable {
    case storage, unit, servingUnit
    
    var id: Int {
        switch self {
        case .storage: return 0
        case .unit: return 1
        case .servingUnit: return 2
        }
    }
}

struct CreateItemView: View {
    @Environment(\.dismiss) var dismiss
    @StateObject private var viewModel = CreateItemViewModel()
    @State private var showScanner = false
    @State private var activeSheet: ActiveSheet?
    
    var body: some View {
        NavigationView {
            ScrollView {
                VStack(spacing: 20) {
                    Button(action: { showScanner = true }) {
                        HStack {
                            Image(systemName: "camera")
                                .font(.system(size: 24))
                            Text("Scan Items or Receipt")
                                .font(.system(size: 18, weight: .semibold))
                        }
                        .foregroundColor(.white)
                        .frame(maxWidth: .infinity)
                        .frame(height: 56)
                        .background(Theme.primaryGreen)
                        .cornerRadius(16)
                        .shadow(color: Theme.primaryGreen.opacity(0.3), radius: 8, y: 4)
                    }
                    .padding(.horizontal)
                    
                    Text("Or input item details manually")
                        .font(.system(size: 16))
                        .foregroundColor(Theme.textColor.opacity(0.6))
                        .padding(.vertical, 5)
                    
                    ItemDetailsSection(viewModel: viewModel, activeSheet: $activeSheet)
                    ServingInformationSection(viewModel: viewModel, activeSheet: $activeSheet)
                    StorageInformationSection(viewModel: viewModel, activeSheet: $activeSheet)
                }
                .padding(.vertical)
            }
            .background(Theme.backgroundGreen.opacity(0.1))
            .navigationTitle("Add Item")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarLeading) {
                    Button("Cancel") {
                        dismiss()
                    }
                    .foregroundColor(Theme.primaryGreen)
                }
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button("Save") {
                        Task {
                            await viewModel.saveItem()
                            dismiss()
                        }
                    }
                    .foregroundColor(Theme.primaryGreen)
                    .disabled(!viewModel.isValid)
                    .opacity(viewModel.isValid ? 1.0 : 0.5)
                }
            }
        }
        .sheet(item: $activeSheet) { sheet in
            NavigationView {
                SheetContent(sheet: sheet, viewModel: viewModel, activeSheet: $activeSheet)
                    .navigationTitle(sheet.title)
                    .navigationBarTitleDisplayMode(.inline)
                    .toolbar {
                        ToolbarItem(placement: .navigationBarTrailing) {
                            Button("Done") {
                                activeSheet = nil
                            }
                        }
                    }
            }
        }
        .sheet(isPresented: $showScanner) {
            ScannerView(scannedCode: $viewModel.scannedBarcode)
        }
        .alert("Error", isPresented: $viewModel.showError) {
            Button("OK", role: .cancel) { }
        } message: {
            Text(viewModel.errorMessage)
        }
    }
}

extension ActiveSheet {
    var title: String {
        switch self {
        case .storage: return "Select Storage Type"
        case .unit: return "Select Unit"
        case .servingUnit: return "Select Serving Unit"
        }
    }
}

struct ItemDetailsSection: View {
    @ObservedObject var viewModel: CreateItemViewModel
    @Binding var activeSheet: ActiveSheet?
    
    var body: some View {
        GroupBox(
            label: Label("Item Details", systemImage: "cart")
                .foregroundColor(Theme.textColor)
        ) {
            VStack(spacing: 15) {
                ThemedTextField(title: "Name", text: $viewModel.name)
                
                HStack {
                    ThemedTextField(title: "Quantity", text: $viewModel.quantity)
                        .keyboardType(.decimalPad)
                        .frame(maxWidth: .infinity)
                    
                    ThemedButton(
                        title: "Unit",
                        value: viewModel.unit.displayName,
                        action: { activeSheet = .unit }
                    )
                    .frame(maxWidth: .infinity)
                }
                
                ThemedTextField(title: "Price ($)", text: $viewModel.price)
                    .keyboardType(.decimalPad)
            }
            .padding(.vertical, 10)
        }
        .padding(.horizontal)
    }
}

struct ServingInformationSection: View {
    @ObservedObject var viewModel: CreateItemViewModel
    @Binding var activeSheet: ActiveSheet?
    
    var body: some View {
        GroupBox(
            label: Label("Serving Information", systemImage: "scalemass")
                .foregroundColor(Theme.textColor)
        ) {
            VStack(spacing: 15) {
                HStack {
                    ThemedTextField(title: "Serving Size", text: $viewModel.servingSize)
                        .keyboardType(.decimalPad)
                        .frame(maxWidth: .infinity)
                    
                    ThemedButton(
                        title: "Unit",
                        value: viewModel.servingSizeUnit.displayName,
                        action: { activeSheet = .servingUnit }
                    )
                    .frame(maxWidth: .infinity)
                }
                
                ThemedTextField(title: "Calories", text: $viewModel.calories)
                    .keyboardType(.decimalPad)
                
                HStack {
                    ThemedTextField(title: "Protein (g)", text: $viewModel.protein)
                        .keyboardType(.decimalPad)
                    
                    ThemedTextField(title: "Carbs (g)", text: $viewModel.carbs)
                        .keyboardType(.decimalPad)
                }
                
                ThemedTextField(title: "Fat (g)", text: $viewModel.fat)
                    .keyboardType(.decimalPad)
            }
            .padding(.vertical, 10)
        }
        .padding(.horizontal)
    }
}

struct StorageInformationSection: View {
    @ObservedObject var viewModel: CreateItemViewModel
    @Binding var activeSheet: ActiveSheet?
    
    var body: some View {
        GroupBox(
            label: Label("Storage Information", systemImage: "refrigerator")
                .foregroundColor(Theme.textColor)
        ) {
            VStack(spacing: 15) {
                ThemedButton(
                    title: "Storage Type",
                    value: viewModel.storageType.rawValue.capitalized,
                    action: { activeSheet = .storage }
                )
                
                DatePicker(
                    "Expiration Date",
                    selection: $viewModel.expirationDate,
                    displayedComponents: .date
                )
                .tint(Theme.primaryGreen)
            }
            .padding(.vertical, 10)
        }
        .padding(.horizontal)
    }
}

struct SheetContent: View {
    let sheet: ActiveSheet
    @ObservedObject var viewModel: CreateItemViewModel
    @Binding var activeSheet: ActiveSheet?
    
    var body: some View {
        switch sheet {
        case .storage:
            List {
                ForEach(StorageType.allCases, id: \.self) { type in
                    Button(type.rawValue.capitalized) {
                        viewModel.storageType = type
                        activeSheet = nil
                    }
                }
            }
        case .unit:
            List {
                ForEach(Unit.allCases, id: \.self) { unit in
                    Button(unit.displayName) {
                        viewModel.unit = unit
                        activeSheet = nil
                    }
                }
            }
        case .servingUnit:
            List {
                ForEach(Unit.allCases, id: \.self) { unit in
                    Button(unit.displayName) {
                        viewModel.servingSizeUnit = unit
                        activeSheet = nil
                    }
                }
            }
        }
    }
}

struct ThemedTextField: View {
    let title: String
    @Binding var text: String
    @State private var isFocused: Bool = false
    
    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text(title)
                .font(.system(size: 14, weight: .medium))
                .foregroundColor(Theme.textColor.opacity(0.8))
            
            TextField("", text: $text) { focused in
                isFocused = focused
                if focused && text == "0" || text == "0.0" || text == "0.00" {
                    text = ""
                }
                if !focused && text.isEmpty {
                    // Reset to appropriate default based on field type
                    if title.contains("Price") {
                        text = "0.00"
                    } else if title.contains("Calories") {
                        text = "0"
                    } else {
                        text = "0.0"
                    }
                }
            }
            .textFieldStyle(RoundedBorderTextFieldStyle())
            .overlay(
                RoundedRectangle(cornerRadius: 8)
                    .stroke(isFocused ? Theme.primaryGreen : Theme.primaryGreen.opacity(0.3), lineWidth: 1)
            )
        }
    }
}

// New ThemedButton component for consistent styling
struct ThemedButton: View {
    let title: String
    let value: String
    let action: () -> Void
    
    var body: some View {
        Button(action: action) {
            VStack(alignment: .leading, spacing: 8) {
                Text(title)
                    .font(.system(size: 14, weight: .medium))
                    .foregroundColor(Theme.textColor.opacity(0.8))
                
                HStack {
                    Text(value)
                        .foregroundColor(Theme.primaryGreen)
                    Spacer()
                    Image(systemName: "chevron.down")
                        .foregroundColor(Theme.primaryGreen)
                        .font(.system(size: 12))
                }
                .padding(.horizontal, 8)
                .padding(.vertical, 8)
                .background(Color.white)
                .cornerRadius(8)
                .overlay(
                    RoundedRectangle(cornerRadius: 8)
                        .stroke(Theme.primaryGreen.opacity(0.3), lineWidth: 1)
                )
            }
        }
    }
}

class CreateItemViewModel: ObservableObject {
    @Published var name = ""
    @Published var quantity: String = "0.0"
    @Published var unit: Unit = .none
    @Published var servingSizeUnit: Unit = .none
    @Published var price: String = "0.00"
    @Published var servingSize: String = "0.0"
    @Published var calories: String = "0"
    @Published var protein: String = "0.0"
    @Published var carbs: String = "0.0"
    @Published var fat: String = "0.0"
    @Published var storageType = StorageType.pantry
    @Published var expirationDate = Date()
    @Published var scannedBarcode = ""
    @Published var showError = false
    @Published var errorMessage = ""
    
    private let itemManager = ItemManager()
    
    var isValid: Bool {
        !name.isEmpty &&
        (Double(quantity) ?? 0) > 0 &&
        unit != .none &&
        (Double(price) ?? 0) >= 0 &&
        (Double(servingSize) ?? 0) > 0
    }
    
    func saveItem() async {
        do {
            let item = Item(
                id: UUID().uuidString,
                name: name,
                quantity: Item.Quantity(value: Double(quantity) ?? 0, unit: unit.rawValue),
                price: Double(price) ?? 0,
                perServingMacros: [
                    "calories": Item.Quantity(value: Double(calories) ?? 0, unit: "kcal"),
                    "protein": Item.Quantity(value: Double(protein) ?? 0, unit: "g"),
                    "carbs": Item.Quantity(value: Double(carbs) ?? 0, unit: "g"),
                    "fat": Item.Quantity(value: Double(fat) ?? 0, unit: "g")
                ],
                servingSize: Item.Quantity(value: Double(servingSize) ?? 0, unit: servingSizeUnit.rawValue),
                shelfLife: Calendar.current.dateComponents([.day], from: Date(), to: expirationDate).day ?? 0,
                storage: storageType,
                expirationDate: expirationDate
            )
            
            try await itemManager.createItem(item)
        } catch {
            DispatchQueue.main.async {
                self.errorMessage = "Failed to save item: \(error.localizedDescription)"
                self.showError = true
            }
        }
    }
}
