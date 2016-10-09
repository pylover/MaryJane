# MaryJane

Simple Task runner

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
    
      ECHO: Concatenating {split(file1)[1]} {' '.join(split(f)[1] for f in files)} into: {split(outfile)}.
      SHELL: mkdir -p $(dirname {outfile})
      SHELL: cat {file1} {' '.join(files)} > {outfile}
      PY: bag.count += 1

  

