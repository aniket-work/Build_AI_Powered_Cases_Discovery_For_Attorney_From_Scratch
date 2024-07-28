import torch
print(torch.cuda.is_available())
print(torch.cuda.get_device_name(0))



import bitsandbytes
print(bitsandbytes.cuda.cuda_is_available())