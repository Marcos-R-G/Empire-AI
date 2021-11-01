#!/usr/bin/env python3


import os
import pickle
import math
import copy
# import parse

f = open("sectors.p", "rb")
sectors = pickle.load(f)
f.close()

f2 = open("ship_sectors.p", "rb")
ship_sectors = pickle.load(f2)
f.close()

def dictAll(words):
    dictAll = {}
    listOfMeaning = ["uid", "owner", "xloc", "yloc", "type", "effic", "mobil", "off", "tech", "opx", "opy", "mission", "radius", "fleet", "civil", "milit", "shell", "gun", "petrol", "iron", "dust", "bar", "food", "oil", "lcm", "hcm", "uw", "rad", "access", "name", "rflags", "rpath"]
    for i in range(len(listOfMeaning)):
        dictAll[listOfMeaning[i]] = words[i]
    return dictAll

class Model:
    def __init__(self, s,b):
        self.sectors = s
        self.ship_sectors = b

        # self.Nusectors = len(self.sectors)
        # self.NumShips = len(self.ship_sectors)

        self.mStarvation = False
        self.mBuiltShip = False

        self.capital = ""
        for key in sectors:
            ##print(key)
            if sectors[key]["des"] == 5:
                self.mCapital = key

        largest = 0
        for key in self.ship_sectors:
            if int(key) > largest:
                largest = int(key)

        self.mNextID = largest


        self.fishing = 0
        self.mTrackedCommodities = {"civil": "c_dist", "food": "f_dist", "iron": "i_dist", "lcm": "l_dist",
                                    "hcm": "h_dist"}
        self.mTrackedWeights = {'food': 1, "iron": 1, "lcm": 1, "hcm": 1, "civil": 1}
        self.mTrackedDesignations = {"c": "5", "h": "12", "m": "10", "a": "15", "k": "18", "j": "17"}
        self.mShipTypes = {"frg": {"lcm": "30", "hcm": "30", "type": "6"}, "fb": {"lcm": 25, "hcm": 15, "type": "0"}}
    #
    # def RESULT(s1, a):  # -> s2 |returns new state with copy of model after applying commands of Action a
    #     # consider using copy.deepcopy
    #     playmodel = copy.deepcopy(s1.mModel)
    #     newmodel = a.apply(playmodel)
    #     s2 = State(s1, a, newmodel, s1.mPathCost)  # correct path cost will be calculated in class init
    #     return s2
    def getSectors(self):
        return self.sectors
    def move(self, comm,fromsect, numtoMove, tosect):
        if comm not in self.mTrackedCommodities:
            print("Error in Model.move:", comm, "not a tracked commodity. ")
            return False
        if fromsect not in self.sectors:
            print("Error in Model.move:", fromsect, "not an owned sector. ")
            return False
        if tosect not in self.sectors:
            print("Error in Model.move:", tosect, "not an owned sector.")
            return False
        if int(self.sectors[fromsect][comm]) < numtoMove:
            print("Not enough", comm, "in", fromsect, "to move", numtoMove, comm, "moving", self.sectors[fromsect][comm],
                  "instead. ")
        num = int(self.sectors[fromsect][comm])


        eff = self.getEffic(fromsect)
        # comms = {"food": 1 , "iron": 1, "hcm": 1 , "lcm": 1, "civil": 1 }

        # mob cost = (amount) * (weight) * (path cost) / (source packing bonus)

        if eff < 60:
            sourceBonus = 1
        elif self.sectors[fromsect]["des"] == "12":
            sourceBonus = 10
        elif self.sectors[fromsect]["des"] == "12" and comm == "civ":
            sourceBonus = 10
        else:
            sourceBonus = 1

        mobil = int(self.sectors[fromsect]["mobil"])

        path_cost = (abs(float(self.sectors[tosect]["yloc"]) - float(self.sectors[fromsect]["yloc"])) + abs(
            float(self.sectors[tosect]["xloc"]) - float(self.sectors[fromsect]["xloc"]))) / 2.0
        mcost = num * path_cost / sourceBonus

        while mcost > mobil:
            mcost = num * path_cost / sourceBonus
            num -= 1
        mobil -= mcost

        self.sectors[fromsect][comm] -= num
        self.sectors[fromsect][comm] += num

        return True



        # pathCost = |y2-y1| + (|x2-x1|)/2
        # x1 = int(self.sectors[fromsect]["xloc"])
        # x2 = int(self.sectors[tosect]["xloc"])
        # y1 = int(self.sectors[fromsect]["yloc"])
        # y2 = int(self.sectors[tosect]["yloc"])
        #
        # pathCost = abs(y2 - y1) \
        #            + (abs(x2 - x1)) / 2
        #
        # mobCost = numtoMove * comms[comm] * (pathCost * .4) / sourceBonus
        # mobility = int(self.sectors[fromsect]["mobil"])
        # mobility2 = mobility
        # mobility -= mobCost


        # if mobility < 0:
        #     mobility = 0
        #     fromCivs = int(int(self.sectors[fromsect]["civil"]) /mobility2)
        #     fromsend = str(int(self.sectors[fromsect]["civil"]) - fromCivs)
        #     self.sectors[fromsect]["civil"] = fromsend
        #
        #     fromsend = str(int(self.sectors[tosect]["civil"]) + fromCivs)
        #     self.sectors[tosect]["civil"] = fromsend
        #
        # else:
        #     fromCivs = int(int(self.sectors[fromsect]["civil"]) / mobility)
        #
        #     fromsend = str(int(self.sectors[fromsect]["civil"]) - fromCivs)
        #     self.sectors[fromsect]["civil"] = fromsend
        #
        #     fromsend = str(int(self.sectors[tosect]["civil"]) + fromCivs)
        #     self.sectors[tosect]["civil"] = fromsend
        #
        # self.sectors[fromsect]["mobil"] = str(mobility)




    def getEffic(self, sector):
        x = self.sectors[sector]["effic"]
        return int(x)


    def designate(self,sect, type):
        if sect not in self.sectors:
            print("Error in Model.designate:", sect, "not an owned sector. ")
            return False
        if type not in self.mTrackedDesignations:
            print("Error in Model.designate:", type, "not a tracked designation. ")
            return False
        if type == "h" or "harbor":
            if self.sectors[sect]["coastal"] != "1":
                print("Error in Model.designate: harbors must be placed on the coast. ")
                return False

        self.sectors[sect]["newdes"] = self.mTrackedDesignations[type]

        if int(self.sectors[sect]["effic"]) < 5:
            self.sectors[sect]["des"] = self.sectors[sect]["newdes"]
            self.sectors[sect]["effic"] = "0"
        return True

        # eff = self.getEffic(sector)
        # types = {'h': "12", "m": "10", "c": "5", "j": "17","k": "18", "a": "15"}
        # if type in types:
        #     if self.sectors[sector]["des"] != type:
        #         # if type == "h" and self.sectors[sector]["coastal"] == "1":
        #         if type != "h":
        #             if eff < 5:
        #                 self.sectors[sector]["des"] = types[type]
        #             self.sectors[sector]["newdes"] = types[type]
        #             return
        #         if eff < 5:
        #             if self.sectors[sector]["coastal"] == "1":
        #                 self.sectors[sector]["des"] = types["h"]
        #             print("sector is not coastal")
        #             return
        #         if self.sectors[sector]["coastal"] == "1":
        #             self.sectors[sector]["newdes"] = types["h"]
        #             return
        #         print("sector is not coastal")
        #         return
        #
        # print("type is incorrect")
        # return

    # fb   fishing boat          25  15    75    0 $180
    # frg  frigate               30  30   110    0 $600

    def threshold(self, comm,sect, thresh):
        if comm not in self.mTrackedCommodities:
            print("Error in Model.threshold:", comm, "not a tracked commodity. ")
            return False
        if sect not in self.sectors:
            print("Error in Model.threshold:", sect, "not an owned sector. ")
            return False
        if thresh < 0 or thresh > 9999:
            print("Error in Model.threshold: value out of accepted bounds. (0-9999) ")
            return False

        self.sectors[sect][self.mTrackedCommodities[comm]] = thresh

        return True




    def distribute(self, sect):
        # sets sect as distribution point for all sectors, assumes * input
        if sect not in self.sectors:
            print("Error in Model.distribute:", sect, "is not an owned sector. ")
            return False
        for key in self.sectors:
            self.sectors[key]["xdist"] = self.sectors[sect]["xloc"]
            self.sectors[key]["ydist"] = self.sectors[sect]["yloc"]
        return

    def shipDict(self, words):
        dictShip = {}
        str(words)
        listOfMeaning = ["uid", "owner", "xloc", "yloc", "type", "effic", "mobil", "off", "tech", "opx", "opy", "mission", "radius", "fleet", "civil", "milit", "shell", "gun", "petrol", "iron", "dust", "bar", "food", "oil", "lcm", "hcm", "uw", "rad", "access", "name", "rflags", "rpath"]
        for i in range(len(listOfMeaning)):
            x = words.split(" ")
            dictShip[listOfMeaning[i]] = x[i]
        return dictShip

    def build_ship(self,sect, ship):
        if sect not in self.sectors:
            print("Error in Model.build_ship:", sect, "not an owned sector. ")
            return False
        if self.sectors[sect]["des"] != "12":
            print("Error in Model.build_ship: ships must be built in a harbor. ")
            return False
        if ship not in self.mShipTypes:
            print("Error in Model.build_ship:", ship, "not an accepted ship type. ")
            return False

        if int(float(self.sectors[sect]["lcm"])) < int(float(self.mShipTypes[ship]["lcm"])):
            print("Error in Model.build_ship: not enough lcm to build ship. ")
            return False
        if int(float(self.sectors[sect]["hcm"])) < int(float(self.mShipTypes[ship]["hcm"])):
            print("Error in Model.build_ship: not enough hcm to build ship. ")
            return False

            # {'uid': '31', 'owner': '54', 'xloc': '-1', 'yloc': '-1', 'type': '0', 'effic': '100', 'mobil': '127', 'off': '0', 'tech': '9', 'opx': '-10', 'opy': '0', 'mission': '0', 'radius': '0', 'fleet': '""', 'civil': '0', 'milit': '0', 'shell': '0', 'gun': '0', 'petrol': '0', 'iron': '0', 'dust': '0', 'bar': '0', 'food': '0', 'oil': '0', 'lcm': '0', 'hcm': '0', 'uw': '0', 'rad': '0', 'access': '0', 'name': '""', 'rflags': '0', 'rpath': '""'}
        self.mNextID += 1
        words = [str(self.mNextID), "54", self.sectors[sect]["xloc"], self.sectors[sect]["yloc"],
                 self.mShipTypes[ship]["type"], "20", "127", "0", "9", "-10", "0", "0", "0", "", "0", "0", "0", "0",
                 "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "", "0", ""]

        new_ship = dictAll(words)
        self.ship_sectors[self.mNextID] = new_ship
        # print(self.mShips[self.mNextID])

        new_lcm = int(float(self.sectors[sect]["lcm"])) - int(float(self.mShipTypes[ship]["lcm"]))
        new_hcm = int(float(self.sectors[sect]["hcm"])) - int(float(self.mShipTypes[ship]["hcm"]))

        self.sectors[sect]["lcm"] = str(new_lcm)
        self.sectors[sect]["hcm"] = str(new_hcm)

        self.mBuiltShip = True
        return True

        # shipTypes = {"frg":{"lcm":"30","hcm":"30", "type":"6"},"fb":{"lcm":25,"hcm":15, "type": "0"}}
        # newUID = 68
        #
        # if sect not in self.sectors:
        #     print(sect, "Is not Currently Owned")
        #     return
        # if self.sectors[sect]["des"] != "12":
        #     print("ships must be built in a harbor. ")
        #     return
        # if ship not in shipTypes:
        #     print(ship, "is not an a correct ship type ")
        #     return
        #
        # if int(self.sectors[sect]["lcm"]) < int(shipTypes[ship]["lcm"]):
        #     print("not enough lcm to build ship. ")
        #     return
        # if int(self.sectors[sect]["hcm"]) < int(shipTypes[ship]["hcm"]):
        #     print("not enough hcm to build ship. ")
        #     return
        #
        # # if int(self.sectors[sect]['effic']) < 20:   ---------- talk to dawson
        #
        # words = str( str(newUID) + " " + self.sectors[sect]["owner"] + " " +  self.sectors[sect]["xloc"] + " " + self.sectors[sect]["yloc"]
        #             + " " + shipTypes[ship]["type"] + " 20 127 0 9 -10 0 0 0 \"\" 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 \"\" 0 \"\"")
        #
        # new_ship = self.shipDict(words)
        # self.ship_sectors[newUID] = new_ship
        # newUID += 1
        # self.fishing +=1
        #
        #
        # new_lcm = int(self.sectors[sect]["lcm"]) - int(shipTypes[ship]["lcm"])
        # new_hcm = int(self.sectors[sect]["hcm"]) - int(shipTypes[ship]["hcm"])
        #
        # self.sectors[sect]["lcm"] = str(new_lcm)
        # self.sectors[sect]["hcm"] = str(new_hcm)

    def capital(self, sect):
        if sect not in self.sectors:
            print("Error in Model.capital:", sect, "not an owned sector. ")
            return False
        if self.sectors[sect]["des"] != "5":
            print("Error in Model.capital:", sect, "does not have correct designation to become capital (c). ")
            return False

        self.mCapital = sect
        return True

    def update(self):
        self.mStarvation = False
        etu = 60

        ##set availability
        for sec in self.sectors:
            self.sectors[sec]["avail"] = str(int(math.floor((float(self.sectors[sec]["civil"]) * float(
                self.sectors[sec]["work"]) / 100.0 + float(self.sectors[sec]["milit"]) / 2.5 + float(
                self.sectors[sec]["uw"])) * etu / 100.0)))

        ##refill mobility
        for sec in self.sectors:
            if int(float(self.sectors[sec]["mobil"])) < 127:
                self.sectors[sec]["mobil"] = str(float(self.sectors[sec]["mobil"]) + 60)
                if int(float(self.sectors[sec]["mobil"])) > 127:
                    self.sectors[sec]["mobil"] = "127"

        # food consumption
        for sec in self.sectors:
            civ = float(self.sectors[sec]["civil"])
            consumed = math.floor(civ * .035)
            sec_food = float(self.sectors[sec]["food"])
            remaining = sec_food - consumed
            if remaining < 0:
                remaining = 0
            self.sectors[sec]["food"] = str(remaining)

        # set efficiency
        for sec in self.sectors:
            avail = float(self.sectors[sec]["avail"])
            avail = avail / 2 * 100
            if self.sectors[sec]["newdes"] != self.sectors[sec]["des"]:
                b = 4 * avail / 100
                if b < float(self.sectors[sec]["effic"]):
                    self.sectors[sec]["effic"] = str(float(self.sectors[sec]["effic"]) - b)
                else:
                    b = float(self.sectors[sec]["effic"])
                    self.sectors[sec]["effic"] = "0"
                    self.sectors[sec]["des"] = self.sectors[sec]["newdes"]
                avail -= b / 4 * 100

                if self.sectors[sec]["newdes"] == self.sectors[sec]["des"]:
                    change = avail / 100
                    b = min(change, 100 - float(self.sectors[sec]["effic"]))
                    self.sectors[sec]["effic"] = str(math.floor(b))
                    avail -= b * 100

                self.sectors[sec]["avail"] = str(float(self.sectors[sec]["avail"]) / 2 + avail / 100)

        for key in self.ship_sectors:
            etus = 60
            mobil = int(float(self.ship_sectors[key]["mobil"]))
            # print(key, self.mShips[key]["effic"])
            effic = int(float(self.ship_sectors[key]["effic"]))
            civ = int(float(self.ship_sectors[key]["civil"]))
            sector = (int(float(self.ship_sectors[key]["xloc"])), int(float(self.ship_sectors[key]["yloc"])))
            sector_fertility = int(float(self.sectors[sector]["fert"]))
            food = int(float(self.ship_sectors[key]["food"]))
            grate = 2.0

            mobil += etus
            if mobil > 127:
                mobil = 127
            effic += etus
            if effic > 100:
                effic = 100
            food += etus * civ * sector_fertility / 10000
            food -= etus * civ * grate
            self.ship_sectors[key]["mobil"] = mobil
            self.ship_sectors[key]["effic"] = effic
            self.ship_sectors[key]["civil"] = civ
            self.ship_sectors[key]["food"] = food

        # natural resources
        for sec in self.sectors:
            if float(self.sectors[sec]["effic"]) > 60:
                if self.sectors[sec]["des"] == self.mTrackedDesignations["m"]:
                    eff = float(self.sectors[sec]["effic"]) / 100
                    eff *= (float(self.sectors[sec]["min"]) / 100)
                    consumed = (float(self.sectors[sec]["avail"]) * eff)

                    output = consumed * eff
                    self.sectors[sec]["iron"] = str(float(self.sectors[sec]["iron"]) + output)
                    self.sectors[sec]["avail"] = str(float(self.sectors[sec]["avail"]) - math.floor(consumed / eff))

                    if eff > 0:
                        self.sectors[sec]["avail"] = str(
                            float(self.sectors[sec]["avail"]) - math.floor(consumed / eff))

                elif self.sectors[sec]["des"] == self.mTrackedDesignations["a"]:
                    eff = float(self.sectors[sec]["effic"]) / 100
                    eff *= (float(self.sectors[sec]["fert"]) / 100)
                    consumed = float(self.sectors[sec]["avail"]) * eff

                    output = consumed * eff
                    self.sectors[sec]["food"] = str(float(self.sectors[sec]["food"]) + output)

                    if eff > 0:
                        self.sectors[sec]["avail"] = str(
                            float(self.sectors[sec]["avail"]) - math.floor(consumed / eff))

        # produce items
        for sec in self.sectors:
            if float(self.sectors[sec]["effic"]) > 60:
                if self.sectors[sec]["des"] == self.mTrackedDesignations["k"]:
                    # hcms
                    eff = float(self.sectors[sec]["effic"]) / 100
                    eff *= float(self.sectors[sec]["iron"]) / 100
                    possible_from_workers = float(self.sectors[sec]["avail"]) * eff
                    if float(self.sectors[sec]["iron"]) > 9999.0:
                        self.sectors[sec]["iron"] = "9999"
                    elif float(self.sectors[sec]["iron"]) < 0:
                        self.sectors[sec]["iron"] = "0"
                    print(float(self.sectors[sec]["iron"]))
                    materials = math.floor(float(self.sectors[sec]["iron"]) / 2)
                    # materials = float(self.sectors[sec]["iron"]) / 2
                    consumed = 0
                    if possible_from_workers < materials:
                        consumed = possible_from_workers
                    else:
                        consumed = materials
                    output = consumed * eff
                    self.sectors[sec]["iron"] = str(float(self.sectors[sec]["iron"]) - output)
                    self.sectors[sec]["hcm"] = str(float(self.sectors[sec]["hcm"]) - output)
                    if eff > 0:
                        self.sectors[sec]["avail"] = str(
                            float(self.sectors[sec]["avail"]) - math.floor(consumed / eff))

            if float(self.sectors[sec]["effic"]) > 60:
                if self.sectors[sec]["des"] == self.mTrackedDesignations["j"]:
                    # lcms
                    eff = float(self.sectors[sec]["effic"]) / 100
                    eff *= float(self.sectors[sec]["iron"]) / 100
                    possible_from_workers = float(self.sectors[sec]["avail"]) * eff
                    # math.floor around floatself.msectors in next line
                    if float(self.sectors[sec]["iron"]) > 9999.0:
                        self.sectors[sec]["iron"] = "9999"
                    elif float(self.sectors[sec]["iron"]) < 0:
                        self.sectors[sec]["iron"] = "0"
                    materials = math.floor(float(self.sectors[sec]["iron"]) / 2)
                    print(materials)
                    consumed = 0
                    if possible_from_workers < materials:
                        consumed = possible_from_workers
                    else:
                        consumed = materials
                    output = consumed * eff
                    self.sectors[sec]["iron"] = str(float(self.sectors[sec]["iron"]) - output)
                    self.sectors[sec]["lcm"] = str(float(self.sectors[sec]["lcm"]) - output)
                    if eff > 0:
                        self.sectors[sec]["avail"] = str(
                            float(self.sectors[sec]["avail"]) - math.floor(consumed / eff))

        # population
        grate = 2.0

        for sec in self.sectors:
            civ = float(self.sectors[sec]["civil"])
            food = float(self.sectors[sec]["food"])
            required = math.floor(civ * .035)

            if food >= required:
                civ += civ * grate
                if civ > 1000:
                    civ = 1000
                self.sectors[sec]["civil"] = str(float(civ))
            else:
                falta = required - food
                starved = math.floor(falta / .035)
                now = civ - starved
                if now < 0:
                    now = 0
                self.sectors[sec]["civil"] = str(now)

                self.mStarvation = True  # FAIL state, starvation occuring
                print("Starvation in sector: ", self.sectors[sec]["xloc"], ",", self.sectors[sec]["yloc"])

        # distribution

        for source in self.sectors:
            for com in self.mTrackedCommodities:
                # test for key error
                # print("Source: ", source)
                # print("Com: ", com)
                # print("Sectors.source: ", self.sectors[source])
                # print("Tracked.com: ", self.mTrackedCommodities[com])
                # print("All: ", self.sectors[source][self.mTrackedCommodities[com]])
                thresh = float(self.sectors[source][self.mTrackedCommodities[com]])
                if thresh > 0:
                    item = com
                    amount = float(self.sectors[source][com])
                    if amount > thresh:
                        # dist = "(" + self.sectors[source]["xdist"] + ", " + self.sectors[source]["ydist"] + ")"
                        dist = (int(self.sectors[source]["xdist"]), int(self.sectors[source]["ydist"]))
                        diff = thresh - amount
                        if diff > 0:
                            current = float(self.sectors[source][item])
                            sx = int(self.sectors[source]["xloc"])
                            sy = int(self.sectors[source]["yloc"])
                            dx = int(self.sectors[source]["xdist"])
                            dy = int(self.sectors[source]["ydist"])
                            distance = (abs(dy - sy) + abs(dx - sx)) // 2
                            path_cost = distance * .4
                            mcost = path_cost / 10 * self.mTrackedWeights[item] / 10
                            secmob = float(self.sectors[source]["mobil"])
                            if mcost > secmob:
                                print("Not enough mobility in", source, "for distribute. ")
                            else:
                                nmob = secmob - mcost
                                new_amount = current - diff
                                if new_amount < 0:
                                    print("Not enough", item, "in", source, "for distribute. ")
                                else:
                                    self.sectors[source][item] = str(new_amount)
                                    self.sectors[source]["mobil"] = str(nmob)
                                    dist_current = float(self.sectors[dist][item])
                                    new_dist_amount = dist_current + diff
                                    if new_dist_amount > 9999:
                                        new_dist_amount = 9999
                                    self.sectors[dist][item] = str(new_dist_amount)

        for sec in self.sectors:
            for com in self.mTrackedCommodities:
                # test for key error
                # print("Sec: ", sec)
                # print("Com: ", com)
                # print("Tracked.com: ", self.mTrackedCommodities[com])
                # print("All: ", self.sectors[sec][self.mTrackedCommodities[com]])
                thresh = float(self.sectors[sec][self.mTrackedCommodities[com]])
                if thresh > 0:
                    item = com
                    amount = float(self.sectors[sec][item])
                    if amount < thresh:
                        dist = (int(self.sectors[sec]["xdist"]), int(self.sectors[sec]["ydist"]))
                        diff = thresh - amount
                        if diff > 0:
                            # key error test
                            # for key in self.sectors:
                            #    print(key)
                            # print(dist)
                            # print(item)
                            # print(self.sectors[dist])
                            # print(self.sectors[dist][item])
                            current = float(self.sectors[dist][item])
                            sx = int(self.sectors[sec]["xloc"])
                            sy = int(self.sectors[sec]["yloc"])
                            dx = int(self.sectors[dist]["xdist"])
                            dy = int(self.sectors[dist]["ydist"])
                            distance = (abs(dy - sy) + abs(dx - sx)) // 2
                            path_cost = distance * .4
                            mcost = path_cost / 10 * self.mTrackedWeights[item] / 10
                            secmob = float(self.sectors[dist]["mobil"])
                            if mcost > secmob:
                                print("Not enough mobility in", dist, "for distribute. ")
                            else:
                                nmob = secmob - mcost
                                new_amount = current - diff
                                if new_amount < 0:
                                    print("Not enough", item, "in", dist, "for distribute. ")
                                else:
                                    self.sectors[dist][item] = str(new_amount)
                                    self.sectors[dist]["mobil"] = str(nmob)
                                    dist_current = float(self.sectors[sec][item])
                                    new_dist_amount = dist_current + diff
                                    if new_dist_amount > 9999:
                                        new_dist_amount = 9999
                                    self.sectors[sec][item] = str(new_dist_amount)

class State():

    def __init__(self,parent, action, Model, path_cost):
        self.mParentState = parent
        self.mFromAction = action
        self.mModel = Model
        if action != None:
            self.mPathCost = path_cost + action.STEP_COST(parent, self.mFromAction, self)
        else:
            self.mPathCost = path_cost
        self.depth = 1

def change_tuple_to_string(tup):
    tupstring = str(tup)
    allneg = False
    firneg = False
    secneg = False
    noneg = True
    if tupstring[1] == "-":
        firneg = True
    else:
        firneg = False
    if tupstring[5] == "-" or tupstring[4] == "-":
        secneg = True
    else:
        secneg = False
    if firneg and secneg:
        allneg = True
    else:
        allneg = False
    if not firneg and not secneg:
        noneg = True
    else:
        noneg = False

    firp = 0
    if allneg:
        # (-0, -0)
        firn = 1
        xco = 2
        com = 3
        space = 4
        secn = 5
        yco = 6
        secp = 7
        new_string = tupstring[firn] + tupstring[xco] + tupstring[com] + tupstring[secn] + tupstring[yco]
    elif firneg and not secneg:
        # (-0, 0)
        firn = 1
        xco = 2
        com = 3
        space = 4
        yco = 5
        secp = 6
        new_string = tupstring[firn] + tupstring[xco] + tupstring[com] + tupstring[yco]
    elif secneg and not firneg:
        # (0, -0)
        xco = 1
        com = 2
        space = 3
        secn = 4
        yco = 5
        secp = 6
        new_string = tupstring[xco] + tupstring[com] + tupstring[secn] + tupstring[yco]
    else:
        # (0, 0)
        xco = 1
        com = 2
        space = 3
        yco = 4
        secp = 5
        new_string = tupstring[xco] + tupstring[com] + tupstring[yco]
    return new_string







class action():


    def __init__(self, group, commands):
        self.mCommands = commands
        self.mGroup = group

    def apply(self, model):
        if self.mGroup == "Designate1":
            DESIGNATE_USED = True
            for command in self.mCommands:
                getattr(model, command[:-1])(*self.mCommands[command])
        elif self.mGroup == "Network1":
            NETWORK_USED = True
            for command in self.mCommands:
                if command == "distribute":
                    getattr(model, command)(*self.mCommands[command])
                else:
                    getattr(model, command[:-1])(*self.mCommands[command])
        elif self.mGroup == "Spread1":
            SPREAD_USED = True
            for command in self.mCommands:
                getattr(model, command[:-1])(*self.mCommands[command])
        else:
            for command in self.mCommands:
                getattr(model, command)(*self.mCommands[command])

        return model


    def getGroup(self):
        return self.mGroup

    def getCommands(self):
        return self.mCommands

    def STEP_COST(self, s1, a, s2):
        sc = 0
        commands = 0
        for command in self.getCommands():
            if command == "update":
                sc += 1.0
            else:
                commands += 1
        sc += commands * 0.01
        return sc


def ACTION(s):  # -> [a1, a2, ...] |list of possible actions to take in state s
    # Designate1, Spread1, Network1, Update, and BuildFishingBoat
    m = s.mModel
    actions = []

    sector_list = []



    need_designate1 = True
    allow_designate1 = True
    city1 = 0
    city2 = 0
    harbor = 0
    farm1 = 0
    farm2 = 0
    farm3 = 0
    mine1 = 0
    mine2 = 0
    light = 0
    heavy = 0
    city1_found = False
    harbor_found = False
    onefarm = False
    twofarm = False
    onemine = False
    for sector in m.sectors:
        if m.sectors[sector]["des"] == m.mTrackedDesignations["h"]:
            need_designate1 = False
            harbor = sector
        elif m.sectors[sector]["des"] == m.mTrackedDesignations["a"]:
            if twofarm:
                farm3 = sector
            elif onefarm:
                farm2 = sector
                twofarm = True
            else:
                need_designate1 = False
                farm1 = sector
                onefarm = True
        elif m.sectors[sector]["des"] == m.mTrackedDesignations["m"]:
            if onemine:
                mine2 = sector
            else:
                need_designate1 = False
                mine1 = sector
                onemine = True
        elif m.sectors[sector]["des"] == m.mTrackedDesignations["j"]:
            need_designate1 = False
            light = sector
        elif m.sectors[sector]["des"] == m.mTrackedDesignations["k"]:
            need_designate1 = False
            heavy = sector

    for sector in m.sectors:
        if m.sectors[sector]["des"] == m.mTrackedDesignations["c"] and not city1_found:
            city1 = sector
            city1_found = True
        elif m.sectors[sector]["des"] == m.mTrackedDesignations["c"] and city1_found:
            city2 = sector
        else:
            sector_list.append(sector)

    if need_designate1 and allow_designate1:
        coastal_list = []
        for sector in sector_list:
            if m.sectors[sector]["coastal"] == "1":
                coastal_list.append(sector)

        resources = 2000000000.0

        for sector in coastal_list:
            if float(m.sectors[sector]["min"]) + float(m.sectors[sector]["fert"]) < resources:
                harbor = sector
                resources = float(m.sectors[sector]["min"]) + float(m.sectors[sector]["fert"])
                harbor_found = True

        for i in range(len(sector_list)):
            if sector_list[i] == harbor:
                index = i

        sector_list.pop(index)

        fert = 0

        for i in range(len(sector_list)):
            if float(m.sectors[sector_list[i]]["fert"]) > fert:
                fert = float(m.sectors[sector_list[i]]["fert"])
                farm1 = sector_list[i]
                index = i

        sector_list.pop(index)

        min = 0

        for i in range(len(sector_list)):
            if float(m.sectors[sector_list[i]]["min"]) > min:
                fert = float(m.sectors[sector_list[i]]["min"])
                mine1 = sector_list[i]
                index = i

        sector_list.pop(index)

        fert = 0

        for i in range(len(sector_list)):
            if float(m.sectors[sector_list[i]]["fert"]) > fert:
                fert = float(m.sectors[sector_list[i]]["fert"])
                farm2 = sector_list[i]
                index = i

        sector_list.pop(index)

        min = 0

        for i in range(len(sector_list)):
            if float(m.sectors[sector_list[i]]["min"]) > min:
                fert = float(m.sectors[sector_list[i]]["min"])
                mine2 = sector_list[i]
                index = i

        sector_list.pop(index)

        fert = 0

        for i in range(len(sector_list)):
            if float(m.sectors[sector_list[i]]["fert"]) > fert:
                fert = float(m.sectors[sector_list[i]]["fert"])
                farm3 = sector_list[i]
                index = i

        sector_list.pop(index)

        light = sector_list[0]
        heavy = sector_list[1]

        designate1 = action("Designate1",
                            {"designate2": [harbor, "h"], "designate3": [mine1, "m"], "designate4": [mine2, "m"],
                             "designate5": [light, "j"], "designate6": [heavy, "k"], "designate7": [farm1, "a"],
                             "designate8": [farm2, "a"], "designate9": [farm3, "a"]})
        if allow_designate1 and need_designate1:
            actions.append(designate1)  # ADDS TO ACTION LIST

    #   Spread1
    allow_spread1 = False
    harbor_exists = False
    need_spread1 = False
    need_list = []
    for sector in m.sectors:
        if m.sectors[sector]["des"] == m.mTrackedDesignations["h"]:
            harbor_exists = True
            harbor = sector
        if float(m.sectors[sector]["civil"]) < 50.0:
            need_spread1 = True
            need_list.append(sector)
    if harbor_exists:
        if float(m.sectors[city1]["food"]) > 200 and float(m.sectors[city1]["civil"]) > 300 and float(
                m.sectors[city2]["food"]) > 200 and float(m.sectors[city2]["civil"]) > 300:
            allow_spread1 = True

    indices = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p"]

    if allow_spread1:
        spread1_innards = {}
        for i in range(len(need_list)):
            if i < 4:
                key = "move" + str(i)
                spread1_innards[key] = ["food", city1, 20, need_list[i]]
                key = "move" + indices[i]
                spread1_innards[key] = ["civil", city1, 50, need_list[i]]
            else:
                key = "move" + str(i)
                spread1_innards[key] = ["food", city2, 20, need_list[i]]
                key = "move" + indices[i]
                spread1_innards[key] = ["civil", city2, 50, need_list[i]]
        spread1_innards["move!"] = ["civil", city1, 50, harbor]
        spread1_innards["move@"] = ["civil", city2, 50, harbor]
        spread1_innards["move#"] = ["food", city1, 25, harbor]
        spread1_innards["move^"] = ["food", city2, 25, harbor]
        spread1 = action("Spread1", spread1_innards)
    if allow_spread1 and need_spread1:
        actions.append(spread1)  # ADDS TO ACTION LIST

    #   Network1
    allow_network1 = False
    harbor_exists = False
    need_network1 = False
    city1_found = False
    sector_list = []
    for sector in m.sectors:
        if m.sectors[sector]["des"] == m.mTrackedDesignations["h"]:
            harbor = sector
        elif m.sectors[sector]["des"] == m.mTrackedDesignations["c"]:
            if city1_found:
                city2 = sector
            else:
                city1 = sector
                city1_found = True
        elif m.sectors[sector]["des"] == m.mTrackedDesignations["a"]:
            if twofarm:
                farm3 = sector
            elif onefarm:
                farm2 = sector
                twofarm = True
            else:
                farm1 = sector
                onefarm = True
        elif m.sectors[sector]["des"] == m.mTrackedDesignations["m"]:
            if onemine:
                mine2 = sector
            else:
                mine1 = sector
                onemine = True
        elif m.sectors[sector]["des"] == m.mTrackedDesignations["j"]:
            light = sector
        elif m.sectors[sector]["des"] == m.mTrackedDesignations["k"]:
            heavy = sector
    for sector in m.sectors:
        if m.sectors[sector]["des"] == m.mTrackedDesignations["h"]:
            harbor_exists = True
            check_harb = sector
            harbor = sector
            sector_list.append(sector)
        else:
            sector_list.append(sector)
    if harbor_exists:
        for sector in m.sectors:
            if m.sectors[sector]["des"] != m.mTrackedDesignations["h"]:
                if m.sectors[sector]["xdist"] != m.sectors[check_harb]["xloc"] or m.sectors[sector]["ydist"] != \
                        m.sectors[check_harb]["yloc"]:
                    need_network1 = True

    if harbor_exists:
        allow_network1 = True
        network1 = action("Network1", {"distribute": [harbor], "threshold1": ["food", farm1, 200],
                                       "threshold2": ["food", farm2, 200], "threshold3": ["food", farm3, 200],
                                       "threshold4": ["food", mine1, 200], "threshold5": ["food", mine2, 200],
                                       "threshold6": ["food", light, 200], "threshold7": ["food", heavy, 200],
                                       "threshold8": ["food", city1, 200], "threshold9": ["food", city2, 200],
                                       "threshold0": ["iron", light, 100], "thresholda": ["iron", heavy, 200],
                                       "thresholdb": ["iron", mine1, 1], "thresholdz": ["iron", mine2, 1],
                                       "thresholdc": ["lcm", light, 1], "thresholdd": ["hcm", heavy, 1]})
    if allow_network1 and need_network1:
        actions.append(network1)  # ADDS TO ACTION LIST

    #   BuildFishingBoat
    allow_buildfishingboat = False
    harbor_exists = False
    for sector in m.sectors:
        if m.sectors[sector]["des"] == m.mTrackedDesignations["h"]:
            harbor_exists = True
            build_harb = sector

    if harbor_exists:
        if float(m.sectors[build_harb]["lcm"]) >= m.mShipTypes["fb"]["lcm"] and float(m.sectors[build_harb]["hcm"]) >= \
                m.mShipTypes["fb"]["hcm"]:
            allow_buildfishingboat = True

    if allow_buildfishingboat:
        buildfishingboat = action("BuildFishingBoat", {"build_ship": [harbor, "fb"]})
    if allow_buildfishingboat:
        weight = 100
        for i in range(weight):
            actions.append(buildfishingboat)

    #   Update
    update = action("Update", {"update": []})
    if len(actions) < 1:
        actions.append(update)  # ADD TO ACTION LIST

    return actions


def GOAL(s):
    sectors = False
    starvation = True
    built_ship = False
    # print(s)
    if len(s.mModel.sectors) >= 10:
        sectors = True
    starvation = s.mModel.mStarvation
    built_ship = s.mModel.mBuiltShip

    if sectors and built_ship and not starvation:
        return True
    else:
        return False

def openmodel():
    sectors = pickle.load(open("sectors.p", "rb"))

    ships = pickle.load(open("ship_sectors.p.p", "rb"))

    m = Model(sectors, ships)

    foutsector = open("sectors.p", "wb")
    pickle.dump(m.sectors, foutsector)
    foutsector.close()
    # print("Sectors closed. ")

    foutship = open("ship_sectors.p.p", "wb")
    pickle.dump(m.ship_sectors, foutship)
    foutship.close()

    return m

def main():
    sectors = pickle.load(open("sectors.p", "rb"))
    print("Sectors loaded into dictionary. ")

    ships = pickle.load(open("ship_sectors.p", "rb"))
    print("Ships loaded into dictionary. ")
    m = Model(sectors, ships)

    ##make changes, update model, etc

    ##

    foutsector = open("sectors.p", "wb")
    pickle.dump(m.sectors, foutsector)
    foutsector.close()
    # print("Sectors closed. ")

    foutship = open("ship_sectors.p.p", "wb")
    pickle.dump(m.ship_sectors, foutship)
    foutship.close()
    # print("Ships closed. ")


main()