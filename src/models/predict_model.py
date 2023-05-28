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
    encode,
    BATCH_SIZE,
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

text = "В Литтл-Хэнглтоне по-прежнему зовут его Домом Реддлов,"
data = encode(text_seq=text, tokenizer=tokenizer)
ix = torch.arange(len(data) - 1, 0, -BLOCK_SIZE, dtype=int)
ix = torch.flip(ix,[0])


# print(data)
# print(ix)

# we stack batch_size rows of sentences
# so x and y are the matrices with rows_num=batch_size
# and col_num=block_size
x = torch.stack([data[-BLOCK_SIZE::]])
# example to decode sequence
# context = torch.zeros((1, 1), dtype=torch.long, device=DEVICE)
context = x.to(DEVICE)
# print(context)
# print(context.shape)
print(
    decode(
        enc_sec=m.generate(idx=context, max_new_tokens=100, block_size=BLOCK_SIZE)[0],
        tokenizer=tokenizer,
    )
)
