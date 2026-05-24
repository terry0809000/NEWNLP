# Literature Review

Biomedical abstract sentence classification has been used to support evidence-based medicine by identifying rhetorical and PICO-related elements in abstracts. PubMed-PICO and PubMed RCT resources are especially useful for reproducible CPU-only studies because the text is public and the labels can be loaded without credentialed clinical-data access.

The modelling literature justifies comparing strong sparse linear baselines with recurrent neural models. Support vector machines and logistic regression over TF-IDF features remain credible CPU baselines for text classification, while LSTM and bidirectional recurrent networks provide lightweight sequence-aware alternatives. The local results therefore test a substantive methodological question rather than assuming neural superiority.

Calibration is central in healthcare machine learning. Brier score, ECE, reliability curves, and calibration slope/intercept are reported because good discrimination alone does not ensure reliable probability estimates. This framing follows calibration-focused clinical prediction literature and modern neural calibration work.

External validation is handled conservatively. PubMed 20k RCT is external to the primary PubMed-PICO split and label-compatible for the restricted findings/conclusion construct, but it remains an abstract-domain corpus and does not establish deployment readiness.

The included matrix and BibTeX file list all cited works and URLs/DOIs found during the search.
