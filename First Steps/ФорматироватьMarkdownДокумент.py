import os
import pathlib
import codecs
from pathlib import Path

sim1 = chr(8226) # код символа первого уровня группировки
sim2 = chr(9675) # код символа второго уровня группировки
sim3 = '§'
sim4 = '□'
sim5 = '®'

path = Path("Python", "test.md") 
pathbase = Path("Python", "test_base.md") 
base = codecs.open(pathbase, 'r', 'utf-8').read()
FileMarcdown = codecs.open(path, 'w', 'utf8')
for line in base:
    sim = line[0]
    sim11 = ord(line[0])
    if sim == sim1:
       FileMarcdown.write(line.replace(sim, "##", 1))
    elif sim == sim2:
       FileMarcdown.write(line.replace(sim, "\n*", 1))
    elif sim == sim3:
       FileMarcdown.write(line.replace(sim, "  *", 1))
    elif sim == sim4:
       FileMarcdown.write(line.replace(sim, "    *", 1))
    elif sim == sim5:
       FileMarcdown.write(line.replace(sim, "      *", 1))
    else:
        FileMarcdown.write(line)
    #break
FileMarcdown.close()