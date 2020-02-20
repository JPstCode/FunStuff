import torch
import torch.nn as nn

class CustomModule(nn.Module):
    def __init__(self, num_inputs, num_classes, dropout_prob=0.3):
        super(CustomModule, self).__init__()
        self.pipeline = nn.Sequential(
            nn.Linear(num_inputs, 5),
            nn.ReLU(),
            nn.Linear(5, 20),
            nn.ReLU(),
            nn.Linear(20, num_classes),
            nn.Dropout(p=dropout_prob),
            nn.Softmax(dim=None)
        )

    def forward(self, x):
        return self.pipeline(x)

if __name__ == '__main__':

    net = CustomModule(num_inputs=2, num_classes=3)
    v = torch.FloatTensor([[1,2]])

    out = net(v)
    print(net)
    print(out)