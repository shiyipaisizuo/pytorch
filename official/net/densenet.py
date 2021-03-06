import os
import time

import torchvision
from torch import optim
from torch.utils import data
from torchvision import transforms

from official.net.denset_util import *

# Device configuration
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

WORK_DIR = '/tmp/imagenet'
NUM_EPOCHS = 10
BATCH_SIZE = 128
LEARNING_RATE = 1e-4

MODEL_PATH = './models'
MODEL_NAME = 'DenseNet.pth'

# Create model
if not os.path.exists(MODEL_PATH):
  os.makedirs(MODEL_PATH)

transform = transforms.Compose([
  transforms.RandomCrop(256, padding=32),
  transforms.RandomSizedCrop(224),
  transforms.RandomHorizontalFlip(),
  transforms.ToTensor(),
  transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])
])

# Load data
train_dataset = torchvision.datasets.ImageFolder(root=WORK_DIR + '/' + 'train',
                                                 transform=transform)

train_loader = torch.utils.data.DataLoader(dataset=train_dataset,
                                           batch_size=BATCH_SIZE,
                                           shuffle=True)


def main():
  print(f"Train numbers:{len(train_dataset)}")
  
  # load model
  model = densenet201().to(device)
  # cast
  cast = nn.CrossEntropyLoss().to(device)
  # Optimization
  optimizer = optim.Adam(
    model.parameters(),
    lr=LEARNING_RATE,
    weight_decay=1e-8)
  step = 1
  for epoch in range(1, NUM_EPOCHS + 1):
    model.train()
    
    # cal one epoch time
    start = time.time()
    
    for images, labels in train_loader:
      images = images.to(device)
      labels = labels.to(device)
      
      # Forward pass
      outputs = model(images)
      loss = cast(outputs, labels)
      
      # Backward and optimize
      optimizer.zero_grad()
      loss.backward()
      optimizer.step()
      
      print(f"Step [{step * BATCH_SIZE}/{NUM_EPOCHS * len(train_dataset)}], "
            f"Loss: {loss.item():.8f}.")
      step += 1
    
    # cal train one epoch time
    end = time.time()
    print(f"Epoch [{epoch}/{NUM_EPOCHS}], "
          f"time: {end - start} sec!")
    
    # Save the model checkpoint
    torch.save(model, MODEL_PATH + '/' + MODEL_NAME)
  print(f"Model save to {MODEL_PATH + '/' + MODEL_NAME}.")


if __name__ == '__main__':
  main()
