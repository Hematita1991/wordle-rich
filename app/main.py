# from rich import print
from rich.console import Console
from rich.text import Text


class Game(object):
    def __init__(self, use_rich=False) -> None:
        self.number_guesses = 5
        self.current_round = 1
        self.number_rounds = 5
        self.grid = None
        self.correct_word = "apple"
        self.use_rich = use_rich
    
    def update_round(self):
        self.current_round += 1
    
    def is_over(self):
        return self.current_round == self.number_rounds
    
    def check_if_correct_word(self, input_word):
        return self.correct_word == input_word

    def set_text_format_option(self, option):
        self.use_rich = option
    
    def setup_grid(self):
        self.grid = Grid()
        self.grid.use_rich = self.use_rich


class TextSettings(object):
    def __init__(self) -> None:
        self.color_is_in_word = "bold yellow"
        self.color_is_in_place = "bold green"
    
    def color_word(self, input_word, correct_word):
        text = Text()
        for idx, s in enumerate(input_word):
            if s == correct_word[idx]:
                text.append(s, style=self.color_is_in_place)
            elif s in correct_word:
                text.append(s, style=self.color_is_in_word)
            else:
                text.append(s)
        return text


class Grid(object):
    def __init__(self) -> None:
        self.num_words = 5
        self.word_length = 5
        list_words = list([" "*self.word_length]*self.num_words)
        self.word_dict = dict(zip(list(range(1, self.num_words + 1, 1)), list_words))
        self.use_rich = False
    
    def set_text_format_option(self, option):
        self.use_rich = option
    
    def print_grid(self):
        if not self.use_rich:
            for k in self.word_dict.keys():
                print(self.word_dict[k])
        else:
            for k in self.word_dict.keys():
                console.print(self.word_dict[k])
        print()

    def update_grid(self, input_word, guess_number):
        new_dict = self.word_dict
        new_dict[guess_number] = input_word
        self.word_dict = new_dict
    
    def check_if_valid_word(self, input_word):
        value = False
        if len(input_word)==self.word_length:
            value = True
        return value    

    def color_word(self, input_word, correct_word, text_obj):
        return text_obj.color_word(input_word, correct_word)


if __name__ == '__main__':
    play_game = True
    use_rich = True
    game = Game(use_rich=use_rich)
    game.setup_grid()
    console = Console()
    text_obj = TextSettings()
    
    while play_game:
        user_input = input("Enter your guess: ")

        if game.grid.check_if_valid_word(user_input):
            formatted_word = game.grid.color_word(user_input, game.correct_word, text_obj)
            game.grid.update_grid(formatted_word, game.current_round)
            game.grid.print_grid()
            game.update_round()

        if game.check_if_correct_word(user_input):
            print("Congratulations! You guessed correctly.")
            offer_new_game = True

        else:
            if game.current_round > game.number_rounds:
                print("Too bad! You lose this game.")
                print(f"The correct word is: {game.correct_word}")
                offer_new_game = True
            
            else:
                play_game = True
                offer_new_game = False

        if offer_new_game:
            user_input_new_game = input("Would you like to play another game? Enter Y or N: ")

            if user_input_new_game == "N":
                print("Thank you for playing. Goodbye.")
                play_game = False
            elif user_input_new_game == "Y":
                print("Capital! New game will start shortly...")
                play_game = True
                game = Game(use_rich=use_rich)
                game.setup_grid()