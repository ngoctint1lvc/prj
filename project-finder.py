import sys
import os
import glob2
from fuzzywuzzy import process, fuzz
from fuzzywuzzy.string_processing import StringProcessor
from prompt_toolkit import prompt
from prompt_toolkit.completion import Completer, Completion
import json
import argparse
import re
from pprint import pformat

def debug(msg):
    global verbose
    if verbose: print(f"[DEBUG] {msg}")

def remove_duplicated(lst: list, dup_checking_fn = lambda item, lst: item in lst):
    result = []
    for item in lst:
        if dup_checking_fn(item, lst):
            result.append(item)
    return result

def generateSearchSpacePattern(search_space, maxDepth):
    result = []
    for dir in search_space:
        absDir = os.path.abspath(dir)
        result.append(absDir)
        if (not '*' in absDir) and os.path.isdir(absDir):
            for i in range(maxDepth):
                result.append(os.path.join(absDir, "/".join(["*"] * (i + 1))))
    return result

processor_regex = re.compile(r"(?ui)[^\w\-_./\\]")
def query_processor(s, force_ascii=False):
    global processor_regex
    # Keep only letters, numbers and some special character in path
    string_out = processor_regex.sub(" ", s)
    # Force into lowercase.
    string_out = StringProcessor.to_lower_case(string_out)
    # Remove leading and trailing whitespaces.
    string_out = StringProcessor.strip(string_out)
    return string_out

def custom_scorer(s1, s2):
    return 0.8*fuzz.partial_ratio(s1, s2) + 0.2*fuzz.token_sort_ratio(s1, s2)

class MyCustomCompleter(Completer):

    def get_completions(self, document, complete_event):
        global limitResult, projects, verbose
        global fileOnly, dirOnly

        # skip search with empty line
        if document.current_line:
            # if current line is a valid path, list all files inside it with full 100 score
            subfiles = list(map(lambda i: (i, 100), glob2.glob(os.path.join(document.current_line, "*"))))

            fuzzyResult = process.extract(document.current_line, projects, scorer=custom_scorer, limit=limitResult, processor=query_processor)
            
            if len(subfiles) > 0:
                fuzzyResult = remove_duplicated(fuzzyResult, lambda item, lst: item in subfiles)
            
            results = subfiles + fuzzyResult
        else:
            results = []
        
        for result in results:
            if dirOnly and not os.path.isdir(result[0]):
                continue

            if fileOnly and not os.path.isfile(result[0]):
                continue

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
parser.add_argument('-H', '--hidden', dest='show_hidden', action="store_true",
                    help='show hidden files and directories')
parser.add_argument('-v', '--verbose', dest='verbose', action="store_true",
                    help='verbosity (for debugging purpose)')
parser.add_argument('--file-only', dest='fileOnly', action="store_true",
                    help='only list file in output')
parser.add_argument('--dir-only', dest='dirOnly', action="store_true",
                    help='only list directory in output')

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
show_hidden = args.show_hidden
fileOnly = args.fileOnly
dirOnly = args.dirOnly

debug(f"Argument: {pformat(args)}")

search_space = generateSearchSpacePattern(search_space, maxDepth)

if len(search_space) <= 0:
    configFile = args.config or os.path.join(os.path.dirname(sys.argv[0]), "config.json")
    debug(f"Load config file from: {configFile}")

    with open(os.path.abspath(configFile), 'r') as fd:
        search_space = list(map(lambda dir: os.path.abspath(dir), json.loads(fd.read())))

# remove duplicated values
search_space = list(map(lambda path: os.path.realpath(path), search_space))
search_space = remove_duplicated(search_space)

debug(f"Search space: {pformat(search_space)}")

projects = []
for folder in search_space:
    projects += glob2.glob(os.path.abspath(folder), include_hidden=show_hidden)

debug(f"Number of scanned projects: {len(projects)}")

complete_in_thread = True if len(projects) > 2000 else False
debug(f"Thread mode: {complete_in_thread}")
directory = prompt('> ', completer=MyCustomCompleter(), complete_in_thread=complete_in_thread)

try:
    with os.fdopen(3, 'wb', 0) as fd:
        fd.write(bytes(directory, 'utf-8'))
except:
    print(directory)