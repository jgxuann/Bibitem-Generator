# Bibitem-Generator

## Overview
The **Bibitem-Generator** is a Python-based tool designed to process BibTeX references and convert them into a standardized `\bibitem` format. The tool automates the process of organizing references, searching for missing DOIs, and formatting them into a final, clean output.

This repository contains four main scripts that should be executed in sequence to achieve the desired output. Each script performs a specific task in the pipeline, as described below.

---

## Workflow

### 1. `rank_by_author.py`
This script processes the input file `reference.txt` and organizes the BibTeX entries by author. The output is saved as `1.0.txt`.

- **Input**: `reference.txt` (replace the path with your own file)
- **Output**: `1.0.txt`

**How to run**:
```bash
python rank_by_author.py
```
### 2. `search_doi.py`
This script takes `1.0.txt` as input and searches for missing DOIs using external APIs (e.g., CrossRef). It appends the missing DOIs to the corresponding BibTeX entries and saves the updated references as `2.0.txt`.

- **Input**: `1.0.txt` (replace the path with your own file)
- **Output**: `2.0.txt`
**How to run**:
```bash
python search_doi.py
```

