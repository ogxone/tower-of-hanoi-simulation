class Rod:
    def __init__(self):
        self.disks = []

    def get_size(self):
        if len(self) > 0:
            return self.disks[0].get_size()
        return 0

    def is_not_empty(self):
        return len(self) > 0

    def add_disk(self, disk):
        self.disks.insert(disk.get_size(), disk)

    def unshift_disk(self, disk):
        self.disks.insert(0, disk)

        if len(self.disks) > 1 and self.disks[0].get_size() > self.disks[1].get_size():
            raise RuntimeError(
                f"disk of size {self.disks[0].get_size()} should not be put on disk of size {self.disks[1].get_size()}")

    def shift_disk(self):
        return self.disks.pop(0)

    def __len__(self):
        return len(self.disks)


class Disk:
    def __init__(self, size):
        self.size = int(size)

    def get_size(self):
        return self.size


class EndSimulationError(Exception):
    pass


def generate_source_rod(size):
    rod = Rod()
    for i in range(1, int(size) + 1):
        rod.add_disk(Disk(i))

    return rod


class TowerSimulator:
    def __init__(self, rods):
        self.rods = rods
        self.dim = len(rods[0])

    def simulate(self, drawer):
        self.drawer = drawer

        self.move(*self.rods)

    def move(self, frm, to, via):
        self.swap_via(frm, to, via)

        if not self.is_swappable(frm, via):
            return
        self.swap(frm, via)

        self.move(to, via, frm)
        if not self.is_swappable(frm, to):
            return
        self.swap(frm, to)
        self.move(via, frm, to)
        if not self.is_swappable(via, to):
            return
        self.swap(via, to)
        self.move(frm, to, via)

    def is_swappable(self, frm, to):
        if len(frm) == 0:
            return False

        if len(to) > 0 and frm.get_size() > to.get_size():
            return False

        return True

    def swap_via(self, frm, to, via):
        self.swap(frm, via)
        self.swap(frm, to)
        self.swap(via, to)

    def swap(self, frm, to):
        error = None

        try:
            to.unshift_disk(frm.shift_disk())
        except RuntimeError as e:
            error = e

        self.drawer.draw_rods()

        if error is not None:
            raise error

        if self.is_complete():
            raise EndSimulationError

    def is_complete(self):
        return len(self.rods[0]) == 0 and (len(self.rods[1]) == self.dim or len(self.rods[2]) == self.dim)
