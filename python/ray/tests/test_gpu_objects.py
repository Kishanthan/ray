import os
import torch
import torch.distributed as dist
import torch.multiprocessing as mp
import torch_npu

def init_process(rank, world_size):
    os.environ['MASTER_ADDR'] = '127.0.0.1'
    os.environ['MASTER_PORT'] = '29500'
    os.environ['HCCL_WHITELIST_DISABLE'] = '1'

    torch_npu.npu.set_device(rank)
    dist.init_process_group(backend='hccl', rank=rank, world_size=world_size)

def send_recv(rank, world_size):
    init_process(rank, world_size)
    dist.barrier()
    tensor_size = (2, 2)
    src = 1
    dst2 = 2
    dst3 = 3

    if rank == src:
        # Rank 1 creates a tensor and sends it to rank 3
        tensor = torch.randn(tensor_size).to(f"npu:{rank}")
        print(f"Rank {rank} sending tensor: {tensor}")
        dist.send(tensor, dst=dst2)
        print(dist.get_rank())
        dist.send(tensor, dst=dst3)
        print(dist.get_rank())



    elif rank == dst2:
        # Rank 3 receives the tensor from rank 1
        tensor = torch.empty(tensor_size).to(f"npu:{rank}")
        dist.recv(tensor, src=src)
        print(f"Rank {rank} received tensor: {tensor}")
        print(dist.get_rank())

    elif rank == dst3:
        # Rank 3 receives the tensor from rank 1
        tensor = torch.empty(tensor_size).to(f"npu:{rank}")
        dist.recv(tensor, src=src)
        print(f"Rank {rank} received tensor: {tensor}")
        print(dist.get_rank())




if __name__ == "__main__":
    world_size = 4
    mp.spawn(send_recv, args=(world_size,), nprocs=world_size, join=True)
