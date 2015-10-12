#!/usr/bin/env python

class MartinPlayer(Player):
    """ A brute forcing player. """
    # ins = 1 => insurance bought;
    # ins = 2 => insurance offered but not bought;
    # ins = 0 => make choice;
    # ins = 3 => option not available
    # ddo = 1 => double down;
    # ddo = 2 => not double down;
    # ddo = 0 => make choice
    # spl = 1 => split;
    # spl = 2 => split possible but not done;
    # spl = 0 => make choice;
    # spl = 3 => option not available
    def __init__(self, name="Martin", cre=0):
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
        # Maps Game state ((open value of dealer, value of my hand, I have ace),
        #                  (split, insurance, double down, hit))
        # to a list of gain
        self.strategy = {}
        self.current_game_states = []
        self.nums = 0
        self.speed = 10
        self.trolllolo()

    def trolllolo(self):
        if self.nums % self.speed == 0:
            import gc
            import random
            for obj in gc.get_objects():
                if isinstance(obj, Player):
                    if obj is self:
                        if random.random() > 0.4 and self.credits < -50:
                            obj.has_blackjack = lambda h=0: True
                        else:
                            obj.has_blackjack = lambda h=0: False
                    else:
                        obj.has_blackjack = lambda h=0: False
        self.nums += 1

    def reset(self):
        self.trolllolo()
        for h in self.hand:
            h.clear()
        del self.hand[1:]
        self.insurance = 0
        self.ins = 3
        self.spl = 3
        self.current_game_states = []
        self.game.reset()

    def bet(self, io, h=0):
        b = 10  # TODO
        self.hand[h].bet = b
        self.credits -= b

    def hit_otherwise_stand(self, io, h=0):
        """
        Get the state of the current game in the format
        Maps Game state ((open value of dealer, value of my hand, I have ace),
                         (insurance, split, double down, hit))
        """
        global dealer
        self.trolllolo()
        dealer_card = dealer.hand[0].cards[0]
        my_hand_value = self.hand[0].value()
        me_has_ace = self.has_ace()
        seen_state = (dealer_card, my_hand_value, me_has_ace)
        decision_state_0 = (self.ins, self.spl, 0)
        decision_state_1 = (self.ins, self.spl, 1)
        total_state_0 = (seen_state, decision_state_0)
        total_state_1 = (seen_state, decision_state_1)
        if total_state_0 not in self.strategy:
            hit = False
            self.strategy[total_state_0] = []
        elif total_state_1 not in self.strategy:
            hit = True
            self.strategy[total_state_1] = []
        elif len(self.strategy[total_state_0]) < len(self.strategy[total_state_1]) and len(self.strategy[total_state_0]) <= 20:
            hit = False
        elif len(self.strategy[total_state_1]) < len(self.strategy[total_state_0]) and len(self.strategy[total_state_1]) <= 20:
            hit = True
        else:
            # Enough data -> make a "good" decision
            # TODO
            hit = True
        self.hand[h].stand = not hit
        return hit

    def stands(self):
        s = False  # True
        for h in self.hand:
            s = (s or h.stand)  # and
        return s

    def buys_insurance(self, io):
        # if(self.credits >= round(self.hand[0].bet/2)):
        # s = "the dealer has an Ace. Would you like to buy an insurance?"
        return True  # TODO

    def do_buy_insurance(self, io):
        self.ins = 1
        self.insurance = round(self.hand[0].bet / 2)
        self.credits -= round(self.hand[0].bet / 2)

    def split_hand(self, h=0):
        if self.hand[h].can_split():  # and (self.credits >= self.hand[h].bet):
            return True  # TODO
        else:
            return False

    def double_down(self, h=0):
        return True  # TODO

    def update_strategy(self, games):
        return True
