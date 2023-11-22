from __future__ import division
from __future__ import print_function
from __future__ import absolute_import


import torch
from torch.utils.data import DataLoader, Dataset

import pytorch_lightning as pl
from pytorch_lightning.utilities.types import EVAL_DATALOADERS, TRAIN_DATALOADERS

import numpy as np
import lmdb
import cv2
import os

from . import *


class LMDBDataModule(pl.LightningDataModule):
    def __init__(self) -> None:
        super(LMDBDataModule, self).__init__()

    def prepare_data(self) -> None:
        pass

    def setup(self, stage: str) -> None:
        if stage == "fit":
            self.train_dataset = LMDBDataSet("Train")
            self.valid_dataset = LMDBDataSet("Eval")
        if stage == "test":
            pass
    
    def train_dataloader(self) -> TRAIN_DATALOADERS:
        return DataLoader(self.train_dataset,
                          batch_size=cfg['Train']['loader']['batch_size'],
                          num_workers=cfg['Train']['loader']['num_workers'],
                          pin_memory=cfg['Train']['loader']['use_shared_memory'],
                          collate_fn=lmdb_collate_fn)
    
    def val_dataloader(self) -> EVAL_DATALOADERS:
        return DataLoader(self.valid_dataset,
                          batch_size=cfg['Eval']['loader']['batch_size'],
                          num_workers=cfg['Eval']['loader']['num_workers'],
                          pin_memory=cfg['Eval']['loader']['use_shared_memory'],
                          collate_fn=lmdb_collate_fn)
    
    def test_dataloader(self) -> EVAL_DATALOADERS:
        pass