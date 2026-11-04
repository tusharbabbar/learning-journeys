# LSTM: learning journey

Dated entries, newest last. Questions are recorded in the learner's words.

## 2026-11-03: first pass
- Started from: FNNs, RNNs, and the RNN memory problem (vanishing/exploding gradients)
- Research: differential pass (baseline RNN → target LSTM); 6 primary sources kept, 4 secondary cut
- Covered: the additive cell update, the constant error carousel, the three gates, why the direct cell path has no weight matrix, the forget-bias-of-1 result, the 4× parameter cost
- Topic questions asked: none yet
- Still open: GRU as a comparison, attention as the successor, gradient clipping in practice

## 2026-11-04: dossier created
- Built the technical document, claims and verify scripts from the 2026-11-03 research
- Correction while verifying: the b_f=1 case over 50 steps is 1.6e-7 (earlier write-up said 1.5e-7)
