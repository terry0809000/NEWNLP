# Methods

## Data

The primary dataset was PubMed-PICO Detection. Official train, validation, and test files were downloaded from the public GitHub repository. Sentences with source labels `R` or `C` were mapped to the positive class, and all other labels were mapped to the negative class. The external validation dataset was the official PubMed 20k RCT test file, with `RESULTS` and `CONCLUSIONS` mapped to positive.

## Models

We evaluated a majority baseline, TF-IDF logistic regression, TF-IDF linear SVM, feed-forward average embeddings, LSTM, BiLSTM, and BiLSTM with dropout. TF-IDF models used word 1-2 grams and character 3-5 grams fitted only on training text. Neural tokenizers were fitted on training text only. Neural models used CPU-only PyTorch with maximum sequence length 64, embedding dimension 64, hidden dimension 64, and a stratified 120,000-sentence training cap to keep runtime feasible.

## Calibration and Thresholding

Classical models used Platt calibration fitted on validation scores. Neural models used temperature scaling fitted on validation logits. Thresholds were optimized for validation F1 only. Test and external sets were never used for fitting, calibration, threshold selection, or model selection.

## Metrics

The primary metric was ROC AUC. Secondary metrics included PR AUC, accuracy, sensitivity, specificity, precision, F1, confusion matrix, Brier score, ECE, calibration intercept, calibration slope, ROC/PR curves, calibration curve, and reliability plot. A bootstrap confidence interval was computed for the selected model's internal test AUC.
