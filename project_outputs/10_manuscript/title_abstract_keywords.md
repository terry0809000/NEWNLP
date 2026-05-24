# A CPU-feasible benchmark for calibrated biomedical abstract sentence classification with external validation

## Abstract


Background: Healthcare NLP benchmarks often emphasize discrimination while under-reporting calibration and external validation. We evaluated CPU-feasible models for identifying findings/conclusion sentences in biomedical abstracts.

Methods: PubMed-PICO official train/dev/test splits were used as the primary dataset. Sentences labelled Results or Conclusion were mapped to the positive class. PubMed 20k RCT official test sentences with RESULTS or CONCLUSIONS labels were used only for external validation. Models included a majority baseline, TF-IDF logistic regression, TF-IDF linear SVM, feed-forward average-embedding network, LSTM, BiLSTM, and BiLSTM with dropout. Calibration used validation-fitted Platt scaling for classical models and temperature scaling for neural models.

Results: The validation-selected model was tfidf_logistic_regression. It achieved validation AUC 0.977, internal test AUC 0.976, and external AUC 0.948. Internal test Brier score was 0.055 and ECE was 0.011. External validation showed lower but still strong discrimination, with Brier score 0.085 and ECE 0.024.

Conclusions: Strong sparse linear models were competitive with lightweight recurrent neural networks for this public biomedical sentence-classification task under a CPU-only budget. The benchmark achieved the empirical AUC target, but corpus shift and proxy labels limit clinical interpretation.


## Keywords

Biomedical NLP; sentence classification; calibration; external validation; TF-IDF; LSTM; reproducibility
