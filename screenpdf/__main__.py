from __future__ import absolute_import
import sys
import argparse
from .version import __version__
from .converter import Converter
import logging
from logging import getLevelName as get_level
import os.path as path

parser = argparse.ArgumentParser(
    prog='screenpdf', description='%(prog)s converts text to '
    'proper screenplay PDF format.')
parser.add_argument(
    'file', action='store', help='text file to be formated')
parser.add_argument(
    '-V', '--version', action='version',
    version='%(prog)s: v{}'.format(__version__))
log_group = parser.add_argument_group('logging arguments')
log_group.add_argument(
    '-d', '--debug', help='set verbosity level to DEBUG',
    action='store_const', dest='log_level',
    const='DEBUG', default='INFO')
log_group.add_argument(
    '-s', '--save-log', help='save log output',
    action='store_true', dest='save_log')
log_group.add_argument(
    '-q', '--quiet', help='less verbose',
    action='store_const', dest='log_level',
    const='ERROR')

args = parser.parse_args()


logger = logging.getLogger('screenpdf')
logger.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(get_level(args.log_level))
stream_formatter = logging.Formatter('%(levelname)s %(message)s')
stream_handler.setFormatter(stream_formatter)
logger.addHandler(stream_handler)

if args.save_log:
    file_handler = logging.FileHandler('screenpdf.log', 'w')
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter('''
%(asctime)s (%(name)s, line %(lineno)d)
%(levelname)s %(message)s''')
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    logger.info('Recording log file at {}'.format(
        path.abspath('screenpdf.log')))

filename = path.abspath(args.file)

spdf = ''
with open(filename, 'r') as text:
    spdf = text.read()

# [1:] removes first empty item e.g. ['', 'chars', 'dia', 'etc']
lines = [line.strip() for line in spdf.split('\\')[1:]]

converter = Converter()
functions = converter.TRANSLATOR

for line in lines:
    command, _, text = line.partition(' ')
    try:
        getattr(converter, functions.get(command, command))(text)
    except AttributeError:
        print(f"\nERROR Command '{command}' doesn't exist.")
        print(f'\\{line}\n')

sys.exit(converter.savePdf())
