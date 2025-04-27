from assets import Card, Deck, DeckType, Pile
import random

#Classe à appeler pour jouer au Solitaire
class Solitaire:
    def __init__(self, difficulty):
        self.difficulty = difficulty

        self.deck = Deck(DeckType.TINY_FRENCH_SUIT, shuffled=True)
        self.stock = Pile(size=52, name="Stock")
        self.waste = Pile(size=52, name="Stock", revealed_policy="all")

        self.foundations = [
            Pile(name=f"Foundation_{suit}", revealed_policy="all", accept_rule="same_suit", ordered="increasing")
            for suit in ["Pique", "Coeur", "Trefle", "Carreau"]
        ]

        self.tableaus = [
            Pile(size=i+1, name=f"Tableau_{i}", revealed_policy="top")
            for i in range(7)
        ]

        self.temp = Pile(size=20, name="Temp", revealed_policy="all")
    
    def initialize_game(self):
        self.stock.make_pile(self.deck)
        
        i = 0
        for tableau in self.tableaus:
            tableau.make_pile(self.stock)
            tableau._are_cards_up()
            tableau.accept_rule = "alternate_colors"
            tableau.ordered = "decreasing"
            i += 1
        
    def select_card(self, card): # "temp" désigne la Pile temp initialisée dans le constructeur de Solitaire.
        if not card.revealed:
            return False
        
        self.temp.cards.append(card)
        if card.top_neighbor != None:
            self.select_card(card.top_neighbor)
        
        origin = None # Cette variable va désigner la pile d'origine de la (ou des) carte(s)
        for pile in self.tableaus:
            if pile.is_origin(card): # Méthode issue de la classe Pile, dans assets.
                origin = pile
                break
        if not origin and hasattr(self.waste, "origin"):
            origin = self.waste
        if not origin:
            raise ValueError(f"Card {card.suit} {card.value} doesn't have an origin pile. This shouldn't happen!")

        origin.origin = True # Cet attribut sera supprimé avec les méthodes unselect_card() ou drop_card()

        return True
    
    def unselect_card(self): #temp" désigne la Pile temp initialisée dans le constructeur de Solitaire.
        self.temp.cards.clear()
        
        origin = None
        for pile in self.tableaus:
            if hasattr(pile, "origin"):
                origin = pile
                break
        if not origin and hasattr(self.waste, "origin"):
            origin = self.waste
        if not origin:
            raise ValueError(f"No origin pile. This shouldn't happen!")

        del origin.origin
    
    def temp_drop_selection(self, destination):
        # temp désigne la Pile temp initialisée dans le constructeur de Solitaire.
        
        for card in self.temp.cards:
            destination.append_build(card)

        origin = None
        for pile in self.tableaus:
            if hasattr(pile, "origin"):
                origin = pile
                break
        if not origin and hasattr(self.waste, "origin"):
            origin = self.waste
        if not origin:
            raise ValueError(f"No origin pile. This shouldn't happen!")
        
        if origin.cards:
            for card in self.temp.cards:
                if card in origin.cards:
                    origin.cards.remove(card)
            origin.cards[-1].revealed = True
            origin._are_cards_up()
        del origin.origin
        self.temp.cards.clear()

    def solitaire_draw_card(self):
        if self.difficulty == "hard":
            self.stock.draw_card(self.waste, 3)
        
        else:
            self.stock.draw_card(self.waste, 1)
    
    def clic_card(self, card):
        # Va détecter la foundation associée à la carte et vérifier si la carte peut y aller.
        # Sinon, se contentera de sélectionner la carte.
        for found in self.foundations:
            if found.name == f"Foundation_{card.suit}":
                foundation = found
        if not foundation:
            raise ValueError("No foundation found :(")

        if foundation._can_add_card(card):
            origin = None
            for pile in self.tableaus:
                if pile.is_origin(card): #Méthode issue de la classe Pile, dans assets.
                    origin = pile
            if self.waste.is_origin(card):
                origin = self.waste
            if not origin:
                raise ValueError(f"Card {card} doesn't have an origin pile. This shouldn't happen!")
            foundation.cards.append(card)
            origin.cards.remove(card)
        
        else:
            self.select_card(card)
