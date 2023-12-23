import torch
from model import Transformer
from transformers import GPT2Tokenizer
import click
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
)


@click.command()
@click.argument("text", type=click.STRING)
@click.argument("max_new_tokens", type=click.INT)
@click.argument("path_to_model", type=click.Path(exists=True))
def main(text: str, max_new_tokens: int, path_to_model: str):
    model_name_or_path = "sberbank-ai/rugpt3large_based_on_gpt2"
    tokenizer = GPT2Tokenizer.from_pretrained(model_name_or_path)
    vocab_size = tokenizer.vocab_size
    assert path_to_model.split('.')[-1] == "pt", "Wrong model extension"
    # load model from checkpoint
    m = load_model_from_checkpoint(
        Transformer,
        path_to_checkpoint=path_to_model,
        vocab_size=vocab_size,
        num_embed=NUM_EMBED,
        block_size=BLOCK_SIZE,
        num_heads=NUM_HEAD,
        num_layers=NUM_LAYER,
        dropout=DROPOUT,
    )
    text = text
    data = encode(text_seq=text, tokenizer=tokenizer)
    ix = torch.arange(len(data) - 1, 0, -BLOCK_SIZE, dtype=int)
    ix = torch.flip(ix, [0])

    x = torch.stack([data[-BLOCK_SIZE::]])
    # example to decode sequence
    context = x.to(DEVICE)
    print(
        decode(
            enc_sec=m.generate(
                idx=context, max_new_tokens=max_new_tokens, block_size=BLOCK_SIZE
            )[0],
            tokenizer=tokenizer,
        )
    )


if __name__ == "__main__":
    main()
