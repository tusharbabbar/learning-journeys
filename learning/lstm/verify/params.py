"""Parameter counts for one recurrent layer, input size m, hidden size n.

RNN:  W (n x m) + R (n x n) + b (n)            = n(n+m) + n
LSTM: four such blocks (f, i, o, g)            = 4 * [n(n+m) + n]
PyTorch's nn.LSTM keeps two bias vectors per gate (b_ih, b_hh), so it reports 4 * [n(n+m) + 2n].
"""
m, n = 128, 256

rnn = n * (n + m) + n
lstm = 4 * rnn
lstm_pytorch = 4 * (n * (n + m) + 2 * n)

print(f"m={m}, n={n}")
print(f"RNN params:               {rnn:,}")
print(f"LSTM params:              {lstm:,}")
print(f"LSTM params (PyTorch, 2 biases): {lstm_pytorch:,}")
print(f"LSTM / RNN ratio:         {lstm / rnn:.1f}x")
