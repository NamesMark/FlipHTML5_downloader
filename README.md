## FlipHTML5 donwloader

Downloads all books from a given [FlipHTML5](https://fliphtml5.com) bookcase.

## Usage

The books are saved as PDF in `../downloads`.

```bash
python src/main.py https://fliphtml5.com/bookcase/<BOOKCASE_ID>
```

### On Windows
```shell
.\flip_download https://fliphtml5.com/bookcase/<BOOKCASE_ID>
```

### On Linux
```shell
./flip_download.sh https://fliphtml5.com/bookcase/<BOOKCASE_ID>
```

## Python requirements

- os
- sys
- requests
- json
- csv
- html
- re
- time
- bs4
- selenium
- webdriver_manager
