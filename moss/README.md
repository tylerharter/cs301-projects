# Usage
The script only supports Linux/MacOS. 

1. Run `python fetch\_projects.py [project id, e.g. p8]` to get all submissions. You should have the credentials info in `~/.aws/credentials`.
2. Run `python moss.py [moss user id]` to run the official moss script and get pair-to-pair comparison result.
3. Run `python mossparse.py` to run union find algorithm and generate final result. You may want to run `python mossparse.py > result.md` to save the generated MarkDown report to a local file.
