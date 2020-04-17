# wows-clanbattle-scanner
A simply python script to parse results of the World of Warships clan battle sessions into a lean csv format for further analysis.

## prerequisites
1. Python 3 is required to run this script: https://www.python.org/downloads/
1. [Download](https://github.com/Fargrath/wows-clanbattle-scanner/raw/master/clanbattle_scanner.py) the file `clanbattle_scanner.py` (or checkout the repository)

## usage
Unfortunately, WoWS doesn't offer a programming api for clanbattle data. Therefore, you have to save the html page to your local files.

1. Go to https://clans.worldofwarships.eu/clans/gateway/wows/clan-battles/history
1. Open the developer tools
   * Opera shortcut (Ctrl + Shift + I)
1. Right-click on the `body` element, choose `Copy` and `Copy element`
1. Paste the content into a new local file `Clans.html`
   * for simplicity: create the file in the same location where this script resides
1. Run the script: `python clanbattle_scanner.py Clans.html Results.csv`

Note: You might have to edit some of the values in lines 6-9 to your language settings, and the team size & map pool of the current season.

## tests
There are some simple unit tests. Just run `python clanbattle_scanner_test.py`
