# External Validation

The external validation set is the official PubMed 20k RCT test split. It was not used for model fitting, hyperparameter selection, calibration fitting, or threshold selection.

Positive labels were RESULTS and CONCLUSIONS; all other PubMed RCT section labels were mapped to the negative class. This is label-compatible with the primary PubMed-PICO task only for the rhetorical finding/conclusion construct and should not be interpreted as validation of PICO Population, Intervention, or Outcome extraction.

```text
                    model     n  prevalence  threshold  accuracy  precision_ppv  sensitivity_recall       f1  specificity  true_negative  false_positive  false_negative  true_positive  brier_score  ece_10bin  roc_auc   pr_auc  calibration_intercept  calibration_slope  auc_ci_low  auc_ci_high
                   bilstm 30135       0.474   0.531940  0.865738       0.866114            0.847802 0.856860     0.881900          13979            1872            2174          12110     0.099737   0.041808 0.936519 0.937450               0.074732           0.737297    0.933862     0.938888
           bilstm_dropout 30135       0.474   0.366299  0.840252       0.850689            0.804116 0.826747     0.872816          13835            2016            2798          11486     0.119944   0.060033 0.915961 0.918498               0.413967           0.755832    0.913154     0.918901
      ffnn_avg_embeddings 30135       0.474   0.471596  0.840219       0.843802            0.813498 0.828373     0.864299          13700            2151            2664          11620     0.119475   0.036605 0.912108 0.906706               0.239391           0.784062    0.908968     0.915207
                     lstm 30135       0.474   0.299730  0.779326       0.811490            0.696164 0.749416     0.854268          13541            2310            4340           9944     0.168727   0.096596 0.834595 0.854852               0.656373           0.981423    0.830533     0.839630
        majority_baseline 30135       0.474   0.500000  0.526000       0.000000            0.000000 0.000000     1.000000          15851               0           14284              0     0.251088   0.042005 0.500000 0.474000              -0.096833           0.026505    0.500000     0.500000
         tfidf_linear_svm 30135       0.474   0.433294  0.882363       0.870438            0.883296 0.876820     0.881522          13973            1878            1667          12617     0.087888   0.025495 0.944993 0.943585               0.023687           0.762657    0.942388     0.947625
tfidf_logistic_regression 30135       0.474   0.384477  0.882927       0.862155            0.896318 0.878904     0.870860          13804            2047            1481          12803     0.085359   0.023584 0.947783 0.947438               0.007127           0.770131    0.945330     0.950225
```