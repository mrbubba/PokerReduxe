from random import shuffle


def get_range(pct, rnd):
    """ returns a list of card combos within a given percentage takes a number from 1 to 100 as an argument
    for percentage of hands to be played, the second parameter also a number from 1 to 100 is the percentage of hands
    to be removed from the bottom of the new hand range and replaced with hands from the bottom of the full_range
    list """

    # full_range is a list of all possible pre-flop hands ranked from best to worst.
    full_range = ('AA', 'KK', 'QQ', 'AKs', 'JJ', 'AQs', 'KQs', 'AJs', 'KJs', '1010', 'AK', 'A10s', 'QJs',
                  'K10s', 'Q10s', 'J10s', '99', 'AQ', 'A9s', 'KQ', '88', 'K9s', '109s', 'A8s', 'Q9s', 'J9s', 'AJ',
                  'A5s', '77', 'A7s', 'KJ', 'A4s', 'A3s', 'A6s', 'QJ', '66', 'K8s', '108s', 'A2s', '98s', 'J8s', 'A10',
                  'Q8s', 'K7s', 'K10', '55', 'J10', '87s', 'Q10', '44', '33', '22', 'K6s', '97s', 'K5s', '76s', '107s',
                  'K4s', 'K3s', 'K2s', 'Q7s', '86s', '65s', 'J7s', '54s', 'Q6s', '75s', '96s', 'Q5s', '64s', 'Q4s',
                  'Q3s', '109', '106s', 'Q2s', 'A9', '53s', '85s', 'J6s', 'J9', 'K9', 'J5s', 'Q9', '43s', '74s', 'J4s',
                  'J3s', '95s', 'J2s', '63s', 'A8', '52s', '105s', '84s', '104s', '103s', '42s', '102s', '98', '108',
                  'A5', 'A7', '73s', 'A4', '32s', '94s' '93s', 'J8', 'A3', '62s', '92s', 'K8', 'A6', '87', 'Q8', '83s',
                  'A2s', '82S', '97', '72s', '76', 'K7', '65', '107', 'K6', '86', '54', 'K5', 'J7', '75', 'Q7s', 'K4',
                  'K3', '96', 'K2', '64', 'Q6', '53', '85', '106', 'Q5', '43', 'Q4', 'Q3', '74', 'Q2', 'J6', '63', 'J5',
                  '95', '52', 'J4', 'J3', '42', 'J2', '84', '105', '104', '32', '103', '73', '102', '62', '94', '93',
                  '92', '83', '82', '72')

    limit = 0
    my_range = ()
    pairs = ('AA', 'KK', 'QQ', 'JJ', '1010', '99', '88', '77', '66', '55', '44', '33', '22')

    for hand in full_range:

        if limit < pct:
            my_range.append(hand)
            # The numbers below represent the percent chance of getting any given pair, suited combo,
            # or lastly unsuited combo
            if hand in pairs:
                limit += 0.004524887
            elif 's' in hand:
                limit += 0.003016591
            else:
                limit += 0.009049774

        # rnd indicates whether the range will have replaced some number of the worst hands with even worse hands
        # to keep people from actually knowing your range
    if rnd > 0:
        my_range_combos = int
        # my_range_combos is the actual number of combos in a hand range out of the 2574 possible combos.
        for hand in my_range:
            if hand in pairs:
                my_range_combos += 6
            elif 's' in hand:
                my_range_combos += 4
            else:
                my_range_combos += 12
        #  swap count is the actual number of combos we're trading out
        swap_count = round(rnd * my_range_combos * .01)
        # get all of the hands that aren't good enough to be in my range
        garbage_range = ()
        for hand in full_range:
            if hand not in my_range:
                garbage_range.append(hand)
        counter = 0
        while counter < swap_count:
            combo = my_range.pop()
            if combo in pairs:
                counter += 6
            elif 's' in combo:
                counter += 4
            else:
                counter += 12

        shuffle(garbage_range)
        #  We're adding pairs or suited combos back in to the hand 
        while swap_count > 0 and garbage_range:
            garbage_hand = garbage_range.pop()
            if garbage_hand in pairs:
                swap_count -= 6
                my_range.append(garbage_hand)
            elif 's' in garbage_hand:
                swap_count -= 4
                my_range.append(garbage_hand)

    return my_range
