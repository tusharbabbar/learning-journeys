# Attention → Transformer: design review

**Status:** draft at 10,000 ft · **Last updated:** 2026-11-07
Resource IDs like (R3) point to `resources.md`.

---

## 1. Problem statement

A sequence model has to produce output that depends on specific, possibly distant, parts of its input. In translation, the encoder-decoder LSTM reads the whole source sentence and passes the decoder a single fixed-length vector (R2). The decoder must then write every target word from that one summary.

**Failing case:** as source sentences get longer, translation quality from these encoder-decoders drops quickly (R3). A 40-word sentence has to fit in the same-sized vector as a 5-word one, and details from early in the sentence get lost by the time the decoder needs them (R1).

A second, practical limit: the model reads one word after another, so a sentence can't be processed in parallel, and training on large datasets is slow (R8, R28).

**Requirement:** when producing each output, the model can reach any part of the input directly, with a path that doesn't get longer with distance. Training must also run in parallel across a sequence so it scales to very large datasets.

---

## 2. Background

- **Encoder-decoder (seq2seq), 2014.** One LSTM encodes the source, another decodes the target from the encoder's final state (R2, R4). It was the first end-to-end neural translator to rival phrase-based systems.
- **LSTMs already ease the memory problem** inside one sequence, but the hand-off between encoder and decoder is still one vector, and steps still run one at a time.
- **Tricks before attention:** reversing the source sentence so early words sit near the decoder helped short-range alignment, but didn't remove the bottleneck (R2).
- **Convolutional sequence models** (ByteNet, ConvS2S) computed positions in parallel, but the number of steps linking two distant words still grew with their distance (R8).

---

## 3. Solution comparison

| | Seq2seq LSTM (no attention) | LSTM + attention (2014–2016) | Convolutional seq2seq | Transformer (2017) |
|---|---|---|---|---|
| How the decoder sees the input | One fixed vector (R2) | Fresh weighted mix of all encoder states per output word (R1, R5) | Stacked convolutions over the input (R8) | Self-attention within each text, cross-attention between them (R8) |
| Steps linking two distant words | Grows with distance | One hop decoder→encoder, but within each text still step-by-step | Grows with distance, more slowly (R8) | One attention step, any distance (R8) |
| Parallel across a sentence in training | No | No | Yes | Yes (R8) |
| Main weakness | Quality falls with length (R3) | Still sequential, slow to train at scale (R6) | Distant links need many layers (R8) | Cost grows with length squared (R16); uneven use of long inputs (R17) |
| Cost per layer, n words, width d (R8, Table 1) | ~n·d² | ~n·d² + n² attention | ~k·n·d² | ~n²·d (R8) |
| Best when | Short sequences, tiny models | Moderate data; was production default in 2016 (R6) | Fixed local patterns | Large data and hardware; today's default for language (R14) |

The Transformer won because it met both halves of the requirement at once: one step between any two words, and full parallelism in training. It matched or beat attention-LSTMs on translation at a fraction of the training cost (R8), and the same block scaled into decoder-only language models (R14). Its price is cost that grows with the square of the input length (R16), and long inputs aren't used evenly (R17).

---

## 4. Approach: how the Transformer meets the requirement

**Core idea.** Drop recurrence. At every layer, each word builds its new representation by attending to all the words it's allowed to see and taking a weighted mix of them (R8, R19).

**Key components.**
- **Self-attention with queries, keys and values:** each word's query is compared with every key; the scaled, softmaxed scores weight the values (R8, R31).
- **Multi-head attention:** several attention patterns in parallel, so one layer can track several relationships at once (R8, R23).
- **Positional information:** attention has no sense of order, so position is injected: sinusoidal or learned vectors originally (R8, R32), rotary encodings (RoPE) in most modern models (R12).
- **Causal masking:** in the decoder, each word can only attend to earlier words, which keeps next-word prediction honest and still lets training run in parallel (R8, R27).
- **Feed-forward layer:** a per-word network after attention, holding most of the parameters (R13).
- **Residuals and layer norm:** each sub-layer adds to a running residual stream and is normalized, so deep stacks stay trainable (R9, R10, R11, R15).
- **Stacking:** the block repeats many times; GPT-style models keep only the masked decoder stack (R14, R24).

**What it still doesn't solve.**
- **Quadratic cost:** comparing every word with every other makes long inputs expensive in time and memory; FlashAttention makes the exact computation faster, not cheaper in principle (R16).
- **Uneven use of long context:** information in the middle of long inputs is used less reliably than at the edges (R17).
- **Generation is still one token at a time:** parallelism helps training and reading the prompt, not writing the output (R8, R24).
- **Interpretability:** what individual heads and layers do is only partly understood (R15, R13).
