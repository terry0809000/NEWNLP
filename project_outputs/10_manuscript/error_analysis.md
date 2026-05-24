# Error Analysis

Best model: `tfidf_logistic_regression`. Error analysis uses the internal PubMed-PICO test set unless otherwise stated.

## Common False Positives
False positives are usually method or outcome-definition sentences that contain result-like lexical cues, clinical endpoints, or summary statements without being labelled R/C in the source section labels.

- `PubMed-PICO/test` source=O label=0 prob=1.000: There was a significantly lower FSH use in the once daily arm compared to the twice daily arm ( @ IU vs. @ , P = @ ) , and a trend towards lower hMG use in the once daily arm ( @ IU vs. @ , P = @ ) , without compromising clinical pregnancy rate ( PR ) ( @ % vs. @ % , P = NS ) or delivery/ongoing PR ( @ % vs. @ % , P = NS ) .
- `PubMed-PICO/test` source=O label=0 prob=1.000: Our overall results showed no difference in BMD between the treated or placebo groups , indicating that hormone therapy did not change or normalize BMD when compared to normals .
- `PubMed-PICO/test` source=O label=0 prob=1.000: RESULTS There was no significant difference in mortality between the PAC group [ @ ( @ % ) ] and the control group [ @ ( @ ) ] ( @ % confidence intervals for the difference @ to @ % , p > @ ) .
- `PubMed-PICO/test` source=O label=0 prob=1.000: RESULTS As predicted , the C-CT or fluoxetine groups were significantly less likely to relapse than the PBO group across @ months .
- `PubMed-PICO/test` source=P label=0 prob=1.000: There was no significant effect of aspirin at the end of the trial .
- `PubMed-PICO/test` source=O label=0 prob=1.000: The PAC group had significantly more fluids in the first @ h ( @ ( @ , @ ) versus @ ( @ , @ ) ml ) and an increased incidence of renal failure ( @ versus @ % of patients at day @ post randomisation p < @ ) and thrombocytopenia ( p < @ ) .
- `PubMed-PICO/test` source=A label=0 prob=1.000: This demonstrates statistically significant improvements following IDET ; however , the clinical significance of these improvements is questionable .
- `PubMed-PICO/test` source=P label=0 prob=1.000: The protective effect of aspirin was mainly observed in patients in whom @ initial expression was low ( RR for recurrence in patients taking aspirin with low @ expression : @ ; @ % CI @ to @ ; p = @ ) .

## Common False Negatives
False negatives are often short or numerically dense finding sentences where section-heading labels identify R/C but the sentence lacks explicit result language after de-identification or number masking.

- `PubMed-PICO/test` source=R label=1 prob=0.000: Linear mixed models were employed to test the primary study hypotheses .
- `PubMed-PICO/test` source=R label=1 prob=0.000: We used Rasch rating scale analysis and multilevel modeling to investigate the @ measures .
- `PubMed-PICO/test` source=C label=1 prob=0.001: All participants have been recruited from one centre , St George 's University Hospitals NHS Foundation Trust .
- `PubMed-PICO/test` source=R label=1 prob=0.002: Patients received either placebo ( n = @ ) or cabergoline @ ( n = @ ) , @ ( n = @ ) , @ ( n = @ ) or @ mg ( n = @ ) twice weekly for @ weeks .
- `PubMed-PICO/test` source=R label=1 prob=0.002: PGC costs included one glycated hemoglobin assay used by the dietitian to evaluate nutrition outcomes .
- `PubMed-PICO/test` source=R label=1 prob=0.003: A total of @ consecutive records were reviewed to determine eligibility .
- `PubMed-PICO/test` source=R label=1 prob=0.003: RFA has also been used to treat colorectal and neuroendocrine liver metastases and kidney , lung , breast , and bone cancer .
- `PubMed-PICO/test` source=C label=1 prob=0.003: Anti-hypertensive intervention therapy in pregnancy induced hypertension has been examined using a placebo controlled randomised double-blind trial of labetalol in pregnancy .

## High-Confidence Errors
The highest-confidence errors show the limits of treating section headings as sentence-level rhetorical truth; some individual sentences are semantically compatible with more than one role.

- `PubMed-PICO/test` source=O label=0 prob=1.000: There was a significantly lower FSH use in the once daily arm compared to the twice daily arm ( @ IU vs. @ , P = @ ) , and a trend towards lower hMG use in the once daily arm ( @ IU vs. @ , P = @ ) , without compromising clinical pregnancy rate ( PR ) ( @ % vs. @ % , P = NS ) or delivery/ongoing PR ( @ % vs. @ % , P = NS ) .
- `PubMed-PICO/test` source=O label=0 prob=1.000: Our overall results showed no difference in BMD between the treated or placebo groups , indicating that hormone therapy did not change or normalize BMD when compared to normals .
- `PubMed-PICO/test` source=O label=0 prob=1.000: RESULTS There was no significant difference in mortality between the PAC group [ @ ( @ % ) ] and the control group [ @ ( @ ) ] ( @ % confidence intervals for the difference @ to @ % , p > @ ) .
- `PubMed-PICO/test` source=O label=0 prob=1.000: RESULTS As predicted , the C-CT or fluoxetine groups were significantly less likely to relapse than the PBO group across @ months .
- `PubMed-PICO/test` source=P label=0 prob=1.000: There was no significant effect of aspirin at the end of the trial .
- `PubMed-PICO/test` source=O label=0 prob=1.000: The PAC group had significantly more fluids in the first @ h ( @ ( @ , @ ) versus @ ( @ , @ ) ml ) and an increased incidence of renal failure ( @ versus @ % of patients at day @ post randomisation p < @ ) and thrombocytopenia ( p < @ ) .
- `PubMed-PICO/test` source=A label=0 prob=1.000: This demonstrates statistically significant improvements following IDET ; however , the clinical significance of these improvements is questionable .
- `PubMed-PICO/test` source=P label=0 prob=1.000: The protective effect of aspirin was mainly observed in patients in whom @ initial expression was low ( RR for recurrence in patients taking aspirin with low @ expression : @ ; @ % CI @ to @ ; p = @ ) .
- `PubMed-PICO/test` source=O label=0 prob=1.000: The rate of subjects who developed postoperative adhesions was significantly lower in group A in comparison with group B ( @ % vs. @ % ) .
- `PubMed-PICO/test` source=O label=0 prob=1.000: Compared with the lowest flow rate , the @ index decreased with double and even more with quadruple flow rate , suggesting a clinically relevant worsening of the health state with higher flow rates .

## Short-Text Failures
Internal-test errors among the shortest decile of sentences: 221.

- `PubMed-PICO/test` source=P label=0 prob=0.997: There were no deaths in either group .
- `PubMed-PICO/test` source=O label=0 prob=0.993: p values less than @ indicated statistical significance .
- `PubMed-PICO/test` source=O label=0 prob=0.993: Statistical significance is at P < @ .
- `PubMed-PICO/test` source=P label=0 prob=0.991: There were no adverse reactions .
- `PubMed-PICO/test` source=I label=0 prob=0.984: Results were revealed to patients and clinicians .
- `PubMed-PICO/test` source=P label=0 prob=0.981: The overall participation rate was @ % .
- `PubMed-PICO/test` source=I label=0 prob=0.979: There was no intervention performed .
- `PubMed-PICO/test` source=O label=0 prob=0.976: No adverse events were reported .

## Ambiguous-Label Cases
Ambiguity is concentrated in source labels such as OUTCOME, METHOD, and CONCLUSION because endpoints, methods, and take-home interpretations can share vocabulary. This is a dataset-label limitation, not evidence of clinical unsafety.

## Examples Where BiLSTM Beats Classical
- `PubMed-PICO/test` source=R label=1 prob=0.689: A total of @ patients ( study @ ) and @ patients ( study @ ) completed @ weeks treatment .
- `PubMed-PICO/test` source=P label=0 prob=0.518: Seven hundred twenty-two were screened , and @ were randomized and available for inclusion in an intention-to-treat efficacy analysis ; @ ( @ % ) were male , @ ( @ % ) were white , and mean age was @ years .
- `PubMed-PICO/test` source=O label=0 prob=0.298: Mean ERMA at @ months .
- `PubMed-PICO/test` source=A label=0 prob=0.010: To test whether ursodeoxycholic acid reduces pruritus in women with intrahepatic cholestasis of pregnancy , whether early term delivery does not increase the incidence of caesarean section , and the feasibility of recruiting women with intrahepatic cholestasis of pregnancy to trials of these interventions .
- `PubMed-PICO/test` source=O label=0 prob=0.003: The primary outcome for ursodeoxycholic acid was maternal itch ( arithmetic mean of measures ( @ mm visual analogue scale ) of worst itch in past @ hours ) and for the timing of delivery was caesarean section .
- `PubMed-PICO/test` source=I label=0 prob=0.157: Children were randomly assigned in a @ ratio to @ % , @ % , and @ % atropine to be administered once nightly to both eyes for @ years .

## Examples Where Classical Beats BiLSTM
- `PubMed-PICO/test` source=C label=1 prob=0.859: The gemfibrozil-induced elevation of @ and apoA-II may reflect the combined action of LPL , HL and CETP on plasma HDL metabolism .
- `PubMed-PICO/test` source=P label=0 prob=0.131: The studies included @ ( study @ ) and @ ( study @ ) patients with type @ diabetes , no clinically significant respiratory disease and glycosylated haemoglobin ( HbA ( @ ) ) levels of @ % .
- `PubMed-PICO/test` source=R label=1 prob=0.518: Glycaemic control was maintained over @ years .
- `PubMed-PICO/test` source=C label=1 prob=0.706: Pulmonary function changes compared with comparator groups were small , non-progressive and reversed upon treatment discontinuation .
- `PubMed-PICO/test` source=C label=1 prob=0.879: Importantly , rates of lung function change were indistinguishable between EXU and comparator after @ months of therapy .
- `PubMed-PICO/test` source=P label=0 prob=0.312: Seven hundred eighty-nine patients ( BRAVO , n = @ ; CRUISE , n = @ ) .

## Subgroup Summary
Subgroup analysis was limited to ethically neutral metadata available in the public corpora: source label and sentence length. No demographic or patient-level attributes were available.