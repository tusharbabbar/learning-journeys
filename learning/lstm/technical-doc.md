# LSTM (Long Short-Term Memory)

**Baseline:** Vanilla (Elman) RNN trained with BPTT, and its vanishing/exploding gradient problem
**Status:** in progress · **Last updated:** 2026-11-04

Source IDs like [S1] point to `sources.json`. Claim IDs like (C4) point to `claims.json`. Every number has a script in `verify/` that prints it.

---

## 1. Problem statement

A recurrent network is supposed to carry information forward in its hidden state. In practice a vanilla RNN can't learn dependencies that span more than a short window.

**Failing example.** A model reads a long sequence and has to output something that depends on a token from 50 steps earlier. The training signal for that token has to travel back through 50 steps of BPTT. In a vanilla RNN each step multiplies the gradient by the recurrent Jacobian $W_{rec}^\top \mathrm{diag}(\sigma'(\cdot))$ (C1). With a per-step factor of 0.54, the signal that reaches step $t-50$ is about $4 \times 10^{-14}$ of its original size (C19, `verify/decay.py`). That's too small to change the weights, so the model never learns the dependency.

The goal is an architecture in which a gradient can travel hundreds of steps backward without shrinking or blowing up, while the network still controls what it stores and what it discards.

---

## 2. Prerequisites

| Concept | Status | Why it's needed |
|---|---|---|
| Feed-forward networks, backprop, chain rule | known | Gates are small feed-forward layers |
| Sigmoid and tanh, and their derivatives | known | Gates use sigmoid; $\tanh' \le 1$ drives decay |
| RNN recurrence and BPTT | known | LSTM keeps the same training procedure |
| Vanishing/exploding gradients, eigenvalue view | known | The problem LSTM solves |
| Elementwise (Hadamard) product | known | Every gate acts through $\odot$ |
| Gradient clipping | to learn | LSTM still needs it (Section 7) |
| GRU | to learn | The main competitor (Section 5) |
| Attention | to learn | What removed LSTM's sequential bottleneck |

---

## 3. Glossary

| Term | Meaning |
|---|---|
| **Cell state** $c_t$ | The LSTM's memory vector. Updated by addition, not overwritten. |
| **Hidden state** $h_t$ | The exposed output at step $t$: a gated, squashed view of $c_t$. |
| **Gate** | A sigmoid layer whose output in $(0,1)$ multiplies another vector elementwise, acting as a learned valve. |
| **Forget gate** $f_t$ | Scales how much of $c_{t-1}$ is kept. Added in 2000 [S2]. |
| **Input gate** $i_t$ | Scales how much of the new candidate is written into the cell. |
| **Output gate** $o_t$ | Scales how much of the cell is exposed as $h_t$. |
| **Candidate** $g_t$ | The proposed new content (Greff et al. call it the "block input"). |
| **Constant Error Carousel (CEC)** | The original cell's self-loop with fixed weight 1.0, which lets error flow back unchanged (C4). |
| **Peephole connections** | Optional links from the cell state into the gates [S4]. Not used in most modern libraries. |
| **Forget-gate bias** $b_f$ | Initial bias of the forget gate. Setting it to 1 matters a lot (C15). |

---

## 4. Lineage

| Year | Model | What it did | Where it failed |
|---|---|---|---|
| 1980s–1990 | Vanilla / Elman RNN | Hidden state carried across time, trained with BPTT or RTRL | Gradients vanish or explode exponentially with time lag (C1, C2) |
| 1997 | LSTM, original [S1] | Additive cell with a fixed self-loop of 1.0 (CEC) plus input and output gates (C4, C5). Bridged lags of more than 1000 steps (C6) | No way to forget. On continual streams, the cell state grows without bound (C9) |
| 2000 | LSTM + forget gate [S2] | A learned gate that lets the cell reset itself (C10) | Gives up exact gradient preservation; depends on forget-bias initialisation |
| 2013 | Gradient clipping [S3] | Caps the gradient norm and handles explosion in any RNN (C3) | Does nothing for vanishing gradients |

The step from RNN to LSTM is one swap: **the state update goes from a full rewrite through a weight matrix and tanh to an additive edit controlled by gates.**

---

## 5. Comparative analysis

| Dimension | Vanilla RNN | LSTM (1997) | LSTM + forget gate | GRU |
|---|---|---|---|---|
| State update | $h_t = \tanh(Wh_{t-1} + Ux_t)$ | $c_t = c_{t-1} + i \odot g$ | $c_t = f \odot c_{t-1} + i \odot g$ | Interpolates between old and new state |
| Backward factor on memory path | $W^\top\mathrm{diag}(\tanh')$ | 1 (exact) | $f_t$ (learned) | Update-gate driven |
| Can forget | Implicitly, always | No | Yes, learned | Yes |
| Gates | 0 | 2 | 3 | 2 |
| Params vs RNN | 1× | — | 4× (C20) | — (not yet verified) |
| Long lags | Short | > 1000 steps (C6) | Long | Long |

**When each one wins**
- **Vanilla RNN:** short dependencies and tiny models, where gates cost 4× the parameters for nothing.
- **LSTM + forget gate:** the default for long dependencies. Across 5400 runs no variant beat it significantly (C11).
- **GRU:** comparable quality with fewer gates. Once the LSTM gets a forget bias of 1, the gap between them disappears (C15).
- **Forget-gate-only LSTM:** beat the full LSTM on all five tasks in one study (C17). Promising, but a single paper.

GRU details are still to be researched; the GRU column holds only what the current sources support.

---

## 6. The solution in depth

### 6.1 Forward pass (standard LSTM, forget gate, no peepholes)

$$
\begin{aligned}
f_t &= \sigma(W_f x_t + R_f h_{t-1} + b_f)\\
i_t &= \sigma(W_i x_t + R_i h_{t-1} + b_i)\\
o_t &= \sigma(W_o x_t + R_o h_{t-1} + b_o)\\
g_t &= \tanh(W_g x_t + R_g h_{t-1} + b_g)\\
c_t &= f_t \odot c_{t-1} + i_t \odot g_t\\
h_t &= o_t \odot \tanh(c_t)
\end{aligned}
$$

- $x_t \in \mathbb{R}^m$: input
- $h_t, c_t \in \mathbb{R}^n$: hidden and cell states
- $W_\ast \in \mathbb{R}^{n\times m}$: input weights; $R_\ast \in \mathbb{R}^{n\times n}$: recurrent weights; $b_\ast$: biases
- $\sigma$: logistic sigmoid; $\odot$: elementwise product (C13)

```
            c_{t-1} ──(×f_t)──(+)──────────────► c_t
                               ▲          │
                         (×i_t)│        tanh
                               g_t        │
                               ▲        (×o_t)──► h_t
   [x_t, h_{t-1}] ──► σ,σ,σ,tanh ──────────┘
```

### 6.2 Why the gradient survives

Along the direct cell path:

$$
\frac{\partial c_t}{\partial c_{t-1}}\Big|_{\text{direct}} = \mathrm{diag}(f_t)
\quad\Rightarrow\quad
\frac{\partial c_t}{\partial c_k}\Big|_{\text{direct}} = \prod_{j=k+1}^{t}\mathrm{diag}(f_j)
$$

This path contains no $R$ matrix and no $\tanh'$ (C18). The gates depend on $h_{t-1}$, so there are also indirect paths through $R$, but the direct path alone is enough to carry long-range signal. With no forget gate ($f \equiv 1$), the factor is exactly 1: the CEC (C4, C8).

### 6.3 Worked example: gradient after 50 steps

Output of `verify/decay.py`:

| Model | Per-step factor | After 50 steps |
|---|---|---|
| Vanilla RNN ($w=0.9$, $\tanh'=0.6$) | 0.54 | $4.2\times10^{-14}$ |
| LSTM at init, $b_f=0$ ($f=0.5$) | 0.50 | $8.9\times10^{-16}$ |
| LSTM at init, $b_f=1$ ($f\approx0.73$) | 0.73 | $1.6\times10^{-7}$ |
| LSTM after learning to hold ($f=0.99$) | 0.99 | 0.61 |
| 1997 LSTM ($f=1$) | 1.00 | 1.0 |

**Reading it:** an LSTM is not better by default. With $b_f=0$ it starts out forgetting faster than this RNN. What the LSTM provides is a path the optimiser *can* push toward a factor of 1, and a forget bias of 1 starts that path roughly 8 orders of magnitude closer (C15, C19).

### 6.4 Cost

- **Parameters:** $4[n(n+m)+n]$. For $m=128$, $n=256$, that's 394,240, compared with 98,560 for an RNN. PyTorch reports 395,264 because it stores two bias vectors per gate (C20, `verify/params.py`).
- **Compute per step:** about 4× the RNN's matrix multiplies, usually fused into one $(4n)\times(n+m)$ GEMM.
- **BPTT memory:** caches $f, i, o, g, c$ at every step, about 5 vectors of size $n$ compared with 1 for an RNN.

---

## 7. Why it won, and where it doesn't

**Why it won**
- It solved long-lag tasks that no earlier recurrent algorithm could, with many more successful runs (C6, C7).
- It is robust: large ablations found nothing that reliably beats the standard form (C11, C14).
- The forget gate is the component that does the work (C12, C16, C17).

**Where it doesn't**
- **Exploding gradients are not fixed.** The indirect paths through $R$ can still blow up, so clipping is still needed (C3).
- **Initialisation trap.** With $b_f \le 0$, memory decays quickly at the start of training (C19).
- **Sequential bottleneck.** Steps can't be computed in parallel across time.
- **Fixed-size memory.** All of history has to fit in $n$ numbers.
- **Overkill for short dependencies:** 4× the parameters (C20).

**What came next:** the GRU (fewer gates), then attention and Transformers, which remove the sequential bottleneck and the fixed-size memory. Both are still to be researched.

---

## 8. References

| ID | Source | Type |
|---|---|---|
| S1 | Hochreiter & Schmidhuber, *Long Short-Term Memory*, Neural Computation, 1997 | paper |
| S2 | Gers, Schmidhuber & Cummins, *Learning to Forget*, Neural Computation, 2000 | paper |
| S3 | Pascanu, Mikolov & Bengio, *On the difficulty of training RNNs*, ICML 2013 | paper |
| S4 | Greff et al., *LSTM: A Search Space Odyssey*, IEEE TNNLS 2017 | benchmark |
| S5 | Jozefowicz, Zaremba & Sutskever, *An Empirical Exploration of Recurrent Network Architectures*, ICML 2015 | benchmark |
| S6 | van der Westhuizen & Lasenby, *The Unreasonable Effectiveness of the Forget Gate*, 2018 | paper |

URLs and notes for these, and for the cut sources S7–S10, are in `sources.json`.
