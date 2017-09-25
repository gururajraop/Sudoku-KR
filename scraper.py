import requests
import os
from bs4 import BeautifulSoup
import numpy as np

START, END = 4101, 4500
PUZZLE_SIZE = 3
DOWNLOAD_DIR = "./scraped/"+str(PUZZLE_SIZE)+"/"
PUZZLE_DIR = "./puzzles/"+str(PUZZLE_SIZE)+"/"

if PUZZLE_SIZE != 3:
    URL = "http://www.menneske.no/sudoku/"+str(PUZZLE_SIZE)+"/eng/showpuzzle.html?number={}"
else:
    URL = "http://www.menneske.no/sudoku/eng/showpuzzle.html?number={}"

for index in range(START, END + 1):
    path = os.path.join(DOWNLOAD_DIR, "{}.html".format(index))
    if os.path.exists(path):
        continue
    print("Downloading {} to {}".format(index, path))
    response = requests.get(URL.format(index))
    if response.status_code != 200:
        print("Couldn't get {} :(".format(index))
        continue

    with open(path, "w") as writer:
        writer.write(response.text)
    print("Saved file {}".format(path))


def parse_html(puzzle_no, puzzle_size):

    numbers = []
    for i in range(puzzle_size):
        numbers.append(str(i+1))

    with open(os.path.join(DOWNLOAD_DIR, "{}.html".format(puzzle_no))) as reader:
        html = reader.read()

    soup = BeautifulSoup(html, "html.parser")
    grid = soup.find("div", {"class": "grid"})

    puzzle = np.zeros((puzzle_size, puzzle_size))

    data = []
    sub_grids = grid.findAll("tr")
    assert len(sub_grids) == puzzle_size
    for i, sub in enumerate(sub_grids):
        tds = sub.findAll("td")
        assert len(tds) == puzzle_size
        for index, element in enumerate(tds):
            number = next(element.children).strip()
            if number in numbers:
                puzzle[i, index] = int(number)
                data.append((i, index, int(number)))
            else:
                puzzle[i, index] = int(0)
                data.append((i, index, int(0)))
    with open(os.path.join(PUZZLE_DIR, "{}.txt".format(puzzle_no)), "w") as writer:
        for d in data:
            writer.write("{}\n".format(",".join(str(_) for _ in d)))

for index in range(START, END + 1):
    parse_html(index, PUZZLE_SIZE*PUZZLE_SIZE)
