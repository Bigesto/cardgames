from assets import Card, Deck, DeckType, Pile
import random

#Classe à appeler pour jouer au Solitaire
class Solitaire:
    def __init__(self, difficulty):
        self.difficulty = difficulty

        self.deck = Deck(DeckType.TINY_FRENCH_SUIT, shuffled=True)
        self.stock = Pile(size=52, name="Stock")
        self.waste = Pile(size=52, name="Waste", revealed_policy="all")

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

    def solitaire_draw_card(self):
        if self.difficulty == "hard":
            self.stock.draw_card(self.waste, 3)
        
        else:
            self.stock.draw_card(self.waste, 1)
    
    def solitaire_clic_card_in_waste(self, card): # "card" doit être la dernière carte de la pile waste.cards.
        if not card in self.waste.cards:
            return False
        if not card == self.waste.cards[-1]:
            return False

        foundation = None
        for found in self.foundations:
            if found.name == f"Foundation_{card.suit}":
                foundation = found
        if not foundation:
            raise ValueError(f"""No foundation found, this should not happen. Card foundation should be "Foundation_{card.suit}".""")
        
        if foundation._can_add_card(card):
            foundation.cards.append(self.waste.cards.pop())
            card.in_pile = foundation.name
            return True
        
        for tableau in self.tableaus:
            if tableau._can_add_card(card):
                tableau.cards.append(self.waste.cards.pop())
                card.in_pile = tableau.name
                return True
        
        return False
        
    def solitaire_clic_card_in_foundation(self, card): #card doit être la dernière carte de sa pile.
        foundation = None
        for found in self.foundations:
            if found.name == card.in_pile:
                foundation = found
        
        if not foundation:
            raise ValueError(f"""No foundation found, this should not happen. Card foundation should be "Foundation_{card.suit}".""")
        if not card in foundation.cards:
            raise ValueError("Card is not in this foundation, but should be...")
        if not card == foundation.cards[-1]:
            print("This is not the last card in this foundation...")
            return False
        
        for tableau in self.tableaus:
            if tableau._can_add_card(card):
                tableau.cards.append(foundation.cards.pop())
                card.in_pile = tableau.name
                return True
        
        return False
        
    def solitaire_clic_card_in_tableau(self, card):
        if not card.revealed:
            return False
        tableau = None
        foundation = None
        position = None

        for found in self.foundations:
            if found.name == f"Foundation_{card.suit}":
                foundation = found
        if not foundation:
            raise ValueError(f"""No foundation found, this should not happen. Card foundation should be "Foundation_{card.suit}".""")

        for tab in self.tableaus:
            if tab.name == card.in_pile:
                tableau = tab
                position = tableau.cards.index(card)
        if not tableau:
            raise ValueError(f"""No tableau found, this should not happen.""")
        
        if (card == tableau.cards[-1]) and foundation._can_add_card(card):
            foundation.cards.append(tableau.cards.pop())
            card.in_pile = foundation.name
            return True
        
        for tab in self.tableaus:
            if tab.name == tableau.name:
                continue
            if tab._can_add_card(card):
                cards_to_move = tableau.cards[position:]
                for card in cards_to_move:
                    card.in_pile = tab.name
                tab.cards.extend(cards_to_move)
                tableau.cards[position:] = []
                return True
      
        return False

        # foundation = None
        # for found in self.foundations:
        #     if card in found.cards:
        #         self.select_card(card)
        #         return
        #     if found.name == f"Foundation_{card.suit}":
        #         foundation = found
        #         print(f"{foundation.name} is foundation")
        #         break
        # if not foundation:
        #     raise ValueError("No foundation found :(")
        
        # if len(self.temp.cards) > 0:
        #     if destination and destination._can_add_card(self.temp.cards[0]):
        #         self.temp_drop_selection(destination)
        #         return
        #     self.unselect_card()
        #     print("cards unselected")
        #     return

        # if foundation._can_add_card(card):
        #     origin = None
        #     for pile in self.tableaus:
        #         if pile.is_origin(card): #Méthode issue de la classe Pile, dans assets.
        #             origin = pile
        #             break
            
        #     if origin == None and self.waste.is_origin(card):
        #         origin = self.waste

        #     if origin == None:
        #         raise ValueError(f"Card {card} doesn't have an origin pile. This shouldn't happen!")
            
        #     if card == origin.cards[-1]:
        #         foundation.cards.append(card)
        #         origin.cards.remove(card)
        
        # else:
        #     self.select_card(card)
