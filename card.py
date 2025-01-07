#!/usr/bin/env python3

from abc import ABC, abstractmethod
from enum import Enum

class CardCategory(Enum):
    Suit = 1
    Pirate = 2
    Mermaid = 3
    SkullKing = 4
    Tigress = 5
    Escape = 6

class Suit(Enum):
    JollyRoger = 1
    Parrot = 2
    TreasureMap = 3
    TreasureChest = 4

class TigressMode(Enum):
    Pirate = 1
    Escape = 2

class Card(ABC):
    def __init__(self, card_category):
        self.card_category = card_category

    @abstractmethod
    def defeats_suit_card(self, other_card, trump_suit):
        pass

    @abstractmethod
    def defeats_pirate(self):
        pass

    @abstractmethod
    def defeats_mermaid(self):
        pass

    @abstractmethod
    def defeats_skull_king(self):
        pass

    @abstractmethod
    def defeats_tigress(self, other_card):
        pass

    @abstractmethod
    def defeats_escape(self):
        pass

    def defeats(self, other_card, trump_suit):
        if other_card.card_category == CardCategory.Suit:
            return self.defeats_suit_card(other_card, trump_suit)
        elif other_card.card_category == CardCategory.Pirate:
            return self.defeats_pirate()
        elif other_card.card_category == CardCategory.Mermaid:
            return self.defeats_mermaid()
        elif other_card.card_category == CardCategory.SkullKing:
            return self.defeats_skull_king()
        elif other_card.card_category == CardCategory.Tigress:
            return self.defeats_tigress(other_card)
        else:
            return self.defeats_escape()

class SuitCard(Card):
    def __init__(self, suit, number):
        super().__init__(CardCategory.Suit)
        self.suit = suit
        self.number = number

    def defeats_suit_card(self, other_card, trump_suit):
        """
        Be careful of the order here. Must do both of these:
        1. Check if self is Jolly Roger before checking if other is trump.
        2. Check if other is Jolly Roger before checking if self is trump.
        """
        if other_card.suit == self.suit:
            return self.number > other_card.number
        elif self.suit == Suit.JollyRoger:
            return True
        elif other_card.suit == trump_suit or other_card.suit == Suit.JollyRoger:
            return False
        elif self.suit == trump_suit:
            return True
        else:
            # Comparing two non-trumps returns False? Shouldn't matter.
            return False

    def defeats_pirate(self):
        return False;

    def defeats_mermaid(self):
        return False

    def defeats_skull_king(self):
        return False

    def defeats_tigress(self, other_card):
        return other_card.tigress_mode == TigressMode.Escape

    def defeats_escape(self):
        return True

class PirateCard(Card):
    def __init__(self):
        super().__init__(CardCategory.Pirate)

    def defeats_suit_card(self, other_card, trump_suit):
        return True

    def defeats_pirate(self):
        return False

    def defeats_mermaid(self):
        return True

    def defeats_skull_king(self):
        return False

    def defeats_tigress(self, other_card):
        return other_card.tigress_mode == TigressMode.Escape

    def defeats_escape(self):
        return True

class MermaidCard(Card):
    def __init__(self):
        super().__init__(CardCategory.Mermaid)

    def defeats_suit_card(self, other_card, trump_suit):
        return True

    def defeats_pirate(self):
        return False

    def defeats_mermaid(self):
        return False

    def defeats_skull_king(self):
        return True

    def defeats_tigress(self, other_card):
        return other_card.tigress_mode == TigressMode.Escape

    def defeats_escape(self):
        return True

class SkullKingCard(Card):
    def __init__(self):
        super().__init__(CardCategory.SkullKing)

    def defeats_suit_card(self, other_card, trump_suit):
        return True

    def defeats_pirate(self):
        return True

    def defeats_mermaid(self):
        return False

    def defeats_skull_king(self):
        raise NotImplementedError("There can only be one Skull King in the deck.")

    def defeats_tigress(self, other_card):
        return True

    def defeats_escape(self):
        return True

class TigressCard(Card):
    def __init__(self):
        super().__init__(CardCategory.Tigress)
        self.tigress_mode = TigressMode.Pirate
 
    def escape(self):
        self.tigress_mode = TigressMode.Escape

    def defeats_suit_card(self, other_card, trump_suit):
        return self.tigress_mode == TigressMode.Pirate

    def defeats_pirate(self):
        return False

    def defeats_mermaid(self):
        return self.tigress_mode == TigressMode.Pirate

    def defeats_skull_king(self):
        return False

    def defeats_tigress(self, other_card):
        raise NotImplementedError("There can only be one Tigress in the deck.")

    def defeats_escape(self):
        return self.tigress_mode == TigressMode.Pirate

class EscapeCard(Card):
    def __init__(self):
        super().__init__(CardCategory.Escape)
  
    def defeats_suit_card(self, other_card, trump_suit):
        return False

    def defeats_pirate(self):
        return False

    def defeats_mermaid(self):
        return False

    def defeats_skull_king(self):
        return False

    def defeats_tigress(self, other_card):
        return False

    def defeats_escape(self):
        return False
