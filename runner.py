from drawer.pygame import Drawer
from simulator import generate_source_rod, Rod, TowerSimulator

if __name__ == '__main__':
    rods = [generate_source_rod(8), Rod(), Rod()]

    Drawer(TowerSimulator(rods), rods, rods[0].disks).show_simulation()
