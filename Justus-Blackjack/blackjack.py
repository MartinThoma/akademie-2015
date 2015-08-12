#%matplotlib inline
import time
import matplotlib.pyplot as plt
import numpy as np
from IPython import display
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 15:33:36 2015

@author: Justus
"""
import random
#from itertools import *

class IO(object):
    def bet(self,player):
        return 10


class Text(IO):
    def bet(self,player):
        response = raw_input(player.name + ", how much would you like to bet? You have " + str(player.credits) + " credits: ")
        try:
            b = min(player.credits, int(response))
        except:
            b = player.credits
        if output:
            print("You have bet " + str(b) + " credits.")
        return b
            
    def show_cards(self,player,h):
        if output:
            print(player.name + " has drawn the following cards:")
            print(player.hand[h].__str__() + " (Value: " + str(player.hand[h].value()) + ")")
     
    def message(self,player,s):
        if output:
            print(s)

    def yes_no(self,player,s):
        response = raw_input(player.name + ", " + s + " (Y/N): ")
        return (response == "y" or response == "Y")
    
    def continueplay(self):
        response = raw_input("Do you want to continue playing? (Y/N): ")
        return not(response == "n" or response == "N")
    
    def player(self):
        response = raw_input("How many players do want to play? Please enter a number: ")
        try:
            b = max(1, int(response))
        except:
            b = 1
        return b
#class Gui(IO):


class Card(object):
    """ A playing card. """
    RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    SUITS = ["c", "d", "h", "s"]
    RANK_VALUE = {'A': 11,'2': 2,'3': 3,'4': 4,'5': 5,'6': 6,'7': 7,'8': 8,'9': 9,'10': 10,'J': 10,'Q': 10,'K': 10}

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        rep = self.rank + self.suit
        return rep
        
    def value(self):
        return Card.RANK_VALUE[self.rank]

class Deck(object):
    """ One or multiple decks of playing cards """
    def __init__(self, number=1):
        self.cards = []
        for x in range(number):        
            for suit in Card.SUITS:
                for rank in Card.RANKS:
                    self.cards.append(Card(rank, suit))

    def __str__(self):
        if self.cards:
           rep = ""
           for card in self.cards:
               rep += str(card) + "  "
        else:
            rep = "<empty>"
        return rep

    def shuffle(self):
        random.shuffle(self.cards)
    
    def next_card(self):
        return self.cards.pop()
        
    def cards_left(self):
        return len(self.cards)

class Hand(object):
    """ A hand of playing cards. """
    def __init__(self):
        self.cards = []
        self.bet = 0
        self.stand = False
        self.out = False
        self.dd = 0

    def __str__(self):
        if self.cards:
           rep = ""
           for card in self.cards:
               rep += str(card) + "  "
        else:
            rep = "<empty>"
        return rep
    
    def sorted_list(self):
        card_list = []
        for card in self.cards:
            card_list.append(card.rank)
        card_list.sort()
        return card_list
    
    def clear(self):
        self.cards = []
        self.bet = 0
        self.stand = False
        self.out = False
        self.dd = 0

    def draw_from(self,deck):
        c = deck.next_card()
        self.cards.append(c)
        return c
        
    def add(self,card):
        self.cards.append(card)
        
    def value(self):
        ace = 0
        val = 0
        for card in self.cards:
            val += card.value()
            if card.value() == 11:
                ace += 1
        while val > 21 and ace > 0:
            val -= 10
            ace -= 1
        return val
        
    def triple_seven(self):
        seven = True
        for card in self.cards:
            seven = (seven and card.rank == 7)
        return seven and (len(self.cards) == 3)
        
    def is_blackjack(self):
        return (len(self.cards) == 2) and (self.value() == 21)
        
    def can_split(self):
        return (len(self.cards) == 2) and (self.cards[0].rank == self.cards[1].rank)

class Player(object):
    """ A Player. """
    def __init__(self, name, cre=0):
        self.credits = cre
        self.hand = []
        hand1 = Hand()
        self.hand.append(hand1)
        self.name = name
        self.ins = 3
        self.spl = 3
        self.insurance = 0
        self.game = Game()
        self.history = History()
        
    def reset(self):
        for h in self.hand:
            h.clear()
        del self.hand[1:]
        self.insurance = 0
        self.ins = 3
        self.spl = 3
        self.game.reset()

    def draw_card(self,io,deck,h=0):
        c = self.hand[h].draw_from(deck)
        io.message(self, self.name + " has drawn a " + c.__str__() + ".")
    
    def bet(self,io,h=0):
        b = io.bet(self)
        self.hand[h].bet = b
        self.credits -= b
    
    def hit_otherwise_stand(self,io,h=0):
        io.show_cards(self,h)
        s = "do you want a hit?"
        hit = io.yes_no(self,s)
        self.hand[h].stand = not hit
        return hit

    def is_out(self):
        out = True
        for h in self.hand:
            out = (out and (h.out or (h.value()>21)))
        return out
        
    def stands(self):
        s = False #True
        for h in self.hand:
            s = (s or h.stand) #and
        return s
        
    def can_play(self):
        s = True
        for h in self.hand:
            s = (s and (h.stand or h.out or h.value()>21))
        return not s
        
    def is_busted(self,h=0):
        return (self.hand[h].value()>21)

    def is_bankrupt(self):
        return (self.credits == 0)
        
    def show_cards(self,io,h=0):
        io.show_cards(self,h)        
        
    def has_triple_seven(self,h=0):
        return self.hand[h].triple_seven()
    
    def has_blackjack(self,h=0):
        return self.hand[h].is_blackjack()

    def buys_insurance(self,io):
        #if(self.credits >= round(self.hand[0].bet/2)):
        s = "the dealer has an Ace. Would you like to buy an insurance?"
        if io.yes_no(self,s):
            s = "You have bought an insurance for " + str(round(self.hand[0].bet/2)) + " credits."
            io.message(self,s)
            return True
        else:
            return False            
            
    def do_buy_insurance(self,io):
        self.ins = 1
        self.insurance = round(self.hand[0].bet/2)
        self.credits -= round(self.hand[0].bet/2)
    
    def split_hand(self,h=0):
        if self.hand[h].can_split(): #and (self.credits >= self.hand[h].bet):
            s = "do you want to split your hand?"
            return io.yes_no(self,s)
        else:
            return False
    
    def do_split_hand(self, h=0):
        self.spl = 1
        hand2 = Hand()         
        hand2.add(self.hand[h].cards.pop())
        hand2.bet = self.hand[h].bet
        self.credits -= self.hand[h].bet
        self.hand.append(hand2)
        
    def double_down(self,h=0):
        s = "do you want to double your bet and get exactly one more card?"
        return io.yes_no(self,s)
        
    def do_double_down(self,io,deck,h=0):
        self.hand[h].dd = 1
        self.draw_card(io,deck,h)
        self.credits -= self.hand[h].bet
        if self.hand[h].value()>21:
            self.hand[h].out = True
            s = "You busted!"
            self.message(io,s)
        else:
            self.hand[h].stand = True
            self.hand[h].bet = self.hand[h].bet * 2
    
    def message(self,io,s):
        io.message(self,s)
        
        
class Dealer(Player):
    """ Dealer, a player with a predefined strategy. """
    def __init__(self):
        self.credits = 0
        self.name = "Dealer"
        self.hand = []
        hand1 = Hand()
        self.hand.append(hand1)
        self.game = Game()
        
    def hit_otherwise_stand(self,io):
        return (self.hand[0].value() < 17)
        
    def has_ace(self):
        return (self.hand[0].cards[0].rank == "A")

class StrategicPlayer(Player):
    """ A player with different strategies. """
    #has an object strategy, which is a look-up table and defines all actions
    def __init__(self, name, cre=0):
        self.credits = cre
        self.hand = []
        hand1 = Hand()
        self.hand.append(hand1)
        self.name = name
        self.ins = 3
        self.spl = 3
        self.insurance = 0
        self.strategy = Strategy()
        self.default = [0.5,0,0,0.5]
             # insurance o/wise not
             # split o/wise not
             # doubledown o/wise not
             # hit o/wise stand       
        self.game = Game()
        self.history = History()

    def get_state(self, h):
        #ins = 1 => insurance bought; ins = 2 => insurance offered but not bought; ins = 0 => make choice; ins = 3 => option not available
        #ddo = 1 => double down; ddo = 2 => not double down; ddo = 0 => make choice
        #spl = 1 => split; spl = 2 => split possible but not done; spl = 0 => make choice; spl = 3 => option not available
        #check double down status

        #        ddo1 = self.hand[0].dd
        #ddo2 = 0
        #hand2 = Hand()
        #if len(self.hand) != 1:
        #    ddo2 = self.hand[1].dd
        #    hand2 = self.hand[1]
        #s = GameState(self.ins,self.spl,ddo1,ddo2,self.hand[0].cards,hand2.cards,dh)
 
        if output:
            print "complete game sate: (ins, spl, dd, hand, dealer)", self.ins, self.spl, self.hand[h].dd, self.hand[h].sorted_list(), dealer.hand[0].sorted_list()
        s = GameState(self.ins,self.spl,self.hand[h].dd,self.hand[h].sorted_list(),dealer.hand[0].sorted_list())
        
        return s.__hash__()
    
    def action(self, h):
        #if self.strategy.table.has_key(self.get_state()):
        gstmp = self.get_state(h)
        if gstmp in self.strategy.table:
            p = self.strategy.table[gstmp]
        else:
            if output:
                print "ins. status: ", self.ins, " --splt status: " , self.spl, " -- double down status of hand ",h,self.hand[h].dd
            if self.ins == 0:
                p = self.default[0] #insurance o/wise not
            elif self.spl == 0:
                p = self.default[1] #split o/wise not
            elif self.hand[h].dd == 0:
                p = self.default[2] # doubledown o/wise not
            else:
                p = self.default[3] # hit o/wise stand       
            
        act = p > random.random()
        self.game.game_state.append(gstmp)
        self.game.action.append(act)
        return act
        
    def double_down(self,h=0):
        dd = self.action(h)
        if dd:
            if output:
                print(self.name + " chose double down.")
            self.hand[h].dd = 1
        else:
            self.hand[h].dd = 2
        return dd
        
    def hit_otherwise_stand(self,io,h=0):
        hit = self.action(h)        
        self.hand[h].stand = not hit
        if hit:
            if output:
                print(self.name + " chose to hit.")
        else:
            if output:
                print(self.name + " chose to stand.")
        return hit
    
    def buys_insurance(self,io):
        self.ins = 0
        res = self.action(h)
        if res:
            self.ins = 1
        else:
            self.ins = 2
    
    def split_hand(self,h=0):
        if self.hand[h].can_split():
            self.spl = 0
            res = self.action(h)
            if res:
                self.spl = 1
                if output:
                    print(self.name + " chose to split.")
                return True
            else:
                self.spl = 2
                if output:
                    print(self.name + " chose not to split.")
                return False
        else:
            self.spl = 3
            return False
        
    def bet(self,io,h=0):
        b = 10
        self.hand[h].bet = b
        self.credits -= b
        self.game.gain -= b
        
    def update_strategy(self,games):
        return True
    
    
class History(object):
    def __init__(self):
        self.game = []

        
class Game(object):
    def __init__(self):
        self.game_state = []
        self.action = []
        self.gain = 0
        
    def reset(self):
        self.game_state = []
        self.action = []
        self.gain = 0

        
class GameState(object):
    def __init__(self,ins,spl,ddo,h1,dh):
        self.ins = ins
        self.spl = spl
        self.ddo = ddo
        self.h1 = h1
        self.dh = dh
        
    def __hash__(self):
        return hash((self.ins,self.spl,self.ddo,self.h1.__str__(),"-",self.dh.__str__()))
    
class Strategy(object):
    def __init__(self):
        self.table = {}




class ServanPlayer(StrategicPlayer):
    def __init__(self, name = "Servan", cre=0):
        self.credits = cre
        self.hand = []
        hand1 = Hand()
        self.hand.append(hand1)
        self.name = "Servan"
        self.ins = 3
        self.spl = 3
        self.insurance = 0
        self.strategy = Strategy()
        self.default = [0,0,0,0]
             # insurance o/wise not
             # split o/wise not
             # doubledown o/wise not
             # hit o/wise stand       
        self.game = Game()
        self.history = History()
    
    def update_strategy(self,games):
        return True
    

class OptimalPlayer(StrategicPlayer):
    def __init__(self, name = "optimal", cre=0):
        self.credits = cre
        self.hand = []
        hand1 = Hand()
        self.hand.append(hand1)
        self.name = "optimal"
        self.ins = 3
        self.spl = 3
        self.insurance = 0
        self.strategy = Strategy()
        self.default = [0.5,0.5,0.5,0.5]
             # insurance o/wise not
             # split o/wise not
             # doubledown o/wise not
             # hit o/wise stand       
        self.game = Game()
        self.history = History()
        
        
    def action(self, h):
        #if self.strategy.table.has_key(self.get_state()):
        gstmp = self.get_state(h)
        if gstmp in self.strategy.table:
            p = self.strategy.table[gstmp]
        else:
            if output:
                print "ins. status: ", self.ins, " --splt status: " , self.spl, " -- double down status of hand ",h,self.hand[h].dd
            if self.ins == 0:
                p = 0 #insurance o/wise not -- optimal: never insure
            elif self.spl == 0:
                if output:
                    print self.hand[0].cards
                
              #  if (playerHand.cards[0].Face == Faces.Ace || playerHand.cards[0].Face == Faces.Eight)
              #      return BJDecisions.Split;
              #  else if (playerHand.cards[0].Face == Faces.Nine)
              #  {
              #      if (2 <= dealerHand.Value && dealerHand.Value <= 9 && dealerHand.Value != 7)
              #          return BJDecisions.Split;
              #  }
              #  else if (playerHand.cards[0].Face == Faces.Seven)
              #  {
              #      if (2 <= dealerHand.Value && dealerHand.Value <= 8)
              #          return BJDecisions.Split;
              #  }
              #  else if (playerHand.cards[0].Face == Faces.Six || playerHand.cards[0].Face == Faces.Three || playerHand.cards[0].Face == Faces.Two)
              #  {
              #      if (2 <= dealerHand.Value && dealerHand.Value <= 7)
              #          return BJDecisions.Split;
              #  }
              #  else if (playerHand.cards[0].Face == Faces.Four && dealerHand.Value == 5)
              #      return BJDecisions.Split;
                
                
                
                
                
                p = self.default[1] #split o/wise not
            elif self.hand[h].dd == 0:
                p = self.default[2] # doubledown o/wise not
            else:
                p = self.default[3] # hit o/wise stand       
            
        act = p > random.random()
        self.game.game_state.append(gstmp)
        self.game.action.append(act)
        return act
        

%matplotlib

#define in and output class
io = Text()
output = True

#create a number of players
player = []
#n = io.player()
#for h in range(n):
#    p = StrategicPlayer("Player " + str(h),0)
#    player.append(p)

p = ServanPlayer()
player.append(p)

p = OptimalPlayer()
player.append(p)


#create the dealer
dealer = Dealer()

#the game
play = True
numGame = 0
totalNumGame = 500

Credits = np.ones((len(player),totalNumGame+1))
plt.close("all")
plt.axis([0, totalNumGame, -1000, 1000])
#plt.ion()

lines = [plt.plot([], [])[0] for _ in range(len(player))]
plt.show()

while numGame < totalNumGame:
    #create a deck of cards and shuffle
    deck1 = Deck(6)
    deck1.shuffle()

    numGame = numGame + 1
    if output:
        print " \n\n\n game number: ", numGame , "\n"
    #empty hands
    for p in player:
        p.reset()
    dealer.reset()
    #betting
    for p in player:
        p.bet(io)
    #dealer draws card
    dealer.draw_card(io,deck1)
    #player draw cards
    for p in player:
        p.draw_card(io,deck1)
        p.draw_card(io,deck1)

    #insurance
    #if dealer.has_ace():
    #    for p in player:
    #        if p.buys_insurance(io):
    #            p.do_buy_insurance()
    #            if p.has_blackjack():
    #                ###player wins
    #                p.hand[0].out = True
    #                p.game.gain += 2 * p.hand[0].bet
    #                p.credits += 2 * p.hand[0].bet
    #                s = p.name + ", you have a Black Jack and bought an insurance. This gives you " + str(p.hand[0].bet) + " credits!"
    #                p.message(io,s)

    #split or blackjack
    for p in player:    
        if p.split_hand():
            p.do_split_hand()
        #elif p.has_blackjack():
        #    p.hand[0].stand = True

    #double down
    for p in player:
        for h in range(len(p.hand)):
            if p.double_down(h):
                p.do_double_down(io,deck1,h)
            # else:
                #####

    #all player draw their cards and make their game
    for p in player:
        while p.can_play():
            for h in range(len(p.hand)):
                if not p.hand[h].stand and not p.hand[h].out:
                    if p.hit_otherwise_stand(io,h):
                        p.draw_card(io,deck1,h)
                        if p.has_triple_seven(h):
                            ###Player wins
                            p.hand[h].out = True
                            p.game.gain += int(round(2.5 * p.hand[h].bet))
                            p.credits += int(round(2.5 * p.hand[h].bet))
                            s = "You have triple seven and won " + str(int(round(1.5 * p.hand[h].bet))) + " credits!"
                            p.message(io,s)
                        #elif p.hand[h].value() == 21:
                        #    p.hand[h].stand = True
                        elif p.is_busted(h):
                            ###Player loses
                            p.hand[h].out = True
                            s = "You busted!"
                            p.message(io,s)

    #dealer makes his game if at least one player stands
    stand = False
    for p in player:
        stand = stand or p.stands()
    #the above test can be implemented more elegant I guess. please let me know
    if stand:
        #dealer makes his game
        while dealer.hit_otherwise_stand(io):
            dealer.draw_card(io,deck1)
            dealer.show_cards(io)

        #evaluation
        for p in player:
            if output:
                print " player's (", p.name, ") credit: ", p.credits
            
            if p.stands():#is it possible to combine for loop and if condition in python?
                for h in range(len(p.hand)):
                    if p.hand[h].stand and not p.hand[h].out:
                        if dealer.has_blackjack() and p.has_blackjack(h):
                            ###drawn
                            p.game.gain += p.hand[h].bet
                            p.credits += p.hand[h].bet
                            s = p.name + ": BlackJack vs. BlackJack! You don't lose the bet " + str(p.hand[h].bet) + " credits!"
                            p.message(io,s)
                        #elif dealer.has_blackjack() and p.insurance > 0:
                            ###player loses
                            p.game.gain += 3 * p.insurance
                            p.credits += 3 * p.insurance
                            s = p.name + ": You lost, but your insurance pays you " + str(p.insurance * 3) + " credits!"
                            p.message(io,s)
                        elif dealer.has_blackjack():
                            ###player loses
                            s = p.name + ": You lost!"
                            p.message(io,s)
                        elif p.has_blackjack(h):
                            ###player wins
                            p.game.gain += int(2.5 * p.hand[h].bet)
                            p.credits += int(2.5 * p.hand[h].bet)
                            s = p.name + ": You have a Black Jack and won " + str(int(round(1.5*p.hand[h].bet))) + " credits!"
                            p.message(io,s)
                        elif dealer.is_out():
                            ###player wins
                            p.game.gain += 2 * p.hand[h].bet
                            p.credits += 2 * p.hand[h].bet
                            s = p.name + ": Dealer busted! You won " + str(p.hand[h].bet) + " credits!"
                            p.message(io,s)      
                        elif dealer.hand[0].value() < p.hand[h].value():
                            ###player wins
                            p.game.gain += 2 * p.hand[h].bet
                            p.credits += 2 * p.hand[h].bet
                            s = p.name + ": You won " + str(p.hand[h].bet) + " credits!"
                            p.message(io,s)
                        elif dealer.hand[0].value() == p.hand[h].value():
                            ###drawn
                            p.game.gain += p.hand[h].bet
                            p.credits += p.hand[h].bet
                            s = p.name + ": Drawn! You don't lose the bet " + str(p.hand[h].bet) + " credits!"
                            p.message(io,s)
                        else:
                            ###player loses
                            s = p.name + ": You lost!"
                            p.message(io,s)
                            
    
    for i in range(len(player)):
        p = player[i]
        #for p in player:
        Credits[i,numGame] = p.credits
        p.history.game.append(p.game)
        p.update_strategy(len(p.history.game))        

    # Update plot every 20 games
    if (numGame % 20 == 0):
        if (np.min(Credits) < plt.gca().get_ylim()[0]):
            plt.gca().set_ylim([np.min(Credits)-1000,100])
        for i in range(len(player)):
            lines[i].set_xdata(range(numGame+1))
            lines[i].set_ydata(Credits[i,0:(numGame+1)])
            #plt.plot(Y[i,0:(numGame+1)])
            #time.sleep(0.05)
        plt.draw()

    
    #play = io.continueplay()

"""
globale function um spielfluss herum
"""

"""
game state ist noch nicht richtig gespeichert
"""

plt.close("all")