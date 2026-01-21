# by default CycleGAN will try to load an unaligned dataset using unaligned_dataset.py, but I will use this custom data loader instead in order to load hsi images (which would normally be ignored by CycleGAN because they don't meet the expected file format)

import os
import torch
from torch.utils.data import Dataset
import numpy as np
import spectral
from data.image_folder import make_dataset

class HSIUnalignedDataset(Dataset):
    """
    This dataset class can load unaligned/unpaired datasets of HSI and RGB images.

    It requires two directories to host training images from domain A '/path/to/data/trainA'
    and from domain B '/path/to/data/trainB' respectively.
    You can train the model with the dataset flag '--dataroot /path/to/data'.
    Similarly, you need to prepare two directories:
    '/path/to/data/testA' and '/path/to/data/testB' during test time.
    """

    def __init__(self, opt):
        """Initialize this dataset class.

        Parameters:
            opt (Option class) -- stores all the experiment flags; needs to be a subclass of BaseOptions
        """
        
        self.opt = opt
        self.root = opt.dataroot
        
        self.dir_A = os.path.join(opt.dataroot, opt.phase + "A")  # create a path '/path/to/data/trainA'
        self.dir_B = os.path.join(opt.dataroot, opt.phase + "B")  # create a path '/path/to/data/trainB'

        self.A_paths = sorted(make_dataset(self.dir_A))  # load images from '/path/to/data/trainA'
        self.B_paths = sorted(make_dataset(self.dir_B))  # load images from '/path/to/data/trainB'
        self.A_size = len(self.A_paths)  # get the size of dataset A
        self.B_size = len(self.B_paths)  # get the size of dataset B

        # make sure any loading problems resulting in lack of images are obvious
        assert self.A_size > 0, f"No HSI images found in {self.dir_A}"
        assert self.B_size > 0, f"No HSI images found in {self.dir_B}"

    def __len__(self):
        return max(self.A_size, self.B_size)

    def load_hsi(self, hdr_path):
        pass



# keep building from unaligned_datasets.py