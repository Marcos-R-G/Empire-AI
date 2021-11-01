import actions
import random


def search(s1):
    depth_limit = 30
    depth = 0
    sz = []
    sz.append(s1)

    while len(sz) > 0:
        depth += 1
        s = sz.pop()
        az = actions.ACTION(s)

        if actions.GOAL(s) == True:
            print("GOAL state reached! ")
            return s
        if depth > depth_limit:
            print("Exceeded depth limit without finding goal state.  Failure. ")
            return s

        pick = random.randrange(0, len(az))
        a = az[pick]
        # s2 = state.RESULT(s, a)
        s2 = actions.RESULT(s,a)
        sz.append(s2)

        if a.mGroup == "Designate1":
            DESIGNATE_USED = True
            for command in a.mCommands:
                print("des", actions.change_tuple_to_string(a.mCommands[command][0]), a.mCommands[command][1])
        elif a.mGroup == "Network1":
            NETWORK_USED = True
            for command in a.mCommands:
                if command == "distribute":
                    print("distribute", "*", actions.change_tuple_to_string(a.mCommands[command][0]))
                else:
                    print("threshold", a.mCommands[command][0], actions.change_tuple_to_string(a.mCommands[command][1]),
                          a.mCommands[command][2])
        elif a.mGroup == "Spread1":
            SPREAD_USED = True
            for command in a.mCommands:
                print("move", a.mCommands[command][0], actions.change_tuple_to_string(a.mCommands[command][1]),
                      a.mCommands[command][2], actions.change_tuple_to_string(a.mCommands[command][3]))
        else:
            for command in a.mCommands:
                if command == "build_ship":
                    print("build ship", actions.change_tuple_to_string(a.mCommands[command][0]), str(a.mCommands[command][1]))
                else:
                    print("update")
                    print("cens *")
    return

def main():
    m = actions.openmodel()
    s1 = actions.State(None, None, m, 0)
    search(s1)
    return
main()