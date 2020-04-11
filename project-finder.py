import sys
import os
import glob
from fuzzywuzzy import process, fuzz
from prompt_toolkit import prompt
from prompt_toolkit.completion import Completer, Completion
import json
import argparse

def debug(msg):
    global verbose
    if verbose: print(f"[DEBUG] {msg}")

def generateSearchSpacePattern(search_space, maxDepth):
    result = []
    for dir in search_space:
        absDir = os.path.abspath(dir)
        result.append(absDir)
        if (not '*' in absDir) and os.path.isdir(absDir):
            for i in range(maxDepth):
                result.append(os.path.join(absDir, "/".join(["*"] * (i + 1))))
    return result

class MyCustomCompleter(Completer):
    def get_completions(self, document, complete_event):
        global limitResult, projects, verbose

        # skip search with empty line
        if document.current_line:
            results = process.extract(document.current_line, projects, limit=limitResult, scorer=fuzz.partial_ratio)
        else:
            results = []
        
        for result in results:
            display_meta = f"Score: {result[1]}" if verbose else ""
            yield Completion(result[0], start_position=-len(document.current_line), display_meta=display_meta)
                

parser = argparse.ArgumentParser(description='Project finder utility for cli user')
parser.add_argument('searchDirs', metavar='searchDir', type=str, nargs='*',
                    help='custom search directories')
parser.add_argument('-c', '--config', dest='config', default='',
                    help='custom config file')
parser.add_argument('-d', '--max-depth', dest='maxDepth', type=int, default=3,
                    help='maximum depth to search (only affected when providing searchDir arguments)')
parser.add_argument('-l', '--limit', dest='limit', type=int, default=40,
                    help='limit number of results')
parser.add_argument('-v', '--verbose', dest='verbose', action="store_true",
                    help='verbosity (for debugging purpose)')

args = parser.parse_args()

# Search space order:
# 1. Using search directories from positional arguments
# 2. If no positional argument is specified, read custom config file
# 3. Else, using defaull config.json file

search_space = args.searchDirs
configFile = args.config
maxDepth = args.maxDepth
limitResult = args.limit
verbose = args.verbose

debug(f"Argument: {args.__dict__}")

search_space = generateSearchSpacePattern(search_space, maxDepth)

if len(search_space) <= 0:
    configFile = args.config or os.path.join(os.path.dirname(sys.argv[0]), "config.json")
    with open(os.path.abspath(configFile), 'r') as fd:
        search_space = json.loads(fd.read())

debug(f"Search space: {search_space}")

projects = []
for folder in search_space:
    projects += glob.glob(os.path.abspath(folder), recursive=True)

debug(f"Number of projects: {len(projects)}")

complete_in_thread = True if len(projects) > 2000 else False
debug(f"Thread mode: {complete_in_thread}")
directory = prompt('> ', completer=MyCustomCompleter(), complete_in_thread=complete_in_thread)

try:
    with os.fdopen(3, 'wb', 0) as fd:
        fd.write(bytes(directory, 'utf-8'))
except:
    print(directory)