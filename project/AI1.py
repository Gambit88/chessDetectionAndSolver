import chess    
import random

def bestMove(board,color):
    nextMove = None
    counter = 0
    numOfMoves = 0
    min = float("inf")
    for move in board.legal_moves:
        numOfMoves += 1
        value = moveValue(board,move,color)
        if value < min:
            min = value
            counter += 1 
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
        
        
        
           
def moveValue(board,move,color):
    b = board.copy()
    b.push(move)
    if b.is_checkmate():
        return -50

    b = board.board_fen().split()[0]
    sum = 0
    if color == chess.WHITE:
        pawn = b.count("p") - b.count("P")
        rook = b.count("r") - b.count("R")
        knight = b.count("n") - b.count("N")
        bishop = b.count("b") - b.count("B")
        queen = b.count("q") - b.count("Q")
    else:
        pawn = b.count("P") - b.count("p")
        rook = b.count("R") - b.count("r")
        knight = b.count("N") - b.count("n")
        bishop = b.count("B") - b.count("b")
        queen = b.count("Q") - b.count("q")
    sum = pawn + rook * 5 + (knight+bishop)*3 + queen * 9

    attackDef = -1
    if board.is_into_check(move):
        if color == chess.WHITE:
            a = board.attackers(chess.BLACK,move.to_square)
            d = board.attackers(chess.WHITE,move.to_square)
        else:
            a = board.attackers(chess.WHITE,move.to_square)
            d = board.attackers(chess.BLACK,move.to_square)
        countA = 0
        countD = 0
        for i in a:
            countA += 1
        if countA == 0:
            return -45
        for i in d:
            countD += 1
        attackDef = countD - countA
        if attackDef >= 0:
            return -45

    if board.is_capture(move):
        fr = move.from_square
        to = move.to_square
        at = board.piece_type_at(fr)
        df = board.piece_type_at(to)
        if color == chess.WHITE:
            a = board.attackers(chess.BLACK,move.to_square)
            d = board.attackers(chess.WHITE,move.to_square)
        else:
            a = board.attackers(chess.WHITE,move.to_square)
            d = board.attackers(chess.BLACK,move.to_square)
        countA = 0
        countD = 0
        for i in a:
            countA += 1
        for i in d:
            countD += 1
        attackDef = countD - countA
        if at < df:
            if countA == 0:
                return -43
            else:
                return -40
        if at >= df:
            if countA == 0:
                return -43
            else:
                return 0
        if attackDef > 0:
            return -39

    return sum