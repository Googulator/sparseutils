# mksparse
#
# Copyright 2013-2014  Lars Wirzenius
#
# Copyright 2017 Richard Ipsum
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# =*= License: GPL-3+ =*=

DESCRIPTION = '''Create a sparse file.

This tool reads a specification for how the file is to be made sparse
from stdin: a sequence of "data" and "hole" words, which may be
interspersed with spaces, commas, or the word "a", all of which are
ignored, except that the "data" and "hole" words must have something
in between them.

For example, to create a file `foo' with 4096 bytes of data followed by
an 8192 byte hole followed by 4096 bytes of data:

echo data,hole,data | mksparse --hole-size 8192 --data-size 4096 foo

'''

import argparse
import os
import sys

DEFAULT_DATA_SIZE = 4096
DEFAULT_HOLE_SIZE = 1024 ** 2

def parse_spec():
    text = sys.stdin.read()
    # Remove commas.
    text = ' '.join(text.split(','))

    # Split into words.
    words = text.split()

    # Remove any words that are not "data" or "hole".
    spec = [x for x in words if x in ('data', 'hole')]

    return spec

def append_data(f, data_size):
    f.write('x' * data_size)
    f.flush()

def append_hole(f, hole_size):
    fd = f.fileno()
    pos = os.lseek(fd, hole_size, os.SEEK_CUR)
    os.ftruncate(fd, pos)

def main():
    parser = argparse.ArgumentParser(
                    description=DESCRIPTION,
                    formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('OUTPUT_FILE')

    parser.add_argument('--hole-size',
                        type=int,
                        metavar='SIZE',
                        default=DEFAULT_HOLE_SIZE,
                        help='hole size in bytes')

    parser.add_argument('--data-size',
                        type=int,
                        metavar='SIZE',
                        default=DEFAULT_DATA_SIZE,
                        help='data size in bytes')

    args = vars(parser.parse_args())
    spec = parse_spec()

    with open(args['OUTPUT_FILE'], 'w') as f:
        for word in spec:
            if word == 'hole':
                append_hole(f, args['hole_size'])
            else:
                assert word == 'data'
                append_data(f, args['data_size'])

if __name__ == '__main__':
    main()
