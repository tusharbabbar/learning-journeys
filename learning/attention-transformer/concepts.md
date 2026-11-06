# Attention → Transformer: core concepts

Status: `proposed` (drafted by the assistant), `kept` (you said it's worth having) or `dropped`.
**Real-life link** is filled in only from your own words.

---

### Fixed-length bottleneck
- **Status:** proposed
- **Definition:** In an encoder-decoder without attention, the whole input sentence is squeezed into one vector of fixed size, so long inputs lose detail.
- **Related:** Encoder-decoder, Context vector, Attention
- **Real-life link:**
- **Study:** R1, R2, R3

### Encoder-decoder
- **Status:** proposed
- **Definition:** Two networks: one reads the input into a representation, the other generates the output from it.
- **Related:** Fixed-length bottleneck, Cross-attention, Decoder-only model
- **Real-life link:**
- **Study:** R2, R4, R18

### Attention
- **Status:** proposed
- **Definition:** At each step, score every available input position for relevance and take a weighted mix of them, instead of relying on one carried memory.
- **Related:** Attention weights, Context vector, Self-attention
- **Real-life link:**
- **Study:** R1, R18, R21, R29

### Alignment
- **Status:** proposed
- **Definition:** Which input words an output word draws on; attention learns it softly, without anyone labelling it.
- **Related:** Attention, Attention weights
- **Real-life link:**
- **Study:** R1, R5

### Attention weights
- **Status:** proposed
- **Definition:** Relevance scores passed through softmax so they are positive and sum to one; they decide how much each position contributes.
- **Related:** Scaled dot-product attention, Alignment
- **Real-life link:**
- **Study:** R1, R23, R31

### Context vector
- **Status:** proposed
- **Definition:** The weighted mix of input states built fresh for each output step; replaces the single fixed vector.
- **Related:** Fixed-length bottleneck, Attention weights
- **Real-life link:**
- **Study:** R1, R18

### Additive vs dot-product scoring
- **Status:** proposed
- **Definition:** Two ways to score relevance: a small learned network (Bahdanau) or a plain dot product of two vectors (Luong); the Transformer uses the scaled dot product.
- **Related:** Scaled dot-product attention, Attention
- **Real-life link:**
- **Study:** R1, R5, R22

### Self-attention
- **Status:** proposed
- **Definition:** Attention within a single text: every word attends to the other words of the same sequence to update its own meaning.
- **Related:** Query, key and value, Cross-attention, Multi-head attention
- **Real-life link:**
- **Study:** R7, R8, R19, R23

### Cross-attention
- **Status:** proposed
- **Definition:** Attention from one sequence to another, e.g. the decoder's words attending to the encoder's words in translation.
- **Related:** Self-attention, Encoder-decoder
- **Real-life link:**
- **Study:** R8, R31

### Query, key and value
- **Status:** proposed
- **Definition:** Three learned projections of each word: the query says what it's looking for, the key what it offers to be matched on, the value what it passes on if chosen.
- **Related:** Scaled dot-product attention, Self-attention
- **Real-life link:**
- **Study:** R8, R19, R23, R29

### Scaled dot-product attention
- **Status:** proposed
- **Definition:** Score = query·key divided by the square root of the vector size, softmaxed into weights over the values; the scaling keeps scores from saturating.
- **Related:** Query, key and value, Attention weights
- **Real-life link:**
- **Study:** R8, R31, R30

### Multi-head attention
- **Status:** proposed
- **Definition:** Several attention computations run in parallel with their own projections, then combined, so one layer can track several relationships at once.
- **Related:** Self-attention, Query, key and value
- **Real-life link:**
- **Study:** R8, R19, R23, R31

### Order-blindness
- **Status:** proposed
- **Definition:** Plain attention treats the input as an unordered set; without position information, reordered words give the same result.
- **Related:** Positional encoding, RoPE
- **Real-life link:**
- **Study:** R27, R24

### Positional encoding
- **Status:** proposed
- **Definition:** A position-dependent vector (sinusoidal or learned) added to each word's embedding so attention can use order.
- **Related:** Order-blindness, RoPE
- **Real-life link:**
- **Study:** R8, R32

### RoPE (rotary position embedding)
- **Status:** proposed
- **Definition:** Encodes position by rotating queries and keys, so the attention score depends on how far apart two words are; used by most modern LLMs.
- **Related:** Positional encoding, Query, key and value
- **Real-life link:**
- **Study:** R12

### Causal masking
- **Status:** proposed
- **Definition:** Blocks each word from attending to later words, so the model can't see the answer when predicting the next token, while training still runs in parallel.
- **Related:** Decoder-only model, Self-attention, Parallel training
- **Real-life link:**
- **Study:** R8, R27, R31

### Feed-forward layer
- **Status:** proposed
- **Definition:** A small two-layer network applied to each word on its own after attention; holds about two-thirds of the parameters and much stored knowledge.
- **Related:** Transformer block, Residual stream
- **Real-life link:**
- **Study:** R8, R13, R27

### Residual stream
- **Status:** proposed
- **Definition:** The running vector for each word that every sub-layer reads from and adds its output to, rather than overwriting.
- **Related:** Layer normalization, Transformer block, Feed-forward layer
- **Real-life link:**
- **Study:** R9, R15, R6

### Layer normalization
- **Status:** proposed
- **Definition:** Rescales each word's vector to a standard range inside every block; placing it before each sub-layer (pre-norm) makes deep stacks train more stably.
- **Related:** Residual stream, Transformer block
- **Real-life link:**
- **Study:** R10, R11

### Transformer block
- **Status:** proposed
- **Definition:** Attention, then feed-forward, each wrapped in a residual connection and normalization; the unit stacked many times to form the model.
- **Related:** Multi-head attention, Feed-forward layer, Residual stream, Layer normalization
- **Real-life link:**
- **Study:** R8, R19, R24, R25

### Decoder-only model
- **Status:** proposed
- **Definition:** A stack of masked self-attention blocks with no encoder, trained to predict the next token; the GPT design.
- **Related:** Causal masking, Encoder-decoder, Transformer block
- **Real-life link:**
- **Study:** R14, R33, R15

### Parallel training
- **Status:** proposed
- **Definition:** Because no position waits for the previous one, all positions in a sequence are computed at once on GPUs, which made scale affordable.
- **Related:** Causal masking, Quadratic cost
- **Real-life link:**
- **Study:** R8, R19

### Quadratic cost
- **Status:** proposed
- **Definition:** Every word compares with every other, so attention's time and memory grow with the square of the input length.
- **Related:** Parallel training, Lost in the middle
- **Real-life link:**
- **Study:** R8, R16

### Lost in the middle
- **Status:** proposed
- **Definition:** Long-context models use facts at the start and end of their input more reliably than facts in the middle.
- **Related:** Quadratic cost, Attention weights
- **Real-life link:**
- **Study:** R17
