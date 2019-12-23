#!/usr/bin/env python3
# Program that converts text to text in da terminal
#
# Copywrite Cat Inc, All rights reserved.
# Programmed by Samuel Davenport, member of Cat Inc.
#
# DISCLAIMER:
# Additinal programs used in this program
# may contain code or code based off other code
# not owned by Cat Inc.

PREBOOTERR = 'NULL'
try:
    tmp = 1
    import os, subprocess, time
    tmp = 2
    from colorama import Fore
    tmp = 3
    import maths
except ImportError:
    if not tmp == 3:
        PREBOOTERR = 'A module failed to import'
    else:
        PREBOOTERR = 'Maths module failed to import'

DEV = True
pyinstallered = False
STOPERRCATCHING = False
NAME = 'Terminal Text Convert'
__version__ = '0.0.0'
MUST = (str(NAME+'.py'), 'maths.py')

ISTERM = False
global filedata
global filemod
global fileinfo

class file:
    # File Loading
    def loadfile(filename):
        global filedata
        try:
            with open(str(filename), mode='r', encoding='utf-8') as loadfile:
                filedata = []
                for line in loadfile:
                    filedata.append(str(line).rstrip())
        except IOError:
            filedata.svfile(filename)
    
    def svfile(filename):
        global filedata
        with open(str(filename), mode='w', encoding='utf-8') as savefile:
            for data in filedata:
                savefile.write(str(data)+'\n')
            savefile.close()
    pass

class Ttc:#terminal text convert
    def changemode(lst, mode):
        if not bool(mode):#mode 0
            tmp = list(lst)
            for i in range(len(tmp)):
                tmp[i] = maths.replace('\\', '\\\\', tmp[i])
        else:
            tmp = list(lst)
            for i in range(len(tmp)):
                tmp[i] = maths.replace('\\\\', '\\', str(tmp[i]))
                tmp[i] = str(''.join(list(tmp[i])[1:len(list(tmp[i]))]))
        return tuple(tmp)
    
    def main():
        global filedata
        #do stuff
        while True:
            #while running loop
            while True:
                print()
                print('Please Select An Option:')
                print('1. Convert Text to Terminal Text')
                print('2. Convert Terminal Text to Text')
                print('3. Credits')
                print('4. Quit')
                print()
                mode = input('Option : ')
                if mode.isdigit():
                    if int(mode) in (1, 2, 3, 4):
                        break
                print()
                print('Please Try Again.')
            mode = int(mode)
            print()
            if not mode-2 > 0: # modes 1 and 2
                cfrom = list(maths.scandir(os.getcwd(), ('txt')))
                if len(cfrom) >= 1:
                    print()
                    print('File Options:')
                    for i in range(len(cfrom)):
                        print(str(i+1)+'. - '+cfrom[i])
                    print()
                    num = input('I select file number: ')
                    print(str(cfrom[int(num) - 1]))
                    file.loadfile(str(cfrom[int(num) - 1]))
                    for i in range(len(filedata)):
                        filedata[i] = str(filedata[i].rstrip())
                    filedata = Ttc.changemode(filedata, int(mode-1))
                    file.svfile(str(cfrom[int(num) - 1]))
                    print()
                    print('Done!')
                else:
                    raise IOError('No valid text files!')
            elif not mode-4 > 0: #modes 3 and 4
                if not bool(mode-3): #mode 3
                    print('This is the '+NAME+' Program, v'+__version__)
                    print('')
                    print('Copywrite (c) Cat Inc.')
                    print('All Rights Reserved.')
                    print()
                    print('Programmed by Samuel Davenport, member of Cat Inc.')
                    print()
                    print('Visit github.com/Cat-Software-Inc for more projects by Cat Software Inc.')
                    print()
                    cat = input('Press Return to Continue ')
                else:
                    print('Thank you for using the '+NAME+' Program v'+__version__+'!')
                    break
                    
        print()

def importRequired():
    tmp = MUST
    tmp = list(str(''.join(tmp)).split(sep='.py'))
    del tmp[len(tmp)-1]
    for i in range(len(tmp)-1):
        if tmp[i] == NAME:
            del tmp[i]
    modules = tmp
    for module in modules:
        try:
            exec('import %s' % module)
        except ImportError:
            raise ImportError('Required module '+module+' Failed to import.')

def startup():
    # Set some globals
    global SYSNAME
    global NODENAME
    global CURFOLD
    SYSNAME = str(os.sys.platform.title())
    if os.name == 'posix':
        NODENAME = str(os.uname()[1])
    else:
        NODENAME = 'Unknown'
    os.chdir(os.path.split(os.sys.argv[0])[0])
    CURFOLD = str(os.path.split(os.getcwd())[1])
    pythontype = os.sys.executable.split(sep='/')[3]
    ##Find Errors:
    error = ''
    # Find out if we are in our own folder
    if CURFOLD != NAME:
        os.chdir(os.path.split(os.sys.argv[0])[0])
        if not pyinstallered:
            # If it's not, fix it.
            src = os.sys.argv[0]
            os.chdir(os.path.split(os.getcwd())[0])
            os.mkdir(NAME)
            dst = os.path.split(os.getcwd())[0] +'/'+NAME+'/'+NAME+'.py'
            subprocess.call(str('cp %s %s' % (src, dst)))
            os.chdir(os.path.split(dst)[0])
            os.remove(src)
            error = '''Program was not in it's own folder, but repaired.
            Please put any additinal files the program came with in the
            new file and restart the program.'''
    if str(error) == '' and not pyinstallered:
        # Make sure we have everything
        contents = os.listdir(os.getcwd())
        lostmodules = []
        for i in MUST:
            if not i in contents:
                lostmodules.append(i)
                lostmodules.append(',\n')
        if len(lostmodules) > 0:
            lostmodules = list(str(''.join(lostmodules)).split(sep='.py'))
            lostmodules = str(''.join(lostmodules)).splitlines()
            for i in range(len(lostmodules)):
                lostmodules.append(lostmodules[0])
                lostmodules.append(' ')
                del lostmodules[0]
            lostmodules = list(''.join(list(lostmodules)[0:int(len(list(lostmodules))-1)]))
            lostmodules = str(''.join(lostmodules[0:int(len(lostmodules)-1)]))
            error = str('Some required module files were not found: '+lostmodules)
    if str(error) != '':
        return str('ERR: '+error)
    else:
        return error

def main():
    # Greet user
    print('Welcome to the '+NAME+' Program v'+__version__+'!')
    print('Copywrite (c) Cat Inc.\nAll rights reserved.')
    print()
    errors = startup()
    if errors == '':
        if SYSNAME != 'Linux':
            print('WARNING: Operating System is not Linux.', file=os.sys.stderr)
            print('Some features may not work and/or cause errors')
            print('If you would like an official port of this')
            print('program for your operating system, please')
            print('contact CoolCat467 on github.com/coolcat467')
            print()
            print('Proceed with Caution!')
        importRequired()
        Ttc.main()
    else:
        print(errors, file=os.sys.stderr)

def detectTerm():
    screen = bool(os.sys.stdout.isatty())
    #tmp = termRun('ps -AF')
    #for i in tmp:
    #    tmpi = tmp[i].rstrip().split()
    #    if len(tmpi) == 9:
    #        if tmpi[0]+' '+tmpi[2]+' '+tmpi[7]+' '+tmpi[8] == '/usr/sbin/cron -f':
    #            cronpid = tmpi[1]
    #        elif NAME in tmpi:
    #            progpid = tmpi[1]
    #iscron = progpid == cronpid
    idle = bool('idlelib' in os.sys.modules)
    return not idle

def termRun(run, out=0):
    if bool(out):
        program = subprocess.Popen(run.split(), stdout=subprocess.PIPE)
        output = program.communicate()
        data = str(output[0].splitlines())
        data = tuple(maths.strlist(str(data)))
    else:
        program = subprocess.Popen(run.split())
        data = ''
    return data

def clearterm():
    if ISTERM:
        termRun('clear')

def terminate():
    print('Quiting...')
    os.abort()
    exit()

def nuke(supersecretpassword):
    if supersecretpassword == 'Just Do It!!':
        subprocess.call(str('rm -r %s' % CURFOLD))
    terminate()

# Activation Program
if __name__ == '__main__':
    startTime = time.time()
    ISTERM = detectTerm()
    if DEV:
        print('DEV Mode = '+str(DEV))
        print('ErrorCatchingEnabled = '+str(not STOPERRCATCHING))
        print('RunningFromTerm = '+str(ISTERM))
        print()
    print('Copywrite (c) Cat Inc.')
    print('All Rights Reserved.')
    print()
    print('Programmed by Samuel Davenport, member of Cat Inc.')
    #for when this may happen:
    #print('Programmed by Anthony Williams, based on a template')
    #print('made by Samuel Davenport, both members of Cat Inc')
    print()
    if not DEV:
        STOPERRCATCHING = False
    if not STOPERRCATCHING:
        try:
            if PREBOOTERR != 'NULL':
                if not PREBOOTERR.split()[0].lower() == 'maths':
                    raise ImportError(PREBOOTERR)
            main()
        except Exception as e:#Catch errors and make them not scary for end users
            print()
            print('An error has occored', file=os.sys.stderr)
            error = str(e)
            if error.isprintable():
                errormessage = str('ERR: %s' % error)
                print(errormessage, file=os.sys.stderr)
            print()
            if str(os.sys.platform.title()) != 'Linux':
                print('I told you there might be errors!')
                print()
        except KeyboardInterrupt:
            print()
            print('ERR: KeyboardInterrupt', file=os.sys.stderr)
        except SystemExit:
            print()
            print('ERR: SystemExit', file=os.sys.stderr)
    else:
        main()
else:
    print('Bad.')
if not DEV:
    terminate()
