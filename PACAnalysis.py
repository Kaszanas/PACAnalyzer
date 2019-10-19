#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals, division

import os
import argparse

import sc2reader
from sc2reader import utils
from sc2reader.exceptions import ReadError
from sc2reader.engine.plugins.pacanalyzer import *

sc2reader.engine.register_plugin(PACAnalyzer())

def printReplay(filepath:str, analysis:dict, arguments):
    """
    Prints summary information about SC2 replay file
    filepath (str) - path to the file.
    analysis (dict) - dictionary holding information on players.
    arguments (parser.parse_args()) - object containing arguments for further processing.
    """

    replay = sc2reader.load_replay(filepath, debug=True)

    if arguments.displayreplays:
        print("\n--------------------------------------\n{0}\n".format(filepath))
        print("   Map:      {0}".format(replay.map_name))
        print("   Date:     {0}".format(replay.start_time))
        print("   Version:  {0}".format(replay.release_string))
        print("   Length:   {0} minutes".format(replay.game_length))
        lineups = [team.lineup for team in replay.teams]
        print("   Teams:    {0}".format("v".join(lineups)))
        if len(replay.observers) > 0:
            print("   Observers:")
            for observer in replay.observers:
                print("      {0}".format(observer.name))
    for team in replay.teams:
        if arguments.displayreplays:
            print("      Team {0}".format(team.number))
        for player in team.players:
            if player.is_human:
                if arguments.displayreplays:
                    print("      \t{0} ({1})".format(player.name, player.pick_race[0]))
                    print("      \t\tPPM: {0:>6.2f}".format(player.PACStats.ppm))
                    print("      \t\tPAL: {0:>6.2f}".format(player.PACStats.pal))
                    print("      \t\tAPP: {0:>6.2f}".format(player.PACStats.app))
                    print("      \t\tGAP: {0:>6.2f}".format(player.PACStats.gap))
                if player.toon_id in analysis:
                    analysis[player.toon_id].ppm = (analysis[player.toon_id].count * analysis[player.toon_id].ppm +
                                                    player.PACStats.ppm) / (analysis[player.toon_id].count + 1)
                    analysis[player.toon_id].pal = (analysis[player.toon_id].count * analysis[player.toon_id].pal +
                                                    player.PACStats.pal) / (analysis[player.toon_id].count + 1)
                    analysis[player.toon_id].app = (analysis[player.toon_id].count * analysis[player.toon_id].app +
                                                    player.PACStats.app) / (analysis[player.toon_id].count + 1)
                    analysis[player.toon_id].gap = (analysis[player.toon_id].count * analysis[player.toon_id].gap +
                                                    player.PACStats.gap) / (analysis[player.toon_id].count + 1)
                    analysis[player.toon_id].count += 1
                else:
                    analysis[player.toon_id] = PACStats()
                    analysis[player.toon_id].name = player.name
                    analysis[player.toon_id].count = 1
                    analysis[player.toon_id].ppm = player.PACStats.ppm
                    analysis[player.toon_id].pal = player.PACStats.pal
                    analysis[player.toon_id].app = player.PACStats.app
                    analysis[player.toon_id].gap = player.PACStats.gap
            else:
                if arguments.displayreplays:
                    print("      \t{0} ({1})".format(player.name, player.pick_race[0]))
    print