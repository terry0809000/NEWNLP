# Evidence Lock File

Created: 2026-05-25T00:06:27.704925

Only the results and citations listed here are authorized for insertion into the submission-ready manuscript.

## Selected model and target

- Validation-selected model: `tfidf_logistic_regression`.
- AUC >= 0.70 achieved: yes.
- External validation exists: yes.
- External validation dataset: PubMed 20k RCT official test split, mapped to the same binary findings/conclusion construct.
- Calibration improved Brier/ECE: not determined. Saved evidence contains post-calibration predictions and metrics, but pre-calibration Brier/ECE values were not saved for all models.
- LaTeX compilation possible locally: yes.

## Selected-model confidence intervals available

- Internal test ROC AUC 95% bootstrap CI: 0.975 to 0.977.
- External ROC AUC 95% bootstrap CI: 0.945 to 0.950.

## Main metrics available

```text
                    model      split     n  prevalence  threshold  accuracy  precision_ppv  sensitivity_recall       f1  specificity  true_negative  false_positive  false_negative  true_positive  brier_score  ece_10bin  roc_auc   pr_auc  calibration_intercept  calibration_slope
tfidf_logistic_regression   external 30135    0.474000   0.384477  0.882927       0.862155            0.896318 0.878904     0.870860          13804            2047            1481          12803     0.085359   0.023584 0.947783 0.947438               0.007127           0.770131
         tfidf_linear_svm   external 30135    0.474000   0.433294  0.882363       0.870438            0.883296 0.876820     0.881522          13973            1878            1667          12617     0.087888   0.025495 0.944993 0.943585               0.023687           0.762657
                   bilstm   external 30135    0.474000   0.531940  0.865738       0.866114            0.847802 0.856860     0.881900          13979            1872            2174          12110     0.099737   0.041808 0.936519 0.937450               0.074732           0.737297
           bilstm_dropout   external 30135    0.474000   0.366299  0.840252       0.850689            0.804116 0.826747     0.872816          13835            2016            2798          11486     0.119944   0.060033 0.915961 0.918498               0.413967           0.755832
      ffnn_avg_embeddings   external 30135    0.474000   0.471596  0.840219       0.843802            0.813498 0.828373     0.864299          13700            2151            2664          11620     0.119475   0.036605 0.912108 0.906706               0.239391           0.784062
                     lstm   external 30135    0.474000   0.299730  0.779326       0.811490            0.696164 0.749416     0.854268          13541            2310            4340           9944     0.168727   0.096596 0.834595 0.854852               0.656373           0.981423
        majority_baseline   external 30135    0.474000   0.500000  0.526000       0.000000            0.000000 0.000000     1.000000          15851               0           14284              0     0.251088   0.042005 0.500000 0.474000              -0.096833           0.026505
tfidf_logistic_regression       test 31270    0.433515   0.384477  0.925712       0.897516            0.935453 0.916092     0.918257          16266            1448             875          12681     0.055240   0.011093 0.975971 0.966760              -0.021090           0.983072
         tfidf_linear_svm       test 31270    0.433515   0.433294  0.925744       0.905677            0.925052 0.915262     0.926273          16408            1306            1016          12540     0.056658   0.011386 0.974378 0.964400              -0.009120           0.984707
                   bilstm       test 31270    0.433515   0.531940  0.919603       0.901527            0.914429 0.907932     0.923563          16360            1354            1160          12396     0.060198   0.009594 0.973744 0.964868              -0.161200           0.996646
           bilstm_dropout       test 31270    0.433515   0.366299  0.906460       0.887060            0.898643 0.892814     0.912442          16163            1551            1374          12182     0.071138   0.014678 0.964281 0.952940               0.188867           1.007571
      ffnn_avg_embeddings       test 31270    0.433515   0.471596  0.900000       0.871853            0.901888 0.886617     0.898555          15917            1797            1330          12226     0.073926   0.009580 0.961723 0.948479              -0.127510           1.002875
                     lstm       test 31270    0.433515   0.299730  0.829325       0.812248            0.788581 0.800240     0.860506          15243            2471            2866          10690     0.128554   0.039062 0.891169 0.885972               0.434854           1.147599
        majority_baseline       test 31270    0.433515   0.500000  0.566485       0.000000            0.000000 0.000000     1.000000          17714               0           13556              0     0.245582   0.001519 0.500000 0.433515              -0.248844           0.068112
tfidf_logistic_regression validation 30878    0.433513   0.384477  0.929302       0.903131            0.937472 0.919981     0.923051          16146            1346             837          12549     0.053599   0.011768 0.976919 0.967295              -0.000039           1.000000
         tfidf_linear_svm validation 30878    0.433513   0.433294  0.927716       0.910496            0.924100 0.917248     0.930483          16276            1216            1016          12370     0.055134   0.010865 0.975563 0.966415               0.000022           1.001182
                   bilstm validation 30878    0.433513   0.531940  0.922145       0.904166            0.917675 0.910871     0.925566          16190            1302            1102          12284     0.058673   0.009869 0.974576 0.966332              -0.170863           1.005690
           bilstm_dropout validation 30878    0.433513   0.366299  0.908349       0.888488            0.901763 0.895076     0.913389          15977            1515            1315          12071     0.070040   0.015941 0.965263 0.954307               0.173866           1.011389
      ffnn_avg_embeddings validation 30878    0.433513   0.471596  0.901516       0.872256            0.905424 0.888530     0.898525          15717            1775            1266          12120     0.073686   0.011160 0.961720 0.949451              -0.151787           1.001563
                     lstm validation 30878    0.433513   0.299730  0.832405       0.816563            0.791125 0.803643     0.863995          15113            2379            2796          10590     0.127890   0.039342 0.891632 0.887370               0.446512           1.156128
        majority_baseline validation 30878    0.433513   0.500000  0.566487       0.000000            0.000000 0.000000     1.000000          17492               0           13386              0     0.245582   0.001517 0.500000 0.433513              -0.248852           0.068115
```

## Calibration metrics available

```text
                    model      split     n  prevalence  brier_score  ece_10bin  calibration_intercept  calibration_slope
                   bilstm validation 30878    0.433513     0.058673   0.009869              -0.170863           1.005690
                   bilstm       test 31270    0.433515     0.060198   0.009594              -0.161200           0.996646
                   bilstm   external 30135    0.474000     0.099737   0.041808               0.074732           0.737297
           bilstm_dropout validation 30878    0.433513     0.070040   0.015941               0.173866           1.011389
           bilstm_dropout       test 31270    0.433515     0.071138   0.014678               0.188867           1.007571
           bilstm_dropout   external 30135    0.474000     0.119944   0.060033               0.413967           0.755832
      ffnn_avg_embeddings validation 30878    0.433513     0.073686   0.011160              -0.151787           1.001563
      ffnn_avg_embeddings       test 31270    0.433515     0.073926   0.009580              -0.127510           1.002875
      ffnn_avg_embeddings   external 30135    0.474000     0.119475   0.036605               0.239391           0.784062
                     lstm validation 30878    0.433513     0.127890   0.039342               0.446512           1.156128
                     lstm       test 31270    0.433515     0.128554   0.039062               0.434854           1.147599
                     lstm   external 30135    0.474000     0.168727   0.096596               0.656373           0.981423
        majority_baseline validation 30878    0.433513     0.245582   0.001517              -0.248852           0.068115
        majority_baseline       test 31270    0.433515     0.245582   0.001519              -0.248844           0.068112
        majority_baseline   external 30135    0.474000     0.251088   0.042005              -0.096833           0.026505
         tfidf_linear_svm validation 30878    0.433513     0.055134   0.010865               0.000022           1.001182
         tfidf_linear_svm       test 31270    0.433515     0.056658   0.011386              -0.009120           0.984707
         tfidf_linear_svm   external 30135    0.474000     0.087888   0.025495               0.023687           0.762657
tfidf_logistic_regression validation 30878    0.433513     0.053599   0.011768              -0.000039           1.000000
tfidf_logistic_regression       test 31270    0.433515     0.055240   0.011093              -0.021090           0.983072
tfidf_logistic_regression   external 30135    0.474000     0.085359   0.023584               0.007127           0.770131
```

## Dataset class distribution available

```text
       dataset         split          label_name      n  proportion
PubMed-20k-RCT external_test findings_conclusion  14284    0.474000
PubMed-20k-RCT external_test               other  15851    0.526000
   PubMed-PICO          test findings_conclusion  13556    0.433515
   PubMed-PICO          test               other  17714    0.566485
   PubMed-PICO         train findings_conclusion 111377    0.431995
   PubMed-PICO         train               other 146443    0.568005
   PubMed-PICO    validation findings_conclusion  13386    0.433513
   PubMed-PICO    validation               other  17492    0.566487
```

## Text length summary available

```text
       dataset         split          label_name  count      mean       std  median  min  max
PubMed-20k-RCT external_test findings_conclusion  14284 27.962335 16.442163    24.0    2  211
PubMed-20k-RCT external_test               other  15851 24.571320 14.068858    22.0    1  158
   PubMed-PICO          test findings_conclusion  13556 27.488566 15.804662    24.0    1  194
   PubMed-PICO          test               other  17714 20.997911 12.901760    19.0    1  129
   PubMed-PICO         train findings_conclusion 111377 27.717051 16.333645    24.0    1  345
   PubMed-PICO         train               other 146443 21.110405 13.138003    19.0    1  429
   PubMed-PICO    validation findings_conclusion  13386 27.686239 16.318217    24.0    1  208
   PubMed-PICO    validation               other  17492 21.072204 13.043946    19.0    1  150
```

## External validation values available

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

## Subgroup values available

```text
                    model    split            subgroup    n  prevalence  threshold  accuracy  precision_ppv  sensitivity_recall       f1  specificity  true_negative  false_positive  false_negative  true_positive  brier_score  ece_10bin  roc_auc   pr_auc  calibration_intercept  calibration_slope
tfidf_logistic_regression     test        length:short 8600    0.269419        0.5  0.931512       0.879280            0.864480 0.871817     0.956231           6008             275             314           2003     0.053101   0.016020 0.973575 0.934795              -0.196561           0.944800
tfidf_logistic_regression     test length:medium_short 7404    0.449352        0.5  0.908158       0.909372            0.883679 0.896341     0.928133           3784             293             387           2940     0.069460   0.015156 0.965052 0.954863               0.123971           0.951874
tfidf_logistic_regression     test  length:medium_long 7480    0.476070        0.5  0.924465       0.926295            0.914069 0.920141     0.933912           3660             259             306           3255     0.057703   0.012276 0.973649 0.966915               0.055355           0.987098
tfidf_logistic_regression     test         length:long 7786    0.558824        0.5  0.947341       0.948759            0.957481 0.953100     0.934498           3210             225             185           4166     0.041713   0.014088 0.983563 0.984441              -0.134030           1.057083
tfidf_logistic_regression external        length:short 8216    0.414679        0.5  0.849440       0.823687            0.810390 0.816985     0.877105           4218             591             646           2761     0.107891   0.039861 0.921209 0.904979              -0.110740           0.714695
tfidf_logistic_regression external length:medium_short 7154    0.460302        0.5  0.873497       0.875236            0.845733 0.860232     0.897177           3464             397             508           2785     0.094576   0.027894 0.938422 0.933590               0.055351           0.763132
tfidf_logistic_regression external  length:medium_long 7676    0.483325        0.5  0.896300       0.899397            0.884367 0.891818     0.907463           3599             367             429           3281     0.078163   0.019810 0.954302 0.954206               0.028460           0.809506
tfidf_logistic_regression external         length:long 7089    0.546480        0.5  0.926224       0.939648            0.924368 0.931945     0.928460           2985             230             293           3581     0.057735   0.017548 0.969661 0.975940               0.109378           0.804849
```

## Figures available

- `calibration_curve_best_model.png`
- `class_distribution.png`
- `confusion_matrix_best_model.png`
- `pr_curve_best_model.png`
- `roc_curve_best_model.png`
- `subgroup_performance.png`
- `text_length_distribution.png`

## Tables available

- `calibration_results.csv`
- `class_distribution.csv`
- `external_validation_results.csv`
- `main_results.csv`
- `per_class_results.csv`
- `subgroup_analysis.csv`
- `text_length_summary.csv`

## Citations available

- `amini2018nicta`
- `austin2019ici`
- `beltagy2019scibert`
- `brier1950verification`
- `char2018ethical`
- `chen2017prediction`
- `cohen2006workload`
- `collins2015tripod`
- `cortes1995svm`
- `davis2006prroc`
- `dernoncourt2017pubmed`
- `devlin2019bert`
- `fan2008liblinear`
- `fawcett2006roc`
- `gebru2021datasheets`
- `gu2021pubmedbert`
- `guo2017calibration`
- `gurulingappa2012ade`
- `hochreiter1997lstm`
- `jin2018pico`
- `jin2019pubmedqa`
- `joachims1998text`
- `johnson2016mimic`
- `kelly2019challenges`
- `kim2011ebm`
- `kim2014cnn`
- `kreimeyer2017nlpsystems`
- `lee2020biobert`
- `liu2020consortai`
- `luo2016mlguidelines`
- `marshall2014risk`
- `marshall2015risk`
- `marshall2015robotreviewer`
- `mikolov2013word2vec`
- `mitchell2019modelcards`
- `moons2015tripod`
- `nadkarni2011nlp`
- `nagendran2020clinicians`
- `niculescu2005probabilities`
- `norgeot2020miclaim`
- `nye2018ebmnlp`
- `pedregosa2011sklearn`
- `peters2018elmo`
- `pineau2021reproducibility`
- `platt1999probabilistic`
- `rajkomar2019medicine`
- `rivera2020spiritai`
- `saito2015pr`
- `salton1988term`
- `schuster1997brnn`
- `sebastiani2002text`
- `tsafnat2014automation`
- `uzuner2011i2b2`
- `vancalster2016hierarchy`
- `vancalster2019calibration`
- `vasey2022decideai`
- `vaswani2017attention`
- `wang2018clinicalie`
- `wiens2019roadmap`
- `wilkinson2016fair`
- `zadrozny2002classifier`
- `zweigenbaum2007frontiers`

## Missing values that cannot be invented

- Pre-calibration Brier scores and ECE values for all models.
- P-values for model comparisons.
- DeLong or paired statistical comparison tests.
- Confidence intervals except the saved bootstrap AUC CI for the selected internal test model.
- Author affiliation, correspondence email, ORCID, public repository URL, and submission-system funding/competing-interest confirmations.
- Manually adjudicated clinical external validation.
