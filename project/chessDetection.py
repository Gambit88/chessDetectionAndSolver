import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
import data

def intersection(first, second):
    x = (first[1] - second[1])/(second[0] - first[0])
    y = first[0]*x + first[1]
    return (int(round(x)), int(round(y)))

def findPosition(point, hLines, vLines, img):
    cv.circle(img, point, 5, [255, 0, 0], 3)
    hnum = 0
    vnum = 0
    for i in range(0, len(hLines)):
        if point[1] < hLines[i][0]*point[0] + hLines[i][1]:
            hnum = i
            break
    for i in range(0, len(vLines)):
        if vLines[i][0] == 0:
            continue
        if point[0] < (point[1] - vLines[i][1])/vLines[i][0]:
            vnum = i
            break
    if(hnum <= 0 or vnum <= 0):
        return -1
    retVal = (hnum-1)*8 + (vnum-1)
    return retVal

def findLines(a, b):
    tableLines = []
    # A(x)
    m1ax = int(round((a[0] + a[2]) / 2))
    m2ax = int(round((a[0] + m1ax) / 2))
    m3ax = int(round((m1ax + a[2]) / 2))
    m4ax = int(round((a[0] + m2ax) / 2))
    m5ax = int(round((m2ax + m1ax) / 2))
    m6ax = int(round((m1ax + m3ax) / 2))
    m7ax = int(round((m3ax + a[2]) / 2))
    # A(y)
    m1ay = int(round((a[1] + a[3]) / 2))
    m2ay = int(round((a[1] + m1ay) / 2))
    m3ay = int(round((m1ay + a[3]) / 2))
    m4ay = int(round((a[1] + m2ay) / 2))
    m5ay = int(round((m2ay + m1ay) / 2))
    m6ay = int(round((m1ay + m3ay) / 2))
    m7ay = int(round((m3ay + a[3]) / 2))
    # B(x)
    m1bx = int(round((b[0] + b[2]) / 2))
    m2bx = int(round((b[0] + m1bx) / 2))
    m3bx = int(round((m1bx + b[2]) / 2))
    m4bx = int(round((b[0] + m2bx) / 2))
    m5bx = int(round((m2bx + m1bx) / 2))
    m6bx = int(round((m1bx + m3bx) / 2))
    m7bx = int(round((m3bx + b[2]) / 2))
    # B(y)
    m1by = int(round((b[1] + b[3]) / 2))
    m2by = int(round((b[1] + m1by) / 2))
    m3by = int(round((m1by + b[3]) / 2))
    m4by = int(round((b[1] + m2by) / 2))
    m5by = int(round((m2by + m1by) / 2))
    m6by = int(round((m1by + m3by) / 2))
    m7by = int(round((m3by + b[3]) / 2))
    # linije za obradu
    if b[0]-a[0] == 0:
        m = b[1] - a[1]
    else:
        m = (b[1] - a[1])/((b[0] - a[0])*1.0)
    d = b[1] - m*b[0]
    res = (m, d)
    tableLines.append(res)

    if m4bx - m4ax == 0:
        m = m4by - m4ay
    else:
        m = (m4by - m4ay)/((m4bx - m4ax)*1.0)
    d = m4by - m*m4bx
    res = (m, d)
    tableLines.append(res)

    if m2bx - m2ax==0:
        m = m2by - m2ay
    else:
        m = (m2by - m2ay)/((m2bx - m2ax)*1.0)
    d = m2by - m*m2bx
    res = (m, d)
    tableLines.append(res)

    if m5bx - m5ax==0:
        m = m5by - m5ay
    else:
        m = (m5by - m5ay)/((m5bx - m5ax)*1.0)
    d = m5by - m*m5bx
    res = (m, d)
    tableLines.append(res)

    if m1bx-m1ax==0:
        m=  m1by - m1ay
    else:
        m = (m1by - m1ay)/((m1bx - m1ax)*1.0)
    d = m1by - m*m1bx
    res = (m, d)
    tableLines.append(res)

    if m6bx - m6ax==0:
        m=m6by - m6ay
    else:
        m = (m6by - m6ay)/((m6bx - m6ax)*1.0)
    d = m6by - m*m6bx
    res = (m, d)
    tableLines.append(res)

    if m3bx - m3ax == 0:
        m = m3by - m3ay
    else:
        m = (m3by - m3ay)/((m3bx - m3ax)*1.0)
    d = m3by - m*m3bx
    res = (m, d)
    tableLines.append(res)

    if m7bx - m7ax==0:
        m=m7by - m7ay
    else:
        m = (m7by - m7ay)/((m7bx - m7ax)*1.0)
    d = m7by - m*m7bx
    res = (m, d)
    tableLines.append(res)

    if b[2] - a[2]==0:
        m = b[3] - a[3]
    else:
        m = (b[3] - a[3])/((b[2] - a[2])*1.0)
    d = b[3] - m*b[2]
    res = (m, d)
    tableLines.append(res)

    return tableLines

def getPieceType(conture, isWhitePiece, database, board):
    lowVal = 0.25
    retVal = "L"
    enableKing = True
    enableQuuen = True
    enableBishop = True
    enableKnight = True
    enableRock = True
    enablePawn = True
    currentPicesCount = {x:board.count(x) for x in board}
    if isWhitePiece:
        if 'K' in currentPicesCount and currentPicesCount['K']>=1:
            enableKing = False
        if 'Q' in currentPicesCount and currentPicesCount['Q']>=1:
            enableQuuen = False
        if 'B' in currentPicesCount and currentPicesCount['B']>=2:
            enableBishop = False
        if 'N' in currentPicesCount and currentPicesCount['N']>=2:
            enableKnight = False
        if 'R' in currentPicesCount and currentPicesCount['R']>=2:
            enableRock = False
        if 'P' in currentPicesCount and currentPicesCount['P']>=8:
            enablePawn = False
    else:
        if 'k' in currentPicesCount and currentPicesCount['k']>=1:
            enableKing = False
        if 'q' in currentPicesCount and currentPicesCount['q']>=1:
            enableQuuen = False
        if 'b' in currentPicesCount and currentPicesCount['b']>=2:
            enableBishop = False
        if 'n' in currentPicesCount and currentPicesCount['n']>=2:
            enableKnight = False
        if 'r' in currentPicesCount and currentPicesCount['r']>=2:
            enableRock = False
        if 'p' in currentPicesCount and currentPicesCount['p']>=8:
            enablePawn = False

    if enableQuuen:
        for i in range(0, len(database[data.QUEEN][1])):
            res = cv.matchShapes(conture, database[data.QUEEN][1][i], 3, 0.0)
            if(res < lowVal):
                lowVal = res
                retVal = "q"
    if enableKing:
        for i in range(0, len(database[data.KING][1])):
            res = cv.matchShapes(conture, database[data.KING][1][i], 3, 0.0)
            if(res < lowVal):
                lowVal = res
                retVal = "k"

    if enableBishop:
        for i in range(0, len(database[data.BISHOP][1])):
            res = cv.matchShapes(conture, database[data.BISHOP][1][i], 3, 0.0)
            if(res < lowVal):
                lowVal = res
                retVal = "b"

    if enableKnight:
        for i in range(0, len(database[data.KNIGHT][1])):
            res = cv.matchShapes(conture, database[data.KNIGHT][1][i], 3, 0.0)
            if(res < lowVal):
                lowVal = res
                retVal = "n"

    if enableRock:
        for i in range(0, len(database[data.ROCK][1])):
            res = cv.matchShapes(conture, database[data.ROCK][1][i], 3, 0.0)
            if(res < lowVal):
                lowVal = res
                retVal = "r"

    if enablePawn:
        for i in range(0, len(database[data.PAWN][1])):
            res = cv.matchShapes(conture, database[data.PAWN][1][i], 3, 0.0)
            if(res < lowVal):
                lowVal = res
                retVal = "p"

    if isWhitePiece:
        retVal = retVal.upper()
    #print(retVal)
    return retVal

def getBoardFromImg(imgPath, whiteOnMove):
    picesData = np.load('chessBaseData.npy')
    board = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    # Ucitavanje, izmena velicine, blur radi bolje i brze obrade, hsl prostor boja radi boljeg selektovanja delova slike
    img = cv.imread(imgPath, cv.IMREAD_COLOR)
    img = cv.resize(img, (1200, 900))
    blur = cv.GaussianBlur(img, (5, 5), 0)
    imgHSL = cv.cvtColor(blur, cv.COLOR_BGR2HLS)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    blurG = cv.GaussianBlur(gray, (5, 5), 0)
    # Granice boje crnih figura
    lowerBoundB = np.array([0, 0, 0])
    upperBoundB = np.array([179, 75, 80])
    # Granice boje belih figura
    lowerBoundW = np.array([15, 60, 20])
    upperBoundW = np.array([35, 255, 255])
    # Granice za selektovanje table
    lowerBoundT = np.array([0, 130, 0])
    upperBoundT = np.array([179, 200, 255])
    # Pravljenje maski u cilju detektovanja ivica figura/polja tabele
    maskBlack = cv.inRange(imgHSL, lowerBoundB, upperBoundB)
    maskWhite = cv.inRange(imgHSL, lowerBoundW, upperBoundW)
    maskTable = cv.inRange(imgHSL, lowerBoundT, upperBoundT)
    # Konture figura
    imB, contoursB, hierarchyB = cv.findContours(
        maskBlack, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    imW, contoursW, hierarchyW = cv.findContours(
        maskWhite, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    # Filter kontura da se uklone manje konture koje sigurno nisu figure
    cntB = []
    for c in contoursB:
        area = cv.contourArea(c)
        if area < 5000 and area > 600:
            cntB.append(c)
    cntW = []
    for c in contoursW:
        area = cv.contourArea(c)
        if area < 5000 and area > 600:
            cntW.append(c)
    # Iscrtavanje kontura
    #cv.drawContours(img, cntB, -1, (255, 255, 0), 1)
    #cv.drawContours(img, cntW, -1, (0, 0, 255), 1)
    # hugove linije, pronalazenje ivica table
    edge = cv.Canny(blurG, 40, 90, apertureSize=3)
    leftLine = [10000, 10000, 10000, 10000]
    rightLine = [0, 0, 0, 0]
    topLine = [10000, 10000, 10000, 10000]
    bottomLine = [0, 0, 0, 0]
    lines = cv.HoughLinesP(edge, 1, np.pi/180, 100,
                        minLineLength=250, maxLineGap=500)
    for line in lines:
        x1, y1, x2, y2 = line[0]
        mpx = (x1+x2)/2.0
        mpy = (y1+y2)/2.0
        if (mpx > (rightLine[0]+rightLine[2])/2.0):
            rightLine = line[0]
        if (mpx < (leftLine[0]+leftLine[2])/2.0):
            leftLine = line[0]
        if (mpy > (bottomLine[1]+bottomLine[3])/2.0):
            bottomLine = line[0]
        if (mpy < (topLine[1]+topLine[3])/2.0):
            topLine = line[0]
        # cv.line(img,(x1,y1),(x2,y2),(0,255,0),2)
    # leftLineF
    m = (leftLine[1]-leftLine[3])/(leftLine[0]-leftLine[2])*1.0
    b = leftLine[1] - m*leftLine[0]
    leftLineF = [m, b]
    # rightLineF
    m = (rightLine[1]-rightLine[3])/(rightLine[0]-rightLine[2])*1.0
    b = rightLine[1] - m*rightLine[0]
    rightLineF = [m, b]
    # topLineF
    m = (topLine[1]-topLine[3])/(topLine[0]-topLine[2])*1.0
    b = topLine[1] - m*topLine[0]
    topLineF = [m, b]
    # bottomLineF
    m = (bottomLine[1]-bottomLine[3])/(bottomLine[0]-bottomLine[2])*1.0
    b = bottomLine[1] - m*bottomLine[0]
    bottomLineF = [m, b]
    # pronalazenje tacki preseka ivica table
    topRightCorner = intersection(topLineF, rightLineF)
    topLeftCorner = intersection(topLineF, leftLineF)
    bottomRightCorner = intersection(bottomLineF, rightLineF)
    bottomLeftCorner = intersection(bottomLineF, leftLineF)
    # potpune ivice table
    correction = 5
    topLine = [topLeftCorner[0]+correction, topLeftCorner[1]+correction,
            topRightCorner[0]-correction, topRightCorner[1]+correction]
    bottomLine = [bottomLeftCorner[0]+correction, bottomLeftCorner[1]-correction,
                bottomRightCorner[0]-correction, bottomRightCorner[1]-correction]
    rightLine = [topRightCorner[0]-correction, topRightCorner[1]-correction,
                bottomRightCorner[0]-correction, bottomRightCorner[1]+correction]
    leftLine = [topLeftCorner[0]+correction, topLeftCorner[1]-correction,
                bottomLeftCorner[0]+correction, bottomLeftCorner[1]+correction]
    # prikaz ivica table
    cv.line(img, (leftLine[0], leftLine[1]),
            (leftLine[2], leftLine[3]), (255, 0, 0), 3)
    cv.line(img, (rightLine[0], rightLine[1]),
            (rightLine[2], rightLine[3]), (255, 0, 0), 3)
    cv.line(img, (topLine[0], topLine[1]),
            (topLine[2], topLine[3]), (255, 0, 0), 3)
    cv.line(img, (bottomLine[0], bottomLine[1]),
            (bottomLine[2], bottomLine[3]), (255, 0, 0), 3)
    # pronalazenje ostalih linija table
    verticalLines = findLines(topLine, bottomLine)
    horizontalLines = findLines(leftLine, rightLine)
    #crtanje svih linija
    for line in verticalLines:
        cv.line(img,(0,int(round(line[1]))),(900,int(round(900*line[0]+line[1]))),(0,255,0),2)
    for line in horizontalLines:
        cv.line(img,(0,int(round(line[1]))),(1200,int(round(1200*line[0]+line[1]))),(255,0,0),2)
    # proci kroz sve konture, utvrditi koja je koja, zatim minimum konture uzeti za tacku i naci joj poziciju, nakon toga je dodati u tablu
    for conture in cntB:
        piece = getPieceType(conture, False, picesData,board)
        leftmost = tuple(conture[conture[:,:,0].argmin()][0])
        rightmost = tuple(conture[conture[:,:,0].argmax()][0])
        bottommost = tuple(conture[conture[:, :, 1].argmax()][0])
        posx = (leftmost[0]+rightmost[0])/2
        posy = (leftmost[1]+rightmost[1])/2
        posx = (bottommost[0]+posx)/2
        posy = (bottommost[1]+posy)/2
        point = (int(posx),int(posy))
        location = findPosition(point, horizontalLines, verticalLines,img)
        if(location!=-1 and piece.find("L")==-1 and board[location]==0):
            board[location] = piece
    for conture in cntW:
        piece = getPieceType(conture, True, picesData, board)
        leftmost = tuple(conture[conture[:,:,0].argmin()][0])
        rightmost = tuple(conture[conture[:,:,0].argmax()][0])
        bottommost = tuple(conture[conture[:, :, 1].argmax()][0])
        posx = (leftmost[0]+rightmost[0])/2
        posy = (leftmost[1]+rightmost[1])/2
        posx = (bottommost[0]+posx)/2
        posy = (bottommost[1]+posy)/2
        point = (int(posx),int(posy))
        location = findPosition(point, horizontalLines, verticalLines,img)
        if(location!=-1 and piece.find("L")==-1 and board[location]==0):
            board[location] = piece
    ''' for  i in range(0,len(board)):
        if (i+1)%8 != 0:
            print(board[i],end=" ")
        else:
            print(board[i]) '''

    # proci kroz tablu i napraviti string za chess
    boardString = ""
    counter = 0
    iteration = 0
    for i in board:
        iteration = iteration + 1
        if i==0:
            counter= counter + 1
        else:
            if counter!=0:
                boardString = boardString + str(counter) + i
                counter = 0
            else:
                boardString = boardString + i
        if iteration%8==0:
            if counter!=0:
                boardString = boardString + str(counter)+'/'
                counter = 0
            else:
                boardString = boardString + '/'

    if whiteOnMove:
        boardString = boardString[:-1] + " w - - 0 1"
    else:
        boardString = boardString[:-1] + " b - - 0 1"
    # iscrtavanje slika
    #cv.imshow("Selektovane figure", img)
    # cv.imshow("Bela maska",maskWhite)
    # cv.imshow("Crna maska",maskBlack)
    #cv.waitKey()
    return boardString

#print(getBoardFromImg('./CHESS/Set2/Test/fin4.jpg',True))