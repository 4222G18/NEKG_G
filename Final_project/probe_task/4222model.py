import torch.nn as nn
import os
import logging
import random
import torch
import torch.optim as optim
from torch.nn.modules.loss import MSELoss
import numpy as np


class DecodingModel(nn.Module):
    def __init__(self,dim_in,dim_hid):
        super(DecodingModel,self).__init__()
        self.loss = MSELoss()
        self.dim_in = dim_in
        self.dim_hid = dim_hid
        self.network = nn.Sequential(
            nn.Linear(dim_in,dim_hid),
            nn.ReLU(),
            nn.Linear(dim_hid,dim_hid),
            nn.ReLU(),
            nn.Linear(dim_hid,1)
        )
    def forward(self,x):
        out = self.network(x)
        return out

class AdditionModel(nn.Module):
    def __init__(self,dim_in,dim_hid):
        super(AdditionModel,self).__init__()
        self.loss = MSELoss()
        self.dim_in = dim_in
        self.dim_hid = dim_hid
        self.network = nn.Sequential(
            nn.Linear(in_features=dim_in,out_features=dim_hid),
            nn.ReLU(),
            nn.Linear(in_features=dim_hid,out_features=dim_hid),
            nn.ReLU(),
            nn.Linear(in_features=dim_hid,out_features=1)
        )
    def forward(self,x):
        out = self.network(x)
        return out

