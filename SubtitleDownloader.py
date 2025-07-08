###############################################################################
# Subtitle Downloader
# -----------------------------------------------------------------------------
# Author: Miksu2001
# License: https://github.com/Miksu2001/subtitle-downloader/blob/main/LICENSE
# -----------------------------------------------------------------------------
# This script reads download links from a text file, checks which links are
# valid, and downloads files from the valid links to the given output directory.
#
# Please note that the format of the input file is crusial!
# The input file should contain one link per line and the line numbers should
# correspond to the episode numbers. Empty or invalid lines will increase the
# running episode number. This is the intended behavior.
#
###############################################################################

import re
import requests


LINK_PATTERN = r"http(s)?://.*\.((vtt)|(srt))"
"""Defines what a valid download link looks like."""


def read_file(filepath:str) -> list[str]:
    """Reads the contents of the given file to a list.

    One line should correspond to one link and the line numbers should
    correspond to the episode numbers. Last line of the file should be left
    empty.

    Parameters
    ----------
    filepath : str
        Path to the file containing the links.

    Returns
    -------
        A string list containing lines found in the file if file was read
        successfully, None otherwise.

    """

    try:
        print(f"Reading file '{filepath}'...")
        lines:list[str] = []
        with open(filepath, "r", encoding="utf-8") as file:
            for line in file:
                lines.append(line[:-1])
        return lines
    except Exception as e:
        print(f"Cannot read file '{filepath}': {e}")
        return None



def get_links(lines:list[str]) -> list[str]:
    """Looks for links in the given list and saves them to a dictionary.

    The dictionary uses the episode numbers as keys. If a link in the list is
    invalid, the line is skipped but the episode number is still increased.

    Parameters
    ----------
    lines : list[str]
        List to find links from.

    Returns
    -------
        A dictionary containing valid download links.

    """

    valid_links:dict[int,str] = {}
    line_number:int = 0

    for line in lines:
        line_number += 1
        print(f"Line {line_number:02}: ", end="")

        if (re.match(LINK_PATTERN, line)):
            valid_links[line_number] = line
            print(f"Added '{line}' to download list.")
        else:
            print(f"'{line}' is not a valid link! Skipping.")

    print(f"Found {len(valid_links)} valid links ({len(valid_links)/line_number:%}).")
    return valid_links


def download_file(url:str, output_directory_path:str, output_filename:str) -> None:
    """
    Downloads the file from the given URL and saves it to the given directory
    with the given name.

    Parameters
    ----------
    url : str
        Link to the file on the internet.
    output_directory_path : str
        Path to the directory where the file should be saved.
    output_filename : str
        Name of the saved file.

    """

    response = requests.get(url)
    ouput_path = f"{output_directory_path}\\{output_filename}"

    if (response.status_code == 200):
        with open(ouput_path, "wb") as file:
            file.write(response.content)
        print(f"Downloaded from '{url}' to '{ouput_path}'.")
    else:
        print(f"Failed to download file from '{url}': {response.status_code}.")



def download_files(links:dict[int,str], output_directory_path:str) -> None:
    """
    Downloads files from all links in the given dict and saves them to the
    given output directory.

    Parameters
    ----------
    links : dict[int,str]
        Dictionary containing valid links and their. Episode numbers are used as
        keys.
    output_directory_path : str
        Path to the directory where the downloaded files should be saved in.

    """
    for key in links:
        url:str = links[key]
        file_extension:str = f"{url.split(".")[-1]}"
        filename:str = f"E{key:02}.{file_extension}"
        download_file(url, output_directory_path, filename)


def main():
    input_file = input("Enter path to link list file (txt): ")
    output_directory_path = input("Enter path to output directory: ")
    print()
    links:dict[int,str] = get_links(read_file(input_file))
    download_files(links, output_directory_path)
    input("Finished. Press [Enter] to exit.")


main()
