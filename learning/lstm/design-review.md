# LSTM: design review

**Status:** draft at 10,000 ft · **Last updated:** 2026-11-04
Resource IDs like (R3) point to `resources.md`.

---

## 1. Problem statement

A sequence model has to use information from far back in the input: a word at the start of a sentence, a sound a second ago, a stroke earlier in a handwritten line. Plain recurrent networks can't learn this when the gap is more than a few dozen steps. During training, the signal that would teach the network about an early input shrinks, or occasionally blows up, every time it passes back through a step (R3). Past a short horizon, the network gets no usable feedback about long-range dependencies.

**Requirement:** a recurrent architecture whose training signal survives hundreds of steps, while the network still learns what to keep and what to discard.

---

## 2. Background

- **Recurrent networks** carry a hidden state from step to step and are trained by unrolling them through time.
- At every step the hidden state is **fully rewritten**: multiplied by a weight matrix and squashed. Going backwards, the gradient is multiplied by that same kind of factor once per step, so it shrinks or grows exponentially with distance (R3).
- Before LSTM, the alternative learning algorithms of the time (RTRL, BPTT variants, Elman nets, sequence chunking) all struggled on long time lags (R1).
- **Gradient clipping** (R3) later handled the exploding side, but nothing short of changing the architecture fixes the vanishing side.

---

## 3. Solution comparison

| | Plain RNN | LSTM, 1997 | LSTM + forget gate, 2000 | GRU |
|---|---|---|---|---|
| How memory updates | Full rewrite each step | Additive, never forgets | Additive, learns to forget | Blends old and new state |
| Long-range signal | Fades exponentially | Passes through unchanged | Controlled by the forget gate | Controlled by its update gate |
| Gates | 0 | 2 (input, output) | 3 (forget, input, output) | 2 |
| Main weakness | Short memory | State grows forever on endless input (R2) | Sensitive to forget-bias init (R5) | Slightly less expressive (to confirm) |
| Cost vs plain RNN | 1× | — | ~4× | Less than LSTM |
| Best when | Short dependencies, tiny models | Historical only | The default for long dependencies (R4) | Similar quality at lower cost (R5) |

Ablations across thousands of runs found no LSTM variant that reliably beats the standard three-gate design, and they identified the forget gate as its most important part (R4, R5, R6).

---

## 4. Approach: how LSTM achieves it

**Core idea:** separate *memory* from *output*, and change memory by editing it rather than rewriting it.

- A **cell state** carries memory from step to step. Each step it is scaled by the **forget gate** (how much to keep), then a gated amount of new content is **added** through the **input gate**:
  $c_t = f_t \odot c_{t-1} + i_t \odot g_t$
- The **output gate** decides how much of the memory to expose as the hidden state used for predictions.
- Because memory changes by addition, the backward signal along the cell passes through only the forget gate's values, with no weight matrix and no squashing in between. When the network learns to hold a memory (forget gate near 1), the signal survives across long gaps (R1, R2).
- The original 1997 design fixed that path at exactly 1, which preserved the signal perfectly but meant the cell could never let go. The forget gate (2000) traded perfect preservation for learned, controllable decay (R2).

**What it doesn't solve:** exploding gradients still need clipping (R3); steps still run one after another; all history has to fit in a fixed-size memory. Attention-based models later addressed the last two.
