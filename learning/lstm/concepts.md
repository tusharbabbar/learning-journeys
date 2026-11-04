# LSTM: core concepts

Status: `proposed` (drafted by the assistant), `kept` (you said it's worth having) or `dropped`.
**Real-life link** is filled in only from your own words.

---

### Vanishing gradient
- **Status:** proposed
- **Definition:** The training signal shrinks exponentially as it travels back through time steps, so early inputs stop influencing learning.
- **Related:** Exploding gradient, Cell state
- **Real-life link:**
- **Study:** R3, R1

### Exploding gradient
- **Status:** proposed
- **Definition:** The same repeated multiplication makes the training signal grow out of control, destabilising training.
- **Related:** Vanishing gradient, Gradient clipping
- **Real-life link:**
- **Study:** R3

### Cell state
- **Status:** proposed
- **Definition:** LSTM's memory vector, carried across steps and changed by gated addition instead of being rewritten.
- **Related:** Forget gate, Input gate, Constant error carousel
- **Real-life link:**
- **Study:** R1, R9

### Gate
- **Status:** proposed
- **Definition:** A small learned layer that outputs values between 0 and 1 and multiplies another signal, acting as a valve.
- **Related:** Forget gate, Input gate, Output gate
- **Real-life link:**
- **Study:** R9, R1

### Forget gate
- **Status:** proposed
- **Definition:** Decides, at each step and from the current input, how much of the old memory to keep.
- **Related:** Cell state, Forget-gate bias
- **Real-life link:**
- **Study:** R2, R4, R6

### Input gate
- **Status:** proposed
- **Definition:** Decides how much of the newly proposed content gets written into memory.
- **Related:** Cell state, Gate
- **Real-life link:**
- **Study:** R1, R9

### Output gate
- **Status:** proposed
- **Definition:** Decides how much of the memory is exposed as the hidden state used for predictions.
- **Related:** Cell state, Gate
- **Real-life link:**
- **Study:** R1, R5

### Constant error carousel
- **Status:** proposed
- **Definition:** The 1997 design's self-loop with a fixed weight of 1, which lets the training signal pass back unchanged.
- **Related:** Cell state, Forget gate
- **Real-life link:**
- **Study:** R1, R8

### Forget-gate bias
- **Status:** proposed
- **Definition:** The forget gate's starting offset; setting it to 1 makes the cell remember by default and noticeably improves results.
- **Related:** Forget gate
- **Real-life link:**
- **Study:** R5, R2

### Gradient clipping
- **Status:** proposed
- **Definition:** Capping the size of the gradient during training to stop explosions; still needed with LSTMs.
- **Related:** Exploding gradient
- **Real-life link:**
- **Study:** R3

### GRU
- **Status:** proposed
- **Definition:** A lighter gated recurrent unit with two gates that performs comparably to LSTM.
- **Related:** Forget gate, Gate
- **Real-life link:**
- **Study:** R5
