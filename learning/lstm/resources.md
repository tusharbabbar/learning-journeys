# LSTM: resources

Every resource discovered for this topic, with the shortest summary that says what it's useful for. IDs are stable: concepts, maps and the design review refer to them.

> **Coverage note:** this list comes from an earlier pass that only looked for primary evidence (papers and benchmarks). A full discovery pass across lectures, videos, blogs, courses and code still needs to run.

| ID | Resource | Type | Depth | Subtopics | Summary | Link |
|---|---|---|---|---|---|---|
| R1 | Hochreiter & Schmidhuber, *Long Short-Term Memory* (1997) | paper | deep | memory problem, gated cell | The original LSTM: an additive memory cell with a fixed self-loop plus input/output gates; bridges 1000+ step lags. | [link](https://papers.baulab.info/papers/Hochreiter-1997.pdf) |
| R2 | Gers, Schmidhuber & Cummins, *Learning to Forget* (2000) | paper | deep | gated cell, variants | Adds the forget gate so the cell can reset itself on endless input streams. | [link](https://mlanthology.org/neco/2000/gers2000neco-learning) |
| R3 | Pascanu, Mikolov & Bengio, *On the difficulty of training RNNs* (2013) | paper | deep | memory problem, training | Why RNN gradients vanish or explode, with the eigenvalue view; proposes gradient clipping. | [link](https://arxiv.org/abs/1211.5063) |
| R4 | Greff et al., *LSTM: A Search Space Odyssey* (2017) | benchmark | intermediate | gated cell, variants | 5400 runs over 8 LSTM variants: none beats the standard one; forget gate matters most. | [link](https://arxiv.org/abs/1503.04069) |
| R5 | Jozefowicz, Zaremba & Sutskever, *An Empirical Exploration of Recurrent Network Architectures* (2015) | benchmark | intermediate | training, variants | Searched 10k+ RNN designs; a forget-gate bias of 1 puts LSTM level with GRU. | [link](https://proceedings.mlr.press/v37/jozefowicz15.html) |
| R6 | van der Westhuizen & Lasenby, *The Unreasonable Effectiveness of the Forget Gate* (2018) | paper | intermediate | variants | An LSTM with only a forget gate beat the full three-gate LSTM on five tasks. | [link](https://arxiv.org/abs/1804.04849) |
| R7 | Felix Gers (Wikipedia) | encyclopedia | intro | history | Who introduced the forget gate, and where it proved crucial. | [link](https://en.wikipedia.org/wiki/Felix_Gers) |
| R8 | D. Morrison, LSTM lecture slides (Harvey Mudd) | slides | intro | gated cell, history | Short walkthrough of the 1997 and 2000 papers and the tasks the original LSTM solved. | [link](https://www.cs.hmc.edu/~dmorrison/lstm.pdf) |
| R9 | Edinburgh MLP Lecture 10: RNNs 2, LSTM and gates (2018) | slides | intro | gated cell | Gate-by-gate diagrams of the LSTM cell; good for a first visual pass. | [link](https://www.inf.ed.ac.uk/teaching/courses/mlp/2018-19/mlp10-rnn2.pdf) |
| R10 | Long short-term memory (Chinese Wikipedia) | encyclopedia | intro | history, variants | Overview with history (GRU in 2014) and industry use; check claims against primary sources. | [link](https://zh.wikipedia.com/wiki/%E9%95%B7%E7%9F%AD%E6%9C%9F%E8%A8%98%E6%86%B6) |
