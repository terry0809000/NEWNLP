# Related Work

PubMed-PICO and PubMed RCT datasets have enabled reproducible sentence-level biomedical abstract classification. PICO work has motivated LSTM and BiLSTM models for identifying clinically relevant abstract elements, while PubMed RCT resources frame sequential sentence classification using section labels.

Classical TF-IDF linear models remain strong baselines in text classification and are especially attractive in CPU-only settings. LSTM and bidirectional recurrent architectures can encode word order, but their gains must be evaluated against sparse linear baselines rather than assumed.

Calibration work in clinical prediction and machine learning motivates reporting Brier score, reliability curves, ECE, and calibration slope/intercept. External validation and transparent reporting are included as safeguards against over-interpreting internal test performance.
