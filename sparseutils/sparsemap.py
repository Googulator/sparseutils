# sparsemap
#
# Copyright © 2017 Richard Ipsum
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

import sys
import os
import stat
import errno
import argparse

DESCRIPTION = '''Print the structure of a sparse file to stdout.

The file is interpreted as a sequence of data and holes, for example
given a file with 8192 bytes of data followed by a 4096 byte hole followed
by 8192 bytes of data the output of sparsemap would be:

DATA 8192
HOLE 4096
DATA 8192

'''

def sparsemap(fd):

    # First of all, where are we currently, data or hole?
    end_of_file_pos = os.lseek(fd, 0, os.SEEK_END)
    what = os.SEEK_DATA
    pos = os.lseek(fd, 0, os.SEEK_HOLE)

    if pos == 0:
        what = os.SEEK_DATA # we are already in a hole
    elif pos == end_of_file_pos:
        # no holes in this file
        print('DATA', end_of_file_pos)
        return
    else:
        what = os.SEEK_HOLE # we were in data
        pos = 0

    while pos < end_of_file_pos:

        current = 'DATA' if what == os.SEEK_HOLE else 'HOLE'

        try:
            next_pos = os.lseek(fd, pos, what)
        except OSError as e:
            if e.errno == errno.ENXIO:
                # whatever we were looking for isn't in the file
                # that means that either the rest of the file is a hole or data
                print(current, end_of_file_pos - pos)
                return

        print(current, next_pos - pos)

        pos = next_pos
        what = os.SEEK_DATA if what == os.SEEK_HOLE else os.SEEK_HOLE

def main():
    parser = argparse.ArgumentParser(
                    description=DESCRIPTION,
                    formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('FILE')

    args = vars(parser.parse_args())
    path = args['FILE']

    try:
        mode = os.stat(path).st_mode
    except os.error as e:
        print("{}: Couldn't open `{}': {}".format(sys.argv[0], path, e.strerror))
        sys.exit(1)

    if not stat.S_ISREG(mode):
        print("{}: error: `{}' is not a regular file".format(sys.argv[0], path),
              file=sys.stderr)
        sys.exit(1)

    fd = os.open(path, os.O_RDONLY)
    sparsemap(fd)
    os.close(fd)

if __name__ == '__main__':
    main()
