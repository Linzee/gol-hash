#!/usr/bin/env python
# coding=utf-8

import re

class GOL:
    
    def __init__(self, width, height, rule):
        self.board = [[False for x in range(width)] for x in range(height)]
        self.boardProcess = [[False for x in range(width)] for x in range(height)]
        
        match = re.match( r'^B([0-9]+)/S([0-9]+)$', rule)
        self.begin = set(match.group(1))
        self.stay = set(match.group(2))
    
    def get(self, x, y):
        return self.board[y][x]
    
    def set(self, x, y, value):
        self.board[y][x] = bool(value)
    
    def getLevel(self, x, y, r = 1):
        l = 0;
        for ix in xrange(x-r, x + r + 1):
            for iy in xrange(y-r, y + r + 1):
                
                if ix == x and iy ==y:
                    continue
                
                if ix < 0:
                    ix = self.getWidth() + ix
                if iy < 0:
                    iy = self.getHeight() + iy
                if ix >= self.getWidth():
                    ix = ix - self.getWidth()
                if iy >= self.getHeight():
                    iy = iy - self.getHeight()

                l += self.board[iy][ix]
        return l

    def cellStep(self, level, current):
        if str(level) in self.begin:
            return True
        if str(level) in self.stay:
            return current
        return False

    def step(self):
        #process step
        for y in xrange(self.getHeight()):
            for x in xrange(self.getWidth()):
                level = self.getLevel(x, y)
                self.boardProcess[y][x] = self.cellStep(level, self.board[y][x])
        #swap boards
        self.board, self.boardProcess = self.boardProcess, self.board
    
    def printBoard(self):
        for y in range(self.getHeight()):
            for x in range(self.getWidth()):
                if self.board[y][x]:
                    print "#",
                else:
                    print ".",
            print
        print
    
    def getWidth(self):
        return len(self.board[0])
    
    def getHeight(self):
        return len(self.board)
    
    def getSize(self):
        return self.getWidth() * self.getHeight()