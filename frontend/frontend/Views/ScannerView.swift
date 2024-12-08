import SwiftUI
import AVFoundation

enum ScanStep {
    case receiptPrompt
    case receiptScan
    case itemPrompt
    case itemScan
}

struct ScannerView: View {
    @Environment(\.dismiss) var dismiss
    @StateObject private var viewModel = ScannerViewModel()
    @Binding var scannedCode: String  // We'll update this to handle images later
    
    var body: some View {
        NavigationView {
            ZStack {
                switch viewModel.currentStep {
                case .receiptPrompt:
                    PromptView(
                        title: "Scan Receipt",
                        description: "Take a photo of your receipt to automatically extract item details",
                        primaryButton: "Scan Receipt",
                        secondaryButton: "Skip",
                        primaryAction: { viewModel.currentStep = .receiptScan },
                        secondaryAction: { viewModel.currentStep = .itemPrompt }
                    )
                
                case .receiptScan:
                    CameraView(
                        title: "Receipt Scanner",
                        instruction: "Position receipt within frame",
                        onCapture: { image in
                            viewModel.receiptImage = image
                            viewModel.currentStep = .itemPrompt
                        },
                        onCancel: {
                            viewModel.currentStep = .receiptPrompt
                        }
                    )
                
                case .itemPrompt:
                    PromptView(
                        title: "Scan Items",
                        description: "Take photos of your items to help identify them",
                        primaryButton: "Scan Items",
                        secondaryButton: "Skip",
                        primaryAction: { viewModel.currentStep = .itemScan },
                        secondaryAction: { 
                            viewModel.processImages()
                            dismiss()
                        }
                    )
                
                case .itemScan:
                    CameraView(
                        title: "Item Scanner",
                        instruction: "Position item within frame",
                        onCapture: { image in
                            viewModel.itemImages.append(image)
                            viewModel.showMoreItemsPrompt = true
                        },
                        onCancel: {
                            viewModel.currentStep = .itemPrompt
                        }
                    )
                }
            }
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarLeading) {
                    Button("Cancel") {
                        dismiss()
                    }
                    .foregroundColor(Theme.primaryGreen)
                }
                
                if viewModel.currentStep != .receiptPrompt {
                    ToolbarItem(placement: .navigationBarTrailing) {
                        Button("Back") {
                            switch viewModel.currentStep {
                            case .receiptScan:
                                viewModel.currentStep = .receiptPrompt
                            case .itemPrompt:
                                viewModel.currentStep = .receiptPrompt
                            case .itemScan:
                                viewModel.currentStep = .itemPrompt
                            case .receiptPrompt:
                                break
                            }
                        }
                        .foregroundColor(Theme.primaryGreen)
                    }
                }
            }
        }
        .alert("Add Another Item?", isPresented: $viewModel.showMoreItemsPrompt) {
            Button("Scan More") {
                viewModel.showMoreItemsPrompt = false
            }
            Button("Finish") {
                viewModel.processImages()
                dismiss()
            }
        }
    }
}

struct PromptView: View {
    let title: String
    let description: String
    let primaryButton: String
    let secondaryButton: String
    let primaryAction: () -> Void
    let secondaryAction: () -> Void
    
    var body: some View {
        VStack(spacing: 24) {
            Spacer()
            
            VStack(spacing: 16) {
                Text(title)
                    .font(.system(size: 24, weight: .bold))
                    .foregroundColor(Theme.textColor)
                
                Text(description)
                    .font(.system(size: 16))
                    .foregroundColor(Theme.textColor.opacity(0.8))
                    .multilineTextAlignment(.center)
                    .padding(.horizontal)
            }
            
            Spacer()
            
            VStack(spacing: 16) {
                Button(action: primaryAction) {
                    Text(primaryButton)
                        .font(.system(size: 18, weight: .semibold))
                        .foregroundColor(.white)
                        .frame(maxWidth: .infinity)
                        .frame(height: 56)
                        .background(Theme.primaryGreen)
                        .cornerRadius(16)
                }
                
                Button(action: secondaryAction) {
                    Text(secondaryButton)
                        .font(.system(size: 18, weight: .medium))
                        .foregroundColor(Theme.primaryGreen)
                }
            }
            .padding(.horizontal, 24)
            .padding(.bottom, 40)
        }
        .background(Theme.backgroundGreen.opacity(0.1))
    }
}

struct CameraView: View {
    let title: String
    let instruction: String
    let onCapture: (UIImage) -> Void
    let onCancel: () -> Void
    
    @StateObject private var camera = CameraModel()
    
    var body: some View {
        ZStack {
            CameraPreview(session: camera.session)
                .ignoresSafeArea()
            
            VStack {
                Spacer()
                
                // Scanning frame
                Rectangle()
                    .stroke(style: StrokeStyle(lineWidth: 2, dash: [10]))
                    .foregroundColor(Theme.primaryGreen)
                    .frame(width: 300, height: 400)
                
                Spacer()
                
                // Instructions text
                Text(instruction)
                    .font(.system(size: 16, weight: .medium))
                    .foregroundColor(.white)
                    .padding()
                    .background(.black.opacity(0.7))
                    .cornerRadius(8)
                
                // Capture button
                Button(action: {
                    camera.captureImage { image in
                        if let image = image {
                            onCapture(image)
                        }
                    }
                }) {
                    Circle()
                        .fill(.white)
                        .frame(width: 70, height: 70)
                        .overlay(
                            Circle()
                                .stroke(Theme.primaryGreen, lineWidth: 2)
                                .frame(width: 60, height: 60)
                        )
                }
                .padding(.vertical, 30)
            }
        }
        .onAppear {
            camera.requestAccess()
        }
    }
}

struct CameraPreview: UIViewRepresentable {
    let session: AVCaptureSession
    
    func makeUIView(context: Context) -> UIView {
        let view = UIView(frame: UIScreen.main.bounds)
        
        let previewLayer = AVCaptureVideoPreviewLayer(session: session)
        previewLayer.frame = view.frame
        previewLayer.videoGravity = .resizeAspectFill
        view.layer.addSublayer(previewLayer)
        
        return view
    }
    
    func updateUIView(_ uiView: UIView, context: Context) {
        if let previewLayer = uiView.layer.sublayers?.first as? AVCaptureVideoPreviewLayer {
            previewLayer.frame = uiView.frame
        }
    }
}

class ScannerViewModel: ObservableObject {
    @Published var currentStep: ScanStep = .receiptPrompt
    @Published var showMoreItemsPrompt = false
    @Published var receiptImage: UIImage?
    @Published var itemImages: [UIImage] = []
    
    func processImages() {
        // TODO: Process captured images with AI
        // This will be implemented when we add AI integration
    }
}

class CameraModel: NSObject, ObservableObject {
    @Published var session = AVCaptureSession()
    private let output = AVCapturePhotoOutput()
    private var completionHandler: ((UIImage?) -> Void)?
    
    override init() {
        super.init()
        self.session.sessionPreset = .photo
    }
    
    func requestAccess() {
        switch AVCaptureDevice.authorizationStatus(for: .video) {
        case .authorized:
            self.setupCamera()
        case .notDetermined:
            AVCaptureDevice.requestAccess(for: .video) { [weak self] granted in
                if granted {
                    DispatchQueue.main.async {
                        self?.setupCamera()
                    }
                }
            }
        default:
            break
        }
    }
    
    private func setupCamera() {
        guard let device = AVCaptureDevice.default(for: .video),
              let input = try? AVCaptureDeviceInput(device: device) else { return }
        
        if session.canAddInput(input) && session.canAddOutput(output) {
            session.beginConfiguration()
            session.addInput(input)
            session.addOutput(output)
            session.commitConfiguration()
            
            DispatchQueue.global(qos: .userInitiated).async { [weak self] in
                self?.session.startRunning()
            }
        }
    }
    
    func captureImage(completion: @escaping (UIImage?) -> Void) {
        self.completionHandler = completion
        
        let settings = AVCapturePhotoSettings()
        self.output.capturePhoto(with: settings, delegate: self)
    }
}

extension CameraModel: AVCapturePhotoCaptureDelegate {
    func photoOutput(_ output: AVCapturePhotoOutput, didFinishProcessingPhoto photo: AVCapturePhoto, error: Error?) {
        guard let data = photo.fileDataRepresentation(),
              let image = UIImage(data: data) else {
            completionHandler?(nil)
            return
        }
        
        completionHandler?(image)
    }
} 