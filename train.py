import json
from click import clear
from nitk_utils import tokenize, stem, bag_of_words
import numpy as np
from sympy import print_glsl
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from model import NeuralNet
import torch.backends.cudnn as cudnn
cudnn.benchmark = True

with open('intents.json','r') as f:
    intents = json.load(f)

all_words= []
tags = []
xy = []

for intent in intents['intents']:
    tag = intent['tag']
    tags.append(tag)
    for pattern in intent['patterns']:
        w = tokenize(pattern) 
        all_words.extend(w)
        xy.append((w, tag))

ignore_words = ['?','!', '.',',']
all_words=[stem(w) for w in all_words if w not in ignore_words]
all_words= sorted(set(all_words))
tags= sorted(set(tags))

X_train = []
Y_tain = []
for (pattern_sentence, tag) in xy:
   bag = bag_of_words(pattern_sentence, all_words) 
   X_train.append(bag)

   label = tags.index(tag)
   Y_tain.append(label)

X_train = np.array(X_train)
Y_tain = np.array(Y_tain)

class ChatDataset(Dataset):
    def __init__(self):
        self.n_samples = len(X_train)
        self.x_data = X_train
        self.y_data = Y_tain
    
    def __getitem__(self, index):
        return self.x_data[index], self.y_data[index]
    
    def __len__(self):
        return self.n_samples   
     
if __name__ == '__main__':

    batch_size = 4 #8
    hidden_size = 8
    output_size = len(tags)
    input_size = len(X_train[0])
    #print(input_size, len(all_words))
    #print(output_size, tags)
    learning_rate =  0.001
    num_epochs = 500

    dataset = ChatDataset()
    train_loader = DataLoader(dataset=dataset, batch_size=batch_size, shuffle=True, num_workers=1, pin_memory=True)

    device = torch.device('cuda' if torch.cuda.is_available()else 'cpu')
    model= NeuralNet(input_size, hidden_size, output_size).to(device) 
    print(f"Using device: {device}")  # Should print "cuda" if using GPU

    criterion = nn.CrossEntropyLoss()
    optimizer =  torch.optim.Adam(model.parameters(), lr = learning_rate)

    for epoch in range(num_epochs):
        for (words, labels) in train_loader:
            words = words.to(device)
            labels = labels.to(device)

            outputs = model(words)
            loss = criterion(outputs, labels)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        
        if (epoch+1)%100 == 1:
            print(f'epoch {epoch+1}/{num_epochs}, loss={loss.item():0.4f}')

    print(f'final loss, loss={loss.item():0.4f}')

    data = {
        "model_state": model.state_dict(),
        "input_size": input_size,
        "output_size": output_size,
        "hidden_size": hidden_size,
        "all_words": all_words,
        "tags": tags
    }

    FILE = "data.pth"
    torch.save(data, FILE)

    print(f'training complete. File Saved to {FILE}')