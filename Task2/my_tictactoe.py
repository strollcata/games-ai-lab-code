from random import randrange
'''
TTTClass, short for Tic-Tac-Toe Class, contains the winning line tuples and the game variables.
'''
class TTTClass(object):
    WIN_LINES = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))

    def __init__(self):
        self.board = [' '] * 9
        self.noughts = ' '
        self.crosses = ' '
        self.current_player = self.crosses
        self.winner = None
        self.move = None
        self.AI_type = 'random'

        self.display_instructions()
        self.render_board()

    def _check_move(self):
        try:
            self.move = int(self.move)
            if (self.move < 0 or self.move > 8):
                print 'That number does not correspond to any place on the board. Please enter a number from 0 to 8.'
                return False
            else if self.board[self.move] != ' ':
                print 'That space is not vacant. Please select another location.'
                return False
            else:
                return True
        except:
            print 'That is not a number. Please enter a number from 0 to 8.'
            return False
        
    def _check_for_result(self):
        board = self.board
        vacant_spaces = 9
        for i in range(0, 7):
            nought_pieces = 0
            cross_pieces = 0
            current_line = WIN_LINES[i]
            for j in range(0, 2):
                if current_line[j] == 'o':
                    nought_pieces += 1
                else if current_line[j] == 'x':
                    cross_pieces += 1
            if nought_pieces == 3:
                return 'o'
            else if cross_pieces == 3:
                return 'x'
        for k in range(0, 8):
            if board[k] != ' ':
                vacant_spaces -= 1
        if vacant_spaces <= 0:
            return 'tie'
        return None

    def get_player_input(self):
        return raw_input('Enter a number from O to 8 >>> ')

    def get_ai_input(self):
        if self.AI_type = 'random':
            return randrange(9)
        else if self.AI_type = 'non-random':
            if self.board[4] == ' ':
                return 4
            else:
                for l in range(0, 8):
                    if self.board[l] == ' ':
                        return l

    def process_input(self):
        if self.current_player == 'player':
            self.move = self.get_player_input()
        else if self.current_player == 'AI':
            self.move = self.get_ai_input()

    def update_model(self):
        if self._check_move():
            if self.current_player == self.noughts:
                self.board[self.move] = 'o'
            else if self.current_player == self.crosses:
                self.board[self.move] = 'x'
        else:
            if self.current_player == 'player':
                print 'Invalid move. Try again.'
    def render_board(self):
        board = self.board
        print '    %s | %s | %s' % tuple(board[:3])
        print '   -----------'
        print '    %s | %s | %s' % tuple(board[3:6])
        print '   -----------'
        print '    %s | %s | %s' % tuple(board[6:])

        if self.winner is None:
            if self.current_player == self.noughts:
                print 'Current player: Noughts.'
            else if self.current_player == self.crosses:
                print 'Current player: Crosses.'

    def display_instructions(self):
        instructions = '''
Make a move by typing a number from 0 to 8 and pressing Enter.
The numbers each denote one space on the board, as illustrated below.

-------------
| 0 | 1 | 2 |
-------------
| 3 | 4 | 5 |
-------------
| 6 | 7 | 8 |
-------------
'''
        print instructions

    def display_results(self):
        if self.winner == 'tie':
            print 'The result is a tie!'
        else if self.winner == 'o':
            print 'Noughts wins!'
        else if self.winner == 'x':
            print 'Crosses wins!'

#Create main menu.
