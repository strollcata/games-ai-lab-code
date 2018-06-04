class FocusAttack(object):
    def update(self, gameinfo):
        #If there is an active fleet, do not move.
        #if gameinfo.my_fleets:
        #    return
        #If there are planets left both on and off my side...
        if gameinfo.my_planets and gameinfo.not_my_planets:
            #...then choose my planet with the largest fleet as the source.
            src = max(gameinfo.my_planets.values(), key = lambda p: p.num_ships)
            dest = None
            ship_mult = 1
            #Find the enemy planet with the largest fleet that is smaller than my source's fleet.
            destlist = list(gameinfo.not_my_planets.values())
            enlist = list(gameinfo.not_my_planets.values())
            for enplanet in enlist:
                if ((dest == None) and (src.num_ships > enplanet.num_ships)):
                    dest = enplanet
                elif ((src.num_ships > enplanet.num_ships) and (enplanet.num_ships > dest.num_ships)):
                    dest = enplanet
            #If there are no enemy planets, find the strongest planet that I don't own with a fleet smaller than a quarter of my source's fleet.
            if dest == None:
                for nmplanet in gameinfo.not_my_planets.values():
                    if ((dest == None) and ((int(0.25 * src.num_ships)) >= nmplanet.num_ships)):
                        dest = nmplanet
                    elif (((int(0.25 * src.num_ships)) >= nmplanet.num_ships) and (nmplanet.num_ships > dest.num_ships)):
                        dest = nmplanet
                ship_mult = 0.25
            #If there are no planets meeting the above conditions, send my entire source's fleet to the smallest planet I don't own.
            if dest == None:
                dest = min(gameinfo.not_my_planets.values(), key = lambda p: p.num_ships)
            #Finally, if I have a target selected, send the attack order.
            if dest != None:
                gameinfo.planet_order(src, dest, int(src.num_ships * ship_mult))
            pass
