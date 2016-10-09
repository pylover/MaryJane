# MaryJane

Simple Task runner

### Python 3.6 or higher required.

The (Formatted string literals)[https://docs.python.org/3.6/whatsnew/3.6.html#pep-498-formatted-string-literals] are introduced in version 3.6.

It's used to evaluate the values in `{}`, see the example:

### Install

    $ pip install marynaje

#### maryjane.yaml


```yaml
PY: from os.path import split

title: Test Project
version: 0.1.0

empty:

static: {here}/static
temp: {here}/../temp

bag:
  count: 0
  avg: .34
  INCLUDE: {here}/simple.dict.yaml

task1:

  file1: {static}/file1.txt
  files:
    - {static}/file1.txt
    - {static}/file2.txt

  outfile: {temp}/out.txt

  ECHO: Concatenating {split(file1)[1]}, {', '.join(split(f)[1] for f in files)} -> {split(outfile)[1]}.
  SHELL: mkdir -p $(dirname {outfile})
  SHELL: cat {file1} {' '.join(files)} > {outfile}
  PY: bag.count += 1

WATCH: {here}
WATCH_ALL: {static}
NO_WATCH: {here}/temp
```

    
#### simple.dict.yaml

```yaml
item1:
    item2: value2
```

#### Build

    $ maryjane
    
to enable watcher:

    $ maryjane -w
    
Check out `../temp/out.txt` to see the result.
