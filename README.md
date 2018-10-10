## Instructions
- Install `pandas`, `openpyxl` and `scrapy`
- Run crawler -> Run Preprocess Script

1. Running crawler
```
user@dhs$ scrapy crawl general -o results.csv -t csv
```
This will start crawler and dumps results in `results.csv` file.

2. Run `preprocess.py` script.
- This willl load `results.csv` file and provides `OregonFacilities.xslx` file

## Note
- I have explicitly set pages to 330. 
- This behaviour can be controlled using `PAGES` variable on `general.py` file
