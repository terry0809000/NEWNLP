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
