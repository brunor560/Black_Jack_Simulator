import random

def create_deck():
    card_suit = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    cards_list = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
    return [(card, suit) for suit in card_suit for card in cards_list]

def card_value(card, current_score=0):
    if card[0] in ['Jack', 'Queen', 'King']:
        return 10
    elif card[0] == 'Ace':
        return 11 if current_score + 11 <= 21 else 1
    else:
        return int(card[0])

def play_blackjack():
    #Chip System
    starting_chips = 100
    player_chips = starting_chips

    while player_chips > 0:
        print(f'You have {player_chips} chips.')

        #Betting System
        while True:
            try:
                bet = int(input('How much would you like to bet this round (Choose Wisely):'))
                if bet > player_chips:
                    print('You dont have enough chips!')
                elif bet <= 0:
                    print('You have to bet something greater than 0.')
                else:
                    break
            except ValueError:
                print('Please enter a valid number.')

        # Initialization
        deck = create_deck()
        random.shuffle(deck)
        player_card = [deck.pop(), deck.pop()]
        dealer_card = [deck.pop(), deck.pop()]

        #Player Section
        player_busted = False
        while True:
            player_score = sum(card_value(card, sum(card_value(c) for c in player_card)) for card in player_card)
            print(f'\nPlayer Cards: {player_card}')
            print(f'Player Score: {player_score}')

            if player_score > 21:
                print('Player broke 21, Dealer wins.')
                player_chips -= bet
                player_busted = True
                break

            choice = input("What's your next move? (Hit or Stand): ").strip().lower()
            if choice == 'hit':
                player_card.append(deck.pop())
            elif choice == 'stand':
                break
            else:
                print('Invalid Move, Try Again')

        #Dealer Section
        if not player_busted:
            while True:
                dealer_score = sum(card_value(card, sum(card_value(c) for c in dealer_card)) for card in dealer_card)

                if dealer_score > 21:
                    print(f'\nDealer Cards: {dealer_card}')
                    print(f'Dealer Score: {dealer_score}')
                    print('Player Wins, Dealer broke 21!')
                    player_chips += bet
                    break

                if dealer_score < 17:
                    dealer_card.append(deck.pop())
                else:
                    break

            if dealer_score <= 21:
                print(f'\nDealer Cards: {dealer_card}')
                print(f'Dealer Score: {dealer_score}')
                print('\n')
                if player_score > dealer_score:
                    print('Player Wins! Player was closer to 21.')
                    player_chips += bet
                elif dealer_score > player_score:
                    print('Dealer Wins! Dealer was closer to 21.')
                    player_chips -= bet
                else:
                    print('It\'s a Draw!')

        #Out of Chips
        if player_chips <= 0:
            print("You're out of chips, better luck next time!")
            break

        #Update Chip Count
        print(f'\nYou now have {player_chips} chips.')

        #Play Again
        play_again = input('Do you want to play again? (Yes or No): ').strip().lower()
        if play_again != 'yes':
            print(f'You ended with {player_chips} chips, See you next time.')
            break

#Starts Game
play_blackjack()