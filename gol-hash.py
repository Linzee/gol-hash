#!/usr/bin/env python
# coding=utf-8

from optparse import OptionParser
from gol import GOL

WIDTH = 11
HEIGHT = 11
STEPS = 7
LIFE = 'B3/S23'

parser = OptionParser()
parser.add_option("-W", "--width",
                  metavar="NUMBER", type="int",
                  dest="width", default=WIDTH,
                  help="Change width of board used for simulation")
parser.add_option("-H", "--height",
                  metavar="NUMBER", type="int",
                  dest="height", default=WIDTH,
                  help="Change height of board used for simulation")
parser.add_option("-s", "--steps",
                  metavar="NUMBER", type="int",
                  dest="steps", default=STEPS,
                  help="Change number of steps for simulation")
parser.add_option("-l", "--life",
                  dest="life", default=LIFE,
                  help="Change rules for life, correct format is B3/S23")
parser.add_option("-f", "--file",
                  dest="inputFile", metavar="FILE",
                  help="Create hash for file")

options, optionsValues = parser.parse_args()
WIDTH = options.width
HEIGHT = options.height
STEPS = options.steps
LIFE = options.life
inputFile = options.inputFile

if len(optionsValues) > 0:
    inputData = optionsValues[0]
else:
    if not inputFile:
        print 'usage: --flags <input>'
        exit(1)

def gol_hash(bits):
    gol = GOL(WIDTH, HEIGHT, LIFE)
    
    i = 0
    s = gol.getSize()
    w = gol.getWidth()
    
    for bit in bits:
        si = i % s
        gol.set(si % w, si / w, bit)
        i += 1

    #PROCESS
    gol.printBoard()
    for i in xrange(STEPS):
        gol.step()
        gol.printBoard()

    #PULL DATA
    bits = []
    w = gol.getWidth()
    for i in xrange(gol.getSize()):
        bits.append(gol.get(i % w, i / w))
        
    return bits

def bits_from_file(inputFile, chunksize=8192):
    i = 0
    with open(inputFile, "rb") as f:
        while True:
            chunk = f.read(chunksize)
            if chunk:
                for b in chunk:
                    for i in xrange(8): #split to bits
                        yield bool((ord(b) >> i) & 1)
                    i += 1
            else:
                break

def bits_from_string(string):
    i = 0
    for b in string:
        for i in xrange(8): #split to bits
            yield bool((ord(b) >> i) & 1)
        i += 1

def bits_to_string(bits):
    i = 0
    n = 0
    for i in xrange(len(bits)):
        n += int(bits[len(bits) - i - 1]) << i
        i += 1
    
    return hex(n)[2:-1]

#PUT DATA
if inputFile:
    bits = bits_from_file(inputFile)
else:
    bits = bits_from_string(inputData)

bits = gol_hash(bits)

print 'Hash for your data is', bits_to_string(bits)