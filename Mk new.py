#!/usr/bin/env python3
# Program that makes new programs.
#
# Copywrite Cat Software Inc, All rights reserved.
# Programmed by Samuel Davenport, member of Cat Inc.
import os
from shutil import copyfile

def copy(name, path):
    disdir = os.path.split(os.sys.argv[0])[0]#where dis folder at?
    newpath = str(path+'/'+name)
    os.mkdir(newpath)#new folder named the new name 
    src = disdir  + '/Default.py'
    dst = newpath + '/'+name+'.py'
    copyfile(src, dst)
    src = disdir  + '/maths.py'
    dst = newpath + '/maths.py'
    copyfile(src, dst)

def main():
    # Greet user
    print('Welcome to the New Project Program v3.0!')
    print('Copywrite Cat Software Inc, All rights reserved.')
    print()
    if str(os.path.split(os.getcwd())[1]) == 'Mk new':
        name = str(input('What is the project name? : '))
        path = str(input('What is the project destonation path? : '))
        if path == '':
            path = '/home/pi/Desktop'
        copy(name, path)
    else:
        raise FileNotFoundError('Files Required for Operation Not Found')

# Activation Program
if __name__ == '__main__':
    print('Copywrite Cat Software Inc, All rights reserved.')
    print('Programmed by Samuel Davenport, member of Cat Inc.')
    try:
        main()
    except BaseException as e:
        print()
        if str(e) == '':
            error = 'An Error Has Occored.'
        else:
            error = str(e)
        print('ERR: '+str(error), file=os.sys.stderr)
    else:
        print()
        print('Done!')
    print()
    cat = input('Press Return to Quit. ')
os.abort()
exit()
