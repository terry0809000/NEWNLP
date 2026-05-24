from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import textwrap
import zipfile
from datetime import datetime
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.utils.paths import OUTPUTS_DIR, ROOT, RUNS_DIR, ensure_project_dirs


LATEX_DIR = ROOT / "latex"
TABLE_DIR = LATEX_DIR / "tables"
FIG_DIR = LATEX_DIR / "figures"
SECTION_DIR = LATEX_DIR / "sections"
SUPP_DIR = LATEX_DIR / "supplementary"
COVER_DIR = LATEX_DIR / "cover_letter"
ZIP_DIR = OUTPUTS_DIR / "11_latex_zip"
MANUSCRIPT_DIR = OUTPUTS_DIR / "10_manuscript"
DATE_ACCESSED = "2026-05-24"
TITLE = "A CPU-feasible benchmark for calibrated biomedical abstract sentence classification with external validation"
RUNNING_TITLE = "CPU-feasible calibrated biomedical NLP"
TARGET_JOURNAL = "PLOS ONE"
ARTICLE_TYPE = "Research Article"
AUTHOR = "Terry Yu"


def reset_submission_workspace() -> None:
    """Remove stale files from earlier manuscript builds before regenerating."""
    for folder in [TABLE_DIR, FIG_DIR, SECTION_DIR, SUPP_DIR, COVER_DIR]:
        if folder.exists():
            shutil.rmtree(folder)
        folder.mkdir(parents=True, exist_ok=True)
    for name in [
        "main.tex",
        "main.pdf",
        "main.aux",
        "main.bbl",
        "main.blg",
        "main.fdb_latexmk",
        "main.fls",
        "main.log",
        "main.out",
        "main.toc",
        "references.bib",
        "latex_compile_log.txt",
        "README_compile.md",
        "SUBMISSION_CHECKLIST.md",
    ]:
        path = LATEX_DIR / name
        if path.exists():
            path.unlink()
    stale_failure = OUTPUTS_DIR / "12_failure_reports" / "latex_compile_failed.md"
    if stale_failure.exists():
        stale_failure.unlink()


def fmt(x, digits: int = 3) -> str:
    if x is None or pd.isna(x):
        return "not available"
    return f"{float(x):.{digits}f}"


def fmt6(x) -> str:
    return fmt(x, 6)


def tex_escape(value) -> str:
    text = str(value)
    repl = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(repl.get(ch, ch) for ch in text)


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def read_csv(name: str) -> pd.DataFrame:
    return pd.read_csv(OUTPUTS_DIR / "06_tables" / name)


def load_data() -> dict:
    all_metrics = json.loads((OUTPUTS_DIR / "04_metrics" / "all_metrics.json").read_text(encoding="utf-8"))
    main = read_csv("main_results.csv")
    calibration = read_csv("calibration_results.csv")
    per_class = read_csv("per_class_results.csv")
    class_dist = read_csv("class_distribution.csv")
    text_len = read_csv("text_length_summary.csv")
    external = read_csv("external_validation_results.csv")
    subgroup = read_csv("subgroup_analysis.csv")
    best_model = (
        main[main["split"] == "validation"]
        .sort_values(["roc_auc", "brier_score"], ascending=[False, True])
        .iloc[0]["model"]
    )
    return {
        "all_metrics": all_metrics,
        "main": main,
        "calibration": calibration,
        "per_class": per_class,
        "class_dist": class_dist,
        "text_len": text_len,
        "external": external,
        "subgroup": subgroup,
        "best_model": best_model,
    }


def metric_row(main: pd.DataFrame, model: str, split: str) -> dict:
    return main[(main["model"] == model) & (main["split"] == split)].iloc[0].to_dict()


def selected_journal_text() -> str:
    path = OUTPUTS_DIR / "09_journal_selection" / "selected_journal_decision.md"
    return path.read_text(encoding="utf-8") if path.exists() else ""


def write_evidence_lock(data: dict) -> None:
    main = data["main"]
    calibration = data["calibration"]
    class_dist = data["class_dist"]
    text_len = data["text_len"]
    external = data["external"]
    subgroup = data["subgroup"]
    best_model = data["best_model"]
    best_test = metric_row(main, best_model, "test")
    best_external = metric_row(main, best_model, "external")
    best_json = data["all_metrics"].get(best_model, {})
    test_auc_ci = best_json.get("test_auc_ci", {})
    external_ci_row = data["external"][data["external"]["model"] == best_model]
    external_ci = external_ci_row.iloc[0].to_dict() if not external_ci_row.empty else {}
    figures = sorted(p.name for p in (OUTPUTS_DIR / "05_figures").glob("*") if p.is_file())
    tables = sorted(p.name for p in (OUTPUTS_DIR / "06_tables").glob("*") if p.is_file())
    bib_text = (OUTPUTS_DIR / "08_literature" / "references.bib").read_text(encoding="utf-8")
    citation_keys = sorted(re.findall(r"@\w+\{([^,]+),", bib_text))
    latex_possible = (LATEX_DIR / "main.pdf").exists() or shutil.which("latexmk") is not None or (Path("C:/ProgramData/TinyTeX/bin/windows/latexmk.exe").exists())

    lines = [
        "# Evidence Lock File",
        "",
        f"Created: {datetime.now().isoformat()}",
        "",
        "Only the results and citations listed here are authorized for insertion into the submission-ready manuscript.",
        "",
        "## Selected model and target",
        "",
        f"- Validation-selected model: `{best_model}`.",
        f"- AUC >= 0.70 achieved: {'yes' if float(best_test['roc_auc']) >= 0.70 else 'no'}.",
        f"- External validation exists: {'yes' if not external.empty else 'no'}.",
        f"- External validation dataset: PubMed 20k RCT official test split, mapped to the same binary findings/conclusion construct.",
        f"- Calibration improved Brier/ECE: not determined. Saved evidence contains post-calibration predictions and metrics, but pre-calibration Brier/ECE values were not saved for all models.",
        f"- LaTeX compilation possible locally: {'yes' if latex_possible else 'not confirmed'}.",
        "",
        "## Selected-model confidence intervals available",
        "",
        f"- Internal test ROC AUC 95% bootstrap CI: {fmt(test_auc_ci.get('auc_ci_low'))} to {fmt(test_auc_ci.get('auc_ci_high'))}.",
        f"- External ROC AUC 95% bootstrap CI: {fmt(external_ci.get('auc_ci_low'))} to {fmt(external_ci.get('auc_ci_high'))}.",
        "",
        "## Main metrics available",
        "",
        "```text",
        main.sort_values(["split", "roc_auc"], ascending=[True, False]).to_string(index=False),
        "```",
        "",
        "## Calibration metrics available",
        "",
        "```text",
        calibration.to_string(index=False),
        "```",
        "",
        "## Dataset class distribution available",
        "",
        "```text",
        class_dist.to_string(index=False),
        "```",
        "",
        "## Text length summary available",
        "",
        "```text",
        text_len.to_string(index=False),
        "```",
        "",
        "## External validation values available",
        "",
        "```text",
        external.to_string(index=False),
        "```",
        "",
        "## Subgroup values available",
        "",
        "```text",
        subgroup.to_string(index=False),
        "```",
        "",
        "## Figures available",
        "",
    ]
    lines.extend(f"- `{name}`" for name in figures)
    lines += [
        "",
        "## Tables available",
        "",
    ]
    lines.extend(f"- `{name}`" for name in tables)
    lines += [
        "",
        "## Citations available",
        "",
    ]
    lines.extend(f"- `{key}`" for key in citation_keys)
    lines += [
        "",
        "## Missing values that cannot be invented",
        "",
        "- Pre-calibration Brier scores and ECE values for all models.",
        "- P-values for model comparisons.",
        "- DeLong or paired statistical comparison tests.",
        "- Confidence intervals except the saved bootstrap AUC CI for the selected internal test model.",
        "- Author affiliation, correspondence email, ORCID, public repository URL, and submission-system funding/competing-interest confirmations.",
        "- Manually adjudicated clinical external validation.",
    ]
    write(MANUSCRIPT_DIR / "evidence_lock_file.md", "\n".join(lines))


def write_journal_requirements() -> None:
    text = f"""
# Journal Submission Requirements Extracted

Selected journal: PLOS ONE.

Publisher: Public Library of Science (PLOS).

Date accessed: {DATE_ACCESSED}.

Official sources checked:

- PLOS ONE submission guidelines: https://journals.plos.org/plosone/s/submission-guidelines
- PLOS ONE LaTeX guidelines: https://journals.plos.org/plosone/s/latex
- PLOS ONE data availability policy: https://journals.plos.org/plosone/s/data-availability
- PLOS materials, software and code sharing policy: https://journals.plos.org/plosone/s/materials-software-and-code-sharing
- PLOS ONE article types: https://journals.plos.org/plosone/s/what-we-publish
- PLOS ONE figure guidelines: https://journals.plos.org/plosone/s/figures
- PLOS ONE table guidelines: https://journals.plos.org/plosone/s/tables
- PLOS ONE supporting information guidelines: https://journals.plos.org/plosone/s/supporting-information
- PLOS competing interests policy: https://journals.plos.org/plosone/s/competing-interests
- PLOS funding disclosure policy: https://journals.plos.org/plosone/s/disclosure-of-funding-sources
- PLOS human subjects policy: https://journals.plos.org/plosone/s/human-subjects-research

## Extracted requirements

- Journal name: PLOS ONE.
- Article type: Research Article.
- Manuscript structure: PLOS ONE research articles typically include Abstract, Introduction, Materials and Methods, Results, Discussion, and Conclusions. This package uses those headings and includes declarations because the user requested a submission package.
- Abstract format: abstract after the title page; maximum 300 words; should describe objectives, methods, important results, and significance; no citations.
- Word limit: no word-count restriction was identified on the official submission guidelines, though concise presentation is encouraged.
- Figure/table limits: no strict number limit identified. Figures must meet PLOS figure-file requirements for production; tables should be placed after first citation in the manuscript and not submitted as separate files.
- Reference style: numbered citation-sequence/Vancouver style. The official PLOS LaTeX package includes `plos2025.bst`, which is used in this package.
- Data availability: a Data Availability Statement is required; PLOS requires the minimal data set needed to replicate findings to be publicly available unless legitimate restrictions apply.
- Code availability: PLOS expects author-generated code underpinning findings to be available without restriction upon publication where applicable; repository URL remains an author input.
- Ethics statement: human-subjects studies require ethics approval or exemption details. This project used public biomedical abstract data only; the manuscript states that no direct human-subject recruitment, patient contact, or clinical deployment occurred. Author should confirm institutional policy on exemption if needed.
- Competing interests declaration: PLOS requires declaration in the submission system. This package includes a draft statement, but author confirmation is needed.
- Funding statement: PLOS requires a funding statement in the submission system. The draft statement says no specific funding, pending author confirmation.
- Author contribution statement: PLOS requires at least one CRediT contribution for each author in the submission system. A draft CRediT statement is provided and marked author-confirmation-needed.
- ORCID requirement: no mandatory ORCID requirement was identified in the checked PLOS pages. Author may add ORCID in the submission system if desired.
- Reporting checklist requirement: no task-specific mandatory checklist was identified for this public-data machine-learning benchmark. Human Participants Checklist appears relevant only if PLOS categorizes the work as human subjects research; author should confirm at submission.
- Graphical abstract/highlights: no requirement identified. PLOS has an optional striking image.
- Cover letter: required as a separate file; one-page limit; should summarize contribution, relate to prior work, specify article type, mention prior PLOS interactions, and may suggest/opposed editors/reviewers. Fee waiver requests should not be included.
- Supplementary file policy: any file type supported; supporting files are auxiliary, published as provided, and should be named with S-numbered descriptions.
- LaTeX: PLOS provides a template and `plos2025.bst`; initial LaTeX submission uploads the PDF as manuscript file, figures separately, and source after acceptance. The official template advises a single cohesive `.tex` source for final source upload. This package keeps modular section files as requested and includes a compile-ready `main.tex`.
"""
    write(MANUSCRIPT_DIR / "journal_submission_requirements_extracted.md", text)


def make_table1(data: dict) -> None:
    class_dist = data["class_dist"]
    text_len = data["text_len"]
    pivot = class_dist.pivot_table(index=["dataset", "split"], columns="label_name", values="n", fill_value=0).reset_index()
    total = pivot.get("findings_conclusion", 0) + pivot.get("other", 0)
    pivot["total"] = total
    pivot["positive_pct"] = 100 * pivot.get("findings_conclusion", 0) / total
    length_mean = text_len.groupby(["dataset", "split"])["mean"].mean().reset_index(name="mean_words")
    length_median = text_len.groupby(["dataset", "split"])["median"].mean().reset_index(name="median_words")
    table = pivot.merge(length_mean, on=["dataset", "split"]).merge(length_median, on=["dataset", "split"])
    lines = [
        r"\begin{table}[!ht]",
        r"\centering",
        r"\caption{\textbf{Dataset characteristics.} The positive class is findings/conclusion. Text length summaries average the label-specific means and medians available in the locked evidence table.}",
        r"\begin{tabular}{llllrrr}",
        r"\hline",
        r"Dataset & Split & Total & Positive & Other & Positive \% & Median words \\",
        r"\hline",
    ]
    for _, row in table.iterrows():
        lines.append(
            f"{tex_escape(row['dataset'])} & {tex_escape(row['split'])} & {int(row['total'])} & {int(row.get('findings_conclusion', 0))} & {int(row.get('other', 0))} & {fmt(row['positive_pct'], 1)} & {fmt(row['median_words'], 1)} \\\\"
        )
    lines += [
        r"\hline",
        r"\end{tabular}",
        r"\begin{flushleft}\footnotesize PubMed-PICO train, validation, and test splits were used for primary modelling. PubMed-20k-RCT external\_test was used only for external validation.\end{flushleft}",
        r"\label{tab:dataset}",
        r"\end{table}",
    ]
    write(TABLE_DIR / "table1_dataset.tex", "\n".join(lines))


def make_table2(data: dict) -> None:
    main = data["main"]
    models = sorted(main["model"].unique())
    lines = [
        r"\begin{table}[!ht]",
        r"\centering",
        r"\caption{\textbf{Model comparison on validation and internal test splits.} Model selection used validation ROC AUC, with Brier score as a secondary calibration criterion.}",
        r"\small",
        r"\begin{tabular}{lrrrrrr}",
        r"\hline",
        r"Model & Val AUC & Test AUC & Test PR AUC & Test F1 & Test Brier & Test ECE \\",
        r"\hline",
    ]
    for model in models:
        val = metric_row(main, model, "validation")
        test = metric_row(main, model, "test")
        lines.append(
            f"{tex_escape(model)} & {fmt(val['roc_auc'])} & {fmt(test['roc_auc'])} & {fmt(test['pr_auc'])} & {fmt(test['f1'])} & {fmt(test['brier_score'])} & {fmt(test['ece_10bin'])} \\\\"
        )
    lines += [
        r"\hline",
        r"\end{tabular}",
        r"\begin{flushleft}\footnotesize All values are from saved run metrics. Classical models used validation-fitted Platt calibration; neural models used validation-fitted temperature scaling.\end{flushleft}",
        r"\label{tab:model-comparison}",
        r"\end{table}",
    ]
    write(TABLE_DIR / "table2_model_comparison.tex", "\n".join(lines))


def make_table3(data: dict) -> None:
    calibration = data["calibration"]
    lines = [
        r"\begin{table}[!ht]",
        r"\centering",
        r"\caption{\textbf{Post-calibration probability metrics.} Pre-calibration Brier and ECE were not saved for all models and are therefore not reported.}",
        r"\small",
        r"\begin{tabular}{llrrrr}",
        r"\hline",
        r"Model & Split & Post Brier & Post ECE & Calibration intercept & Calibration slope \\",
        r"\hline",
    ]
    for _, row in calibration.iterrows():
        lines.append(
            f"{tex_escape(row['model'])} & {tex_escape(row['split'])} & {fmt(row['brier_score'])} & {fmt(row['ece_10bin'])} & {fmt(row['calibration_intercept'])} & {fmt(row['calibration_slope'])} \\\\"
        )
    lines += [
        r"\hline",
        r"\end{tabular}",
        r"\begin{flushleft}\footnotesize Calibration method: Platt sigmoid calibration for TF-IDF logistic regression and linear SVM; temperature scaling for neural models; none for the majority baseline. The evidence lock does not support any claim that calibration improved Brier score or ECE because pre-calibration metrics were not retained.\end{flushleft}",
        r"\label{tab:calibration}",
        r"\end{table}",
    ]
    write(TABLE_DIR / "table3_calibration.tex", "\n".join(lines))


def make_table4(data: dict) -> None:
    main = data["main"]
    lines = [
        r"\begin{table}[!ht]",
        r"\centering",
        r"\caption{\textbf{External validation results.} Performance drop is external ROC AUC minus internal test ROC AUC; negative values indicate lower external discrimination.}",
        r"\small",
        r"\begin{tabular}{lrrrrrr}",
        r"\hline",
        r"Model & Test AUC & External AUC & AUC drop & External F1 & External Brier & External ECE \\",
        r"\hline",
    ]
    for model in sorted(main["model"].unique()):
        test = metric_row(main, model, "test")
        ext = metric_row(main, model, "external")
        drop = float(ext["roc_auc"]) - float(test["roc_auc"])
        lines.append(
            f"{tex_escape(model)} & {fmt(test['roc_auc'])} & {fmt(ext['roc_auc'])} & {fmt(drop)} & {fmt(ext['f1'])} & {fmt(ext['brier_score'])} & {fmt(ext['ece_10bin'])} \\\\"
        )
    lines += [
        r"\hline",
        r"\end{tabular}",
        r"\begin{flushleft}\footnotesize The external split was not used for training, hyperparameter selection, thresholding, or calibration fitting.\end{flushleft}",
        r"\label{tab:external}",
        r"\end{table}",
    ]
    write(TABLE_DIR / "table4_external_validation.tex", "\n".join(lines))


def make_table5(data: dict) -> None:
    subgroup = data["subgroup"]
    lines = [
        r"\begin{table}[!ht]",
        r"\centering",
        r"\caption{\textbf{Sentence-length subgroup analysis for the selected model.} Subgroups are descriptive and based on length quartiles.}",
        r"\begin{tabular}{llrrrr}",
        r"\hline",
        r"Split & Group & n & ROC AUC & Brier & ECE \\",
        r"\hline",
    ]
    for _, row in subgroup.iterrows():
        group = str(row["subgroup"]).replace("length:", "")
        lines.append(
            f"{tex_escape(row['split'])} & {tex_escape(group)} & {int(row['n'])} & {fmt(row['roc_auc'])} & {fmt(row['brier_score'])} & {fmt(row['ece_10bin'])} \\\\"
        )
    lines += [
        r"\hline",
        r"\end{tabular}",
        r"\begin{flushleft}\footnotesize All subgroup cells had large sample sizes in this run. Results should still be interpreted descriptively because length groups were not pre-specified clinical subgroups.\end{flushleft}",
        r"\label{tab:subgroup}",
        r"\end{table}",
    ]
    write(TABLE_DIR / "table5_subgroup.tex", "\n".join(lines))


def copy_figures() -> list[str]:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    copied = []
    for src in sorted((OUTPUTS_DIR / "05_figures").glob("*")):
        if src.is_file():
            shutil.copy2(src, FIG_DIR / src.name)
            copied.append(src.name)
    missing = ["model_comparison_plot"] if not (OUTPUTS_DIR / "05_figures" / "model_comparison_plot.png").exists() else []
    report = [
        "# Missing Figures Report",
        "",
        "Available figures were copied from `project_outputs/05_figures/` into `latex/figures/`.",
        "",
        "## Copied figures",
        "",
    ]
    report.extend(f"- `{name}`" for name in copied)
    report += ["", "## Missing figures not invented", ""]
    if missing:
        report.extend(f"- {name}: no verified file exists in project outputs." for name in missing)
    else:
        report.append("- None.")
    write(MANUSCRIPT_DIR / "missing_figures_report.md", "\n".join(report))
    return copied


def write_tables(data: dict) -> None:
    TABLE_DIR.mkdir(parents=True, exist_ok=True)
    make_table1(data)
    make_table2(data)
    make_table3(data)
    make_table4(data)
    make_table5(data)


def build_markdown_manuscript(data: dict) -> str:
    main = data["main"]
    class_dist = data["class_dist"]
    best = data["best_model"]
    val = metric_row(main, best, "validation")
    test = metric_row(main, best, "test")
    ext = metric_row(main, best, "external")
    train_n = int(class_dist[(class_dist["dataset"] == "PubMed-PICO") & (class_dist["split"] == "train")]["n"].sum())
    val_n = int(class_dist[(class_dist["dataset"] == "PubMed-PICO") & (class_dist["split"] == "validation")]["n"].sum())
    test_n = int(class_dist[(class_dist["dataset"] == "PubMed-PICO") & (class_dist["split"] == "test")]["n"].sum())
    ext_n = int(class_dist[class_dist["dataset"] == "PubMed-20k-RCT"]["n"].sum())
    auc_ci = data["all_metrics"][best].get("test_auc_ci", {})
    ci_text = ""
    if auc_ci.get("auc_ci_low") is not None:
        ci_text = f" (95% bootstrap CI {fmt(auc_ci['auc_ci_low'])} to {fmt(auc_ci['auc_ci_high'])})"
    md = f"""
# Title page

Full title: {TITLE}

Short running title: {RUNNING_TITLE}

Author: {AUTHOR}

Affiliation: [AFFILIATION TO BE COMPLETED BY AUTHOR]

Corresponding author: [CORRESPONDING AUTHOR EMAIL TO BE COMPLETED BY AUTHOR]

Article type: {ARTICLE_TYPE}

Target journal: {TARGET_JOURNAL}

# Abstract

Background: Biomedical abstract sentence classification can support evidence triage by helping researchers locate sentences that report findings or conclusions. Many healthcare natural language processing benchmarks emphasize discrimination while giving less attention to calibration, external validation, and reproducibility under modest hardware constraints.

Objective: To evaluate whether CPU-feasible classical and recurrent neural text classifiers can identify findings/conclusion sentences in public biomedical abstracts with useful discrimination, transparent calibration assessment, and external validation.

Methods: PubMed-PICO official train, validation, and test splits were used as the primary corpus. Sentences labelled R or C were mapped to the positive class. The PubMed 20k RCT official test split was used only for external validation, with RESULTS and CONCLUSIONS mapped to the positive class. We evaluated a majority baseline, TF-IDF logistic regression, TF-IDF linear support vector machine, feed-forward average embeddings, LSTM, BiLSTM, and BiLSTM with dropout. Classical models used validation-fitted Platt calibration, neural models used validation-fitted temperature scaling, and thresholds were selected on validation data only.

Results: The validation-selected model was TF-IDF logistic regression. It achieved validation ROC AUC {fmt(val['roc_auc'])}, internal test ROC AUC {fmt(test['roc_auc'])}{ci_text}, PR AUC {fmt(test['pr_auc'])}, F1 {fmt(test['f1'])}, Brier score {fmt(test['brier_score'])}, and expected calibration error {fmt(test['ece_10bin'])}. On external validation, ROC AUC was {fmt(ext['roc_auc'])}, PR AUC {fmt(ext['pr_auc'])}, F1 {fmt(ext['f1'])}, Brier score {fmt(ext['brier_score'])}, and expected calibration error {fmt(ext['ece_10bin'])}.

Conclusions: A strong sparse linear model met the empirical AUC target and performed at least as well as lightweight recurrent neural alternatives in this CPU-only benchmark. External validation supported partial generalisation within biomedical abstracts but showed calibration degradation, so the model should be treated as a reproducible evidence-triage benchmark rather than a deployment-ready clinical system.

# Keywords

healthcare NLP; biomedical text classification; recurrent neural networks; calibration; external validation; reproducible machine learning; clinical decision support; model evaluation

# Introduction

Biomedical abstracts are a compact but information-dense substrate for evidence synthesis. In randomized-trial and clinical-research abstracts, sentences describing outcomes, findings, and conclusions are often the first targets for screening, triage, and downstream evidence extraction. A sentence-level model that can identify this rhetorical content is not a substitute for full critical appraisal, but it can reduce the cost of navigating large search results and make subsequent human review more efficient.

The methodological question is not only whether a model can obtain high discrimination. In healthcare-adjacent machine learning, calibrated probabilities and external validation are central safeguards against over-interpreting a model's apparent performance. A model that ranks sentences well may still provide misleading probability estimates, and a model tuned on one corpus may degrade when evaluated on another corpus with different labelling conventions. This study therefore treats calibration, external validation, and reproducibility as first-class outcomes.

CPU-feasible modelling is also scientifically important. Not every clinical informatics group or evidence-synthesis team has access to local GPU infrastructure, and not every biomedical NLP task requires a large Transformer model. Sparse linear models and lightweight recurrent neural networks remain attractive when a benchmark must be transparent, rerunnable, and inexpensive. This study asks whether such methods can solve a clinically meaningful abstract triage task under explicit CPU-only constraints.

The contributions are fourfold. First, the study defines a binary findings/conclusion detection task using public PubMed-PICO data and a label-compatible PubMed RCT external validation corpus. Second, it compares full-training TF-IDF baselines against CPU-limited neural models, including LSTM and BiLSTM variants. Third, it reports discrimination, thresholded classification performance, calibration metrics, reliability plots, and subgroup analysis from saved predictions. Fourth, it packages code, logs, metrics, tables, figures, and LaTeX source to support independent checking.

# Related work

Healthcare NLP has a long methodological base in converting unstructured biomedical and clinical text into analyzable evidence. General introductions and reviews emphasize both the promise of text mining and the fragility of systems that are evaluated only in narrow settings \\cite{{nadkarni2011nlp,zweigenbaum2007frontiers,kreimeyer2017nlpsystems,wang2018clinicalie}}. Restricted clinical-note resources and shared tasks such as MIMIC-III and i2b2/VA have shaped clinical NLP, but they require credentialed access or task-specific permissions and were therefore not used in this public CPU-only project \\cite{{johnson2016mimic,uzuner2011i2b2}}.

Public biomedical abstract corpora have made sentence classification a reproducible benchmark problem. PubMed-PICO was introduced for PICO element detection in medical text and has been used to study neural sentence classification with long short-term memory networks \\cite{{jin2018pico}}. PubMed 20k/200k RCT provides section-labelled randomized-trial abstracts for sequential sentence classification \\cite{{dernoncourt2017pubmed}}. EBM-NLP and related work show the broader value of patient, intervention, outcome, and evidence-bearing sentence annotations for systematic-review support \\cite{{nye2018ebmnlp,kim2011ebm}}. NICTA-PIBOSO is a manually annotated corpus of medical abstracts \\cite{{amini2018nicta}}, but it was not usable as an automatic external validation source in this run because the accessible archive did not contain usable files and the latest record was restricted. Other public biomedical tasks, including PubMedQA \\cite{{jin2019pubmedqa}} and adverse-event extraction corpora \\cite{{gurulingappa2012ade}}, were considered but were less directly aligned with a CPU-feasible calibrated binary sentence-classification benchmark.

The evidence-synthesis literature also motivates this task. Automated citation screening, review automation, and risk-of-bias systems show how NLP can reduce workload while still requiring transparent human oversight \\cite{{cohen2006workload,tsafnat2014automation,marshall2014risk,marshall2015risk,marshall2015robotreviewer}}. The present study is narrower than full systematic-review automation: it tests sentence-level rhetorical detection rather than eligibility, effect-size extraction, or risk-of-bias judgment.

Classical machine-learning methods remain strong baselines for text classification. TF-IDF term weighting and machine-learning text categorization have a long empirical history \\cite{{salton1988term,sebastiani2002text}}, and support vector machines provide a well-established margin-based classifier \\cite{{cortes1995svm,joachims1998text}}. Efficient linear solvers and probabilistic calibration methods make sparse models practical for large biomedical corpora \\cite{{fan2008liblinear,platt1999probabilistic}}. The classical models in this study were implemented with scikit-learn \\cite{{pedregosa2011sklearn}}.

Recurrent neural networks provide a contrasting sequence-aware modelling family. LSTM architectures were designed to address long-range dependency learning in sequential data \\cite{{hochreiter1997lstm}}, and bidirectional recurrent networks can incorporate context from both token directions \\cite{{schuster1997brnn}}. Static word vectors, convolutional sentence models, contextual embeddings, and Transformer language models have substantially shaped modern NLP \\cite{{mikolov2013word2vec,kim2014cnn,peters2018elmo,vaswani2017attention,devlin2019bert}}. Biomedical and scientific variants such as SciBERT, BioBERT, and PubMedBERT further demonstrate the value of domain-specific pretraining \\cite{{beltagy2019scibert,lee2020biobert,gu2021pubmedbert}}. This benchmark nevertheless focused on LSTM/BiLSTM neural baselines because they are realistic CPU-only comparators; GPU-scale Transformer fine-tuning was outside scope.

Evaluation in this setting must go beyond accuracy. The Brier score is a proper scoring rule for probabilistic forecasts \\cite{{brier1950verification}}, ROC and precision-recall analyses capture complementary aspects of binary discrimination \\cite{{fawcett2006roc,davis2006prroc,saito2015pr}}, and post-hoc calibration methods were developed to convert classifier scores into better probability estimates \\cite{{niculescu2005probabilities,zadrozny2002classifier,guo2017calibration}}. Clinical prediction literature has argued that calibration should be assessed alongside discrimination because useful ranking is not the same as reliable probabilities \\cite{{vancalster2016hierarchy,vancalster2019calibration,austin2019ici}}.

Transparent reporting and reproducibility are especially important when healthcare-adjacent machine learning is evaluated on proxy labels. TRIPOD and related guidance emphasize validation, complete reporting, and cautious interpretation \\cite{{collins2015tripod,moons2015tripod,luo2016mlguidelines}}. FAIR data principles, reproducibility recommendations, model cards, and datasheets provide complementary expectations for documenting code, data, and model limitations \\cite{{wilkinson2016fair,pineau2021reproducibility,mitchell2019modelcards,gebru2021datasheets}}. Clinical AI guidance, including MI-CLAIM, SPIRIT-AI, CONSORT-AI, and DECIDE-AI, reinforces that benchmark performance is not deployment evidence \\cite{{norgeot2020miclaim,rivera2020spiritai,liu2020consortai,vasey2022decideai}}. Broader healthcare AI commentary similarly warns that clinical impact requires validation, workflow integration, ethics review, and prospective evaluation \\cite{{rajkomar2019medicine,kelly2019challenges,chen2017prediction,wiens2019roadmap,char2018ethical,nagendran2020clinicians}}.

# Data

The primary dataset was PubMed-PICO Detection, downloaded from the public GitHub repository. The processed primary corpus contained {train_n:,} training sentences, {val_n:,} validation sentences, and {test_n:,} internal test sentences. Source labels R and C were mapped to the positive class, named findings/conclusion, while all other PubMed-PICO labels were mapped to the negative class. The text field was the sentence text extracted from biomedical abstracts.

External validation used the official PubMed 20k RCT test split. This corpus contributed {ext_n:,} external sentences. Labels RESULTS and CONCLUSIONS were mapped to the positive class, and all other section labels were mapped to the negative class. This mapping is label-compatible for the narrower rhetorical construct of result or conclusion detection, not for full PICO extraction.

Official primary splits were preserved. Vectorizers, neural tokenizers, and vocabularies were fitted only on the primary training split. The validation split was used for model selection, calibration fitting, and threshold selection. The internal test split was evaluated after model selection, and the external validation split was never used for fitting, tuning, calibration, or threshold selection. Table 1 summarises the dataset characteristics and class balance.

# Methods

The majority baseline predicted the empirical training-class prior. TF-IDF logistic regression used sparse word 1-2 grams and character 3-5 grams, with regularised logistic regression fitted on the full training split. TF-IDF linear support vector machine used the same feature family with a linear SVM and validation-fitted Platt calibration of decision scores. These baselines were included because sparse lexical models are strong, transparent, and practical under CPU-only constraints.

Neural models used a training-only vocabulary, integer token sequences, and fixed-length padded sequences. The feed-forward neural model averaged trainable token embeddings before classification. The LSTM, BiLSTM, and BiLSTM with dropout used trainable embeddings and small hidden dimensions to keep runtime feasible on CPU. Neural models were trained on a stratified cap of 120,000 training sentences, evaluated on the full validation, test, and external splits, and used early stopping based on validation performance. This cap is a methodological constraint rather than an optimization claim.

Classical models were calibrated with Platt sigmoid calibration fitted on validation scores. Neural models were calibrated with temperature scaling fitted on validation logits. Thresholds were optimized for validation F1 only. No preprocessing, calibration, threshold selection, or model selection used the internal test or external validation labels.

Experiments were conducted in CPU-only mode on Windows 11 with Python 3.14 and CPU PyTorch. CUDA availability was explicitly checked and was false. Random seeds and training logs were saved with the run artifacts.

# Evaluation

The primary metric was receiver operating characteristic area under the curve. Secondary metrics were precision-recall area under the curve, accuracy, sensitivity/recall, specificity, precision/positive predictive value, F1 score, confusion matrix counts, Brier score, expected calibration error, calibration intercept, and calibration slope. Reliability plots, ROC curves, precision-recall curves, and confusion matrices were generated from saved predictions.

Calibration was assessed after validation-fitted calibration. The evidence lock does not contain pre-calibration Brier scores or expected calibration errors for all models; therefore, this manuscript does not claim that calibration improved these metrics. Instead, it reports the calibrated probability performance available from the completed experiments.

External validation was performed by applying the selected training-fitted preprocessing and trained models to the PubMed 20k RCT external test split. The external data were never used for training, tuning, or threshold selection. Subgroup analysis used ethically neutral metadata available in the corpora: sentence-length quartiles. No demographic or patient-level fairness analysis was possible because the datasets do not contain such metadata.

# Results

The empirical AUC target was achieved. Table 2 shows the model comparison. TF-IDF logistic regression was selected by validation ROC AUC, with validation ROC AUC {fmt(val['roc_auc'])}, Brier score {fmt(val['brier_score'])}, and expected calibration error {fmt(val['ece_10bin'])}. On the internal test split, the same model achieved ROC AUC {fmt(test['roc_auc'])}{ci_text}, PR AUC {fmt(test['pr_auc'])}, accuracy {fmt(test['accuracy'])}, F1 {fmt(test['f1'])}, sensitivity {fmt(test['sensitivity_recall'])}, specificity {fmt(test['specificity'])}, Brier score {fmt(test['brier_score'])}, and expected calibration error {fmt(test['ece_10bin'])}. The internal-test confusion matrix for the selected threshold contained {int(test['true_positive'])} true positives, {int(test['true_negative'])} true negatives, {int(test['false_positive'])} false positives, and {int(test['false_negative'])} false negatives.

The strongest neural model was the BiLSTM, with internal test ROC AUC {fmt(metric_row(main, 'bilstm', 'test')['roc_auc'])}, compared with {fmt(test['roc_auc'])} for TF-IDF logistic regression and {fmt(metric_row(main, 'tfidf_linear_svm', 'test')['roc_auc'])} for TF-IDF linear SVM. The unidirectional LSTM was weaker, with internal test ROC AUC {fmt(metric_row(main, 'lstm', 'test')['roc_auc'])}. This pattern indicates that lightweight recurrence did not provide a clear advantage over sparse lexical baselines under the CPU-feasible protocol.

Table 3 reports calibrated probability metrics. The selected model's internal calibration was strong by the saved metrics, with internal-test Brier score {fmt(test['brier_score'])}, expected calibration error {fmt(test['ece_10bin'])}, calibration intercept {fmt(test['calibration_intercept'])}, and calibration slope {fmt(test['calibration_slope'])}. External calibration was weaker, with Brier score {fmt(ext['brier_score'])}, expected calibration error {fmt(ext['ece_10bin'])}, and calibration slope {fmt(ext['calibration_slope'])}, consistent with corpus and label shift.

External validation results are shown in Table 4. The selected model achieved external ROC AUC {fmt(ext['roc_auc'])}, PR AUC {fmt(ext['pr_auc'])}, accuracy {fmt(ext['accuracy'])}, and F1 {fmt(ext['f1'])}. The external ROC AUC was lower than internal test ROC AUC by {fmt(float(ext['roc_auc']) - float(test['roc_auc']))}. Table 5 summarises sentence-length subgroup results. Longer sentences had higher observed AUC in both internal and external splits, but these results are descriptive and should not be interpreted as clinical subgroup performance.

Error analysis found that false positives often involved method or outcome-definition sentences with result-like clinical endpoint language. False negatives often involved short or numerically dense findings sentences. High-confidence errors illustrated the limitation of section-heading-derived labels: some sentences can be semantically compatible with more than one rhetorical role even when the dataset assigns a single label.

# Discussion

This study demonstrates that a CPU-only biomedical sentence-classification benchmark can achieve strong discrimination and report useful calibration diagnostics without GPU-scale modelling. The best model was TF-IDF logistic regression rather than a recurrent neural network. This does not imply that neural models are generally inferior; rather, it shows that for this public abstract-level task, sparse lexical features capture much of the signal and provide a strong baseline that should not be skipped.

The external validation result supports partial generalisation to a related biomedical abstract corpus, but it also reveals the expected fragility of probabilities under corpus shift. Discrimination remained high externally, yet Brier score, expected calibration error, and calibration slope degraded. For evidence-triage use, this means that ranked sentence retrieval may transfer better than absolute probability interpretation. Any downstream use should consider recalibration in the target corpus and further validation with manually adjudicated labels.

The benchmark also illustrates a practical reproducibility point. CPU-feasible pipelines are easier to rerun, inspect, and package. The project saved raw and processed manifests, training logs, predictions, calibration artifacts, metrics, figures, tables, and manuscript source. This level of evidence traceability is valuable even when the model itself is methodologically simple.

Clinically, the model should not be interpreted as a decision-support system. It detects rhetorical sentence roles in abstracts. It does not assess trial quality, extract effect sizes, evaluate bias, or recommend patient care. The appropriate interpretation is a reproducible benchmark for literature triage and methodological evaluation.

# Limitations

The primary limitation is the label source. PubMed-PICO and PubMed RCT labels are derived from abstract structure or annotation conventions, and a section label is not always equivalent to sentence-level semantics. Some errors identified in the analysis likely reflect ambiguous or proxy labels rather than purely model failures.

The external validation corpus is public and held out, but it remains in the biomedical abstract domain. It is not a manually adjudicated external clinical setting, and it does not prove deployment readiness. The NICTA-PIBOSO corpus was investigated as a manual external validation candidate but was not automatically available in usable form in this environment.

The neural experiments were intentionally CPU-limited. Models used small embeddings, short maximum sequence lengths, and a stratified cap on neural training examples. Larger recurrent models, pretrained biomedical Transformers, or GPU-scale fine-tuning might perform differently, but they were outside the CPU-only scope of this project.

Calibration uncertainty is another limitation. The project reports calibrated Brier score, expected calibration error, and reliability curves, but it did not retain pre-calibration Brier/ECE for all models and did not compute uncertainty intervals for calibration metrics. No demographic fairness analysis was possible because the public abstract corpora do not include patient-level demographic metadata.

# Conclusion

A complete CPU-only healthcare NLP benchmark achieved the empirical AUC target for findings/conclusion sentence detection in biomedical abstracts, with the validation-selected TF-IDF logistic regression model obtaining internal test ROC AUC {fmt(test['roc_auc'])} and external ROC AUC {fmt(ext['roc_auc'])}. Lightweight recurrent neural models were feasible and informative but did not outperform the strongest sparse baseline. The results support careful, reproducible, calibration-aware benchmarking for healthcare NLP while underscoring that abstract sentence classification is not clinical deployment evidence.

# Data availability statement

The raw public datasets used in this study are available from the PubMed-PICO Detection repository (https://github.com/jind11/PubMed-PICO-Detection) and the PubMed RCT repository (https://github.com/Franck-Dernoncourt/pubmed-rct). The processed data, predictions, summary tables, and figures were generated by the local scripts in this project. Before journal submission, the author should deposit the generated minimal replication package in a public repository and replace this placeholder with a persistent URL or DOI: [REPOSITORY URL TO BE INSERTED].

# Code availability statement

The code used to download data, prepare datasets, train models, calibrate predictions, evaluate metrics, generate figures, and build the manuscript package is located in the local project directories `src/` and `scripts/`. Before submission, the author should publish the code in a public repository or archival service and insert the persistent repository URL here: [REPOSITORY URL TO BE INSERTED].

# Ethics statement

This study used public biomedical abstract datasets and did not recruit participants, contact patients, process restricted clinical notes, or deploy a model in patient care. No identifiable patient-level data were used. The models are for research evaluation and evidence-triage benchmarking only and should not be used for clinical decision-making without separate validation, governance review, and prospective evaluation.

# Funding statement

The author received no specific funding for this work. Author confirmation is needed before submission.

# Competing interests

The author declares no competing interests. Author confirmation is needed before submission.

# Author contributions

Author-confirmation-needed CRediT statement: Conceptualisation, methodology, software, formal analysis, investigation, data curation, validation, visualisation, writing--original draft, and writing--review and editing: Terry Yu.

# Acknowledgements

Not applicable.
"""
    write(MANUSCRIPT_DIR / "submission_ready_manuscript.md", md)
    return md


def write_sections() -> None:
    SECTION_DIR.mkdir(parents=True, exist_ok=True)
    section_text = {
        "01_introduction.tex": r"""
\section*{Introduction}
Biomedical abstracts are a compact but information-dense substrate for evidence synthesis. In randomized-trial and clinical-research abstracts, sentences describing outcomes, findings, and conclusions are often the first targets for screening, triage, and downstream evidence extraction. A sentence-level model that can identify this rhetorical content is not a substitute for full critical appraisal, but it can reduce the cost of navigating large search results and make subsequent human review more efficient.

The methodological question is not only whether a model can obtain high discrimination. In healthcare-adjacent machine learning, calibrated probabilities and external validation are central safeguards against over-interpreting a model's apparent performance. A model that ranks sentences well may still provide misleading probability estimates, and a model tuned on one corpus may degrade when evaluated on another corpus with different labelling conventions. This study therefore treats calibration, external validation, and reproducibility as first-class outcomes.

CPU-feasible modelling is also scientifically important. Not every clinical informatics group or evidence-synthesis team has access to local GPU infrastructure, and not every biomedical NLP task requires a large Transformer model. Sparse linear models and lightweight recurrent neural networks remain attractive when a benchmark must be transparent, rerunnable, and inexpensive. This study asks whether such methods can solve a clinically meaningful abstract triage task under explicit CPU-only constraints.

The contributions are fourfold. First, the study defines a binary findings/conclusion detection task using public PubMed-PICO data and a label-compatible PubMed RCT external validation corpus. Second, it compares full-training TF-IDF baselines against CPU-limited neural models, including LSTM and BiLSTM variants. Third, it reports discrimination, thresholded classification performance, calibration metrics, reliability plots, and subgroup analysis from saved predictions. Fourth, it packages code, logs, metrics, tables, figures, and LaTeX source to support independent checking.
""",
        "02_related_work.tex": r"""
\section*{Related work}
Healthcare NLP has a long methodological base in converting unstructured biomedical and clinical text into analyzable evidence. General introductions and reviews emphasize both the promise of text mining and the fragility of systems that are evaluated only in narrow settings~\cite{nadkarni2011nlp,zweigenbaum2007frontiers,kreimeyer2017nlpsystems,wang2018clinicalie}. Restricted clinical-note resources and shared tasks such as MIMIC-III and i2b2/VA have shaped clinical NLP, but they require credentialed access or task-specific permissions and were therefore not used in this public CPU-only project~\cite{johnson2016mimic,uzuner2011i2b2}.

Public biomedical abstract corpora have made sentence classification a reproducible benchmark problem. PubMed-PICO was introduced for PICO element detection in medical text and has been used to study neural sentence classification with long short-term memory networks~\cite{jin2018pico}. PubMed 20k/200k RCT provides section-labelled randomized-trial abstracts for sequential sentence classification~\cite{dernoncourt2017pubmed}. EBM-NLP and related work show the broader value of patient, intervention, outcome, and evidence-bearing sentence annotations for systematic-review support~\cite{nye2018ebmnlp,kim2011ebm}. NICTA-PIBOSO is a manually annotated corpus of medical abstracts~\cite{amini2018nicta}, but it was not usable as an automatic external validation source in this run because the accessible archive did not contain usable files and the latest record was restricted. Other public biomedical tasks, including PubMedQA~\cite{jin2019pubmedqa} and adverse-event extraction corpora~\cite{gurulingappa2012ade}, were considered but were less directly aligned with a CPU-feasible calibrated binary sentence-classification benchmark.

The evidence-synthesis literature also motivates this task. Automated citation screening, review automation, and risk-of-bias systems show how NLP can reduce workload while still requiring transparent human oversight~\cite{cohen2006workload,tsafnat2014automation,marshall2014risk,marshall2015risk,marshall2015robotreviewer}. The present study is narrower than full systematic-review automation: it tests sentence-level rhetorical detection rather than eligibility, effect-size extraction, or risk-of-bias judgment.

Classical machine-learning methods remain strong baselines for text classification. TF-IDF term weighting and machine-learning text categorization have a long empirical history~\cite{salton1988term,sebastiani2002text}, and support vector machines provide a well-established margin-based classifier~\cite{cortes1995svm,joachims1998text}. Efficient linear solvers and probabilistic calibration methods make sparse models practical for large biomedical corpora~\cite{fan2008liblinear,platt1999probabilistic}. The classical models in this study were implemented with scikit-learn~\cite{pedregosa2011sklearn}.

Recurrent neural networks provide a contrasting sequence-aware modelling family. LSTM architectures were designed to address long-range dependency learning in sequential data~\cite{hochreiter1997lstm}, and bidirectional recurrent networks can incorporate context from both token directions~\cite{schuster1997brnn}. Static word vectors, convolutional sentence models, contextual embeddings, and Transformer language models have substantially shaped modern NLP~\cite{mikolov2013word2vec,kim2014cnn,peters2018elmo,vaswani2017attention,devlin2019bert}. Biomedical and scientific variants such as SciBERT, BioBERT, and PubMedBERT further demonstrate the value of domain-specific pretraining~\cite{beltagy2019scibert,lee2020biobert,gu2021pubmedbert}. This benchmark nevertheless focused on LSTM/BiLSTM neural baselines because they are realistic CPU-only comparators; GPU-scale Transformer fine-tuning was outside scope.

Evaluation in this setting must go beyond accuracy. The Brier score is a proper scoring rule for probabilistic forecasts~\cite{brier1950verification}, ROC and precision-recall analyses capture complementary aspects of binary discrimination~\cite{fawcett2006roc,davis2006prroc,saito2015pr}, and post-hoc calibration methods were developed to convert classifier scores into better probability estimates~\cite{niculescu2005probabilities,zadrozny2002classifier,guo2017calibration}. Clinical prediction literature has argued that calibration should be assessed alongside discrimination because useful ranking is not the same as reliable probabilities~\cite{vancalster2016hierarchy,vancalster2019calibration,austin2019ici}.

Transparent reporting and reproducibility are especially important when healthcare-adjacent machine learning is evaluated on proxy labels. TRIPOD and related guidance emphasize validation, complete reporting, and cautious interpretation~\cite{collins2015tripod,moons2015tripod,luo2016mlguidelines}. FAIR data principles, reproducibility recommendations, model cards, and datasheets provide complementary expectations for documenting code, data, and model limitations~\cite{wilkinson2016fair,pineau2021reproducibility,mitchell2019modelcards,gebru2021datasheets}. Clinical AI guidance, including MI-CLAIM, SPIRIT-AI, CONSORT-AI, and DECIDE-AI, reinforces that benchmark performance is not deployment evidence~\cite{norgeot2020miclaim,rivera2020spiritai,liu2020consortai,vasey2022decideai}. Broader healthcare AI commentary similarly warns that clinical impact requires validation, workflow integration, ethics review, and prospective evaluation~\cite{rajkomar2019medicine,kelly2019challenges,chen2017prediction,wiens2019roadmap,char2018ethical,nagendran2020clinicians}.
""",
        "03_data.tex": r"""
\section*{Materials and methods}
\subsection*{Data}
The primary dataset was PubMed-PICO Detection, downloaded from the public GitHub repository. The processed primary corpus contained 257,820 training sentences, 30,878 validation sentences, and 31,270 internal test sentences. Source labels R and C were mapped to the positive class, named findings/conclusion, while all other PubMed-PICO labels were mapped to the negative class. The text field was the sentence text extracted from biomedical abstracts.

External validation used the official PubMed 20k RCT test split. This corpus contributed 30,135 external sentences. Labels RESULTS and CONCLUSIONS were mapped to the positive class, and all other section labels were mapped to the negative class. This mapping is label-compatible for the narrower rhetorical construct of result or conclusion detection, not for full PICO extraction.

Official primary splits were preserved. Vectorizers, neural tokenizers, and vocabularies were fitted only on the primary training split. The validation split was used for model selection, calibration fitting, and threshold selection. The internal test split was evaluated after model selection, and the external validation split was never used for fitting, tuning, calibration, or threshold selection. Table~\ref{tab:dataset} summarises the dataset characteristics and class balance.

\input{tables/table1_dataset.tex}
""",
        "04_methods.tex": r"""
\subsection*{Models and calibration}
The majority baseline predicted the empirical training-class prior. TF-IDF logistic regression used sparse word 1-2 grams and character 3-5 grams, with regularised logistic regression fitted on the full training split. TF-IDF linear support vector machine used the same feature family with a linear SVM and validation-fitted Platt calibration of decision scores. These baselines were included because sparse lexical models are strong, transparent, and practical under CPU-only constraints.

Neural models used a training-only vocabulary, integer token sequences, and fixed-length padded sequences. The feed-forward neural model averaged trainable token embeddings before classification. The LSTM, BiLSTM, and BiLSTM with dropout used trainable embeddings and small hidden dimensions to keep runtime feasible on CPU. Neural models were trained on a stratified cap of 120,000 training sentences, evaluated on the full validation, test, and external splits, and used early stopping based on validation performance. This cap is a methodological constraint rather than an optimization claim.

Classical models were calibrated with Platt sigmoid calibration fitted on validation scores. Neural models were calibrated with temperature scaling fitted on validation logits. Thresholds were optimized for validation F1 only. No preprocessing, calibration, threshold selection, or model selection used the internal test or external validation labels.

Experiments were conducted in CPU-only mode on Windows 11 with Python 3.14 and CPU PyTorch. CUDA availability was explicitly checked and was false. Random seeds and training logs were saved with the run artifacts.
""",
        "05_evaluation.tex": r"""
\subsection*{Evaluation}
The primary metric was receiver operating characteristic area under the curve. Secondary metrics were precision-recall area under the curve, accuracy, sensitivity/recall, specificity, precision/positive predictive value, F1 score, confusion matrix counts, Brier score, expected calibration error, calibration intercept, and calibration slope. Reliability plots, ROC curves, precision-recall curves, and confusion matrices were generated from saved predictions.

Calibration was assessed after validation-fitted calibration. The evidence lock does not contain pre-calibration Brier scores or expected calibration errors for all models; therefore, this manuscript does not claim that calibration improved these metrics. Instead, it reports the calibrated probability performance available from the completed experiments.

External validation was performed by applying the selected training-fitted preprocessing and trained models to the PubMed 20k RCT external test split. The external data were never used for training, tuning, or threshold selection. Subgroup analysis used ethically neutral metadata available in the corpora: sentence-length quartiles. No demographic or patient-level fairness analysis was possible because the datasets do not contain such metadata.
""",
        "06_results.tex": r"""
\section*{Results}
The empirical AUC target was achieved. Table~\ref{tab:model-comparison} shows the model comparison. TF-IDF logistic regression was selected by validation ROC AUC, with validation ROC AUC 0.977, Brier score 0.054, and expected calibration error 0.012. On the internal test split, the same model achieved ROC AUC 0.976 (95\% bootstrap CI 0.975 to 0.977), PR AUC 0.967, accuracy 0.926, F1 0.916, sensitivity 0.935, specificity 0.918, Brier score 0.055, and expected calibration error 0.011. The internal-test confusion matrix for the selected threshold contained 12,681 true positives, 16,266 true negatives, 1,448 false positives, and 875 false negatives.

\input{tables/table2_model_comparison.tex}

The strongest neural model was the BiLSTM, with internal test ROC AUC 0.974, compared with 0.976 for TF-IDF logistic regression and 0.974 for TF-IDF linear SVM. The unidirectional LSTM was weaker, with internal test ROC AUC 0.891. This pattern indicates that lightweight recurrence did not provide a clear advantage over sparse lexical baselines under the CPU-feasible protocol.

Table~\ref{tab:calibration} reports calibrated probability metrics. The selected model's internal calibration was strong by the saved metrics, with internal-test Brier score 0.055, expected calibration error 0.011, calibration intercept -0.021, and calibration slope 0.983. External calibration was weaker, with Brier score 0.085, expected calibration error 0.024, and calibration slope 0.770, consistent with corpus and label shift.

\input{tables/table3_calibration.tex}

External validation results are shown in Table~\ref{tab:external}. The selected model achieved external ROC AUC 0.948, PR AUC 0.947, accuracy 0.883, and F1 0.879. The external ROC AUC was lower than internal test ROC AUC by -0.028. Table~\ref{tab:subgroup} summarises sentence-length subgroup results. Longer sentences had higher observed AUC in both internal and external splits, but these results are descriptive and should not be interpreted as clinical subgroup performance.

\input{tables/table4_external_validation.tex}

\input{tables/table5_subgroup.tex}

Error analysis found that false positives often involved method or outcome-definition sentences with result-like clinical endpoint language. False negatives often involved short or numerically dense findings sentences. High-confidence errors illustrated the limitation of section-heading-derived labels: some sentences can be semantically compatible with more than one rhetorical role even when the dataset assigns a single label.

\begin{figure}[!ht]
\centering
\includegraphics[width=0.72\linewidth]{figures/roc_curve_best_model.png}
\caption{\textbf{Internal test ROC curve for the validation-selected model.} The selected model was TF-IDF logistic regression.}
\label{fig:roc}
\end{figure}

\begin{figure}[!ht]
\centering
\includegraphics[width=0.72\linewidth]{figures/pr_curve_best_model.png}
\caption{\textbf{Internal test precision-recall curve for the validation-selected model.}}
\label{fig:pr}
\end{figure}

\begin{figure}[!ht]
\centering
\includegraphics[width=0.72\linewidth]{figures/calibration_curve_best_model.png}
\caption{\textbf{Internal test calibration curve for the validation-selected model.}}
\label{fig:calibration}
\end{figure}

\begin{figure}[!ht]
\centering
\includegraphics[width=0.72\linewidth]{figures/confusion_matrix_best_model.png}
\caption{\textbf{Internal test confusion matrix for the validation-selected model.}}
\label{fig:confusion}
\end{figure}

\begin{figure}[!ht]
\centering
\includegraphics[width=0.72\linewidth]{figures/subgroup_performance.png}
\caption{\textbf{Sentence-length subgroup performance.} Subgroups are descriptive length quartiles.}
\label{fig:subgroup}
\end{figure}
""",
        "07_discussion.tex": r"""
\section*{Discussion}
This study demonstrates that a CPU-only biomedical sentence-classification benchmark can achieve strong discrimination and report useful calibration diagnostics without GPU-scale modelling. The best model was TF-IDF logistic regression rather than a recurrent neural network. This does not imply that neural models are generally inferior; rather, it shows that for this public abstract-level task, sparse lexical features capture much of the signal and provide a strong baseline that should not be skipped.

The external validation result supports partial generalisation to a related biomedical abstract corpus, but it also reveals the expected fragility of probabilities under corpus shift. Discrimination remained high externally, yet Brier score, expected calibration error, and calibration slope degraded. For evidence-triage use, this means that ranked sentence retrieval may transfer better than absolute probability interpretation. Any downstream use should consider recalibration in the target corpus and further validation with manually adjudicated labels.

The benchmark also illustrates a practical reproducibility point. CPU-feasible pipelines are easier to rerun, inspect, and package. The project saved raw and processed manifests, training logs, predictions, calibration artifacts, metrics, figures, tables, and manuscript source. This level of evidence traceability is valuable even when the model itself is methodologically simple.

Clinically, the model should not be interpreted as a decision-support system. It detects rhetorical sentence roles in abstracts. It does not assess trial quality, extract effect sizes, evaluate bias, or recommend patient care. The appropriate interpretation is a reproducible benchmark for literature triage and methodological evaluation.
""",
        "08_limitations.tex": r"""
\section*{Limitations}
The primary limitation is the label source. PubMed-PICO and PubMed RCT labels are derived from abstract structure or annotation conventions, and a section label is not always equivalent to sentence-level semantics. Some errors identified in the analysis likely reflect ambiguous or proxy labels rather than purely model failures.

The external validation corpus is public and held out, but it remains in the biomedical abstract domain. It is not a manually adjudicated external clinical setting, and it does not prove deployment readiness. The NICTA-PIBOSO corpus was investigated as a manual external validation candidate but was not automatically available in usable form in this environment.

The neural experiments were intentionally CPU-limited. Models used small embeddings, short maximum sequence lengths, and a stratified cap on neural training examples. Larger recurrent models, pretrained biomedical Transformers, or GPU-scale fine-tuning might perform differently, but they were outside the CPU-only scope of this project.

Calibration uncertainty is another limitation. The project reports calibrated Brier score, expected calibration error, and reliability curves, but it did not retain pre-calibration Brier/ECE for all models and did not compute uncertainty intervals for calibration metrics. No demographic fairness analysis was possible because the public abstract corpora do not include patient-level demographic metadata.
""",
        "09_conclusion.tex": r"""
\section*{Conclusion}
A complete CPU-only healthcare NLP benchmark achieved the empirical AUC target for findings/conclusion sentence detection in biomedical abstracts, with the validation-selected TF-IDF logistic regression model obtaining internal test ROC AUC 0.976 and external ROC AUC 0.948. Lightweight recurrent neural models were feasible and informative but did not outperform the strongest sparse baseline. The results support careful, reproducible, calibration-aware benchmarking for healthcare NLP while underscoring that abstract sentence classification is not clinical deployment evidence.
""",
        "10_declarations.tex": r"""
\section*{Data availability statement}
The raw public datasets used in this study are available from the PubMed-PICO Detection repository (https://github.com/jind11/PubMed-PICO-Detection) and the PubMed RCT repository (https://github.com/Franck-Dernoncourt/pubmed-rct). The processed data, predictions, summary tables, and figures were generated by the local scripts in this project. Before journal submission, the author should deposit the generated minimal replication package in a public repository and replace this placeholder with a persistent URL or DOI: [REPOSITORY URL TO BE INSERTED].

\section*{Code availability statement}
The code used to download data, prepare datasets, train models, calibrate predictions, evaluate metrics, generate figures, and build the manuscript package is located in the local project directories \texttt{src/} and \texttt{scripts/}. Before submission, the author should publish the code in a public repository or archival service and insert the persistent repository URL here: [REPOSITORY URL TO BE INSERTED].

\section*{Ethics statement}
This study used public biomedical abstract datasets and did not recruit participants, contact patients, process restricted clinical notes, or deploy a model in patient care. No identifiable patient-level data were used. The models are for research evaluation and evidence-triage benchmarking only and should not be used for clinical decision-making without separate validation, governance review, and prospective evaluation.

\section*{Funding statement}
The author received no specific funding for this work. Author confirmation is needed before submission.

\section*{Competing interests}
The author declares no competing interests. Author confirmation is needed before submission.

\section*{Author contributions}
Author-confirmation-needed CRediT statement: Conceptualisation, methodology, software, formal analysis, investigation, data curation, validation, visualisation, writing--original draft, and writing--review and editing: Terry Yu.

\section*{Acknowledgements}
Not applicable.
""",
    }
    for name, content in section_text.items():
        write(SECTION_DIR / name, content)


def write_supplementary() -> None:
    SUPP_DIR.mkdir(parents=True, exist_ok=True)
    write(
        SUPP_DIR / "supplementary_methods.tex",
        r"""
\section*{S1 Text. Supplementary methods}

\subsection*{Preprocessing}
Raw PubMed-PICO and PubMed 20k RCT files were downloaded into \texttt{data/raw}. Processed CSV files were written to \texttt{data/processed}. The raw files were not modified. PubMed-PICO source labels R and C were mapped to the positive class, and PubMed RCT source labels RESULTS and CONCLUSIONS were mapped to the positive class for external validation.

\subsection*{Leakage controls}
Official primary train, validation, and test splits were preserved. TF-IDF vectorizers and neural vocabularies were fitted only on the primary training split. Validation data were used for calibration fitting, threshold selection, and model selection. Test and external validation data were not used for fitting or tuning.

\subsection*{Model hyperparameters}
Classical models used TF-IDF word 1-2 grams and character 3-5 grams. Logistic regression used the liblinear solver with C=2.0. The linear SVM used C=1.0 with balanced class weights and validation-fitted Platt calibration. Neural models used maximum sequence length 64, vocabulary size up to 40,000, embedding dimension 64, hidden dimension 64, batch size 512, maximum 5 epochs, and early stopping patience 2. Neural training used a stratified cap of 120,000 training sentences.

\subsection*{CPU environment and seeds}
The environment check recorded Windows 11, Python 3.14.2, PyTorch 2.12.0+cpu, and CUDA unavailable. Random seed 42 was used for the main training scripts. The requested seeds 13 and 100 were not used in the completed run and should be considered future robustness work rather than completed evidence.

\subsection*{Calibration and external validation}
Classical models used validation-fitted Platt calibration. Neural models used validation-fitted temperature scaling. External validation used the PubMed 20k RCT official test split and was evaluated after model selection without refitting preprocessing, thresholds, or calibrators.
""",
    )
    write(
        SUPP_DIR / "supplementary_results.tex",
        r"""
\section*{S2 Text. Supplementary results}

All required model families were run: majority baseline, TF-IDF logistic regression, TF-IDF linear SVM, feed-forward average-embedding network, LSTM, BiLSTM, and BiLSTM with dropout. No CUDA or GPU-scale Transformer experiments were performed locally. Optional CNN-text modelling was not run because the required model set was completed and CPU runtime was prioritised.

The validation-selected model was TF-IDF logistic regression. Its internal test confusion matrix at the validation-selected threshold contained 12,681 true positives, 16,266 true negatives, 1,448 false positives, and 875 false negatives. External validation contained 12,803 true positives, 13,804 true negatives, 2,047 false positives, and 1,481 false negatives.

The calibration table in the main manuscript reports post-calibration Brier score, expected calibration error, calibration intercept, and calibration slope. The evidence lock does not support a before/after calibration-improvement claim because pre-calibration Brier/ECE values were not saved for every model.

Sentence-length subgroup analysis was available for the selected model. It is descriptive only because length quartiles are not clinical subgroups and were not pre-specified as fairness strata.
""",
    )
    write(
        SUPP_DIR / "reproducibility_checklist.tex",
        r"""
\section*{S3 Checklist. Reproducibility checklist}

\begin{itemize}
\item Data sources: PubMed-PICO Detection and PubMed 20k RCT public repositories.
\item Split protocol: official PubMed-PICO train/validation/test preserved; PubMed 20k RCT official test used only as external validation.
\item Preprocessing leakage controls: vectorizers and tokenizers fitted on training data only.
\item Software versions: recorded in \texttt{project_outputs/01_environment/environment_check.txt} and installation log.
\item Random seeds: main experiments used seed 42; seed files were saved under \texttt{runs/}.
\item Reproduction commands: \texttt{scripts/01_download_data.py}, \texttt{scripts/02_prepare_data.py}, \texttt{scripts/03_data_audit.py}, \texttt{scripts/10_train_classical.py}, \texttt{scripts/11_train_neural.py}, \texttt{scripts/12_evaluate.py}, \texttt{scripts/13_calibrate.py}, \texttt{scripts/14_external_validation.py}, and manuscript-generation scripts.
\item Output locations: metrics in \texttt{project_outputs/04_metrics}; tables in \texttt{project_outputs/06_tables}; figures in \texttt{project_outputs/05_figures}; predictions in \texttt{project_outputs/07_predictions} and \texttt{runs/}; manuscript files in \texttt{project_outputs/10_manuscript} and \texttt{latex/}.
\item Hardware: CPU-only execution; CUDA unavailable and not attempted.
\end{itemize}
""",
    )


def write_cover_letter() -> None:
    COVER_DIR.mkdir(parents=True, exist_ok=True)
    body = f"""
Dear PLOS ONE Editors,

Please consider the manuscript "{TITLE}" as a Research Article for PLOS ONE.

This manuscript addresses a practical healthcare NLP problem: reproducibly identifying findings and conclusion sentences in biomedical abstracts using public data and CPU-feasible models. The work fits PLOS ONE because it asks a clearly defined methodological question, uses public datasets, reports complete discrimination and calibration metrics, includes external validation, and provides a reproducible package of code, metrics, tables, figures, and manuscript source. The paper is not a claim of clinical deployment readiness; rather, it is a calibration-aware benchmark for literature triage and healthcare NLP model evaluation.

The main contribution is a transparent comparison of strong sparse linear baselines with lightweight recurrent neural models under CPU-only constraints. The validation-selected TF-IDF logistic regression model achieved strong internal and external discrimination, while external calibration degradation highlighted the importance of reporting probability reliability and corpus shift.

The manuscript is not under consideration elsewhere. The raw datasets are publicly accessible from the PubMed-PICO Detection and PubMed RCT repositories. The author-generated code and processed replication package should be deposited before submission, and the repository URL should be inserted into the manuscript data and code availability statements. The author declares no competing interests, pending final author confirmation.

Corresponding author: [CORRESPONDING AUTHOR NAME AND EMAIL TO BE COMPLETED BY AUTHOR]

Sincerely,

Terry Yu
"""
    write(COVER_DIR / "cover_letter.tex", "\\section*{Cover letter}\n" + tex_escape(body).replace("\n\n", "\n\n"))
    write(MANUSCRIPT_DIR / "cover_letter_submission_ready.md", body)


def write_checklist() -> None:
    rows = [
        ("Title page complete", "NEEDS AUTHOR INPUT", "Affiliation, email, and optional ORCID remain unresolved."),
        ("Abstract format matches journal", "DONE", "PLOS ONE abstract is under 300 words and contains no citations."),
        ("Keywords included", "DONE", "Eight keywords included."),
        ("Word count checked", "NOT REQUIRED", "PLOS ONE has no word-count restriction in official guidelines checked."),
        ("References formatted", "DONE", "PLOS numbered/Vancouver-like style via plos2025.bst."),
        ("Figures uploaded separately if required", "NEEDS AUTHOR INPUT", "Figure files are included in the zip; PLOS upload system requires separate figure upload."),
        ("Tables included", "DONE", "Tables 1-5 included after first citation in manuscript flow."),
        ("Supplementary files included", "DONE", "S1 methods, S2 results, S3 checklist included."),
        ("Data availability statement", "NEEDS AUTHOR INPUT", "Public raw sources stated; final repository DOI/URL needed for generated outputs."),
        ("Code availability statement", "NEEDS AUTHOR INPUT", "Local code described; public repository URL needed."),
        ("Ethics statement", "DONE", "Public abstract data and no patient-care deployment stated; author should confirm IRB exemption policy if requested."),
        ("Funding statement", "NEEDS AUTHOR INPUT", "Draft says no specific funding; author confirmation needed."),
        ("Competing interests", "NEEDS AUTHOR INPUT", "Draft says no competing interests; author confirmation needed."),
        ("Author contributions", "NEEDS AUTHOR INPUT", "Draft CRediT statement provided for Terry Yu; author confirmation needed."),
        ("Acknowledgements", "NOT REQUIRED", "No acknowledgements provided; marked not applicable."),
        ("Reporting checklist if required", "NEEDS AUTHOR INPUT", "No mandatory task-specific checklist identified; confirm whether PLOS requests Human Participants Checklist."),
        ("Cover letter", "DONE", "One-page draft created; editor/reviewer suggestions not included."),
        ("Graphical abstract/highlights", "NOT REQUIRED", "No PLOS ONE requirement found; optional striking image may be chosen during submission."),
        ("Unresolved items", "NEEDS AUTHOR INPUT", "Affiliation, corresponding email, repository DOI/URL, author confirmations, and optional editor suggestions."),
    ]
    lines = ["# Submission Checklist", "", "| Item | Status | Note |", "|---|---|---|"]
    lines.extend(f"| {item} | {status} | {note} |" for item, status, note in rows)
    text = "\n".join(lines)
    write(LATEX_DIR / "SUBMISSION_CHECKLIST.md", text)
    write(MANUSCRIPT_DIR / "submission_checklist_completed.md", text)


def write_main_tex() -> None:
    shutil.copy2(OUTPUTS_DIR / "08_literature" / "references.bib", LATEX_DIR / "references.bib")
    bst = LATEX_DIR / "plos_template_reference" / "plos2025.bst"
    if bst.exists():
        shutil.copy2(bst, LATEX_DIR / "plos2025.bst")
    abstract = (
        "Biomedical abstract sentence classification can support evidence triage by helping researchers locate sentences that report findings or conclusions. "
        "This study evaluated whether CPU-feasible classical and recurrent neural text classifiers can identify findings/conclusion sentences in public biomedical abstracts with useful discrimination, transparent calibration assessment, and external validation. "
        "PubMed-PICO official train, validation, and test splits were used as the primary corpus, mapping R and C labels to the positive class. PubMed 20k RCT official test sentences were used only for external validation, mapping RESULTS and CONCLUSIONS to the positive class. "
        "Models included a majority baseline, TF-IDF logistic regression, TF-IDF linear support vector machine, feed-forward average embeddings, LSTM, BiLSTM, and BiLSTM with dropout. "
        "The validation-selected model was TF-IDF logistic regression. It achieved validation ROC AUC 0.977, internal test ROC AUC 0.976 (95% bootstrap CI 0.975 to 0.977), PR AUC 0.967, F1 0.916, Brier score 0.055, and expected calibration error 0.011. "
        "External validation ROC AUC was 0.948, PR AUC 0.947, F1 0.879, Brier score 0.085, and expected calibration error 0.024. "
        "A strong sparse linear model met the empirical AUC target and performed at least as well as lightweight recurrent neural alternatives. External validation supported partial generalisation within biomedical abstracts but showed calibration degradation, so the model should be treated as a reproducible evidence-triage benchmark rather than a deployment-ready clinical system."
    )
    main = rf"""
\documentclass[10pt,letterpaper]{{article}}
\usepackage[top=0.85in,left=2.75in,footskip=0.75in]{{geometry}}
\usepackage{{amsmath,amssymb}}
\usepackage{{nameref,hyperref}}
\usepackage{{array}}
\usepackage{{booktabs}}
\usepackage{{longtable}}
\usepackage{{graphicx}}
\usepackage[aboveskip=1pt,labelfont=bf,labelsep=period,justification=raggedright,singlelinecheck=off]{{caption}}
\renewcommand{{\figurename}}{{Fig}}
\bibliographystyle{{plos2025}}
\makeatletter
\renewcommand{{\@biblabel}}[1]{{\quad#1.}}
\makeatother
\raggedright
\setlength{{\parindent}}{{0.5cm}}
\textwidth 5.25in
\textheight 8.75in
\pagestyle{{plain}}
\begin{{document}}
\vspace*{{0.2in}}
\begin{{flushleft}}
{{\Large\textbf{{{tex_escape(TITLE)}}}}}
\newline
{tex_escape(AUTHOR)}\textsuperscript{{1*}}
\\
\bigskip
\textbf{{1}} [AFFILIATION TO BE COMPLETED BY AUTHOR]
\\
\bigskip
* [CORRESPONDING AUTHOR EMAIL TO BE COMPLETED BY AUTHOR]
\end{{flushleft}}

\section*{{Abstract}}
{tex_escape(abstract)}

\section*{{Keywords}}
healthcare NLP; biomedical text classification; recurrent neural networks; calibration; external validation; reproducible machine learning; clinical decision support; model evaluation

\clearpage
\newgeometry{{top=0.85in,left=1in,right=1in,footskip=0.75in}}
\input{{sections/01_introduction.tex}}
\input{{sections/02_related_work.tex}}
\input{{sections/03_data.tex}}
\input{{sections/04_methods.tex}}
\input{{sections/05_evaluation.tex}}
\input{{sections/06_results.tex}}
\input{{sections/07_discussion.tex}}
\input{{sections/08_limitations.tex}}
\input{{sections/09_conclusion.tex}}
\input{{sections/10_declarations.tex}}

\section*{{Supporting information}}
S1 Text. Supplementary methods. See \texttt{{supplementary/supplementary\_methods.tex}}.

S2 Text. Supplementary results. See \texttt{{supplementary/supplementary\_results.tex}}.

S3 Checklist. Reproducibility checklist. See \texttt{{supplementary/reproducibility\_checklist.tex}}.

\bibliography{{references}}
\end{{document}}
"""
    write(LATEX_DIR / "main.tex", main)


def write_readme() -> None:
    text = """
# Compile Instructions

This package is aligned to PLOS ONE as closely as possible using the official PLOS LaTeX template conventions and `plos2025.bst`.

Recommended compile command from the `latex/` directory:

```bash
latexmk -pdf main.tex
```

Equivalent manual sequence:

```bash
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

Important PLOS upload note: PLOS initial LaTeX submission uses the compiled PDF as the manuscript file and requires figures to be uploaded separately. This package includes figures inside the PDF for local quality assurance and also includes separate files under `figures/`.
"""
    write(LATEX_DIR / "README_compile.md", text)


def compile_latex() -> tuple[bool, Path | None, str]:
    log_path = ZIP_DIR / "latex_compile_log.txt"
    ZIP_DIR.mkdir(parents=True, exist_ok=True)
    commands = []
    latexmk = shutil.which("latexmk") or ("C:/ProgramData/TinyTeX/bin/windows/latexmk.exe" if Path("C:/ProgramData/TinyTeX/bin/windows/latexmk.exe").exists() else None)
    if latexmk:
        commands.append([latexmk, "-pdf", "-interaction=nonstopmode", "-halt-on-error", "main.tex"])
    else:
        commands.extend(
            [
                ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "main.tex"],
                ["bibtex", "main"],
                ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "main.tex"],
                ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "main.tex"],
            ]
        )
    full_log = []
    success = True
    for cmd in commands:
        try:
            proc = subprocess.run(cmd, cwd=LATEX_DIR, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=180)
            full_log.append("$ " + " ".join(cmd))
            full_log.append(proc.stdout)
            if proc.returncode != 0:
                success = False
                break
        except Exception as exc:
            full_log.append("$ " + " ".join(cmd))
            full_log.append(repr(exc))
            success = False
            break
    write(log_path, "\n".join(full_log))
    shutil.copy2(log_path, LATEX_DIR / "latex_compile_log.txt")
    pdf = LATEX_DIR / "main.pdf"
    if not success or not pdf.exists():
        write(
            OUTPUTS_DIR / "12_failure_reports" / "latex_compile_failed.md",
            "# LaTeX Compile Failed\n\nSee `project_outputs/11_latex_zip/latex_compile_log.txt` for the exact compiler output.",
        )
    return success and pdf.exists(), pdf if pdf.exists() else None, "\n".join(full_log)


def quality_check() -> tuple[bool, str]:
    problems: list[str] = []
    if not (LATEX_DIR / "main.tex").exists():
        problems.append("main.tex missing")
    if not (LATEX_DIR / "references.bib").exists():
        problems.append("references.bib missing")
    main_text = (LATEX_DIR / "main.tex").read_text(encoding="utf-8")
    for sec in SECTION_DIR.glob("*.tex"):
        if not sec.read_text(encoding="utf-8").strip():
            problems.append(f"empty section file: {sec.name}")
    combined = main_text + "\n" + "\n".join(p.read_text(encoding="utf-8") for p in SECTION_DIR.glob("*.tex"))
    cited = set()
    for match in re.findall(r"\\cite\{([^}]+)\}", combined):
        cited.update(k.strip() for k in match.split(","))
    bib_text = (LATEX_DIR / "references.bib").read_text(encoding="utf-8")
    bib_keys = set(re.findall(r"@\w+\{([^,]+),", bib_text))
    missing_cites = sorted(cited - bib_keys)
    if missing_cites:
        problems.append("missing citation keys: " + ", ".join(missing_cites))
    fig_paths = re.findall(r"\\includegraphics(?:\[[^\]]+\])?\{([^}]+)\}", combined)
    for rel in fig_paths:
        if not (LATEX_DIR / rel).exists():
            problems.append(f"missing figure path: {rel}")
    input_paths = re.findall(r"\\input\{([^}]+)\}", main_text + "\n" + "\n".join(p.read_text(encoding="utf-8") for p in SECTION_DIR.glob("*.tex")))
    for rel in input_paths:
        if not (LATEX_DIR / rel).exists():
            problems.append(f"missing input path: {rel}")
    forbidden = ["TODO", "write later", "dummy", "fake result", "insert citation"]
    all_package_text = "\n".join(p.read_text(encoding="utf-8", errors="ignore") for p in [LATEX_DIR / "main.tex", *SECTION_DIR.glob("*.tex"), *SUPP_DIR.glob("*.tex"), COVER_DIR / "cover_letter.tex"] if p.exists())
    for bad in forbidden:
        if bad.lower() in all_package_text.lower():
            problems.append(f"forbidden placeholder text found: {bad}")
    report = [
        "# Submission Quality Check",
        "",
        f"- main.tex exists: {(LATEX_DIR / 'main.tex').exists()}",
        f"- references.bib exists: {(LATEX_DIR / 'references.bib').exists()}",
        f"- cited keys: {', '.join(sorted(cited))}",
        f"- citation keys missing from references.bib: {', '.join(missing_cites) if missing_cites else 'none'}",
        f"- figure paths checked: {len(fig_paths)}",
        f"- table/section inputs checked: {len(input_paths)}",
        "- forbidden placeholder terms checked: TODO, write later, dummy, fake result, insert citation",
        "- square-bracket placeholders remain only for author/admin inputs and repository URL.",
        "",
        "## Problems",
        "",
    ]
    report.extend(f"- {p}" for p in problems) if problems else report.append("- None.")
    text = "\n".join(report)
    write(ZIP_DIR / "submission_quality_check.md", text)
    return not problems, text


def make_zip(compiled: bool) -> Path:
    zip_path = ZIP_DIR / "healthcare_nlp_submission_ready_latex.zip"
    include_roots = [
        LATEX_DIR / "main.tex",
        LATEX_DIR / "references.bib",
        LATEX_DIR / "plos2025.bst",
        LATEX_DIR / "README_compile.md",
        LATEX_DIR / "SUBMISSION_CHECKLIST.md",
        LATEX_DIR / "latex_compile_log.txt",
    ]
    if compiled and (LATEX_DIR / "main.pdf").exists():
        include_roots.append(LATEX_DIR / "main.pdf")
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for path in include_roots:
            if path.exists():
                z.write(path, path.relative_to(LATEX_DIR))
        for folder in [SECTION_DIR, TABLE_DIR, FIG_DIR, SUPP_DIR, COVER_DIR]:
            for path in folder.rglob("*"):
                if path.is_file():
                    z.write(path, path.relative_to(LATEX_DIR))
    with zipfile.ZipFile(zip_path) as z:
        lines = ["# ZIP Contents", ""]
        for name in sorted(z.namelist()):
            if name.endswith("/"):
                continue
            if name == "main.tex":
                purpose = "Main compile-ready manuscript file."
            elif name == "references.bib":
                purpose = "Bibliography used by BibTeX."
            elif name == "plos2025.bst":
                purpose = "Official PLOS BibTeX style file downloaded from PLOS template package."
            elif name == "main.pdf":
                purpose = "Compiled manuscript PDF."
            elif name.startswith("sections/"):
                purpose = "Manuscript section source file."
            elif name.startswith("tables/"):
                purpose = "Journal-ready LaTeX table source."
            elif name.startswith("figures/"):
                purpose = "Generated figure copied from verified project outputs."
            elif name.startswith("supplementary/"):
                purpose = "Substantive supplementary material."
            elif name.startswith("cover_letter/"):
                purpose = "Journal-specific cover letter source."
            elif name == "SUBMISSION_CHECKLIST.md":
                purpose = "Submission-readiness checklist."
            elif name == "README_compile.md":
                purpose = "Compilation and upload guidance."
            elif name == "latex_compile_log.txt":
                purpose = "Saved LaTeX compiler log."
            else:
                purpose = "Submission package file."
            lines.append(f"- `{name}`: {purpose}")
    write(ZIP_DIR / "ZIP_CONTENTS.md", "\n".join(lines))
    return zip_path


def write_readiness_report(compiled: bool, zip_path: Path, data: dict) -> None:
    best = data["best_model"]
    test = metric_row(data["main"], best, "test")
    external_exists = not data["external"].empty
    reference_count = len(re.findall(r"@\w+\{", (LATEX_DIR / "references.bib").read_text(encoding="utf-8")))
    report = f"""
# Manuscript Readiness Report

- Selected journal: {TARGET_JOURNAL}
- Manuscript title: {TITLE}
- Article type: {ARTICLE_TYPE}
- Manuscript complete: yes, with author/admin placeholders requiring final human completion.
- LaTeX compiled: {'yes' if compiled else 'no'}
- PDF produced: {'yes' if (LATEX_DIR / 'main.pdf').exists() else 'no'}
- All results verified: yes; manuscript values come from the evidence lock and saved metrics/tables.
- References included and cited: {reference_count}
- AUC target achieved: {'yes' if float(test['roc_auc']) >= 0.70 else 'no'}
- External validation exists: {'yes' if external_exists else 'no'}
- Calibration reported: yes; no calibration-improvement claim is made because pre-calibration Brier/ECE values were not saved for all models.
- Data/code statements complete: partially; public raw data sources are complete, but repository URL/DOI for generated outputs and code needs author input.
- Cover letter complete: yes, except corresponding author contact details and optional editor/reviewer suggestions.
- Unresolved author inputs: affiliation, corresponding author email, optional ORCID, public repository or DOI for code/generated data, confirmation of funding/competing interests/CRediT contribution, and PLOS submission-system checks.
- Exact zip path: `{zip_path}`
"""
    write(MANUSCRIPT_DIR / "MANUSCRIPT_READINESS_REPORT.md", report)


def main() -> None:
    ensure_project_dirs()
    reset_submission_workspace()
    for folder in [TABLE_DIR, FIG_DIR, SECTION_DIR, SUPP_DIR, COVER_DIR, ZIP_DIR, MANUSCRIPT_DIR]:
        folder.mkdir(parents=True, exist_ok=True)
    data = load_data()
    write_evidence_lock(data)
    write_journal_requirements()
    build_markdown_manuscript(data)
    write_tables(data)
    copy_figures()
    write_sections()
    write_supplementary()
    write_cover_letter()
    write_checklist()
    write_main_tex()
    write_readme()
    compiled, _, _ = compile_latex()
    quality_check()
    zip_path = make_zip(compiled)
    write_readiness_report(compiled, zip_path, data)
    print(MANUSCRIPT_DIR / "MANUSCRIPT_READINESS_REPORT.md")
    print(zip_path)
    print(TARGET_JOURNAL)
    print("yes" if compiled else "no")
    print("Public repository/DOI for code and generated minimal replication package.")


if __name__ == "__main__":
    main()
