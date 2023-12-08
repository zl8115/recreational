from __future__ import annotations
import argparse
import logging

global_logger: logging.Logger

from enum import Enum
from dataclasses import dataclass
from collections import Counter
import operator

class HandType(Enum):
    HIGH = 1
    ONE_PAIR = 2
    TWO_PAIR = 3
    THREE = 4
    FULL_HOUSE = 5
    FOUR = 6
    FIVE = 7

    def __lt__(self, other):
        return self.value < other.value
    
    @staticmethod
    def from_hand(hand: str|list[Card]|CardHand):
        carry_over_type = HandType.HIGH
        for _, v in sorted(Counter(hand).items(), key=lambda item: item[1], reverse=True):
            if v == 5:
                return HandType.FIVE
            elif v == 4:
                return HandType.FOUR
            elif v == 3:
                carry_over_type = HandType.THREE
            elif v == 2:
                if carry_over_type == HandType.THREE:
                    return HandType.FULL_HOUSE
                elif carry_over_type == HandType.ONE_PAIR:
                    return HandType.TWO_PAIR
                carry_over_type = HandType.ONE_PAIR
            else:
                return carry_over_type

class Card(int):
    _character: str

    def __new__(cls, value: str):
        if not isinstance(value, str):
            raise ValueError("Value is not a str")
        obj = int.__new__(cls, "23456789TJQKA".index(value))
        obj._character = value
        return obj

    def __str__(self):
        return self._character
    
    def __repr__(self):
        return repr(self._character)
    
class CardHand():
    _card_list: list
    _type: HandType

    def __init__(self, cards: str | list[Card]):
        if isinstance(cards, str):
            cards = [Card(c) for c in cards]
        self._card_list = cards
        self._type = HandType.from_hand(cards)

    def __getitem__(self, index):
        return self._card_list[index]

    def __len__(self):
        return len(self._card_list)

    def __lt__(self, other: CardHand):
        if self._type != other._type:
            return self._type < other._type
        
        min_len = min(len(self), len(other))
        for ii in range(min_len):
            if self[ii] != other[ii]:
                return self[ii] < other[ii]

    def __str__(self):
        return f"{''.join([str(c) for c in self._card_list])} ({str(self._type.name)})"
    
    def __repr__(self):
        return f"CardHand({repr(self._card_list)})"

@dataclass
class CamelCardHandAndBid:
    hand: CardHand
    bid: int

    def __init__(self, entry_line: str):
        card_hand, bid = entry_line.strip().split(" ")
        self.hand = CardHand(card_hand)
        self.bid = int(bid)

    def __lt__(self, other:CamelCardHandAndBid):
        return self.hand < other.hand
    
    def __eq__(self, other: CamelCardHandAndBid):
        return self.hand == other.hand
    
    def __repr__(self):
        return f"({self.hand}, {self.bid})"

def solve_p1():
    global_logger.info("Solving P1")
    card_hands = list()
    for line in yield_next_input_line():
        card_hands.append(CamelCardHandAndBid(line))
    card_hands.sort()
    logging.debug("\n".join([str(pair) for pair in card_hands]))
    acc = 0
    for ii, hand_and_bid in enumerate(card_hands):
        rank = ii + 1
        acc += rank * hand_and_bid.bid
    print(acc)

# 251386999 - Too high
# 251442592 - Even Higher? Noo.....
# 251449505
# 250602800 - Too low
# 246703398
# 251420309 
# 251058093 - Just Right

class JokerCard(int):
    _character: str

    def __new__(cls, value: str):
        if not isinstance(value, str):
            raise ValueError("Value is not a str")
        obj = int.__new__(cls, "J23456789TQKA".index(value))
        obj._character = value
        return obj

    def __str__(self):
        return self._character
    
    def __repr__(self):
        return repr(self._character)

class JokerCardHand(CardHand):
    def __init__(self, cards: str):
        if not isinstance(cards, str):
            raise ValueError("Cards is not a str")
        self._card_list = [JokerCard(c) for c in cards]

        normal_cards = cards.replace("J", "")
        card_count = Counter(normal_cards)
        most_card = "J"
        if card_count:
            most_card = max(card_count.items(), key=operator.itemgetter(1))[0]
        self._type = HandType.from_hand(cards.replace("J", most_card))

class CamelCardJokerHandAndBid(CamelCardHandAndBid):
    def __init__(self, entry_line: str):
        card_hand, bid = entry_line.strip().split(" ")
        self.hand = JokerCardHand(card_hand)
        self.bid = int(bid)

def solve_p2():
    global_logger.info("Solving P2")
    card_hands = list()
    for line in yield_next_input_line():
        card_hands.append(CamelCardJokerHandAndBid(line))
    card_hands.sort()
    logging.debug("\n".join([str(pair) for pair in card_hands]))

    acc = 0
    for ii, hand_and_bid in enumerate(card_hands):
        rank = ii + 1
        acc += rank * hand_and_bid.bid
    print(acc)

# 249781879

def yield_next_input_line() -> str:
    input_file = r"input.txt" if not USE_TEST_INPUT else r"test-input.txt"

    with open(input_file, "r") as in_file:
        for line in in_file:
            yield line.strip()

def log_level_type(x):
    x = int(x)
    if x > 5:
        raise argparse.ArgumentTypeError("Maximum log level is 5")
    return x

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p2", help="Solves Part 2 instead of Part 1", action='store_true', default=False)
    parser.add_argument("--test", "-t", help="Use test-input.txt instead of input.txt", action='store_true', default=False)
    parser.add_argument("--log", "-l", help="Sets the log level between 0-5. 0 is all, 5 is Critical-only. Default=3", type=log_level_type, default=3)

    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()

    logging.basicConfig(level=(args.log*10)) # Logs to stderr
    global_logger = logging.getLogger()
    USE_TEST_INPUT = args.test

    if not args.p2:
        solve_p1()
    else:
        solve_p2()