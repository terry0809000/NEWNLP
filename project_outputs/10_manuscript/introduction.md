# Introduction

Evidence synthesis depends on rapidly locating the sentences in biomedical abstracts that state findings and conclusions. This task is narrower than full evidence extraction, but it is useful as an upstream filter for systematic-review triage and biomedical literature navigation.

Many healthcare NLP studies report discrimination without equally careful calibration, external validation, or reproducibility artifacts. In clinical and health-adjacent machine learning, calibrated probabilities matter because a model with high AUC may still produce misleading risk estimates. Even though this benchmark is not a clinical prediction system, calibration is included to keep the methodological standard close to healthcare machine-learning expectations.

We asked whether CPU-feasible classical and recurrent models can solve a public biomedical abstract sentence-classification problem with acceptable discrimination and calibration, and whether performance transfers to an external but label-compatible PubMed RCT corpus.
