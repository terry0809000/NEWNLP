# Final Project Report

## 1. Selected Project and Rationale

This project is a CPU-only, reproducible healthcare NLP benchmark for binary findings/conclusion sentence detection in biomedical abstracts. It was selected because it uses public data, supports ROC AUC and calibration assessment, is feasible without CUDA, and has a credible external validation dataset.

## 2. Selected Dataset

Primary dataset: PubMed-PICO Detection official train/dev/test splits. Positive labels were `R` and `C`; all other labels were negative.

## 3. External Validation Availability

External validation dataset: PubMed 20k RCT official test split. Positive labels were `RESULTS` and `CONCLUSIONS`. External validation was not used for fitting, model selection, thresholding, or calibration.

## 4. Models Run

Majority baseline; TF-IDF logistic regression; TF-IDF linear SVM; feed-forward average-embedding neural model; LSTM; BiLSTM; BiLSTM with dropout.

## 5. Best Model

Validation-selected best model: `tfidf_logistic_regression`.

## 6. Validation Performance

ROC AUC 0.976919; PR AUC 0.967295; F1 0.919981; Brier 0.053599; ECE 0.011768.

## 7. Test Performance

ROC AUC 0.975971; PR AUC 0.966760; accuracy 0.925712; F1 0.916092; Brier 0.055240; ECE 0.011093.

## 8. External Validation Performance

ROC AUC 0.947783; PR AUC 0.947438; accuracy 0.882927; F1 0.878904; Brier 0.085359; ECE 0.023584.

## 9. AUC Target

AUC >= 0.70 achieved: yes.

## 10. Calibration Results

The best model had low internal-test Brier score and ECE. External calibration was weaker than internal calibration, with lower calibration slope, indicating corpus shift and the need for recalibration before any downstream applied use.

## 11. Error Analysis Summary

False positives often involved method or outcome-definition sentences containing endpoint/result-like language. False negatives often involved short or numerically dense findings sentences. High-confidence errors illustrated the limits of section-heading-derived labels.

## 12. Literature Search Summary

The literature review covered PubMed-PICO, PubMed RCT sentence classification, PubMedQA and ADE alternatives, LSTM/BiLSTM methods, classical ML baselines, calibration, external validation, and reporting guidance.

## 13. Selected Journal

Primary target: PLOS ONE. Backups: JAMIA Open and BMC Medical Informatics and Decision Making.

## 14. Manuscript Files Created

Markdown manuscript sections are in `project_outputs/10_manuscript`. LaTeX source and compiled PDF are in `latex/` and the final zip.

## 15. LaTeX Zip Location

`C:\Users\Terry Yu\Documents\Healthcare_NLP_CPU_Project\project_outputs\11_latex_zip\healthcare_nlp_manuscript_latex.zip`

## 16. Failed or Skipped Steps

NICTA-PIBOSO was not used because a usable automatically downloadable version was not available in this environment. CUDA/GPU experiments were intentionally not attempted. Optional CNN-text modelling was not run because the required model set was completed and CPU runtime was prioritized.

## 17. Next Actions

Review the manuscript for target-journal style, decide whether to train neural models on the full primary training split with more CPU time, and consider a manual-label external corpus if access becomes available.

## Most Important Unresolved Issue

External validation is public and held out, but it remains a biomedical-abstract corpus with proxy section labels rather than a clinically deployed or manually adjudicated external setting.
