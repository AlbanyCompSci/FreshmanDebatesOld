#!/usr/bin/env python3.4


import logging
import sys
import os
from   debates.models import Debate, Period
from   string         import Template
from io import open


logger = logging.getLogger('logview.debugger')

ROLL_FILE = "roll_sheet"
TEMPLATE = Template("""
                    Period: $period\n
                    Location: $location\n
                    Teams debating: $aff_teams, $neg_teams\n
                    Spectator teams: $spec_teams\n
                    """)

def writeRoll():
    #clear any existing data from the ROLL_FILE
    open(ROLL_FILE, 'w').close()
    periods = list(map(lambda p: p.period, Period.object.all()))
    logger.debug("Num periods: " + str(len(periods)))
    for p in periods:
        logger.debug("Period is " + p)
        debates = list(Debate.objects.filter(period = p))
        logger.debug("Num debates in period: " + str(len(debates)))
        for d in debates:
            #make the list a string and drop the brackets ([])
            sts = str(d.spectators)[1:-1]
            string = template.substitute(period=p,
                                         location=d.location,
                                         aff_team=d.affirmative,
                                         neg_team=d.negative,
                                         spec_teams=sts)
            with open(ROLL_FILE, 'a') as f:
                f.write(string)
