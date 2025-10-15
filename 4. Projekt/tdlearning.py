import re

class Value:
    def __init__(self, val, rew=False):
        self.rew = rew
        self.val = val

    def __repr__(self):
        return "%.3f"%(self.val) if not self.rew else "rew=%g"%(self.val)

    def get_rew(self):
        return 0 if not self.rew else self.val

    def get_val(self):
        return self.val if not self.rew else 0

    def set_val(self, val):
        if self.rew:
            return
        self.val = val

def parse_util_map(util_map) -> list:
    new = util_map.copy()
    for row in range(len(new)):
        for col in range(len(new[row])):
            try:
                new[row][col] = Value(float(new[row][col]))
            except:
                new[row][col] = Value(float(new[row][col].split("=")[1]), True)

    return new

def get_segment_sur(cols, segment):
    return segment // cols, segment % cols

def tdlearning(util_map, walk, a, g) -> list:
    cols = len(util_map[0])
    for i in range(len(walk)-1):
        seg1 = get_segment_sur(cols, walk[i]-1)
        seg2 = get_segment_sur(cols, walk[i+1]-1)
        seg1_val = util_map[seg1[0]][seg1[1]]
        seg2_val = util_map[seg2[0]][seg2[1]]

        value = seg1_val.get_val() + a * (seg2_val.get_rew() + g * seg2_val.get_val() - seg1_val.get_val())
        util_map[seg1[0]][seg1[1]].set_val(value)

    return util_map

if __name__ == "__main__":
    assignment = None
    with open("xslivk03.txt", "r") as f:
        assignment = f.readlines()
    assignment = "".join(assignment)
    
    re_map = re.compile(r"\n\n(.*?)\n\n", flags=re.S)
    alpha = float(re.search(r"alpha=(\d*\.?\d+)", assignment).group(1))
    gamma = float(re.search(r"gamma=(\d*\.?\d+)", assignment).group(1))
    walk = re.search(r"po\s*prochazce\s*stavy\s*(.*?)\s*a\s*vysledek", assignment).group(1)
    walk = list(map(int, walk.split()))

    print(f"{alpha=}\n{gamma=}\n{walk=}")

    maps = re_map.findall(assignment)
    indx_map = [line.split() for line in maps[0].split("\n")]
    indx_map = parse_util_map(indx_map)

    util_map = [line.split() for line in maps[1].split("\n")]
    util_map = parse_util_map(util_map)

    print("Pos:")
    for row in indx_map:
        for e in row:
            print("%6s"%(str(e).rstrip(".0")), end=" ")
        print()
    print("Before:")
    for row in util_map:
        for e in row:
            print("%6s"%(e), end=" ")
        print()
    util_map = tdlearning(util_map, walk, alpha, gamma)
    print("After:")
    for row in util_map:
        for e in row:
            print("%6s"%(e), end=" ")
        print()
