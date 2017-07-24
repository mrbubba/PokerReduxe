board_list = {'flop':[], 'turn':[], 'river':[]}


def add_board(board):
    """
    Adds a board to the board_list, in the appropriate dictionary slot
        
        Args:
            board (list):  A list of card values that will be either 3 ,4, or 5 in length.
            
        Returns: 
            None        
    """
    length = len(board)
    if length not in [3, 4, 5]:
        raise ValueError('value must be either either 3, 4, or 5 in length. Got {0}'.format(length))
    if length == 3:
        board.sort()
        if board in board_list['flop']:
            pass
        else:
            board_list['flop'].append(board)
    if length == 4:
        board.sort()
        if board in board_list['turn']:
            pass
        else:
            board_list['turn'].append(board)
    if length == 5:
        board.sort()
        if board in board_list['river']:
            pass
        else:
            board_list['river'].append(board)


def get_board():
    yield []









__all__ = ['board_list', 'add_board', 'get_board']