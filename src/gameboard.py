#gameboard.py

import stdarray
from piece import Piece

class GameBoard:
    def __init__(self,k,m,n):
        self._m = m
        self._n = n
        self._k = k
        self.board = stdarray.create2D(m,n)
        
    
    def get_cell(self,x,y):
        return self.board[y][x]
    
    def set_cell(self,x,y,piece: Piece):
        self.board[y][x] = piece
        
    def __str__(self):
        output = ''
        for row in self.board:
            output += ''.join(str(cell) for cell in row) + '\n'
        return output
        
    
        
    