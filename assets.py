from enum import Enum
import random

class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit #"Atout" "Pique" "Trefle" "Coeur" "Carreau"
        self.name = None
        self.color = None
        self.in_pile = None
        self.revealed = False
        self.top_neighbor = None

        if self.suit != "Atout":
            card_names = {1: "As", 11: "Valet", 12: "Dame", 13: "Roi", 14: "Cavalier"}
            self.name = card_names.get(self.value, str(self.value))

        if self.suit == "Atout":
            card_names = {0: "Excuse", 1: "Petit", 21: "Vingt-et-un", 22: "Joker 1", 23: "Jocker 2"}
            self.name = card_names.get(self.value, str(self.value))

        if self.suit == "Pique" or self.suit == "Trefle":
            self.color = "noire"
        if self.suit == "Coeur" or self.suit == "Carreau":
            self.color = "rouge"
        
        
class DeckType(Enum):
    FRENCH_SUIT = 1
    TAROT = 2
    SPIDER_1 = 3
    SPIDER_2 = 4
    SPIDER_3 = 5
    TINY_FRENCH_SUIT = 6

class Deck:
    def __init__(self, type, shuffled=False):
        if not isinstance(type, DeckType):
            raise ValueError("DeckType not recognized")

        self.type = type
        self.shuffled = shuffled

        self.initialize_deck()
        if self.shuffled:
            self.shuffle_deck(2)

    
    def initialize_deck(self): #Initialise le deck du jeu. Est fonction de DeckType, lui-même fonction du type de jeu.
        self.cards = []
        if self.type == DeckType.FRENCH_SUIT:
            enseignes = ["Pique", "Coeur", "Trefle", "Carreau"]

            for enseigne in enseignes:
                for i in range (1, 14):
                    self.cards.append(Card(i, enseigne))

            self.cards.append(Card(22, "atout"))
            self.cards.append(Card(23, "atout"))
        
        if self.type == DeckType.TINY_FRENCH_SUIT:
            enseignes = ["Pique", "Coeur", "Trefle", "Carreau"]

            for enseigne in enseignes:
                for i in range (1, 14):
                    self.cards.append(Card(i, enseigne))
        
    
    def shuffle_deck(self, seed=None):
        if seed is not None:
            random.seed(seed)
        random.shuffle(self.cards)

class Pile:
    def __init__(self, size=None, name=None, max_size=None, revealed_policy="none", accept_rule=None, ordered=None):
        self.size = size
        self.name = name
        self.max_size = max_size #to prevent filthy cheaters to fill their sleeves
        self.revealed_policy = revealed_policy #"none", "top", "all"
        self.accept_rule = accept_rule #"same_suit" "alternate_colors"
        self.ordered = ordered #"increasing" "decreasing"
        self.cards = []
    
    def make_pile(self, deck): #Faire une pile de sa taille (self.size) à partir d'un deck (ou d'un autre ensemble de cartes).
        if self.max_size is not None:
            if self.size > self.max_size:
                raise ValueError("Size > Max-size. Size cannot exceed max-size.")

        i = 0
        while i < self.size and len(deck.cards) > 0:
                card = deck.cards.pop()
                if self.name:
                    card.in_pile = self.name
                self.cards.append(card)
                i += 1

        if len(self.cards) > 0 and self.revealed_policy == "top":
            self.cards[-1].revealed = True

        elif self.cards and self.revealed_policy == "all":
            for card in self.cards:
                card.revealed = True
        
        return i

    def draw_card(self, dest, qty, hidden=False): #Pour piocher une carte d'une pile vers une autre (idéalement la pioche vers la main ou la défausse)
        i = 0
        while i < qty and len(self.cards) > 0:
            card = self.cards.pop()
            if not hidden:
                card.revealed = True
            if dest.name:
                card.in_pile = dest.name
            dest.cards.append(card)
            i += 1

        return i
    
    def _can_add_card(self, card):

        if len(self.cards) == 0:
            if self.ordered == "increasing":
                if card.value != 1:
                    return False
            if self.ordered == "decreasing":
                if card.value != 13:
                    return False
            return True

        if self.accept_rule == "alternate_colors" and card.color == self.cards[-1].color:
            return False
        if self.accept_rule == "same_suit" and card.suit != self.cards[-1].suit:
            return False
        if self.ordered == "increasing" and not card.value == (self.cards[-1].value + 1):
            return False
        if self.ordered == "decreasing" and not card.value == (self.cards[-1].value - 1):
            return False
        return True
    
    def _are_cards_up(self): #Not only a check, will also turn cards that face the wrong direction.
        if self.revealed_policy == "top":
            if not self.cards[-1].revealed:
                self.cards[-1].revealed = True
                return True
            else:
                return True
        
        if self.revealed_policy == "all":
            for card in self.cards:
                if not card.revealed:
                    card.revealed = True
                else:
                    continue
            return True
        
        if self.revealed_policy == "none":
            if self.cards[-1].revealed:
                self.cards[-1].revealed = False
                return False
            else:
                return False

        return True
    
    def is_origin(self, card): #Used to set a pile as origin of the cards in select_card() method (in gameslogic.py)
        if card in self.cards:
            print(f"{self.name} is origin")
            return True
        print("no origin")
        return False
    
    def append_build(self, card): # Utilisé pour libérer une pile sur une autre, carte par carte.
        if len(self.cards) < 1 and card.value != 13:
            return False
        
        # Vérifier si on peut ajouter cette carte au build actuel.
        if len(self.cards) > 0 and not self._can_add_card(card):
            return False
            
        # Ajouter la carte et établir les relations.
        if len(self.cards) > 0:
            self.cards[-1].top_card = card
        self.cards.append(card)
        return True