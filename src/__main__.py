import sys

# Cleaner removes from sys.path any external libs to avoid potential
# conflicts with existing system libraries
from pyenv import Cleaner
sys.path = Cleaner.syspath()

from playbook.cli import CLI
CLI()


