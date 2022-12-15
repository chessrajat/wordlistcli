import argparse
import gzip
import tarfile
import time
import json
import os
import sys
from shutil import copyfileobj
from tqdm import tqdm


try:
    import requests
    from termcolor import colored
except Exception as ex:
    print(f"[-] {ex}", file=sys.stderr)
    sys.exit(-1)


__Author__: str = "Drag0"
__version__: str = "v0.1.1"
__project__: str = "wordlistcli"
__description__: str = "Search and Download wordlists from online archives"


def banner():
    print(colored(f"--==[ {__project__} by {__Author__} ]==--\n",
                  "red", attrs=["bold"]))

def error(string: str) -> None:
    print(colored("[-]", "red", attrs=["bold"]) +
          f" {string}", file=sys.stderr)


def warning(string: str) -> None:
    print(colored("[!]", "yellow", attrs=["bold"]) + f" {string}")


def info(string: str) -> None:
    print(colored("[*]", "blue", attrs=["bold"]) + f" {string}")


def success(string: str) -> None:
    print(colored("[+]", "green", attrs=["bold"]) + f" {string}")

def load_repo():
    global REPOSITORY
    repofile: str = os.path.join(os.path.dirname(os.path.realpath(__file__)), "source.json")
    try:
        if not os.path.isfile(repofile):
            raise FileNotFoundError("repository file not found")
        with open(repofile, "r") as f:
            REPOSITORY = json.load(f)
    except Exception as ex:
        error(f"Error while loading repository: {str(ex)}")
        exit(-1)


def decompress_file(infilename: str) -> None:
    filename: str = os.path.basename(infilename).lower()
    try:
        info(f"decompressing {infilename}")
        if filename.endswith(".tar.gz"):
            with tarfile.open(infilename) as f:
                tar: tarfile.TarFile = f
                def is_within_directory(directory, target):
                    
                    abs_directory = os.path.abspath(directory)
                    abs_target = os.path.abspath(target)
                
                    prefix = os.path.commonprefix([abs_directory, abs_target])
                    
                    return prefix == abs_directory
                
                def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
                
                    for member in tar.getmembers():
                        member_path = os.path.join(path, member.name)
                        if not is_within_directory(path, member_path):
                            raise Exception("Attempted Path Traversal in Tar File")
                
                    tar.extractall(path, members, numeric_owner=numeric_owner) 
                    
                
                safe_extract(tar, os.path.dirname(infilename))
        elif filename.endswith(".gz"):
            gf: gzip.GzipFile = gzip.GzipFile(infilename)
            outfile = open(infilename.split(".gz")[0], "wb")
            copyfileobj(gf, outfile)
            outfile.close()
            gf.close()
        else:
            warning(f"decompressing {infilename.split('.')[-1]} file type not supported")
            return
        success(f"decompressing {filename} completed")
        os.remove(infilename)
    except Exception as ex:
        error(f"Unable to decompress {infilename}: {ex}")
    

def download_file(file_url, destination, is_decompress):
    headers = {"User-Agent": f"{__Author__}  {__version__}"}
    partpath: str = f'{destination}.part'
    try:
        if os.path.isfile(destination):
            warning(f"{destination} already exists -- skipping")
        else:
            if os.path.isfile(partpath):
                info(f"Found Part file : {partpath}")
                info(f"resume downloading {destination} to {partpath}")
                size: int = os.stat(partpath).st_size
                headers["Range"] = f'bytes={size}-'
            else:
                info(f"downloading {destination} to {partpath}")
            for _ in range(5):
                rq: requests.Response = requests.get(file_url, stream=True, headers=headers)
                if rq.status_code == 404:
                    raise FileNotFoundError("host returned 404")
                elif rq.status_code not in [200, 206]:
                    time.sleep(5)
                    continue
                mode: str = "ab" if rq.status_code == 206 else "wb"
                with open(partpath, mode) as fp:
                    for data in tqdm(rq.iter_content(chunk_size=1024), desc="Downloading... "):
                        fp.write(data)
                os.rename(partpath, destination)
                success(f"Download completed: {destination}")
                break
        if is_decompress:
            decompress_file(destination)
    except KeyboardInterrupt:
        return
    except Exception as ex:
        error(f"Error while downloading {destination}: {ex}")


def download_wordlist(args):
    file_name = args.file_name
    destination = args.destination
    decompress = args.decompress

    if file_name is not None:
        if file_name in REPOSITORY.keys():
            file_url = REPOSITORY[file_name]["url"]
            file_name = file_url.split("/")[-1]
            file_destination = os.path.join(os.path.abspath(destination), file_name)
            download_file(file_url, file_destination, decompress)
        else:
            error(f"{file_name} not found, Please spell check or search for keyword again.")

    

def search_wordlist(args):
    global SEARCH_RESULTS
    search_term = args.search_term
    count = 0
    SEARCH_RESULTS = []
    is_group = args.group
    try:
        if is_group:
            info("searching in group...")
            for wordlist in REPOSITORY:
                group = REPOSITORY[wordlist]["group"]
                if group.lower().__contains__(search_term.lower()):
                    size = REPOSITORY[wordlist]["size"]
                    print(f"    {count} > {wordlist} ({size})")
                    count += 1
                    SEARCH_RESULTS.append(wordlist)
            if count == 0:
                error("no wordlists found")
            return

        for wordlist in REPOSITORY:
            if wordlist.lower().__contains__(search_term.lower()):
                size = REPOSITORY[wordlist]["size"]
                print(f"    {count} > {wordlist} ({size})")
                count += 1
                SEARCH_RESULTS.append(wordlist)      

        if count == 0:
            error("no wordlists found")
    except Exception as ex:
        error(str(ex))


def main():
    banner()
    load_repo()

    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument("-v", "--version", help="Show the current version of tool", action="version",
                        version=f"{__project__} - {__version__}")
    
    subparser = parser.add_subparsers(dest="command")

    get = subparser.add_parser("get", help="Download wordlists")
    get.add_argument("file_name", help="File name of the wordlist to download")
    get.add_argument("destination", help="File path where you want to store the downloaded wordlist")
    get.add_argument("-d", "--decompress", action="store_true", help="Decompress the wordlist after download")

    search = subparser.add_parser("search", help="Search wordlists")
    search.add_argument("search_term", help="What to search")
    search.add_argument("-g", "--group", dest="group", help="Search in group category instead of file name example: discovery, fuzzing",
                             action="store_true")


    args = parser.parse_args()
    command = args.command
    if command == "search":
        search_wordlist(args)
    elif command == "get":
        download_wordlist(args)
    


    if sys.argv.__len__() == 1:
        parser.print_help()
        sys.exit(-1)
    


if __name__=="__main__":
    main()
    