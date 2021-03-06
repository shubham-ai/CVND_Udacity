import torch.nn.functional as F
import torch.nn as nn

"""
Model definition for detecting facial keypoints. Outputs feature of size 136 i.e. x and y co-ordinates for 68 facial keypoints.
"""
class FaceNet(nn.Module):
  def __init__(self):
    super(FaceNet,self).__init__()
    self.conv1 = nn.Conv2d(1,16,5,stride=2,padding=3)
    self.bn1 = nn.BatchNorm2d(16)
    self.conv2 = nn.Conv2d(16,16,3)
    self.conv3 = nn.Conv2d(16,16,3)
    self.bn2 = nn.BatchNorm2d(16)
    self.mp1 = nn.MaxPool2d(2,2)
    self.conv4 = nn.Conv2d(16,32,3)
    self.conv5 = nn.Conv2d(32,32,3)
    self.bn3 = nn.BatchNorm2d(32)
    self.d1 = nn.Dropout(p=0.2)
    self.conv6 = nn.Conv2d(32,64,3)
    self.conv7 = nn.Conv2d(64,64,3)
    self.bn4 = nn.BatchNorm2d(64)
    self.d2 = nn.Dropout(p=0.2)
    self.conv8 = nn.Conv2d(64,128,3)
    self.conv9 = nn.Conv2d(128,128,3)
    self.bn5 = nn.BatchNorm2d(128)
    self.d3 = nn.Dropout(p=0.2)
    self.conv10 = nn.Conv2d(128,256,3)
    self.conv11 = nn.Conv2d(256,256,3)
    self.bn6 = nn.BatchNorm2d(256)
    self.d4 = nn.Dropout(p=0.2)
    self.gavg = nn.AdaptiveAvgPool2d((1,1))
    self.fc1 = nn.Linear(256,256)
    self.bn7 = nn.BatchNorm1d(256)
    self.d5 = nn.Dropout(p=0.5)
    self.fc2 = nn.Linear(256,256)
    self.bn8 = nn.BatchNorm1d(256)
    self.fc3 = nn.Linear(256,136)

  
  def forward(self,x):
    out = F.leaky_relu(self.bn1(self.conv1(x)),negative_slope=0.3)
    out = F.leaky_relu(self.conv2(out),negative_slope=0.3)
    out = F.leaky_relu(self.conv3(out),negative_slope=0.3)
    out = self.mp1(self.bn2(out))
    out = F.leaky_relu(self.conv4(out),negative_slope=0.3)
    out = F.leaky_relu(self.conv5(out),negative_slope=0.3)
    out = self.d1(self.bn3(out))
    out = F.leaky_relu(self.conv6(out),negative_slope=0.3)
    out = F.leaky_relu(self.conv7(out),negative_slope=0.3)
    out = self.d2(self.bn4(out))
    out = F.leaky_relu(self.conv8(out),negative_slope=0.3)
    out = F.leaky_relu(self.conv9(out),negative_slope=0.3)
    out = self.d3(self.bn5(out))
    out = F.leaky_relu(self.conv10(out),negative_slope=0.3)
    out = F.leaky_relu(self.conv11(out),negative_slope=0.3)
    out = self.d4(self.bn6(out))
    out = self.gavg(out)
    out = F.leaky_relu(self.fc1(out.view(out.shape[0],-1)),negative_slope=0.3)
    out = self.d5(self.bn7(out))
    out = F.leaky_relu(self.fc2(out),negative_slope=0.3)
    out = self.bn8(out)
    out = self.fc3(out)
    return out
