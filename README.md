# proj-hampshirehope
Repo containing source code and resources for creating heat-maps in the Hampshire/Hampden counties of Massachusetts.

The overall goal of the project is to create heat-maps that let us visualize the disparities in transportation equality to opioid-related treatment resources.

---

## Requirements

- `python >= 3`

## Dependencies

- `numpy`
- `pandas`
- `matplotlib`
- `requests-html`
- `PyPDF2`
- `tabula-py` (Requires Java)
- `pdfplumber`
- `googlemaps`

To install dependencies, run 

```bash
$ pip install -r requirements.txt
```

in the `proj-hampshirehope` directory.

---

## Workflow

1. In the `geocoded` directory, run `hospitals.py`, then `points.py`, and finally `filter_towns.py`. These have already been run, but feel free to rerun these scripts if you want to change the origins.
   - These scripts dump the hospitals to a csv, obtain the raw points, and then filter the points to those in towns of interest respectively.
2. In the `google` directory, run `towns_of_interest.py`.
3. In the same directory, follow the instructions in `README.md` to finish setup for `heatmap.ipynb`. 
   - The notebook has been run for all treatment types, which ultimately outputs html files for the embedded heatmaps. Every html file needs an `API_KEY` from Google Cloud Platform (each html file should have `API_KEY_HERE` which should be replaced). Details for setup are in `README.md` in the `google` directory.

---

## Extraneous Files

All other files except in the `facilities`, `geocoded`, and `google` directories are not used (`hh_resources` is used but a substantial amount of manual labor was necessary). They can be used for future projects or can be completely disregarded. These files include parsing PVTA infopoint data, PVTA schedule info, public opioid data statistics for MA, etc.
