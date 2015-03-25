import sys
import os
def PATH(*args):
	return os.sep.join([str(x) for x in args])

if __name__ == 'phosida.phosida':
	ABSPATH = os.path.abspath('phosida')
else:
	ABSPATH = os.path.abspath(os.path.dirname(sys.argv[0]))
sys.path.append(PATH(ABSPATH, '..'))
#Need to add this for models objects to work
sys.path.append(PATH(ABSPATH, '..', '..'))

import bacil_parser
import ecoli_parser
import humocell_parser
import humoegf_parser
import lact_parser
import musphoini1_parser
import musphoini2_parser
import musphoini_parser

def parse():
    print 'bacil_parser'
    bacil_parser.parse()
    print 'ecoli_parser'
    ecoli_parser.parse()
    print 'humocell_parser'
    humocell_parser.parse()
    print 'humoegf_parser'
    humoegf_parser.parse()
    print 'lact_parser'
    lact_parser.parse()
    print 'musphoini1_parser'
    phosida.musphoini1_parser.parse()
    print 'musphoini2_parser'
    phosida.musphoini2_parser.parse()
    print 'musphoini_parser'
    phosida.musphoini_parser.parse()
if __name__ == '__main__':
	parse()
