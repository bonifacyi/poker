#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -----------------
# Реализуйте функцию best_hand, которая принимает на вход
# покерную "руку" (hand) из 7ми карт и возвращает лучшую
# (относительно значения, возвращаемого hand_rank)
# "руку" из 5ти карт. У каждой карты есть масть(suit) и
# ранг(rank)
# Масти: трефы(clubs, C), пики(spades, S), червы(hearts, H), бубны(diamonds, D)
# Ранги: 2, 3, 4, 5, 6, 7, 8, 9, 10 (ten, T), валет (jack, J), дама (queen, Q), король (king, K), туз (ace, A)
# Например: AS - туз пик (ace of spades), TH - дестяка черв (ten of hearts), 3C - тройка треф (three of clubs)

# Задание со *
# Реализуйте функцию best_wild_hand, которая принимает на вход
# покерную "руку" (hand) из 7ми карт и возвращает лучшую
# (относительно значения, возвращаемого hand_rank)
# "руку" из 5ти карт. Кроме прочего в данном варианте "рука"
# может включать джокера. Джокеры могут заменить карту любой
# масти и ранга того же цвета, в колоде два джокерва.
# Черный джокер '?B' может быть использован в качестве треф
# или пик любого ранга, красный джокер '?R' - в качестве черв и бубен
# любого ранга.

# Одна функция уже реализована, сигнатуры и описания других даны.
# Вам наверняка пригодится itertools.
# Можно свободно определять свои функции и т.п.
# -----------------

from itertools import combinations, product, chain

HAND_SIZE = 5
LETTERS = {'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
SUITS = ['C', 'S', 'D', 'H']
JOKERS = {
    '?R': [str(x[0])+x[1] for x in product(chain(range(2, 10), LETTERS.keys()), SUITS[2:])],
    '?B': [str(x[0])+x[1] for x in product(chain(range(2, 10), LETTERS.keys()), SUITS[:2])],
}


def hand_rank(hand):
    """Возвращает значение определяющее ранг 'руки'"""
    ranks = card_ranks(hand)
    if straight(ranks) and flush(hand):
        return 8, max(ranks)
    elif kind(4, ranks):
        return 7, kind(4, ranks), kind(1, ranks)
    elif kind(3, ranks) and kind(2, ranks):
        return 6, kind(3, ranks), kind(2, ranks)
    elif flush(hand):
        return 5, *ranks
    elif straight(ranks):
        return 4, max(ranks)
    elif kind(3, ranks):
        return 3, kind(3, ranks), *ranks
    elif two_pair(ranks):
        return 2, *two_pair(ranks), *ranks
    elif kind(2, ranks):
        return 1, kind(2, ranks), *ranks
    else:
        return 0, *ranks


def int_rank(r):
    if r in LETTERS.keys():
        r = LETTERS[r]
    return int(r)


def card_ranks(hand):
    """Возвращает список рангов (его числовой эквивалент),
    отсортированный от большего к меньшему"""
    return sorted([int_rank(rank[0]) for rank in hand], reverse=True)


def flush(hand):
    """Возвращает True, если все карты одной масти"""
    return len(set([suit[1] for suit in hand])) == 1


def straight(ranks):
    """Возвращает True, если отсортированные ранги формируют последовательность 5ти,
    где у 5ти карт ранги идут по порядку (стрит)"""
    ans = True
    for i in range(len(ranks) - 1):
        if ranks[i] - ranks[i+1] != 1:
            ans = False
    return ans


def kind(n, ranks):
    """Возвращает первый ранг, который n раз встречается в данной руке.
    Возвращает None, если ничего не найдено"""
    for rank in ranks:
        if ranks.count(rank) == n:
            return rank


def two_pair(ranks):
    """Если есть две пары, то возврщает два соответствующих ранга,
    иначе возвращает None"""
    ranks_dup = ranks.copy()
    pair = []
    for rank in ranks:
        if ranks_dup.count(rank) == 2:
            ranks_dup.remove(rank)
            pair.append(rank)
    if len(pair) == 2:
        return sorted(pair, reverse=True)


def best_hand(big_hand):
    """Из "руки" в 7 карт возвращает лучшую "руку" в 5 карт """
    best_rank = (0,)
    b_hand = []
    for hand in combinations(big_hand, HAND_SIZE):
        rank = hand_rank(hand)
        if rank[0] > best_rank[0] or len(best_rank) == 1:
            best_rank = rank
            b_hand = hand
        elif rank[0] == best_rank[0]:
            for i in range(1, len(rank)):
                if rank[i] > best_rank[i]:
                    best_rank = rank
                    b_hand = hand
    return b_hand


def gen_hands(hand):
    hands = []
    if '?R' in hand:
        for card in JOKERS['?R']:
            if card in hand:
                continue
            h = hand.copy()
            h.remove('?R')
            h.append(card)
            hands.extend(gen_hands(h))
    elif '?B' in hand:
        for card in JOKERS['?B']:
            if card in hand:
                continue
            h = hand.copy()
            h.remove('?B')
            h.append(card)
            hands.extend(gen_hands(h))
    else:
        hands.append(hand)
    return hands


def best_wild_hand(big_hand):
    """best_hand но с джокерами"""
    hands_list = []
    combi = combinations(big_hand, HAND_SIZE)
    for h in combi:
        hands_list.extend(gen_hands(list(h)))

    best_rank = (0,)
    b_hand = []
    for hand in hands_list:
        rank = hand_rank(hand)
        if rank[0] > best_rank[0] or len(best_rank) == 1:
            best_rank = rank
            b_hand = hand
        elif rank[0] == best_rank[0]:
            for i in range(1, len(rank)):
                if rank[i] > best_rank[i]:
                    best_rank = rank
                    b_hand = hand
                    break
                elif rank[i] < best_rank[i]:
                    break
    return b_hand


def test_best_hand():
    print("test_best_hand...")
    assert (sorted(best_hand("6C 7C 8C 9C TC 5C JS".split()))
            == ['6C', '7C', '8C', '9C', 'TC'])
    assert (sorted(best_hand("TD TC TH 7C 7D 8C 8S".split()))
            == ['8C', '8S', 'TC', 'TD', 'TH'])
    assert (sorted(best_hand("JD TC TH 7C 7D 7S 7H".split()))
            == ['7C', '7D', '7H', '7S', 'JD'])
    print('OK')


def test_best_wild_hand():
    print("test_best_wild_hand...")
    assert (sorted(best_wild_hand("6C 7C 8C 9C TC 5C ?B".split()))
            == ['7C', '8C', '9C', 'JC', 'TC'])
    assert (sorted(best_wild_hand("TD TC 5H 5C 7C ?R ?B".split()))
            == ['7C', 'TC', 'TD', 'TH', 'TS'])
    assert (sorted(best_wild_hand("JD TC TH 7C 7D 7S 7H".split()))
            == ['7C', '7D', '7H', '7S', 'JD'])
    print('OK')


if __name__ == '__main__':
    test_best_hand()
    test_best_wild_hand()
    # print(sorted(best_hand("TH TS TD TC 5H 5C 7C".split())))
    # print(sorted(best_wild_hand("TD TC 5H 5C 7C ?R ?B".split())))

    """print(card_ranks(['7C', 'AC', '9C', 'JC', 'TC']))
    print(flush(['7C', 'AC', '9C', 'JC', 'TC']))
    print(straight([14, 13, 12, 11, 9]))
    print(kind(4, [11, 11, 11, 11, 7]))
    print(two_pair([7, 7, 9, 11, 11]))
    print(best_hand("TD TC TH 7C 7D 8C TS".split()))"""