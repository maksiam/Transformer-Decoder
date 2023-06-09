import mlflow
import torch
from model import Transformer
from transformers import GPT2Tokenizer
import pandas as pd
from utils import (
    BATCH_SIZE,
    BLOCK_SIZE,
    DEVICE,
    DROPOUT,
    LEARNING_RATE,
    NUM_EMBED,
    NUM_HEAD,
    NUM_LAYER,
    MAX_ITER,
    EVAL_INTER,
    encode,
    decode,
    get_batch,
    save_model_to_chekpoint,
    estimate_loss,
)

params = {"BATCH_SIZE":BATCH_SIZE,
    "BLOCK_SIZE":BLOCK_SIZE,
    "DEVICE":DEVICE,
    "DROPOUT":DROPOUT,
    "LEARNING_RATE":LEARNING_RATE,
    "NUM_EMBED":NUM_EMBED,
    "NUM_HEAD":NUM_HEAD,
    "NUM_LAYER":NUM_LAYER,
    "MAX_ITER":MAX_ITER,
    "EVAL_INTER":EVAL_INTER,
    "encode":encode,
    "decode":decode,
    "get_batch":get_batch,
    "save_model_to_chekpoint":save_model_to_chekpoint,
    "estimate_loss":estimate_loss}

mlflow.set_tracking_uri("http://188.225.84.65:5000")
mlflow.set_experiment("transformer_decoder")
mlflow.pytorch.autolog()
with mlflow.start_run():
    mlflow.log_params(params)
    # raw data
    path_do_data = r"data/raw/hp_raw.parquet"
    df = pd.read_parquet(path_do_data)
    data_raw = " ".join(df.text)
    # we use pretrained tokenizer for performance improvements
    model_name_or_path = "sberbank-ai/rugpt3large_based_on_gpt2"
    tokenizer = GPT2Tokenizer.from_pretrained(model_name_or_path)
    vocab_size = tokenizer.vocab_size
    # data_raw = data_raw[4000000:] # short dataset

    # train/val split
    data = encode(text_seq=data_raw, tokenizer=tokenizer)
    n = int(0.9 * len(data))  # first 90% will be train, rest val
    train_data = data[:n]
    val_data = data[n:]

    # train a new model
    model = Transformer(
        vocab_size=vocab_size,
        num_embed=NUM_EMBED,
        block_size=BLOCK_SIZE,
        num_heads=NUM_HEAD,
        num_layers=NUM_LAYER,
        dropout=DROPOUT,
    )
    # load model to GPU if available
    m = model.to(DEVICE)
    # print the number of parameters in the model
    print(
        "Model with {:.2f}M parameters".format(
            sum(p.numel() for p in m.parameters()) / 1e6
        )
    )
    # optimizer takes the model's parameters and the learning rate as input,
    # and updates the parameters during the training process in order to
    # minimize the loss function.
    optimizer = torch.optim.AdamW(m.parameters(), lr=LEARNING_RATE)

    for step in range(MAX_ITER):
        # every EVAL_INTER evaluate the loss on train and val sets
        if step % EVAL_INTER == 0 or step == MAX_ITER - 1:
            loss_train = estimate_loss(
                data=train_data, model=m, block_size=BLOCK_SIZE, batch_size=BATCH_SIZE
            )
            loss_val = estimate_loss(
                data=val_data, model=m, block_size=BLOCK_SIZE, batch_size=BATCH_SIZE
            )
            print(
                "step {:10} | train loss {:6.4f} | val loss {:6.4f}".format(
                    step, loss_train, loss_val
                )
            )
        mlflow.log_metric('train loss', loss_train)
        mlflow.log_metric('val loss', loss_val)
        # sample a batch of data
        xb, yb = get_batch(
            data=train_data, block_size=BLOCK_SIZE, batch_size=BATCH_SIZE
        )
        logits, loss = m.forward(xb, yb)
        # zero_grad() method sets the gradients of all parameters in the optimizer to zero
        optimizer.zero_grad(set_to_none=True)
        # backward() method on the loss variable calculates the gradients
        # of the loss with respect to the model's parameters.
        loss.backward()
        # step() method on the optimizer updates the model's parameters
        # using the calculated gradients, in order to minimize the loss.
        optimizer.step()

    save_model_to_chekpoint(model=m, path_to_checkpoint="checkpoints", epoch=step)
    # generate some output based on the context
    context = torch.zeros((1, 1), dtype=torch.long, device=DEVICE)
    print(
        decode(
            enc_sec=m.generate(idx=context, max_new_tokens=100, block_size=BLOCK_SIZE)[
                0
            ],
            tokenizer=tokenizer,
        )
    )
