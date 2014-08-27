from Queue import PriorityQueue


class State(object):
    def __init__(self, value, parent=None, goal=None):
        self.value = value
        self.parent = parent
        if parent:
            self.path = parent.path[:]
            self.path.append(value)
            self.goal = parent.goal
        else:
            self.path = [value]
            self.goal = goal

    def estimate(self):
        raise NotImplementedError

    def get_children(self):
        raise NotImplementedError

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        return hash(self.value)


class GridState(State):
    def estimate(self):
        return abs(self.value.x - self.goal.x) + abs(self.value.y - self.goal.y)

    def get_children(self):
        return [GridState(child, self) for child in self.value.neighbors if child.PASSABLE or child == self.goal]


class AStar(object):
    def __init__(self, start_state):
        self.closedset = set()
        self.openset = PriorityQueue()
        self.openset.put((0, start_state))

    def solve(self):
        while self.openset.qsize():
            priority, closest = self.openset.get(False)
            self.closedset.add(closest)
            for child in closest.get_children():
                if child not in self.closedset:
                    distance = child.estimate()
                    if not distance:
                        return child.path
                    #print child.value, distance
                    self.openset.put((distance, child))
                    #print [(p, s.value) for p, s in sorted(self.openset.queue)]

if __name__ == '__main__':
    from board import Board

    board = Board(4)
    board.update('  ####    ####      ##          ')

    print AStar(GridState(board[0][0], goal=board[0][3])).solve()
