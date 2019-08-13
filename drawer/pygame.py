import pygame
import sys
import random
import time
import traceback

DISPLAY_SIZE = (640, 480)

COLORS = {
    'white': (255, 255, 255),
    'black': (0, 0, 0),
    'green': (0, 200, 0),
    'blue': (0, 0, 128),
    'red': (200, 0, 0),
    'purple': (102, 0, 102)
}

DISC_COLORS = {
    'black': (0, 0, 0),
    'green': (0, 200, 0),
    'blue': (0, 0, 128),
    'red': (200, 0, 0),
    'purple': (102, 205, 170),
    'aquamarine3': (102, 0, 102),
    'azure4': (131, 139, 139),
    'burlywood': (222, 184, 135),
    'bisque2': (238, 213, 183),
    'cadetblue': (95, 158, 160),
    'chartreuse1': (127, 255, 0),
    'cornsilk1': (255, 248, 220),
    'darkgoldenrod1': (255, 185, 15),
    'darkolivegreen1': (202, 255, 112),
    'gold2': (238, 201, 0),
    'darkorange4': (139, 69, 0),
    'darkorchid1': (191, 62, 255),
    'darksalmon': (233, 150, 122),
    'gainsboro': (220, 220, 220),
}


def get_rand_disk_color():
    return DISC_COLORS[random.choice(list(DISC_COLORS.keys()))]


class Drawer:
    def __init__(self, simulator, rods, disks):
        self.simulator = simulator
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(DISPLAY_SIZE)
        self.rods = self.create_rod_figures(rods)
        self.disks = self.create_disk_figures(disks)
        self.clear_screen()
        self.draw_rods()
        pygame.display.update()

    @staticmethod
    def create_rod_figures(rods):
        rod_figures = []
        for pos, rod in enumerate(rods):
            rod_figures.append(RodFigure(rod, pos))
        return rod_figures

    @staticmethod
    def create_disk_figures(disks):
        disk_figures = {}
        for disk in disks:
            disk_figures[disk.get_size()] = DiskFigure(disk)
        return disk_figures

    def show_simulation(self):
        # clock = pygame.time.Clock()

        try:
            self.simulator.simulate(self)
        except Exception as e:
            traceback.print_exc()

        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    pygame.display.quit()
                    sys.exit()

    def clear_screen(self):
        self.screen.fill(COLORS['white'])

    def draw_rods(self):
        self.clear_screen()
        for rod in self.rods:
            self.draw_rod(rod)
        pygame.display.update()
        pygame.event.get()
        time.sleep(0.5)

    def draw_rod(self, rod):

        # draw rod itself
        pygame.draw.rect(
            self.screen,
            COLORS['black'],
            pygame.Rect(
                rod.X,
                rod.Y,
                ROD_WIDTH,
                ROD_HEIGHT
            )
        )

        # draw disks
        for disk_pos, disk in enumerate(rod.traverse_disks()):

            if disk.get_size() in self.disks:
                disk_figure = self.disks[disk.get_size()]
                pygame.draw.rect(
                    self.screen,
                    disk_figure.get_color(),
                    pygame.Rect(
                        rod.X - disk_figure.width / 2 + ROD_WIDTH / 2,
                        rod.Y + DISK_HEIGHT * disk_pos + (DISK_MAX_COUNT - len(rod)) * DISK_HEIGHT,
                        disk_figure.width,
                        disk_figure.height
                    )
                )

    # def compute_rod_position(self):


DISK_UNIT_WIDTH = 20
DISK_HEIGHT = 20
DISK_MAX_COUNT = 8


class DiskFigure:
    def __init__(self, disk):
        self.color = get_rand_disk_color()
        self.height = DISK_HEIGHT
        self.width = DISK_UNIT_WIDTH * disk.get_size()

    def get_color(self):
        return self.color


ROD_WIDTH = 10
ROD_HEIGHT = DISK_HEIGHT * DISK_MAX_COUNT
ROD_Y_OFFSET = 40
ROD_X_OFFSET = 20


class RodFigure:
    def __init__(self, rod, pos):
        self.pos = pos

        self.X = self.get_rod_offset()
        self.Y = ROD_Y_OFFSET

        self.rod = rod

    def get_rod_offset(self):
        return (DISK_UNIT_WIDTH * DISK_MAX_COUNT) * (self.pos + 1) + ROD_X_OFFSET

    def traverse_disks(self):
        for disk in self.rod.disks:
            yield disk

    def __len__(self):
        return len(self.rod)
