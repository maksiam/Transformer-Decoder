import torch
from model import Transformer
from transformers import GPT2Tokenizer
from utils import (
    load_model_from_checkpoint,
    decode,
    BLOCK_SIZE,
    DEVICE,
    NUM_EMBED,
    NUM_HEAD,
    NUM_LAYER,
    DROPOUT,
)

model_name_or_path = "sberbank-ai/rugpt3large_based_on_gpt2"
tokenizer = GPT2Tokenizer.from_pretrained(model_name_or_path)
vocab_size = tokenizer.vocab_size
# load model from checkpoint
m = load_model_from_checkpoint(
    Transformer,
    vocab_size=vocab_size,
    num_embed=NUM_EMBED,
    block_size=BLOCK_SIZE,
    num_heads=NUM_HEAD,
    num_layers=NUM_LAYER,
    dropout=DROPOUT,
)

# example to decode sequence
context = torch.zeros((1, 1), dtype=torch.long, device=DEVICE)
print(
    decode(
        enc_sec=m.generate(idx=context, max_new_tokens=100, block_size=BLOCK_SIZE)[0],
        tokenizer=tokenizer,
    )
)
