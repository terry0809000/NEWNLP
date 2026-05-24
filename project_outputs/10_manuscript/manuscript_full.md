# A CPU-feasible benchmark for calibrated biomedical abstract sentence classification with external validation

## Abstract

Background: Healthcare NLP benchmarks often emphasize discrimination while under-reporting calibration and external validation. We evaluated CPU-feasible models for identifying findings/conclusion sentences in biomedical abstracts.

Methods: PubMed-PICO official train/dev/test splits were used as the primary dataset. Sentences labelled Results or Conclusion were mapped to the positive class. PubMed 20k RCT official test sentences with RESULTS or CONCLUSIONS labels were used only for external validation. Models included a majority baseline, TF-IDF logistic regression, TF-IDF linear SVM, feed-forward average-embedding network, LSTM, BiLSTM, and BiLSTM with dropout. Calibration used validation-fitted Platt scaling for classical models and temperature scaling for neural models.

Results: The validation-selected model was tfidf_logistic_regression. It achieved validation AUC 0.977, internal test AUC 0.976, and external AUC 0.948. Internal test Brier score was 0.055 and ECE was 0.011. External validation showed lower but still strong discrimination, with Brier score 0.085 and ECE 0.024.

Conclusions: Strong sparse linear models were competitive with lightweight recurrent neural networks for this public biomedical sentence-classification task under a CPU-only budget. The benchmark achieved the empirical AUC target, but corpus shift and proxy labels limit clinical interpretation.



# Introduction

Evidence synthesis depends on rapidly locating the sentences in biomedical abstracts that state findings and conclusions. This task is narrower than full evidence extraction, but it is useful as an upstream filter for systematic-review triage and biomedical literature navigation.

Many healthcare NLP studies report discrimination without equally careful calibration, external validation, or reproducibility artifacts. In clinical and health-adjacent machine learning, calibrated probabilities matter because a model with high AUC may still produce misleading risk estimates. Even though this benchmark is not a clinical prediction system, calibration is included to keep the methodological standard close to healthcare machine-learning expectations.

We asked whether CPU-feasible classical and recurrent models can solve a public biomedical abstract sentence-classification problem with acceptable discrimination and calibration, and whether performance transfers to an external but label-compatible PubMed RCT corpus.



# Related Work

PubMed-PICO and PubMed RCT datasets have enabled reproducible sentence-level biomedical abstract classification. PICO work has motivated LSTM and BiLSTM models for identifying clinically relevant abstract elements, while PubMed RCT resources frame sequential sentence classification using section labels.

Classical TF-IDF linear models remain strong baselines in text classification and are especially attractive in CPU-only settings. LSTM and bidirectional recurrent architectures can encode word order, but their gains must be evaluated against sparse linear baselines rather than assumed.

Calibration work in clinical prediction and machine learning motivates reporting Brier score, reliability curves, ECE, and calibration slope/intercept. External validation and transparent reporting are included as safeguards against over-interpreting internal test performance.



# Methods

## Data

The primary dataset was PubMed-PICO Detection. Official train, validation, and test files were downloaded from the public GitHub repository. Sentences with source labels `R` or `C` were mapped to the positive class, and all other labels were mapped to the negative class. The external validation dataset was the official PubMed 20k RCT test file, with `RESULTS` and `CONCLUSIONS` mapped to positive.

## Models

We evaluated a majority baseline, TF-IDF logistic regression, TF-IDF linear SVM, feed-forward average embeddings, LSTM, BiLSTM, and BiLSTM with dropout. TF-IDF models used word 1-2 grams and character 3-5 grams fitted only on training text. Neural tokenizers were fitted on training text only. Neural models used CPU-only PyTorch with maximum sequence length 64, embedding dimension 64, hidden dimension 64, and a stratified 120,000-sentence training cap to keep runtime feasible.

## Calibration and Thresholding

Classical models used Platt calibration fitted on validation scores. Neural models used temperature scaling fitted on validation logits. Thresholds were optimized for validation F1 only. Test and external sets were never used for fitting, calibration, threshold selection, or model selection.

## Metrics

The primary metric was ROC AUC. Secondary metrics included PR AUC, accuracy, sensitivity, specificity, precision, F1, confusion matrix, Brier score, ECE, calibration intercept, calibration slope, ROC/PR curves, calibration curve, and reliability plot. A bootstrap confidence interval was computed for the selected model's internal test AUC.



# Experiments

All experiments were run in CPU-only mode on Windows 11 using Python 3.14 and PyTorch CPU. CUDA availability was checked and reported false. Classical models were trained on the full primary training split. Neural models were trained under the documented CPU cap and evaluated on the full validation, internal test, and external validation sets.



# Results

The empirical AUC target was achieved. The validation-selected model was `tfidf_logistic_regression`.

Internal test performance for `tfidf_logistic_regression`: ROC AUC 0.975971, PR AUC 0.966760, accuracy 0.925712, F1 0.916092, Brier score 0.055240, and ECE 0.011093.

External validation performance for `tfidf_logistic_regression`: ROC AUC 0.947783, PR AUC 0.947438, accuracy 0.882927, F1 0.878904, Brier score 0.085359, and ECE 0.023584.

```text
                    model      split  roc_auc   pr_auc  brier_score  ece_10bin       f1  accuracy
tfidf_logistic_regression   external 0.947783 0.947438     0.085359   0.023584 0.878904  0.882927
         tfidf_linear_svm   external 0.944993 0.943585     0.087888   0.025495 0.876820  0.882363
                   bilstm   external 0.936519 0.937450     0.099737   0.041808 0.856860  0.865738
           bilstm_dropout   external 0.915961 0.918498     0.119944   0.060033 0.826747  0.840252
      ffnn_avg_embeddings   external 0.912108 0.906706     0.119475   0.036605 0.828373  0.840219
                     lstm   external 0.834595 0.854852     0.168727   0.096596 0.749416  0.779326
        majority_baseline   external 0.500000 0.474000     0.251088   0.042005 0.000000  0.526000
tfidf_logistic_regression       test 0.975971 0.966760     0.055240   0.011093 0.916092  0.925712
         tfidf_linear_svm       test 0.974378 0.964400     0.056658   0.011386 0.915262  0.925744
                   bilstm       test 0.973744 0.964868     0.060198   0.009594 0.907932  0.919603
           bilstm_dropout       test 0.964281 0.952940     0.071138   0.014678 0.892814  0.906460
      ffnn_avg_embeddings       test 0.961723 0.948479     0.073926   0.009580 0.886617  0.900000
                     lstm       test 0.891169 0.885972     0.128554   0.039062 0.800240  0.829325
        majority_baseline       test 0.500000 0.433515     0.245582   0.001519 0.000000  0.566485
tfidf_logistic_regression validation 0.976919 0.967295     0.053599   0.011768 0.919981  0.929302
         tfidf_linear_svm validation 0.975563 0.966415     0.055134   0.010865 0.917248  0.927716
                   bilstm validation 0.974576 0.966332     0.058673   0.009869 0.910871  0.922145
           bilstm_dropout validation 0.965263 0.954307     0.070040   0.015941 0.895076  0.908349
      ffnn_avg_embeddings validation 0.961720 0.949451     0.073686   0.011160 0.888530  0.901516
                     lstm validation 0.891632 0.887370     0.127890   0.039342 0.803643  0.832405
        majority_baseline validation 0.500000 0.433513     0.245582   0.001517 0.000000  0.566487
```

The BiLSTM approached the TF-IDF models internally but did not exceed the logistic regression baseline. The unidirectional LSTM was substantially weaker under the CPU-limited configuration.



# Discussion

This benchmark shows that a full-training TF-IDF logistic regression baseline can outperform or match lightweight recurrent neural models for findings/conclusion sentence detection in biomedical abstracts. This is important for reproducible healthcare NLP because CPU-feasible methods are often easier to audit, rerun, calibrate, and deploy in research environments without GPU access.

External validation performance was lower than internal test performance, consistent with corpus and label shift, but remained above the empirical AUC target. Calibration also degraded externally, especially in calibration slope, reinforcing the need to report calibration separately from discrimination.

The results should not be interpreted as clinical safety evidence. The model identifies rhetorical sentence roles in abstracts; it does not extract treatment effects, validate claims, or recommend care.



# Limitations

Labels are derived from abstract section/PICO annotations and may not perfectly represent sentence semantics. External validation is public and label-compatible, but it remains in the PubMed abstract domain rather than a genuinely different clinical setting. Neural models used a CPU training cap, so stronger neural architectures or longer training might perform differently. No demographic fairness analysis was possible because the corpora do not include patient-level demographic metadata.



# Conclusion

A CPU-only, fully reproducible healthcare NLP benchmark achieved strong discrimination and acceptable calibration for biomedical findings/conclusion sentence detection. The strongest model was TF-IDF logistic regression, not a recurrent neural model. The project supports a pragmatic publication message: robust classical baselines, calibration, and external validation can be more scientifically informative than compute-heavy modelling alone.



# Data and Code Availability

All code, configuration files, logs, processed data manifests, metrics, predictions, figures, tables, and manuscript files were saved locally in this project. Raw data were downloaded from public repositories listed in the data manifest. The project does not redistribute restricted clinical data.



# Ethics Statement

This study used publicly accessible biomedical abstract datasets and did not process identifiable patient-level clinical notes. No intervention, patient contact, or clinical deployment was performed. The manuscript avoids claims of clinical safety or deployment readiness.
