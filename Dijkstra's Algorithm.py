#!/usr/bin/env python3
# Dijkstra's Algorythm (Pathfinding AI)
# Written by CoolCat467 12/16/2019

"Dikestra's Algorythm Implementation."

import math
#for make_random_map
import random

__title__ = "Dijkstra's Algorythm"
__version__ = '0.0.0'

def make_random_map(npoints, maxdistance=4):
    "Return a list of random points that are all interconnected."
    #make points
    points = [chr(i + 65) for i in range(npoints)]
    #make conns
    conns = []
    pointsii = list(points)
    for _ in range(npoints-2):
        cidx = random.randrange(len(pointsii))
        cpoint = pointsii[cidx]
        del pointsii[cidx]
        start, end = (0, 0)
        while abs(start - end) < 1:
            start = random.randrange(len(pointsii))
            end = random.randrange(len(pointsii))
        topoints = list(pointsii[start:end])
        lengths = [random.randint(1, maxdistance) for _ in range(len(topoints))]
        conns.append([cpoint, topoints, lengths])
    #fix conns
    conns = Dijkstra.fx_map_conns(conns)
    if not Dijkstra.sep_map(conns, 0) == points:
        for point in points:
            if not point in Dijkstra.sep_map(conns, 0):
                to_point = point
                while to_point == point:
                    to_point = random.choice(points)
                conns.append([point, [to_point], [random.randint(1, maxdistance)]])
        conns = Dijkstra.fx_map_conns(conns)
    return conns

class Dijkstra:
    "Dijkstra's Algorythm"
    def __init__(self, maplist, start, end):
        self.start = start
        self.end = end
        self.map = Dijkstra._sort(maplist, self.start)
        self.priority_queue = None
        # Set up priority queue
        self._reset()
        self.is_solved = False
        self.solved = []
    
    def _reset(self):
        "Set up priority queue and fix connections."
        tmpi = self.sep_map(self.map, 0)
        if self.start in tmpi:
            del tmpi[tmpi.index(self.start)]
            tmpii = [[pos, math.inf, None] for pos in tmpi]
            self.priority_queue = [[self.start, 0, None]] + tmpii
        else:
            if not self.start in self.sep_map(self.fx_map_conns(self.map), 0):
                self.solved = [self.start]
                self.is_solved = True
            else:
                self.map = self.fx_map_conns(self.map)
                self._reset()
    
    def __repr__(self):
        return f"Dijkstra({self.map}, {self.start:r}, {self.end:f})"
    
    def __str__(self):
        if self.is_solved:
            return '<Solved Dijkstra Map>'
        return '<Unsolved Dijkstra Map>'
    
    @staticmethod
    def _sort(lst, start):
        "Make sure start in front."
        lst = list(lst)
        lst.sort()
        tmp = [i[0] for i in lst]
        if not start in tmp:
            raise ValueError(f'{start} not in {lst}!')
        idx = tmp.index(start)
        data = [lst[idx]]
        for i in range(len(tmp)):
            if not i == idx:
                data.append(lst[i])
        return data
    
    @staticmethod
    def sep_map(list_, point):
        "Return all values fron list at index point for each item."
        return [value[point] for value in list_]
    
    @staticmethod
    def fx_map_conns(conns):
        "Fix map connections"
        tmp = []
        for cur_point, to_points, lengths in conns:
            points = Dijkstra.sep_map(tmp, 0)
            if not cur_point in points:
                tmp.append([cur_point, [], []])
                points.append(cur_point)
##            for idx in range(len(to_points)):
            for idx, to_point in enumerate(to_points):
                cpidx = points.index(cur_point)
##                if not to_points[idx] in tmp[cpidx][1]:
##                    tmp[cpidx][1].append(to_points[idx])
                if not to_point in tmp[cpidx][1]:
                    tmp[cpidx][1].append(to_point)
                    tmp[cpidx][2].append(lengths[idx])
##                if to_points[idx] in points:
##                    tpidx = points.index(to_points[idx])
                if to_point in points:
                    tpidx = points.index(to_point)
                    if not cur_point in tmp[tpidx][1]:
                        tmp[tpidx][1].append(cur_point)
                        tmp[tpidx][2].append(lengths[idx])
                else:
                    tmp.append([to_points[idx], [cur_point], [lengths[idx]]])
        tmp.sort()
        return tmp
    
    def solve(self):
        "Solve map."
        cur_point = self.start
        solved = self.is_solved
        #solve for path
        if not solved:
            while not solved:
                cpidx = self.sep_map(self.map, 0).index(cur_point)#current point index
                cpdata = self.map[cpidx]#current point data
                
                for i in cpdata[1]:#for each connected point
                    
                    copidx = self.sep_map(self.map, 0).index(i)#connected point index
                    copdata = self.map[copidx]#connected point data
                    num = copdata[2][copdata[1].index(cur_point)] + self.priority_queue[cpidx][1]
                    if self.priority_queue[copidx][0] != cur_point and num != math.inf:
                        self.priority_queue[copidx][1] = num
                        self.priority_queue[copidx][2] = cur_point
                    
                point, length, to_points = self.priority_queue[cpidx]
                self.solved.append([point, to_points, length])
                # Make mini list so we don't choose an already solved pos
                avoid = self.sep_map(self.solved, 0)
                tmpque = [point for point in self.priority_queue if not point[0] in avoid]
                #if we still solving
                if not ((self.end in self.sep_map(self.solved, 0)) or not tmpque):
                    num = min(self.sep_map(tmpque, 1))
                    cur_point = tmpque[self.sep_map(tmpque, 1).index(num)][0]
                else:
                    solved = True
            solved = self.is_solved
            #assemble path
            self.solved.reverse()
            mmap = list(self.solved)
            self.priority_queue, self.solved = self.solved, []
            while not solved:
                cpidx = self.sep_map(mmap, 0).index(cur_point)#current point index
                cpdata = mmap[cpidx]
                self.solved = [cpdata[0]] + self.solved
                cur_point = cpdata[1]
                solved = self.start in self.solved or cur_point is None
            self.is_solved = True
        return self.solved

#original testing map
#cmap = [['A', ['B', 'C', 'D'], [1, 1, 1]], ['B', ['A', 'D'], [1, 1]], ['C', ['A'], [1]], ['D', ['A', 'B', 'E'], [1, 1, 1]], ['E', ['D', 'F'], [1, 1]], ['F', ['E'], [1]]]

#seccond testing map
#cmap = [['C', ['A', 'B', 'D', 'E'], [1, 1, 1, 1]], ['A', ['C', 'F', 'D'], [1, 1, 1]], ['B', ['C', 'E', 'F'], [1, 1, 1]], ['D', ['C', 'E', 'F', 'A'], [1, 1, 1, 1]], ['E', ['C', 'B', 'D', 'F'], [1, 1, 1, 1]], ['F', ['E', 'A', 'B', 'D'], [1, 1, 1, 1]]]

#Testing Solver
#damap = Dijkstra(cmap, 'A', 'F')
#print(cmap)
#print(damap.solve())

def run():
    "Run example"
##    cmap = [['A', ['B', 'C', 'D'], [1, 1, 1]], ['B', ['A', 'D'], [1, 1]], ['C', ['A'], [1]], ['D', ['A', 'B', 'E'], [1, 1, 1]], ['E', ['D', 'F'], [1, 1]], ['F', ['E'], [1]]]
##    cmap = [['A', ['T', 'K', 'M', 'P'], [4, 3, 1, 2]], ['B', ['T', 'R', 'V'], [1, 2, 4]], ['C', ['S', 'F', 'H', 'I', 'K'], [3, 4, 4, 2, 2]], ['D', ['S', 'T'], [1, 3]], ['E', ['S', 'T', 'R', 'V', 'H', 'K', 'U'], [4, 4, 2, 1, 4, 1, 4]], ['F', ['S', 'C', 'T', 'R', 'V', 'H'], [3, 4, 1, 4, 3, 1]], ['G', ['S'], [2]], ['H', ['S', 'C', 'T', 'R', 'V', 'E', 'F', 'K', 'U'], [4, 4, 1, 1, 1, 4, 1, 1, 3]], ['I', ['S', 'N', 'C', 'T', 'M', 'P', 'R', 'U', 'V'], [4, 1, 2, 3, 1, 2, 1, 2, 3]], ['J', ['L', 'M', 'N', 'O', 'P', 'Q', 'R', 'T', 'U', 'V'], [1, 3, 1, 3, 4, 4, 2, 2, 1, 1]], ['K', ['N', 'C', 'T', 'A', 'R', 'V', 'H', 'E', 'U'], [4, 2, 2, 3, 3, 3, 1, 1, 1]], ['L', ['J', 'N', 'T'], [1, 1, 2]], ['M', ['J', 'N', 'T', 'A', 'I'], [3, 1, 2, 1, 1]], ['N', ['J', 'I', 'K', 'L', 'M', 'P', 'Q', 'R', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'], [1, 1, 4, 1, 1, 2, 4, 1, 4, 4, 4, 3, 4, 4, 3]], ['O', ['J', 'P', 'Q', 'R', 'T', 'U', 'V', 'W', 'X', 'Y'], [3, 2, 3, 3, 3, 2, 2, 1, 1, 2]], ['P', ['J', 'O', 'N', 'T', 'A', 'I', 'W', 'R', 'V'], [4, 2, 2, 3, 2, 2, 3, 1, 3]], ['Q', ['J', 'O', 'N', 'T'], [4, 3, 4, 2]], ['R', ['J', 'O', 'N', 'T', 'I', 'W', 'B', 'E', 'F', 'H', 'K', 'P'], [2, 3, 1, 3, 1, 4, 2, 2, 4, 1, 3, 1]], ['S', ['C', 'D', 'E', 'F', 'G', 'H', 'I'], [3, 1, 4, 3, 2, 4, 4]], ['T', ['J', 'O', 'N', 'A', 'B', 'D', 'E', 'F', 'H', 'I', 'K', 'L', 'M', 'P', 'Q', 'R', 'U'], [2, 3, 4, 4, 1, 3, 4, 1, 1, 3, 2, 2, 2, 3, 2, 3, 2]], ['U', ['J', 'O', 'N', 'T', 'I', 'W', 'H', 'E', 'K'], [1, 2, 4, 2, 2, 1, 3, 4, 1]], ['V', ['J', 'O', 'N', 'I', 'W', 'B', 'E', 'F', 'H', 'K', 'P'], [1, 2, 4, 3, 1, 4, 1, 3, 1, 3, 3]], ['W', ['O', 'N', 'P', 'R', 'U', 'V'], [1, 3, 3, 4, 1, 1]], ['X', ['O', 'N'], [1, 4]], ['Y', ['O', 'N'], [2, 4]], ['Z', ['N'], [3]]]
##    damap = Dijkstra(cmap, 'A', 'Z')
##    print(cmap)
##    print(damap.solve())
##    return
##    filename = str(input('Filename to save to: '))
    tcount = 0
    count = 0
    while True:
        cmap = make_random_map(26)
        damap = Dijkstra(cmap, 'A', 'Z')
        solved = damap.solve()
        if len(solved) > 9:
            add = str(str((tcount, count))+'\n'+str(cmap)+'\n'+str(solved)+'\n--------\n')
            print(add)
            count += 1
        tcount += 1
##        print(tcount, count)
        if count > 1:
            break

if __name__ == '__main__':
    run()
