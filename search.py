import actions
from actions import action
from actions import State
from actions import Model
import random
# def search(initial_state, limit):
#   Q = []
#   Q.append(initial_state)
#   while len(Q) != 0:
#     s = Q.pop()
#     # m = Model_Actions()
#     if actions.GOAL(s):
#       return s
#     if s.depth >= limit:
#         continue
#     for a in actions.ACTION(s):
#       Q.insert(actions.RESULT(s,a))
#
#   return

def search(initial_state, limit):

    sz = []
    sz.append(initial_state)
    astate = actions.ACTION(initial_state)
    i = 0

    while len(sz) > 0:
        initial_state.depth += 1
        s = sz.pop()
        # az = actions.ACTION(s)

        if actions.GOAL(s):
            print("GOAL state reached! ")
            return s
        if initial_state.depth > limit:
            print("Exceeded 100 actions.")
            return s
        for a in actions.ACTION(s):
            if a.mGroup == "Designate1":
                actions.DESIGNATE_USED = True
                for command in a.mCommands:
                    print("des", actions.change_tuple_to_string(a.mCommands[command][0]), a.mCommands[command][1])

            elif a.mGroup == "Network1":
                actions.NETWORK_USED = True
                for command in a.mCommands:
                    if command == "distribute":
                        print("distribute", "*", actions.change_tuple_to_string(a.mCommands[command][0]))
                    else:
                        print("threshold", a.mCommands[command][0], actions.change_tuple_to_string(a.mCommands[command][1]),
                              a.mCommands[command][2])
            elif a.mGroup == "Spread1":
                actions.SPREAD_USED = True
                for command in a.mCommands:
                    print("move", a.mCommands[command][0], actions.change_tuple_to_string(a.mCommands[command][1]),
                          a.mCommands[command][2], actions.change_tuple_to_string(a.mCommands[command][3]))
            else:
                for command in a.mCommands:
                    if command == "build_ship":
                        print("build ship", actions.change_tuple_to_string(a.mCommands[command][0]),
                              str(a.mCommands[command][1]))
                    else:
                        print("update")
                        print("cens *")

    return

#chmod 755 *
# def search(s1):
#     sz = []
#     sz.append(s1)
#     s = sz[0]
#     az = actions.ACTION(s)
#     for i in range(len(az)):
#         if az[i].getGroup == "Designate1":
#             s = sz.pop()
#             s2 = actions.RESULT(s, az[pickl])
#             sz.append(s2)
#     while len(sz) > 0:
#         s = sz.pop()
#         az = actions.ACTION(s)
#
#         if actions.GOAL(s):
#             print("GOAL state reached! ")
#             return s
#
#         pick = random.randrange(0,len(az))
#         a = az[pick]
#
#         #print(a.getGroup())
#
#         s2 = actions.RESULT(s, a)
#         sz.append(s2)
#     return
# def search(s1, limit):


def main():
    m = actions.openmodel()
    s1 = actions.State(None, None, m, 0)

    search(s1,50)
    # print("fasdfjdsaks")
    # print(s1)
    return

main()