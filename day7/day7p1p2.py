from day7.hand import Hand


def read_hand_and_bid(line, hand_constructor):
    parts = line.split()
    return {
        'hand': hand_constructor(parts[0]),
        'bid': int(parts[1])
    }


def sort_plays_by_rank(plays):
    plays.sort(key=lambda p: p['hand'])


def get_total_winnings_for_hands(input_file, hand_constructor=Hand.from_cards):
    lines = open(input_file, 'r').readlines()
    plays = list(map(lambda line: read_hand_and_bid(line, hand_constructor), lines))
    sort_plays_by_rank(plays)
    print('Plays in rank order: ', plays)
    winnings = 0
    for i in range(0, len(plays)):
        rank = i + 1
        play = plays[i]
        winnings += play['bid'] * rank
    return winnings
