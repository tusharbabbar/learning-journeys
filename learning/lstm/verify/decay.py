"""Gradient surviving 50 steps along the memory path: vanilla RNN vs LSTM.

RNN: per-step factor = w * tanh'(.), scalar case with w=0.9, tanh' ~ 0.6.
LSTM: per-step factor on the direct cell path = forget gate value f.
"""
import math

STEPS = 50

def sigmoid(x):
    return 1 / (1 + math.exp(-x))

rows = [
    ("Vanilla RNN, w=0.9, tanh'=0.6", 0.9 * 0.6),
    ("LSTM at init, b_f=0 -> f=sigmoid(0)", sigmoid(0)),
    ("LSTM at init, b_f=1 -> f=sigmoid(1)", sigmoid(1)),
    ("LSTM learned to hold, f=0.99", 0.99),
    ("1997 LSTM, no forget gate, f=1", 1.0),
]

for name, factor in rows:
    print(f"{name:40s} per-step={factor:.4f}  after {STEPS} steps={factor ** STEPS:.2e}")
