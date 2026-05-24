# Discussion

This benchmark shows that a full-training TF-IDF logistic regression baseline can outperform or match lightweight recurrent neural models for findings/conclusion sentence detection in biomedical abstracts. This is important for reproducible healthcare NLP because CPU-feasible methods are often easier to audit, rerun, calibrate, and deploy in research environments without GPU access.

External validation performance was lower than internal test performance, consistent with corpus and label shift, but remained above the empirical AUC target. Calibration also degraded externally, especially in calibration slope, reinforcing the need to report calibration separately from discrimination.

The results should not be interpreted as clinical safety evidence. The model identifies rhetorical sentence roles in abstracts; it does not extract treatment effects, validate claims, or recommend care.
