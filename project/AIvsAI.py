import chess
import AI1
import AI2
import AI3
import chessDetection
import sys

def play(imgPath, whiteMovesFirst, ai1, ai2):
    board = chessDetection.getBoardFromImg(imgPath,whiteMovesFirst)
    board = chess.Board(board)
    ai1 = eval(ai1)
    ai2 = eval(ai2)
    if whiteMovesFirst:
        color = chess.BLACK
    else:
        color = chess.WHITE
    if not board.is_valid():
            print("Board is not valid")
            return
    while True:
        if color == chess.WHITE:
            color = chess.BLACK
        else:
            color = chess.WHITE
        
        colorWB(color)
        print(board)
        print()
        if ai1 == 1:
            board = AI1.bestMove(board, color)
        elif ai1 == 2:
            board = AI2.bestMove(board, color)
        elif ai1 == 3:
            board = AI2.bestMove(board, color)
        if board.is_checkmate():
            if color == chess.WHITE:
                print("White wins!")
                print(board)
                break 
            else:
                print("Black wins!")
                print(board)
                break
        elif board.is_game_over():
            print(board)
            print("Tie game")
            break

        if color == chess.WHITE:
            color = chess.BLACK
        else:
            color = chess.WHITE
        colorWB(color)
        print(board)
        print()
        if ai2 == 1:
            board = AI1.bestMove(board, color)
        elif ai2 == 2:
            board = AI2.bestMove(board, color)
        elif ai2 == 3:
            board = AI2.bestMove(board, color)
        if board.is_checkmate():
            if color == chess.WHITE:
                print("White wins!")
                print(board)
                break 
            else:
                print("Black wins!")
                print(board)
                break
        elif board.is_game_over():
            print(board)
            print("Tie game")
            break

def colorWB(color):
    if color == chess.WHITE:
        print("White thinking...")
    else:
        print("Black thinking...")

if __name__ == "__main__":
    play(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])