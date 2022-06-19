# Description

Command line utility to search and download wordlists from online websites

# Installation

## Option 1 --Git
```
git clone https://github.com/chessrajat/wordlistcli
python setup.py install
```

## Option 2 --pip
```
pip install wordlistcli
```

# Usage

```
usage: wordlistcli [-h] [-v] {get,search} ...

Search and Download wordlists from online archives

positional arguments:
  {get,search}
    get          Download wordlists
    search       Search wordlists
    

optional arguments:
  -h, --help     show this help message and exit
  -v, --version  Show the current version of tool
```

### Search
```
usage: wordlistcli search [-h] [-g] search_term

positional arguments:
  search_term  What to search

optional arguments:
  -h, --help   show this help message and exit
  -g, --group  Search in group category instead of file name example: discovery, fuzzing
```

### GET
```
usage: wordlistcli get [-h] [-d] file_name destination

positional arguments:
  file_name         File name of the wordlist to download
  destination       File path where you want to store the downloaded wordlist

optional arguments:
  -h, --help        show this help message and exit
  -d, --decompress  Decompress the wordlist after download
```

## Examples
```
>> wordlistcli search rockyou
--==[ wordlistcli by Drag0 ]==--

    0 > rockyou-05 (104.00 B)
    1 > rockyou-10 (723.00 B)
    2 > rockyou-15 (1.94 Kb)
    3 > rockyou-20 (4.00 Kb)
    4 > rockyou-25 (7.23 Kb)
    5 > rockyou-30 (12.16 Kb)
    6 > rockyou-35 (19.65 Kb)
    7 > rockyou-40 (31.22 Kb)
    8 > rockyou-45 (49.13 Kb)
    9 > rockyou-50 (75.91 Kb)
    10 > rockyou-55 (115.19 Kb)
    11 > rockyou-60 (170.24 Kb)
    12 > rockyou-65 (244.53 Kb)
    13 > rockyou-70 (344.23 Kb)
    14 > rockyou-75 (478.95 Kb)
    15 > rockyou-withcount (56.02 Mb)
    16 > rockyou (53.29 Mb)
    17 > rockyou-5 (104 B)
```
```
>> wordlistcli get rockyou . -d
--==[ wordlistcli by Drag0 ]==--

[*] downloading D:\wordlistcli\rockyou.txt.tar.gz to D:\wordlistcli\rockyou.txt.tar.gz.part
Downloading... : 52043it [00:05, 9490.31it/s]
[+] Download completed: D:\wordlistcli\rockyou.txt.tar.gz
[*] decompressing D:\wordlistcli\rockyou.txt.tar.gz
[+] decompressing rockyou.txt.tar.gz completed
```

## Contribute

Include more Latest or custom made wordlists

**Issues** : https://github.com/chessrajat/wordlistcli/issues


