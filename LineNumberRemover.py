#!/usr/bin/env python3
# Code Line Number remover
#Created by Samuel Davenport

__version__ = '0.0.1'

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

def partquotes(text, split="'"):
    data = text.split("'")
    tmp = []
    bad = ('[', ']', ',', ', ')
    for i in data:
        if not i in bad:
            tmp.append(i)
    return tmp

def init():
    data = []
    tmp = fileloader.loadfile('tmp.txt')
    for line in tmp:
        tmpi = line.split(' ')
        if tmpi[0].isdecimal():
            tmpi[0] = '  '
        tmpii = ''
        for letter in tmpi:
            tmpii += str(letter)+' '
        data.append(tmpii)
    fileloader.svfile('tmp.txt', data)

if __name__ == '__main__':
    init()
