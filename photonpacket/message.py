
from . import settings
from sys import stdout

def message(str, v, overwrite=None):
    '''
    Print message if verbosity is sufficient
    '''
    if overwrite == None:
        overwrite = settings.overwrite
    if v <= settings.verbose:
        if overwrite:
            stdout.write(str)
            stdout.flush()
        else:
            print(str)

def progress(i):
    '''
    Display progress message
    '''
    if settings.verbose == 0:
        pass
    elif settings.verbose == 1 and i % 100000 == 0:
        progressmessage(str(i/1000) + 'k')
    elif settings.verbose == 2 and i % 10000 == 0:
        progressmessage(str(i/1000) + 'k')
    elif settings.verbose == 3 and i % 1000 == 0:
        progressmessage(str(i/1000) + 'k')
    else:
        pass

def progressmessage(str):
    '''
    Print progress message
    '''
    if settings.overwrite:
        stdout.write("\rprogress=%s" % str)
        stdout.flush()
    else:
        print(str)