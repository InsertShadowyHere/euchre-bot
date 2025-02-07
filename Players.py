from random import choice

from Game import Card, BOWERS


class Team:
    tID = 1

    def __init__(self, name, player1, player2):
        self.score = 0
        self.players = [player1, player2]
        self.name = name
        self.ID = Team.tID
        for player in self.players:
            player.team = self.ID
        Team.tID += 1

    def __str__(self):
        return f"{self.name} ({self.ID})"


class Player:
    def __init__(self, name):
        self.hand = []
        self.name = name
        self.team = None
        self.pos = 0

    # return cards, pls
    def trick(self, cards: list, pls: list, trump: str) -> tuple:
        if cards:
            # --------- card logic handling ---------
            if cards[0].value != "J" or cards[0].suit != BOWERS[trump]:
                forced = cards[0].suit
            else:
                forced = trump
            choices = []
            if trump:
                pass
            for card in self.hand:
                # if the card is forced and not a jack, allow
                if forced == card.suit and card.value != "J":
                    choices.append(card)
                # if the trump is forced and its one of the bowers, allow
                elif forced == trump and (
                        BOWERS[forced] == card.suit or forced == card.suit) and card.value == "J":
                    choices.append(card)
                # if the forced is not the same color as the trump, and the card suit is the forced suit
                elif (forced != BOWERS[trump] and forced != trump) and forced == card.suit and card.value == "J":
                    choices.append(card)
            # ------- end card logic handling -------

            if choices:
                pick = input(f"What card do you pick? The valid cards are {choices}\n")
                while pick not in choices:
                    pick = input("That's not a valid card. Pick again: ")
            else:
                pick = input(f"What card do you pick? Your hand is {self.hand}\n")
                while pick not in self.hand:
                    pick = input("That's not a valid card. Pick again: ")
        # VVV this section is fine VVV
        else:
            pick = input(f"What card do you pick? Your hand is {self.hand}\n")
            while pick not in list(map(str, self.hand)):
                pick = input("That's not a valid card. Pick again: ")
        for card in self.hand:
            if card == pick:
                self.hand.remove(card)
                cards.append(card)
                break
        pls.append(self)
        return cards, pls

    # Handle whether to call the flip
    def flip(self, flip, rnd) -> bool | str:
        if rnd == 1:
            print(f"Do you call to pick it up? (Y/N) Your hand is {self.hand}")
            pick = input()
            if pick == "Y" or pick == "y":
                return True
            else:
                return False
        elif rnd == 2:
            pick = input(
                f"You now have a choice between the four suits.\nYour hand is {self.hand}\nPick one of HSDC or pass with P.\n")
            if pick in "HSDC":
                return pick
            else:
                return 'no'
        elif rnd == 3:
            pick = input()
            # pick must exist, be in HSDC, and not the blocked suit
            while pick not in "HSDC" or pick == flip.suit or not pick:
                pick = input("That's not a valid suit. Please re-enter: ")
            return pick

    # DEALER ONLY - Handle picking up the flip
    def pickup(self, card) -> Card:
        print(f"Your hand is {self.hand}. Pick one card to drop in place of the {card}")
        pick = input()
        while pick not in self.hand:
            pick = input("That's not a valid card. Please re-enter: ")
        self.hand.append(card)
        self.hand.remove(pick)
        return Card(pick[:-1], pick[-1])

    # determine position on table
    def update(self, players) -> None:
        self.pos = players.index(self)

    def __str__(self):
        return f"{self.name}(team={self.team}, hand={self.hand})"


class Bot(Player):
    def __init__(self, name):
        super().__init__(name)
        self.name += "-BOT"

    def trick(self, cards: list, pls: list, trump: str) -> tuple:
        if cards:
            # --------- card logic handling ---------
            if cards[0].value != "J" or cards[0].suit != BOWERS[trump]:
                forced = cards[0].suit
            else:
                forced = trump
            choices = []
            for card in self.hand:
                # if the card is forced and not a jack, allow
                if forced == card.suit and card.value != "J":
                    choices.append(card)
                # if the trump is forced and its one of the bowers, allow
                elif forced == trump and (
                        BOWERS[forced] == card.suit or forced == card.suit) and card.value == "J":
                    choices.append(card)
                # if the forced is not the same color as the trump, and the card suit is the forced suit
                elif (forced != BOWERS[trump] and forced != trump) and cards[
                    0].suit == card.suit and card.value == "J":
                    choices.append(card)
            # ------- end card logic handling -------

            if choices:
                pick = choice(choices)
            else:
                pick = choice(self.hand)
        # VVV this section is fine VVV
        else:
            pick = choice(self.hand)
        self.hand.remove(pick)
        cards.append(pick)
        pls.append(self)
        return cards, pls

    def pickup(self, card) -> str:
        pick = choice(self.hand)
        print(f"DEBUG: {self.name} chooses to drop {pick}")
        self.hand.append(card)
        self.hand.remove(pick)
        return pick

    # evaluates hand value (placeholder for more complex data)
    def evaluate(self):
        pass

    # currently random, placeholder
    def flip(self, card, rnd) -> bool | str:
        if rnd == 1:
            return choice([False] * 3 + [True])
        elif rnd == 2:
            return choice(['P'] * 4 + ["H", "S", "D", "C"])
        elif rnd == 3:
            return choice(["H", "S", "D", "C"])
