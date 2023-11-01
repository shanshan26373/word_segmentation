import torch
f = input("What is the png: ")
# model = torch.load("model/ResNet.pkl")
model = torch.load("model/ResNet.pkl", map_location=torch.device('cpu'))
print(model.predict(f"files/{f}"))