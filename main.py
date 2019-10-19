import os
import argparse

from sc2reader import utils

from PACAnalysis import printReplay

def main():
    parser = argparse.ArgumentParser(
        description="""Prints PAC information from Starcraft II replay files or directories.""")
    parser.add_argument('--recursive', action="store_false", default=True,
                        help="Recursively read through directories of Starcraft II files [default on]")

    required = parser.add_argument_group('Required Arguments')
    required.add_argument('paths', metavar='filename', type=str, nargs='+',
                          help="Paths to one or more Starcraft II files or directories")

    display = parser.add_argument_group('Display Options')
    display.add_argument('--pausestats', action="store_false", default=True,
                        help="Pauses after each stat block [default on]")
    display.add_argument('--pausereplays', action="store_true", default=False,
                        help="Pauses after each replay summary [default off]")
    display.add_argument('--displayreplays', action="store_true", default=False,
                        help="Displays individual replay summaries [default off]")

    arguments = parser.parse_args()
    analysis = {}
    depth = -1 if arguments.recursive else 0

    # Creating a list of replays in the specified directories.
    replays = set(filepath for path in arguments.paths for filepath in utils.get_files(path, depth=depth) if os.path.splitext(filepath)[1].lower() == '.sc2replay')
    replayCount = len(replays)

    if replayCount == 1:
        arguments.displayreplays = True
        arguments.pausereplays = True

    for replay in replays:
        try:
            printReplay(replay, analysis, arguments)
        except:
            print("Error with '{0}': ".format(replay))
            replayCount -= 1
        if arguments.pausereplays:
            print("PRESS ENTER TO CONTINUE")
            input()

    if replayCount > 1:
        print("\n--------------------------------------")
        print("Results - {0} Replays Analyzed".format(replayCount))
        print("{0} Players Analyzed".format(len(analysis)))
        for stats in sorted(analysis.items(), key=lambda t: t[1].count, reverse=True):
            print("\t{0:<15} (pid: {1})\t- {2} replays".format(stats[1].name, stats[0], stats[1].count))
            print("\t\tPPM: {0:>6.2f}".format(stats[1].ppm))
            print("\t\tPAL: {0:>6.2f}".format(stats[1].pal))
            print("\t\tAPP: {0:>6.2f}".format(stats[1].app))
            print("\t\tGAP: {0:>6.2f}".format(stats[1].gap))
            if arguments.pausestats:
                print("PRESS ENTER TO CONTINUE")
                input()

if __name__ == '__main__':
    main()