#!python

import sys
import os
import glob
from fuzzywuzzy import process
from prompt_toolkit import prompt
from prompt_toolkit.completion import Completer, Completion
import json

with open(os.path.join(os.path.dirname(sys.argv[0]), "config.json"), 'r') as fd:
    search_space = json.loads(fd.read())

if len(sys.argv) >= 2:
    pattern = sys.argv[1]
else:
    pattern = ""

projects = []
for folder in search_space:
    projects += glob.glob(folder)

projects += glob.glob(os.getcwd())
projects += glob.glob(os.path.join(os.getcwd(), "*"))
projects += glob.glob(os.path.join(os.getcwd(), "*", "*"))

class MyCustomCompleter(Completer):
    def get_completions(self, document, complete_event):
        # skip search with empty line
        if not document.current_line:
            return

        results = map(lambda i: i[0], process.extract(document.current_line, projects, limit=20))
        
        for result in results:
            yield Completion(result, start_position=-len(document.current_line))

directory = prompt('> ', completer=MyCustomCompleter(), default=pattern)
try:
    os.write(3, bytes(directory, 'utf-8'))
except:
    print(directory)