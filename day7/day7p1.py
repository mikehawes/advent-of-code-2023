from day7.hand import Hand


def read_hand_and_bid(line):
    parts = line.split()
    return hand_and_bid(parts[0], parts[1])


def hand_and_bid(hand, bid):
    return {
        'hand': Hand(hand),
        'bid': int(bid)
    }


def sort_plays_by_rank(plays):
    plays.sort(key=lambda p: p['hand'])


def get_total_winnings_for_hands(input_file):
    lines = open(input_file, 'r').readlines()
    plays = list(map(read_hand_and_bid, lines))
    sort_plays_by_rank(plays)
    print('Plays in rank order: ', plays)
    winnings = 0
    for i in range(0, len(plays)):
        rank = i + 1
        play = plays[i]
        winnings += play['bid'] * rank
    return winnings
