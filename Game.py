import time
from random import shuffle


class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def evaluate(self, winsuit, trump):
        if self.value == "J":
            if self.suit == BOWERS[trump]:
                return 6
            elif self.suit == trump:
                return 7
            elif self.suit == winsuit:
                return 3
            else:
                return -1
        elif self.suit == winsuit:
            return ORDER.index(self.value) + 1
        else:
            return -1
        # point values (Spades win) (Clubs trump):
        # 9S 10S QS KS AS JC JS
        # point values (spades win) (diamonds trump):
        # 9s 10s js qs ks as

    def __str__(self):
        return str(self.value + self.suit)

    def __repr__(self):
        return str(self.value + self.suit)

    def __eq__(self, other):
        if isinstance(other, str):
            return str(self) == other
        elif self.suit == other.suit and self.value == other.value:
            return True
        return False


# values 0     1     2    3    4    5    6(left) 7(right)
ORDER = ['9', '10', '!', 'Q', "K", "A"]
BOWERS = {"S": "C", "C": "S", "H": "D", "D": "H"}

VALUES = ["9", "10", "J", "Q", "K", "A"]
SUITS = ["H", "D", "S", "C"]
DECK = [Card(suit, val) for suit in SUITS for val in VALUES]


def partition(msg=''):
    print(f"\n-------------------------{msg}-------------------------\n")


def evaluate_trick(cards, pls, trump) -> int:
    """
    Evaluates the winner of a trick and return them.\n
    !!!nongraphical!!!
    :param cards:
    :param pls:
    :param trump:
    :return:
    """
    # evaluate winning suit
    winsuit = cards[0].suit
    winind = 4
    winpts = 0
    for card in cards:
        if card.suit == trump:
            winsuit = card.suit

    # evaluate ranking of cards
    for ct, card in enumerate(cards):
        # find value of each card in the winning suit
        if card.suit == winsuit or card.value == "J":
            points = card.evaluate(winsuit, trump)
            print(f"DEBUG: card {card} has points {points}")
            # adjust to max, and insert index
            if points > winpts:
                winpts = points
                winind = ct
    print(f"DEBUG: Trump: {trump}, winning suit: {winsuit}, winning points {winpts}, cards: {cards}, ")
    return pls[winind]


def evaluate_round(tricks: list, maker: int, teams, alone=False) -> tuple:
    """
    :param tricks: list of winning team ids
    :param maker: trump setter team id
    :param alone: whether someone went alone (UNUSED)
    :return:
    """
    if 2 < tricks.count(maker) < 5:
        twinner = maker
        pts = 1
    elif tricks.count(maker) == 5:
        twinner = maker
        pts = 2
    else:
        twinner = 1 if maker == 2 else 2
        pts = 2

    for team in teams:
        if team.ID == twinner:
            team.score += pts
            print(f"{team.name} wins {pts} points!")
            break


class Game:
    def __init__(self, team1, team2):
        print(f"LOG {time.time()} - Board initializing...")
        self.teams = [team1, team2]
        self.players = [team1.players[0], team2.players[0], team1.players[1], team2.players[1]]
        # round based vars
        self.deck = []
        self.trump = "N/A (not in round)"
        self.next = 0  # index for next player (starts at 0, left of dealer)
        self.order = ORDER
        for player in self.players:
            print(f"LOG {time.time()} - Player registered: {player.name}")

    # run one round (rn, may change)
    def run(self):
        maker = self.deal()
        tricks = []
        for i in range(5):
            prev = self.trick()
            tricks.append(prev.team)
            self.next = self.players.index(prev)
            if i < 5:
                partition(msg=f"TRICK {i + 2}")
        print(f"DEBUG: {tricks}")
        evaluate_round(tricks, maker, self.teams)


    def deal(self):
        """
        Handles shuffling, dealing, and determining the trump.
        :param self:
        """
        # shuffle deck
        print(f"LOG {time.time()} - Shuffling deck...")
        shuffle(DECK)
        self.deck = DECK

        # deal 5 cards
        print(f"LOG {time.time()} - Dealing cards...")
        for _ in range(5):
            for player in self.players:
                player.hand.append(self.deck[0])
                del self.deck[0]
        print(f"LOG {time.time()} - Cards dealt!")

        # -----DEV CODE-----
        partition(msg="HANDS")
        for player in self.players:
            print(player.hand)
        # -----END CODE-----

        # next dealer (players[-1])
        self.players.append(self.players[0])
        del self.players[0]

        for player in self.players:
            player.update(self.players)

        partition(msg="TABLE")
        print(f"""The dealer is {self.players[-1].name} and the table is arranged as follows:
   -{self.players[3].name}-
{self.players[2].name} {self.players[0].name}
   {self.players[1].name}""")

        partition(msg="FLIP")

        flip = self.deck[0]
        print(f"The flip is {self.deck[0]}")
        # flip round 1 - pick up
        for player in self.players:
            if player.flip(flip, 1):
                maker = player.team
                print(f"{player.name} has called to pick up the {flip}.")
                self.trump = self.deck[0].suit
                self.deck.append(self.players[-1].pickup(flip))
                del self.deck[0]
                flip = None
                break
            else:
                print(f"{player.name} has passed.")

        # flip round 2 - name
        if flip:
            blocked = flip.suit
            print("Nobody has chosen to pick up the flip.")
            print(f"Each player may now choose to call any suit aside from {blocked}.")
            for player in self.players[:-1]:
                pick = player.flip(flip, 2)
                if pick in "HDSC" and pick != flip.suit:
                    maker = player.team
                    self.trump = pick
                    print(f"The trump suit of {self.trump} has been chosen by {player.name}.")
                    flip = None
                    break
                else:
                    print(f"{player.name} passed.")

        # flip round 3 - screw the dealer
        if flip:
            print("The dealer must pick a trump suit. (HSDC)")
            self.trump = self.players[-1].flip(flip, 3)
            maker = self.players[-1].team
            print(f"The trump suit of {self.trump} has been chosen by {self.players[-1].name}.")

        partition(msg="BOARD")
        print(self)
        partition(msg="ROUND START")
        return maker

    # run 5 tricks, then analyze round
    def trick(self) -> int:
        # number of tricks
        cards = []
        pls = []
        print(f"{self.players[self.next].name} goes first!")
        # run trick the 3 players left
        for _ in range(4):
            cards, pids = self.players[self.next].trick(cards, pls, self.trump)
            print(f"{pids[-1].name} played {cards[-1]}")
            self.next += 1
            if self.next == 4:
                self.next = 0
        winner = evaluate_trick(cards, pls, self.trump)
        print(f"The final board is {cards}. {winner.name} on team {winner.team} wins.")
        return winner

    def __str__(self):
        return f"""
        Current board status:
        Team 1 ({self.teams[0].name}):
        {self.teams[0].players[0]}
        {self.teams[0].players[1]}
        Team 2 ({self.teams[1].name}):
        {self.teams[1].players[0]}
        {self.teams[1].players[1]}

        Kitty: {self.deck}
        Trump: {self.trump}
        """
