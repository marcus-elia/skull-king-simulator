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

SUIT_TO_COLOR = {"JollyRoger": "Black", "Parrot": "Green", "TreasureMap": "Purple", "TreasureChest": "Yellow"}

class Suit(Enum):
    JollyRoger = 1
    Parrot = 2
    TreasureMap = 3
    TreasureChest = 4

    def __str__(self):
        return SUIT_TO_COLOR[self.name]

class TigressMode(Enum):
    Pirate = 1
    Escape = 2

class Card(ABC):
    current_id_number = 1
    def __init__(self, card_category):
        self.card_category = card_category
        self.id_number = Card.current_id_number
        Card.current_id_number += 1

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
        else:
            return self.defeats_no_trump(other_card)

    def defeats_no_trump(self, other_card):
        """
        This version is when no trump suit has been determined.
        """
        if other_card.card_category == CardCategory.Suit:
            return self.defeats_suit_card_no_trump(other_card)
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

    def __eq__(self, other):
        return self.id_number == other.id_number

    @abstractmethod
    def __str__(self):
        pass

    def is_escape(self):
        return self.card_category == CardCategory.Escape or (self.card_category == CardCategory.Tigress and self.tigress_mode == TigressMode.Escape)

    def is_pirate(self):
        return self.card_category == CardCategory.Pirate or (self.card_category == CardCategory.Tigress and self.tigress_mode == TigressMode.Pirate)

class SuitCard(Card):
    def __init__(self, suit, number):
        super().__init__(CardCategory.Suit)
        self.suit = suit
        self.number = number
        self.power = self.number
        if self.suit == Suit.JollyRoger:
            self.power += 14

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

    def defeats_suit_card_no_trump(self, other_card):
        """
        Comparison when there is no trump suit.
        """
        if other_card.suit == self.suit:
            return self.number > other_card.number
        elif self.suit == Suit.JollyRoger:
            return True
        else:
            # If the cards are not the same and this is not a jolly roger.
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

    def __str__(self):
        return str(self.suit) + " " + str(self.number)

class PirateCard(Card):
    def __init__(self):
        super().__init__(CardCategory.Pirate)
        self.power = 30

    def defeats_suit_card_no_trump(self, other_card):
        return True

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

    def __str__(self):
        return "Pirate"

class MermaidCard(Card):
    def __init__(self):
        super().__init__(CardCategory.Mermaid)
        self.power = 29

    def defeats_suit_card_no_trump(self, other_card):
        return True

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

    def __str__(self):
        return "Mermaid"

class SkullKingCard(Card):
    def __init__(self):
        super().__init__(CardCategory.SkullKing)
        self.power = 31

    def defeats_suit_card_no_trump(self, other_card):
        return True

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

    def __str__(self):
        return "The Skull King"

class TigressCard(Card):
    def __init__(self):
        super().__init__(CardCategory.Tigress)
        self.tigress_mode = TigressMode.Pirate
        self.power = 30
 
    def escape(self):
        self.tigress_mode = TigressMode.Escape
        self.power = 0

    def defeats_suit_card_no_trump(self, other_card):
        return self.tigress_mode == TigressMode.Pirate

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

    def __str__(self):
        return "Tigress"

class EscapeCard(Card):
    def __init__(self):
        super().__init__(CardCategory.Escape)
        self.power = 0
  
    def defeats_suit_card_no_trump(self, other_card):
        return False

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

    def __str__(self):
        return "Escape"
