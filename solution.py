#!/usr/bin/env python
#! -*- coding: utf-8 -*-

"""
To paperless reciepts:

Awesome idea ! - How on earth do you get the reciepts out of the till?
I soooo want to be in on this one!

I even have a categorising your own spend app that I will now
outsource - see lifeisstillgood/ISpentWhat (still TBC).  At some point
there was an attemtpt to get gnucash to do sensible things with
importing.  THis is a challenge I think loads of people will have and
the marketing follow-ons will be amazing

So my answer: I have run out of time (well, 20 minutes ago I did)
I would love to know more, and may work on this a bit more, but 
my approach may not have been optimial - simulation without decent state machine,
dived into coding too quickly etc etc

Anyway, thats a hard luck dog. Unless you consider the win "midair" I dont think he can win.


Noooooo!!!! I forgot the turn !!!
(quick hack later. What am I saying - its all hack)



::

    [pbrian@hadrian /usr/home/pbrian/src/thirdparty/paperless-engineering]$ python solution.py 90
    Draw
    ********** ==========================================================================================
    dog        --*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*
    cat        -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
    ********** ==========================================================================================
    [pbrian@hadrian /usr/home/pbrian/src/thirdparty/paperless-engineering]$ python solution.py 6
    Draw
    ********** ======
    dog        --*--*
    cat        -*-*-*
    ********** ======
    [pbrian@hadrian /usr/home/pbrian/src/thirdparty/paperless-engineering]$ python solution.py 2
    cat wins by 2 feet
    ********** ==
    dog        --
    cat        -*
    ********** ==
    [pbrian@hadrian /usr/home/pbrian/src/thirdparty/paperless-engineering]$ python solution.py 3
    dog wins by 1 feet
    ********** ===
    dog        --*
    cat        -*-
    ********** ===

With turn::

    [pbrian@hadrian /usr/home/pbrian/src/thirdparty/paperless-engineering]$ python solution.py 3
    Draw
    ********** ===
    dog        --<--*
    cat        -*-<-*
    ********** ===
    [pbrian@hadrian /usr/home/pbrian/src/thirdparty/paperless-engineering]$ python solution.py 100
    cat wins by 2 feet
    ********** ====================================================================================================
    dog        --*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--<--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*-
    -*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--
    cat        -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-<-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
    *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
    ********** ====================================================================================================



The Challenge:
==============

A trained cat and dog run a race, one hundred feet straight away and
return. The dog leaps three feet at each bound and the cat but two,
but then she makes three leaps to his two. Now, under those
circumstances, who wins the race?

Input

The race distance eg 100, 200

Output

{Animal} wins by {distance}

Cat wins by 50 feet
Dog wins by 10 feet
or Draw


SOlution
========

0. I am going to assume that the animal need to cross the finish line and *land* before its a win (no mid air stuff)

   This now seems a bad assumption, but defensible - the cat seems to win too often.
   I need to rethink my approach, dived in too early and frankly, well, I have to stop now.

1. Iteration or recursion.
   Well, recursion is cooler, but I am short on time so will take the
   easy route

2. Bound - each animal takes one bound, but there is also a cycle...
   SO, we are time dependant, and need to arrange distance of bound and 
   duration of bound
   animal: [<feet_bound>, <duration_of_bound_in_units>]

   bounds = { 'dog': [3, 3],
             'cat': [2, 2]
           }


   so after two leaps by dog (6 secs, cat will have done 3 leaps, and 
   so this is going to be the distance diviisble by 3 or by 2 ...)

"""
import sys

class animal(object):
    """Its just going to be easier to use dotted variables than dict
    calls """
    def __init__(self, name, bound_len, bound_duration):
        """ """
        self.name = name
        self.bound_len = bound_len
        self.bound_duration = bound_duration
        self.track = []
        self.log = []
        self.totdist = 0
        self.turned = False

    def reset(self):
        self.track = []
        self.log = []
        self.totdist = 0

    def __repr__(self):
        #return "The %(animalname)s leaps %(bound_len)s feet in %(bound_duration)s ticks" % self.__dict__
        return " %(name)s [%(bound_len)s ft / %(bound_duration)s ticks]" % self.__dict__


def calc_win(dist, runners):
    """Simulate the race, using a "clock", and updating 
       results each tick

   dist - integer rep. number of feet of race
   runners - list of animal class objects
     """
    
    for tick in range(1000):  ##urrgh - do I want unbounded time???
        if tick == 0: continue

        for animal in runners:
            if tick % animal.bound_duration == 0:
                #hit ground, 
                #am I turning now?
                animal.totdist += animal.bound_len
                if animal.totdist >= dist and animal.turned == False:
                    animal.turned = True
                    animal.track.append("<")
                    animal.log.append([tick, animal.totdist])
                else: ##keep going
                    animal.track.append("*")
                    animal.log.append([tick, animal.totdist])
            else:
                animal.track.append("-")

        for animal in runners:
            if animal.totdist >= dist*2:
                return runners
 
def summarise(runners):

    winners = []
    closestloser = None
    closestlosingdist = 0    


    ###assumption about expaniding into >2 racers
    ### YAGNI !!
    for animal in runners:
        if animal.totdist >= dist*2:
            winners.append(animal)
        else:
            if animal.totdist > closestlosingdist:
                closestlosingdist = animal.totdist 
                closestloser = animal

    if len(winners) > 1:
        results = "Draw"
    else:
        results = "%s wins by %s feet" % (winners[0].name, dist*2 - closestlosingdist)
    print results 

    ##prettyfy
    print "*"*10 + " " +  "="* dist
    for animal in runners:
        print animal.name.ljust(10), 
        print "".join(animal.track)
        #print animal.log
    print "*"*10 + " " +  "="* dist


##setup
dog = animal("dog", 3, 3)
cat = animal("cat", 2, 2)    
dist = int(sys.argv[1:][0]) ##woah - fragile!
runners = calc_win(dist, [dog, cat])
summarise(runners)
