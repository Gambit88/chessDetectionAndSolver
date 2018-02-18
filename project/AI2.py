import chess
import random

def boardValue(board, color):
    boardString = board.fen().split()[0]
    if color == chess.BLACK:
        pawn = boardString.count("P") - boardString.count("p")
        rook = boardString.count("R") - boardString.count("r")
        knight = boardString.count("N") - boardString.count("n")
        bishop = boardString.count("B") - boardString.count("b")
        queen = boardString.count("Q") - boardString.count("q")
    else:
        pawn = boardString.count("p") - boardString.count("P")
        rook = boardString.count("r") - boardString.count("R")
        knight = boardString.count("n") - boardString.count("N")
        bishop = boardString.count("b") - boardString.count("B")
        queen = boardString.count("q") - boardString.count("Q")
    return pawn + 3*(bishop + knight) + 5*rook + 9*queen

def moveValue(board, color, move, depth, alpha, beta, maximize):
    copy = board.copy()
    copy.pop()
    if board.is_checkmate():
        return -50 if maximize else 50
    elif copy.is_into_check(move):
        return -45 if maximize else 45
    elif board.is_game_over():
        return 0
    
    if depth == 0:
        return boardValue(board, color)

    if maximize:
        best = float("-inf")
        for move in board.legal_moves:
            boardCopy = board.copy()
            boardCopy.push(move)
            value = moveValue(boardCopy, color, move, depth, alpha, beta, False)
            best = max(best,value)
            alpha = max(alpha, best)
            if alpha >= beta:
                break
        return best
    else:
        best = float("inf")
        for move in board.legal_moves:
            boardCopy = board.copy()
            boardCopy.push(move)
            value = moveValue(boardCopy, color, move, depth - 1, alpha, beta, True)
            best = min(best,value)
            beta = min(best, beta)
            if alpha >= beta:
                break
        return best
    return 0


def bestMove(board,color):
    nextMove = None
    min = float("inf")
    counter = 0
    numOfMoves = 0
    for move in board.legal_moves:
        numOfMoves += 1
        boardCopy = board.copy()
        boardCopy.push(move)
        value = moveValue(boardCopy, color, move, 2, float("-inf"), float("inf"), False)

        if value < min:
            counter += 1 
            min = value
            nextMove = move
    if counter == 1:
        rand = random.randint(0,numOfMoves-1)
        br = 0
        for i in board.legal_moves:
            br += 1
            if br == rand:
                nextMove = i
                break

    board.push(nextMove)

    return board