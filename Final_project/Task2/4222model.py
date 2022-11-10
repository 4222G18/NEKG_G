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

class BiLSTM_Model(nn.Module):
    def __init__(self,class_num,hid_dim):
        super(BiLSTM_Model,self).__init__()
        self.class_num = class_num
        self.hid_dim = hid_dim
        self.lstm = nn.LSTM(input_size=class_num, hidden_size=hid_dim, bidirectional=True)
        # fc
        self.fc = nn.Linear(hid_dim * 2, class_num)
    def forward(self,x):
        batch_size = x.shape[0]
        input = x.transpose(0, 1)  # input : [max_len, batch_size, n_class]

        hidden_state = torch.randn(1*2, batch_size, self.hid_dim)   # [num_layers(=1) * num_directions(=2), batch_size, n_hidden]
        cell_state = torch.randn(1*2, batch_size, self.hid_dim)     # [num_layers(=1) * num_directions(=2), batch_size, n_hidden]

        outputs, (_, _) = self.lstm(input, (hidden_state, cell_state))
        outputs = outputs[-1]  # [batch_size, n_hidden * 2]
        model = self.fc(outputs)  # model : [batch_size, n_class]
        return model

