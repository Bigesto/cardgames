from assets import Card, Deck, DeckType, Pile
import random

#Classe à appeler pour jouer au Solitaire
class Solitaire:
    def __init__(self, difficulty):
        self.difficulty = difficulty

        self.deck = Deck(DeckType.TINY_FRENCH_SUIT, shuffled=True)
        self.stock = Pile(size=52, name="Stock")
        self.waste = Pile(size=52, name="Stock", face_up_policy="all")

        self.foundation = [
            Pile(name=f"Foundation_{suit}", face_up_policy="all", accept_rule="same_suit", ordered="increasing")
            for suit in ["Pique", "Coeur", "Trefle", "Carreau"]
        ]

        self.tableaus = [
            Pile(size=i+1, name=f"Tableau_{i}", face_up_policy="top", accept_rule="alternate_colors", ordered="decreasing")
            for i in range(7)
        ]

        self.temp = Pile(size=20, name="Temp", face_up_policy="all")

        self.initialize_game()
    
    def initialize_game(self):
        self.stock.make_pile(self.deck)
        i = 0
        for tableau in self.tableaus:
            tableau.make_pile(self.stock)
            tableau._are_cards_up()
            tableau.accept_rule = "alternate_colors"
            tableau.ordered = "decreasing"
            i += 1
        
        
    def select_card(self, temp, card): #"temp" désigne la Pile temp initialisée dans le constructeur de Solitaire.
        if not card.face_up:
            return False
        
        temp.cards.append(card)
        if card.top_neighbor != None:
            self.select_card(card.top_neighbor)
        
        origin = None #Cette variable va désigner la pile d'origine de la (ou des) carte(s)
        for pile in self.tableaus:
            if pile.is_origin(card): #Méthode issue de la classe Pile, dans assets.
                origin = pile
                break
        if not origin:
            raise ValueError(f"Card {card} doesn't have an origin pile. This shouldn't happen!")

        origin.origin = True #Cet attribut sera supprimé avec les méthodes unselect_card() ou drop_card()

        return True
    
    def unselect_card(self, temp): #temp" désigne la Pile temp initialisée dans le constructeur de Solitaire.
        temp.cards.clear()
        
        origin = None
        for pile in self.tableaus:
            if hasattr(pile, "origin"):
                origin = pile
                break
        if not origin:
            raise ValueError(f"No origin pile. This shouldn't happen!")

        del origin.origin
    
    def drop_selection(self, temp, destination): # temp" désigne la Pile temp initialisée dans le constructeur de Solitaire.
        for card in temp.cards:
            destination.append_build(card)

        origin = None
        for pile in self.tableaus:
            if hasattr(pile, "origin"):
                origin = pile
                break
        if not origin:
            raise ValueError(f"No origin pile. This shouldn't happen!")
        
        if origin.cards:
            for card in temp.cards:
                if card in origin.cards:
                    origin.cards.remove(card)
            origin.cards[-1].face_up = True
            origin._are_cards_up()
        del origin.origin
        temp.cards.clear()