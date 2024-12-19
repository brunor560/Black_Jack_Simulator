#Black Jack Simulator
import random
import tkinter as tk
from tkinter import messagebox


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


class BlackjackApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Blackjack Simulator")
        self.root.config(bg="MintCream")

        # Game variables
        self.deck = create_deck()
        random.shuffle(self.deck)
        self.player_hand = []
        self.dealer_hand = []
        self.player_chips = 100
        self.bet = 0

        self.create_widgets()

        self.update_chip_display()

        self.new_round()

    def create_widgets(self):
        self.dealer_frame = tk.Frame(self.root)
        self.dealer_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nw")
        self.player_frame = tk.Frame(self.root)
        self.player_frame.grid(row=0, column=2, padx=10, pady=10, sticky="ne")

        # Dealer Section
        tk.Label(self.dealer_frame, text="Dealer", font=("MS Sans Serif", 16), bg="MintCream").pack()
        self.dealer_label = tk.Label(self.dealer_frame, text="Dealer: ", font=("MS Sans Serif", 14), bg="MintCream")
        self.dealer_label.pack()

        # Player Section
        tk.Label(self.player_frame, text="Player", font=("MS Sans Serif", 16), bg="MintCream").pack()
        self.player_label = tk.Label(self.player_frame, text="Player: ", font=("MS Sans Serif", 14), bg="MintCream")
        self.player_label.pack()

        # Player Score Section
        self.player_score_label = tk.Label(self.player_frame, text="Score: 0", font=("MS Sans Serif", 14), bg="MintCream")
        self.player_score_label.pack()

        # Chip Count (placed in the center, below dealer and player)
        self.chip_label = tk.Label(self.root, text=f"Chips: {self.player_chips}", font=("MS Sans Serif", 16), bg="MintCream")
        self.chip_label.grid(row=1, column=1, pady=10)

        # Bet Entry and Deal Button (center-aligned)
        tk.Label(self.root, text="Bet Amount:", font=("MS Sans Serif", 14), bg="MintCream").grid(row=2, column=1, pady=5)
        self.bet_entry = tk.Entry(self.root, font=("MS Sans Serif", 14), bg="MintCream")
        self.bet_entry.grid(row=3, column=1, pady=5)
        self.deal_button = tk.Button(self.root, text="Deal", command=self.place_bet, font=("MS Sans Serif", 18), bg="lightgreen")
        self.deal_button.grid(row=4, column=1, pady=10)

        # Action Buttons (centered, below the Bet Entry)
        button_width = 10
        button_height = 2
        self.hit_button = tk.Button(self.root, text="Hit", command=self.hit, font=("MS Sans Serif", 14), state="disabled", width = button_width, height = button_height, bg='ivory')
        self.hit_button.grid(row=5, column=0, pady=10)
        self.stand_button = tk.Button(self.root, text="Stand", command=self.stand, font=("MS Sans Serif", 14), state="disabled", width = button_width, height = button_height, bg='ivory')
        self.stand_button.grid(row=5, column=2, pady=10)

        # Result (centered)
        self.result_label = tk.Label(self.root, text="", font=("MS Sans Serif", 16), bg="MintCream")
        self.result_label.grid(row=6, column=1, pady=10)

    def new_round(self):
        """Initialize a new round."""
        self.deck = create_deck()
        random.shuffle(self.deck)
        self.player_hand = [self.deck.pop(), self.deck.pop()]
        self.dealer_hand = [self.deck.pop(), self.deck.pop()]
        self.update_display()

    def place_bet(self):
        """Place a bet and start the game."""
        try:
            self.bet = int(self.bet_entry.get())
            if self.bet > self.player_chips:
                messagebox.showerror("Error", "You don't have enough chips!")
            elif self.bet <= 0:
                messagebox.showerror("Error", "Bet must be greater than 0.")
            else:
                self.start_game()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number.")

    def start_game(self):
        """Enable buttons and start the round."""
        self.result_label.config(text="")
        self.bet_entry.config(state="disabled")
        self.deal_button.config(state="disabled")
        self.hit_button.config(state="normal")
        self.stand_button.config(state="normal")

    def hit(self):
        """Player chooses to draw a card."""
        self.player_hand.append(self.deck.pop())
        self.update_display()

        player_score = self.calculate_score(self.player_hand)
        if player_score > 21:
            self.player_chips -= self.bet
            self.update_chip_display()
            self.end_round("Bust! Dealer Wins.")

    def stand(self):
        """Player stands, dealer's turn."""
        while self.calculate_score(self.dealer_hand) < 17:
            self.dealer_hand.append(self.deck.pop())

        self.update_display(reveal_dealer=True)
        self.check_winner()

    def calculate_score(self, hand):
        """Calculate the total score of a hand."""
        score = 0
        for card in hand:
            score += card_value(card, score)
        return score

    def update_display(self, reveal_dealer=False):
        """Update the player and dealer cards on the screen."""
        self.player_label.config(text=f"Player: {self.player_hand}", bg="MintCream")
        self.player_score_label.config(text=f"Score: {self.calculate_score(self.player_hand)}")

        if reveal_dealer:
            self.dealer_label.config(text=f"Dealer: {self.dealer_hand} (Score: {self.calculate_score(self.dealer_hand)})")
        else:
            self.dealer_label.config(text=f"Dealer: {self.dealer_hand[0]}, [Hidden] \n(Score: ?)")

    def update_chip_display(self):
        """Update the chip count label."""
        self.chip_label.config(text=f"Chips: {self.player_chips}")

    def check_winner(self):
        """Determine the winner after the dealer's turn."""
        player_score = self.calculate_score(self.player_hand)
        dealer_score = self.calculate_score(self.dealer_hand)

        self.dealer_label.config(text=f"Dealer: {self.dealer_hand} (Score: {dealer_score})")

        if dealer_score > 21 or player_score > dealer_score:
            self.end_round("Player Wins!")
            self.player_chips += self.bet
        elif dealer_score > player_score:
            self.end_round("Dealer Wins!")
            self.player_chips -= self.bet
        else:
            self.end_round("It's a Draw!")

        self.update_chip_display()

    def end_round(self, result):
        """End the round, display the result, and reset the game."""
        self.update_display(reveal_dealer=True)
        self.result_label.config(text=result)
        self.chip_label.config(text=f"Chips: {self.player_chips}")

        if self.player_chips <= 0:
            messagebox.showinfo("Game Over", "You're out of chips! Game over.")
            self.root.quit()
        else:
            self.bet_entry.config(state="normal")
            self.deal_button.config(state="normal")
            self.hit_button.config(state="disabled")
            self.stand_button.config(state="disabled")
            self.new_round()


# Run the app
root = tk.Tk()
app = BlackjackApp(root)
root.mainloop()

# def play_blackjack():
#     #Chip System
#     starting_chips = 100
#     player_chips = starting_chips
#
#     while player_chips > 0:
#         print(f'You have {player_chips} chips.')
#
#         #Betting System
#         while True:
#             try:
#                 bet = int(input('How much would you like to bet this round (Choose Wisely):'))
#                 if bet > player_chips:
#                     print('You dont have enough chips!')
#                 elif bet <= 0:
#                     print('You have to bet something greater than 0.')
#                 else:
#                     break
#             except ValueError:
#                 print('Please enter a valid number.')
#
#         # Initialization
#         deck = create_deck()
#         random.shuffle(deck)
#         player_card = [deck.pop(), deck.pop()]
#         dealer_card = [deck.pop(), deck.pop()]
#
#         #Player Section
#         player_busted = False
#         while True:
#             player_score = sum(card_value(card, sum(card_value(c) for c in player_card)) for card in player_card)
#             print(f'\nPlayer Cards: {player_card}')
#             print(f'Player Score: {player_score}')
#
#             if player_score > 21:
#                 print('Player broke 21, Dealer wins.')
#                 player_chips -= bet
#                 player_busted = True
#                 break
#
#             choice = input("What's your next move? (Hit or Stand): ").strip().lower()
#             if choice == 'hit':
#                 player_card.append(deck.pop())
#             elif choice == 'stand':
#                 break
#             else:
#                 print('Invalid Move, Try Again')
#
#         #Dealer Section
#         if not player_busted:
#             while True:
#                 dealer_score = sum(card_value(card, sum(card_value(c) for c in dealer_card)) for card in dealer_card)
#
#                 if dealer_score > 21:
#                     print(f'\nDealer Cards: {dealer_card}')
#                     print(f'Dealer Score: {dealer_score}')
#                     print('Player Wins, Dealer broke 21!')
#                     player_chips += bet
#                     break
#
#                 if dealer_score < 17:
#                     dealer_card.append(deck.pop())
#                 else:
#                     break
#
#             if dealer_score <= 21:
#                 print(f'\nDealer Cards: {dealer_card}')
#                 print(f'Dealer Score: {dealer_score}')
#                 print('\n')
#                 if player_score > dealer_score:
#                     print('Player Wins! Player was closer to 21.')
#                     player_chips += bet
#                 elif dealer_score > player_score:
#                     print('Dealer Wins! Dealer was closer to 21.')
#                     player_chips -= bet
#                 else:
#                     print('It\'s a Draw!')
#
#         #Out of Chips
#         if player_chips <= 0:
#             print("You're out of chips, better luck next time!")
#             break
#
#         #Update Chip Count
#         print(f'\nYou now have {player_chips} chips.')
#
#         #Play Again
#         play_again = input('Do you want to play again? (Yes or No): ').strip().lower()
#         if play_again != 'yes':
#             print(f'You ended with {player_chips} chips, See you next time.')
#             break
#
# #Starts Game
# play_blackjack()