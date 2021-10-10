#!/usr/bin/env python3
# Dijkstra's Algorythm (Pathfinding AI)
# Written by CoolCat467 12/16/2019

NAME = "Dijkstra's Algorythm"
__version__ = '0.0.0'

#for mkRandMap
from random import randint
import math

class fileloader:
    def loadfile(filename):
        filedata = []
        try:
            with open(str(filename), mode='r', encoding='utf-8') as loadfile:
                tmp = []
                for i in loadfile:
                    tmp.append(str(i))
                tmp = str(''.join(tmp))
                for line in tmp.splitlines():
                    filedata.append(line)
                loadfile.close()
        except FileNotFoundError:
            fileloader.svfile(filename, '')
            toret = ['']
        else:
            toret = list(filedata)
        return toret

    def svfile(filename, data, append=False):
        if not append:
            with open(str(filename), mode='w', encoding='utf-8') as savefile:
                for line in data:
                    savefile.write(str(line)+'\n')
        else:
            with open(str(filename), mode='a', encoding='utf-8') as savefile:
                savefile.write(str(data)+'\n')
        savefile.close()
    pass

def mkRandMap(npoints, maxdistance=4):
    #make points
    points = []
    for point in range(npoints):
        points.append(chr(point + 65))
    #make conns
    conns = []
    pointsii = list(points)
    for i in range(npoints-1):
        rp = pointsii[randint(0, len(pointsii)-1)]
        del pointsii[pointsii.index(rp)]
        tmpi, tmpii = (0, 0)
        while abs(tmpi - tmpii) < 1:
            tmpi = randint(0, len(pointsii))
            tmpii = randint(0, len(pointsii))
        tmp = list(pointsii[tmpi:tmpii])
        conns.append([rp, tmp])
    #add length values
    tmp = []
    for i in conns:
        cp, to = i
        tmpi = []
        for ii in range(len(to)):
            tmpi.append(randint(1, maxdistance))
        tmp.append([cp, to, tmpi])
    #fix conns
    conns = Dijkstra.fxMapConns(tmp)
    if not Dijkstra.sepMap(conns, 0) == points:
        for i in points:
            if not i in Dijkstra.sepMap(conns, 0):
                tp = str(i)
                while tp == i:
                    tp = points[randint(0, len(points)-1)]
                conns.append([i, [tp], [randint(1, maxdistance)]])
        conns = Dijkstra.fxMapConns(conns)
    return conns

class Dijkstra:
    def __init__(self, maplist, currentpos, topos):
        self.start = str(currentpos)
        self.end = str(topos)
        self.map = Dijkstra._sort(list(maplist), self.start)
        #MOST IMPORTANT PIECE EVER OR IT CRASH
        self._reset()
        self.isSolved = False
        self.solved = []
    
    def _reset(self):
        tmpi = Dijkstra.sepMap(self.map, 0)
        if self.start in tmpi:
            del tmpi[tmpi.index(self.start)]
            tmpii = []
            for pos in tmpi:
                tmpii.append([pos, math.inf, None])
            self.priorityQue = [[self.start, 0, None]] + tmpii
        else:
            if not self.start in Dijkstra.sepMap(Dijkstra.fxMapConns(self.map), 0):
                self.solved = [self.start]
                self.isSolved = True
            else:
                self.map = Dijkstra.fxMapConns(self.map)
                self._reset()
    
    def __repr__(self):
        return "Dijkstra(%s, '%s', '%s')" % (str(self.map), self.start, self.end)
    
    def __str__(self):
        if self.isSolved:
            toret = '<Solved Dijkstra Map>'
        else:
            toret = '<Unsolved Dijkstra Map>'
    
    @staticmethod
    def _sort(lst, start):
        lst.sort()
        tmp = []
        for i in lst:
            tmp.append(i[0])
        if start in tmp:
            idx = tmp.index(start)
            data = [lst[idx]]
            for i in range(len(tmp)):
                if not i == idx:
                    data.append(lst[i])
        return data
    
    @staticmethod
    def sepMap(lst, point):
        lst, point = list(lst), int(point)
        tmp = []
        for i in lst:
            tmp.append(i[point])
        return tmp
    
    @staticmethod
    def fxMapConns(conns):
        tmp = []
        mode = 2
        for i in conns:
            cp, to, l = i
            if not cp in Dijkstra.sepMap(tmp, 0):
                tmp.append([cp, [], []])
            for ii in to:
                for ii in range(len(to)):
                    if not to[ii] in tmp[Dijkstra.sepMap(tmp, 0).index(cp)][1]:
                        tmp[Dijkstra.sepMap(tmp, 0).index(cp)][1].append(to[ii])
                        tmp[Dijkstra.sepMap(tmp, 0).index(cp)][2].append(l[ii])
                    if to[ii] in Dijkstra.sepMap(tmp, 0):
                        if not cp in tmp[Dijkstra.sepMap(tmp, 0).index(to[ii])][1]:
                            tmp[Dijkstra.sepMap(tmp, 0).index(to[ii])][1].append(cp)
                            tmp[Dijkstra.sepMap(tmp, 0).index(to[ii])][2].append(l[ii])
                    else:
                        tmp.append([to[ii], [cp], [l[ii]]])
        tmp.sort()
        return tmp
    
    def solve(self):
        cp = str(self.start)
        solved = bool(self.isSolved)
        #solve for path
        if not solved:
            while not solved:
                cpidx = Dijkstra.sepMap(self.map, 0).index(cp)#current point index
                cpdata = self.map[cpidx]#current point data
                
                for i in cpdata[1]:#for each connected point
                    
                    copidx = Dijkstra.sepMap(self.map, 0).index(i)#connected point index
                    copdata = self.map[copidx]#connected point data
                    num = copdata[2][copdata[1].index(cp)] + self.priorityQue[cpidx][1]
                    if self.priorityQue[copidx][0] != cp and (not num > 99999):
                        self.priorityQue[copidx][1] = num
                        self.priorityQue[copidx][2] = cp
                    
                p, l, t = self.priorityQue[cpidx]
                self.solved.append([p, t, l])
                #make minni list so we don't choose an alteaty solved pos
                tmpque = list(self.priorityQue)
                for i in Dijkstra.sepMap(self.solved, 0):
                    del tmpque[Dijkstra.sepMap(tmpque, 0).index(i)]
                #if we still solving
                if not ((self.end in Dijkstra.sepMap(self.solved, 0)) or (len(tmpque) == 0)):
                    num = min(Dijkstra.sepMap(tmpque, 1))
                    cp = tmpque[Dijkstra.sepMap(tmpque, 1).index(num)][0]
                else:
                    solved = True
            solved = self.isSolved
            #assemble path
            self.solved.reverse()
            mmap = list(self.solved)
            self.priorityQue, self.solved = self.solved, []
            while not solved:
                cpidx = Dijkstra.sepMap(mmap, 0).index(cp)#current point index
                cpdata = mmap[cpidx]
                self.solved = [cpdata[0]] + self.solved
                cp = cpdata[1]
                solved = ((self.start in self.solved) or (cp == None))
            self.isSolved = True
        return self.solved
    pass

#original testing map
#cmap = [['A', ['B', 'C', 'D'], [1, 1, 1]], ['B', ['A', 'D'], [1, 1]], ['C', ['A'], [1]], ['D', ['A', 'B', 'E'], [1, 1, 1]], ['E', ['D', 'F'], [1, 1]], ['F', ['E'], [1]]]

#seccond testing map
#cmap = [['C', ['A', 'B', 'D', 'E'], [1, 1, 1, 1]], ['A', ['C', 'F', 'D'], [1, 1, 1]], ['B', ['C', 'E', 'F'], [1, 1, 1]], ['D', ['C', 'E', 'F', 'A'], [1, 1, 1, 1]], ['E', ['C', 'B', 'D', 'F'], [1, 1, 1, 1]], ['F', ['E', 'A', 'B', 'D'], [1, 1, 1, 1]]]

#Testing Solver
#damap = Dijkstra(cmap, 'A', 'F')
#print(cmap)
#print(damap.solve())

if __name__ == '__main__':
    filename = str(input('Filename to save to: '))
    tcount = 0
    count = 0
    while True:
        try:
            cmap = mkRandMap(26)
            damap = Dijkstra(cmap, 'A', 'Z')
            solved = damap.solve()
            if len(solved) > 9:
                add = str(str((tcount, count))+'\n'+str(cmap)+'\n'+str(solved)+'\n--------\n')
                fileloader.svfile(filename+'.txt', add, True)
                count += 1
            tcount += 1
            print(tcount, count)
        except BaseException as e:
            print('Error : '+str(e))
            break
