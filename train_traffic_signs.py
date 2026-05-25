import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms, models
import os
import time

# --- Setup & Hyperparameters ---
# This script is explicitly configured to train on the GTSRB (German Traffic Sign Recognition Benchmark)
# Download Dataset: https://www.kaggle.com/datasets/meowmeowmeowmeowmeow/gtsrb-german-traffic-sign

DATA_DIR = './data/gtsrb' # Extracted path for image dataset 
BATCH_SIZE = 64
EPOCHS = 10
LEARNING_RATE = 0.001
NUM_CLASSES = 43 # Standard GTSRB class count

def get_transforms():
    # Traffic signs vary in lighting and blur, so augments are crucial 
    train_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ColorJitter(brightness=0.2, contrast=0.2), # Simulating different road lighting
        transforms.RandomRotation(15),                        # Camera angle shifts
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    val_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    return train_transform, val_transform

def build_model():
    print("[INFO] Loading pre-trained MobileNet_V2 architecture...")
    # MobileNet is highly optimized for Edge Devices (like Raspberry Pi & Jetson Nano)
    model = models.mobilenet_v2(pretrained=True)
    
    # Freeze lower lightweight layers
    for param in model.parameters():
        param.requires_grad = False
        
    # Inject Custom Head for our Specific Traffic Sign Classes
    model.classifier[1] = nn.Sequential(
        nn.Dropout(p=0.2),
        nn.Linear(model.last_channel, NUM_CLASSES)
    )
    
    return model

def train_model():
    print("="*50)
    print("   AI Autonomous Traffic Sign Recognition Training")
    print("="*50)

    if not os.path.exists(DATA_DIR):
        print(f"\n[ERROR] Dataset not found at: {DATA_DIR}")
        print("Please download GTSRB dataset and extract it into a ./data/gtsrb folder.")
        print("Dataset Link: https://www.kaggle.com/datasets/meowmeowmeowmeowmeow/gtsrb-german-traffic-sign")
        return

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"[INFO] Compute Engine Detected: {device}")

    # Load Data
    train_transform, val_transform = get_transforms()
    
    try:
        train_dataset = datasets.ImageFolder(os.path.join(DATA_DIR, 'Train'), transform=train_transform)
        print(f"[INFO] Loaded {len(train_dataset)} training images.")
    except Exception as e:
        print("[ERROR] Failed to load dataset:", e)
        return

    train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True, num_workers=2)
    
    model = build_model().to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.classifier.parameters(), lr=LEARNING_RATE)
    
    # Training Loop
    print("\n[INFO] Commencing AI Matrix Training Routine...\n")
    start_time = time.time()
    
    for epoch in range(EPOCHS):
        model.train()
        running_loss = 0.0
        correct = 0
        total = 0
        
        for batch_idx, (inputs, labels) in enumerate(train_loader):
            inputs, labels = inputs.to(device), labels.to(device)
            
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            
            loss.backward()
            optimizer.step()
            
            running_loss += loss.item()
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()
            
            if batch_idx % 20 == 0:
                print(f"Epoch [{epoch+1}/{EPOCHS}] Batch [{batch_idx}/{len(train_loader)}] | "
                      f"Loss: {loss.item():.4f} | Accuracy: {100.*correct/total:.2f}%")
                      
    time_elapsed = time.time() - start_time
    print(f"\n[SUCCESS] Training completed in {time_elapsed // 60:.0f}m {time_elapsed % 60:.0f}s")
    
    # Export Weights
    export_path = 'model_traffic_signs_mobilenet.pth'
    torch.save(model.state_dict(), export_path)
    print(f"[EXPORT] AI neural edge weights saved to -> {export_path}")

if __name__ == "__main__":
    train_model()
