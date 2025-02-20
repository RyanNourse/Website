import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Blackjack Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 150, 0)
RED = (200, 0, 0)
DARK_RED = (150, 0, 0)

# Load card images
card_images = {}
suits = ['hearts', 'diamonds', 'clubs', 'spades']
values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']

# Resize factor for cards
card_width, card_height = 72, 96

for suit in suits:
    for value in values:
        image_path = f"cards/{value}_of_{suit}.png"
        image = pygame.image.load(image_path)
        card_images[f"{value}_of_{suit}"] = pygame.transform.scale(image, (card_width, card_height))

# Define Card class
class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
        self.image = card_images[f"{value}_of_{suit}"]

    def get_value(self):
        if self.value in ['jack', 'queen', 'king']:
            return 10
        elif self.value == 'ace':
            return 11  # Ace starts as 11
        else:
            return int(self.value)

# Deck class
class Deck:
    def __init__(self):
        self.cards = [Card(value, suit) for suit in suits for value in values]
        random.shuffle(self.cards)

    def draw_card(self):
        return self.cards.pop()

# Button class
class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, callback):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.callback = callback
        self.font = pygame.font.SysFont('Arial', 15)

    def draw(self, screen):
        # Change color if mouse is hovering over the button
        mouse_x, mouse_y = pygame.mouse.get_pos()
        color = self.hover_color if self.rect.collidepoint(mouse_x, mouse_y) else self.color
        pygame.draw.rect(screen, color, self.rect)

        # Draw text on button
        text_surface = self.font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def check_click(self):
        # Check if button is clicked
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_x, mouse_y) and pygame.mouse.get_pressed()[0]:
            self.callback()

# Blackjack game logic
class BlackjackGame:
    def __init__(self):
        self.deck = Deck()
        self.player_hand = [self.deck.draw_card(), self.deck.draw_card()]
        self.dealer_hand = [self.deck.draw_card(), self.deck.draw_card()]
        self.player_turn = True
        self.game_over = False
        self.winner = None

    def get_hand_value(self, hand):
        value = sum(card.get_value() for card in hand)
        # Adjust for Aces
        num_aces = sum(1 for card in hand if card.value == 'A')
        while value > 21 and num_aces:
            value -= 10  # Change Ace from 11 to 1
            num_aces -= 1
        return value

    def hit(self):
        if self.player_turn and not self.game_over:
            self.player_hand.append(self.deck.draw_card())
            if self.get_hand_value(self.player_hand) > 21:
                self.game_over = True
                self.winner = "Dealer"

    def stand(self):
        if self.player_turn and not self.game_over:
            self.player_turn = False
            # Dealer plays automatically
            while self.get_hand_value(self.dealer_hand) < 17:
                self.dealer_hand.append(self.deck.draw_card())

            # Determine winner
            player_value = self.get_hand_value(self.player_hand)
            dealer_value = self.get_hand_value(self.dealer_hand)

            if dealer_value > 21 or player_value > dealer_value:
                self.winner = "Player"
            elif player_value < dealer_value:
                self.winner = "Dealer"
            else:
                self.winner = "Tie"

            self.game_over = True

# Initialize game
game = BlackjackGame()

# Create buttons
hit_button = Button(100, 250, 150, 50, "Hit", GREEN, DARK_GREEN, game.hit)
stand_button = Button(300, 250, 150, 50, "Stand", RED, DARK_RED, game.stand)

# Font
font = pygame.font.SysFont('Arial', 30)

# Game loop
running = True
while running:
    screen.fill(WHITE)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw player and dealer hands
    x_offset = 50
    for card in game.player_hand:
        screen.blit(card.image, (x_offset, HEIGHT - 150))
        x_offset += 90  # Spacing

    x_offset = 50
    for i, card in enumerate(game.dealer_hand):
        if i == 0 and game.player_turn:  # Hide first dealer card if player is still playing
            pygame.draw.rect(screen, BLACK, (x_offset, 50, card_width, card_height))
        else:
            screen.blit(card.image, (x_offset, 50))
        x_offset += 90

    # Display scores
    player_score_text = font.render(f"Player: {game.get_hand_value(game.player_hand)}", True, BLACK)
    screen.blit(player_score_text, (50, HEIGHT - 200))

    dealer_score_text = font.render(f"Dealer: {'?' if game.player_turn else game.get_hand_value(game.dealer_hand)}", True, BLACK)
    screen.blit(dealer_score_text, (50, 20))

    # Draw buttons if game is not over
    if not game.game_over:
        hit_button.draw(screen)
        stand_button.draw(screen)
        hit_button.check_click()
        stand_button.check_click()
    else:
        # Display winner message
        winner_text = font.render(f"Winner: {game.winner}", True, BLACK)
        screen.blit(winner_text, (WIDTH // 2 - 100, HEIGHT // 2))

    pygame.display.flip()

pygame.quit()
sys.exit()
