import getopt
import sys

from drawer.pygame import Drawer
from simulator import generate_source_rod, Rod, TowerSimulator


def get_opts():
    opts = {
        'disk-num': 5
    }

    input_opts, _ = getopt.getopt(sys.argv[1:], '', ['disk-num='])
    for opt_name, opt_val in input_opts:
        if opt_name == '--disk-num':
            opt_val = int(opt_val)
            if 3 <= opt_val <= 8:
                opts['disk-num'] = opt_val
                continue
            raise ValueError(f'disk-num should be an integer between 3 and 8, `{opt_val}` given')

    return opts


if __name__ == '__main__':
    opts = get_opts()
    rods = [generate_source_rod(opts['disk-num']), Rod(), Rod()]

    Drawer(TowerSimulator(rods), rods, rods[0].disks).show_simulation()
