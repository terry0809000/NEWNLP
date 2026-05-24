# Journal Submission Requirements Extracted

Selected journal: PLOS ONE.

Publisher: Public Library of Science (PLOS).

Date accessed: 2026-05-24.

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
