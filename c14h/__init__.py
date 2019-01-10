#!/usr/bin/python3

from renderlib import *
from easing import *

# URL to Schedule-XML
scheduleUrl = 'https://eris.noname-ev.de/~nhg/schedule.xml'

def introFrames(args):



#fade in title
    frames = 1*fps
    for i in range(0, frames):
        yield(
            ('title', 'style', 'opacity', easeInQuad(i, 0, 1, frames)),
            ('persons', 'style', 'opacity', 0),
            ('date', 'style', 'opacity', 0),
            ('logo', 'style', 'opacity', 0),
        )
#fade in persons, date and logo
    frames = 2*fps
    for i in range(0, frames):
        yield(
            ('title', 'style', 'opacity', 1),
            ('persons', 'style', 'opacity', easeInQuad(i, 0, 1, frames)),
            ('date', 'style', 'opacity', easeInQuad(i, 0, 1, frames)),
            ('logo', 'style', 'opacity', easeInQuad(i, 0, 1, frames)),
        )

#show whole image for 2 seconds
    frames = 2*fps
    for i in range(0, frames):
        yield(
            ('title', 'style', 'opacity', 1),
            ('persons', 'style', 'opacity', 1),
            ('date', 'style', 'opacity', 1),
            ('logo', 'style', 'opacity', 1),
        )

#fade out
    frames = 1*fps
    for i in range(0, frames):
        yield(
            ('title', 'style', 'opacity', easeInQuad(i, 1, -1, frames)),
            ('persons', 'style', 'opacity', easeInQuad(i, 1, -1, frames)),
            ('date', 'style', 'opacity', easeInQuad(i, 1, -1, frames)),
            ('logo', 'style', 'opacity', easeInQuad(i, 1, -1, frames)),
        )


def outroFrames(args):
#fadein outro graphics
    frames = 2*fps
    for i in range(0, frames):
        yield(
            ('logo', 'style', 'opacity', easeInQuad(i, 0.01, 1, frames)),
            ('link', 'style', 'opacity', easeInQuad(i, 0.01, 1, frames)),
            ('bysalogo', 'style', 'opacity', easeInQuad(i, 0.01, 1, frames)),
            ('bysatext', 'style', 'opacity', easeInQuad(i, 0.01, 1, frames)),
        )
    frames = 3*fps
    for i in range(0, frames):
        yield(
            ('logo', 'style', 'opacity', 1),
            ('link', 'style', 'opacity', 1),
            ('bysalogo', 'style', 'opacity', 1),
            ('bysatext', 'style', 'opacity', 1),
        )
#fadeout
    frames = 1*fps
    for i in range(0, frames):
        yield(
            ('logo', 'style', 'opacity', easeInQuad(i, 1, -1, frames)),
            ('link', 'style', 'opacity', easeInQuad(i, 1, -1, frames)),
            ('bysalogo', 'style', 'opacity', easeInQuad(i, 1, -1, frames)),
            ('bysatext', 'style', 'opacity', easeInQuad(i, 1, -1, frames)),
        )


def debug():
    render('intro.svg',
        '../intro.ts',
        introFrames,
        {
            '$id': 246,
            '$title': 'Wie man einen Stern sprengt - mit Koks, Blackjack und schwarzen Löchern',
            '$persons':  'cherti',
            '$date': '2015-11-19'
        }
    )

    render('outro.svg',
       '../outro.ts',
        outroFrames,
           {
               '$id': 246
           }
    )
#
#    render(
#        'background.svg',
#        '../background.ts',
#        backgroundFrames
#    )

#    render('pause.svg',
#        '../pause.ts',
#        pauseFrames
#    )


def tasks(queue, args, idlist, skiplist):
    # iterate over all events extracted from the schedule xml-export
    for event in events(scheduleUrl):
        if not (idlist==[]):
                if 000000 in idlist:
                        print("skipping id (%s [%s])" % (event['title'], event['id']))
                        continue
                if int(event['id']) not in idlist:
                        print("skipping id (%s [%s])" % (event['title'], event['id']))
                        continue
        print(event['date'])
        # generate a task description and put them into the queue
        queue.put(Rendertask(
            infile = 'intro.svg',
            outfile = str(event['id'])+"_intro.ts",
            sequence = introFrames,
            parameters = {
                '$id': event['id'],
                '$title': event['title'],
                '$subtitle': event['subtitle'],
                '$persons': event['personnames'],
                '$date': event['date']
            }
        ))

        # place a task for the outro into the queue
        if not "out" in skiplist:
            queue.put(Rendertask(
                infile = 'outro.svg',
                outfile = str(event['id'])+"_outro.ts",
                sequence = outroFrames,
                parameters = {
                    '$id': event['id']
                }
            ))

    # place the pause-sequence into the queue
#    if not "pause" in skiplist:
#       queue.put(Rendertask(
#            infile = 'pause.svg',
#            outfile = 'pause.ts',
#            sequence = pauseFrames
#        ))

    # place the background-sequence into the queue
#    if not "bg" in skiplist:
#        queue.put(Rendertask(
#            infile = 'background.svg',
#           outfile = 'background.ts',
#            sequence = backgroundFrames
 #       ))
