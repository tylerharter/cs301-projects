# tacli
TA command line interface to make reviewing easier

# Installation

Create a python3 virtual environment (suggested) and then install using pip

```
python3 -m venv taclienv
source taclienv/bin/activate
```

Install using pip 

```
git clone https://github.com/tylerharter/cs301-projects
cd tacli
pip install .
```

# First steps

tacli reads three environment variables

### `TACLI_EDITOR` - Launches the editor of your choice.
For example, to ensure vim is used

```
export TACLI_EDITOR=vim
```

You can also pass options to your editor

```
export TACLI_EDITOR="vim -u /path/to/vimrc"
```

### `TACLI_DIFFTOOL` - Launches the difftool of your choice

```
export TACLI_DIFFTOOL=vimdiff
```

### `TACLI_TOKEN` - The google authentication token required for the `pull` and `push` commands

You can copy your token by going to the [reviewer](https://tyler.caraza-harter.com/cs301/fall18/reviewer.html) link and clicking "Copy Token".

```bash
export TACLI_TOKEN=<your-token>
```

> The token is valid only for a certain amount of time, so you may have to copy the token again. The other two environment variables can be placed in your bashrc as they don't change.

# Usage

- `tacli --help` gives you all the commands that can be run.
- `tacli <command> --help` describes the arguments for a particular command.

- Reviews always begin with `#%` to differentiate them from submitted comments. They highlight the line below it.
- The very first `#%` comment at the top of the file are the general comments.  
- Score deductions should also be at the top of the file - `#% DEDUCT x` where x is the amount to reduce.  
- If a file called 'macros.txt' exists in the folder, all macro definitions are loaded from there. (examples provided below)

A common workflow

tacli maintains state about which submission you are currently working on. You can see all submissions with `tacli list`.
The one green colored submission is the one you are currently working on.

Commands like tacli edit, diff, difftool, exec, push work on the current submission.
`tacli expand` expands all macros in the current submission.

`tacli prev` and `tacli next` move to neighbors. `tacli jump 5` jumps to the 5th submission.

```bash
tacli pull 4 # pull submissions for project 4
cd p4
tacli list # list all the submissions to be reviewed.

tacli edit # opens up the current submission in your editor.
# Sometimes you might want to exec the file or fix something 
tacli exec # This runs untrusted code locally, so view the file before running it!

tacli edit # open up the file again and write reviews
tacli dump # ensure that reviews are fine
tacli push # push this review now (you can do this later as well)
tacli next # move to the next review and repeat the edit process
```

An example submission

```python
# My project: 1
import project

def add(x, y):
    return x + y

if __name__ == '__main__':
    add(1, 2)
```

When editing the file, I add my reviews as follows

```python
#% This is a general comment.
#% This is also a general comment. Both get merged together.
#% Also a general comment. The next line deducts a point.
#% DEDUCT 1
# My project: 1
#% This is a comment about the `import project` line below.
import project

#% function-docstrings
def add(x, y):
    #% This highlights the return x + y statement. Make sure not to add new lines of your own!
    #% The only modifications allowed are lines prefixed with #%
    return x + y

if __name__ == '__mian__':
    add(1, 2)
```

You can also use macros such as the one in the example `#% function-docstrings`, which expands based on the definition in `macros.txt`.

```bash
$> cat macros.txt

#define function-docstrings

It is good practice to use docstrings for your functions as follows

def add(x, y):
    """ This function returns the sum of x and y """
    return x + y

#define another-macro

You can define multiple macros in this file with the syntax described.

$>
```

Macros are automatically expanded with a `tacli push`.
`tacli dump` can also show you what your comments look like before you run `tacli push`.
