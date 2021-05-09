# This is where you build your AI for the Chess game.

# <<-- Creer-Merge: imports -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
# you can add additional import(s) here
from joueur.base_ai import BaseAI
import random
import math
import time
import calendar
# <<-- /Creer-Merge: imports -->>

class AI(BaseAI):
    """ The AI you add and improve code inside to play Chess. """

    @property
    def game(self) -> 'games.chess.game.Game':
        """games.chess.game.Game: The reference to the Game instance this AI is playing.
        """
        return self._game # don't directly touch this "private" variable pls

    @property
    def player(self) -> 'games.chess.player.Player':
        """games.chess.player.Player: The reference to the Player this AI controls in the Game.
        """
        return self._player # don't directly touch this "private" variable pls

    def get_name(self) -> str:
        """This is the name you send to the server so your AI will control the player named this string.

        Returns:
            str: The name of your Player.
        """
        # <<-- Creer-Merge: get-name -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        return "Chess Python Player" # REPLACE THIS WITH YOUR TEAM NAME
        # <<-- /Creer-Merge: get-name -->>

    def start(self) -> None:
        """This is called once the game starts and your AI knows its player and game. You can initialize your AI here.
        """
        # <<-- Creer-Merge: start -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        # Put your start logic here
        # name = get_name()

        # <<-- /Creer-Merge: start -->>

    def game_updated(self) -> None:
        """This is called every time the game's state updates, so if you are tracking anything you can update it here.
        """
        # <<-- Creer-Merge: game-updated -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        # replace with your game updated logic
        # <<-- /Creer-Merge: game-updated -->>

    def end(self, won: bool, reason: str) -> None:
        """This is called when the game ends, you can clean up your data and dump files here if need be.

        Args:
            won (bool): True means you won, False means you lost.
            reason (str): The human readable string explaining why your AI won or lost.
        """
        # <<-- Creer-Merge: end -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        # Put you end logic here
        # if won:
        #     print("You won because", reason)
        # else:
        #     print("You lost because", reason)
        # <<-- /Creer-Merge: end -->>






    # NOTE FOR BHARAT:
    # In order to test this code navigate to
    #        bhasr@GameBabe MINGW64 /f/AI/2021-SP-C-game1-bbskkd/Joueur.py (master)
    # in 2 Git Bash terminals (use /f/ to change drives)
    # then run the line
    #        $ ./testRun bha
    # to test the code

    # Moves are denoted "a2a3"
    #   originFile_originRank -> targetFile_targetRank  (Ocolrow > Tcolrow)
    # Rank can be translated by   8-boardRowIndex
    # File can be translated by   

    def make_move(self) -> str:
        """This is called every time it is this AI.player's turn to make a move.

        Returns:
            str: A string in Universal Chess Inferface (UCI) or Standard Algebraic Notation (SAN) formatting for the move you want to make. If the move is invalid or not properly formatted you will lose the game.
        """
        try:
            print(self.game.print())
            # <<-- Creer-Merge: makeMove -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
            # Put your game logic here for make_move()
            gameFen = self.game.fen 
            gameFen = gameFen.split()
            playerColor = self.player.color
            board = self.parseFEN(gameFen[0])


            tempFen = gameFen[:]
            if gameFen[1] == "w": tempFen[1] = "b"
            else: tempFen[1] = "w"
            preMoveOpponentChoices = self.generateOpponentMoves(board, tempFen)
            # Find the location of player's king
            for rank in range(8):
                for file in range(8):
                    if board[rank][file] == "K" and gameFen[1] == "w":
                        kingPos = (self.convertToUCI(rank, file, "-", "-"))[0:2]
                    if board[rank][file] == "k" and gameFen[1] == "b":
                        kingPos = (self.convertToUCI(rank, file, "-", "-"))[0:2]
            # Find all of the moves putting player's king in check (This is for castling later on)
            i = 0
            while i < len(preMoveOpponentChoices):
                if preMoveOpponentChoices[i][2:4] != kingPos:
                    preMoveOpponentChoices.remove(preMoveOpponentChoices[i])
                    i -= 1
                i += 1


            # Generate all of the players moves
            moveChoices = []
            for rank in range(8):
                for file in range(8):
                    #--Find all possible PAWN moves
                    if (board[rank][file] == "P" and gameFen[1] == "w") or (board[rank][file] == "p" and gameFen[1] == "b"):
                        moves = self.pawnMoves(board, rank, file, gameFen[1])
                        for m in moves:
                            moveChoices.append(m)
                    
                    #--Find all possible ROOK moves
                    if (board[rank][file] == "R" and gameFen[1] == "w") or (board[rank][file] == "r" and gameFen[1] == "b"):
                        moves = self.rookMoves(board, rank, file, board[rank][file])
                        for m in moves:
                            moveChoices.append(m)
                    
                    #--Find all possible KNIGHT moves
                    if (board[rank][file] == "N" and gameFen[1] == "w") or (board[rank][file] == "n" and gameFen[1] == "b"):
                        moves = self.knightMoves(board, rank, file, board[rank][file])
                        for m in moves:
                            moveChoices.append(m)

                    #--Find all possible BISHOP moves
                    if (board[rank][file] == "B" and gameFen[1] == "w") or (board[rank][file] == "b" and gameFen[1] == "b"):
                        moves = self.bishopMoves(board, rank, file, board[rank][file])
                        for m in moves:
                            moveChoices.append(m)

                    #--Find all possible QUEEN moves
                    if (board[rank][file] == "Q" and gameFen[1] == "w") or (board[rank][file] == "q" and gameFen[1] == "b"):
                        moves = self.queenMoves(board, rank, file, board[rank][file])
                        for m in moves:
                            moveChoices.append(m)
                    
                    #--Find all possible KING moves
                    if (board[rank][file] == "K" and gameFen[1] == "w") or (board[rank][file] == "k" and gameFen[1] == "b"):
                        moves = self.kingMoves(board, rank, file, board[rank][file])
                        for m in moves:
                            moveChoices.append(m)

                    #--Append the possible castling moves
                    if gameFen[2] != "-":
                        moves = self.castle(board, preMoveOpponentChoices, kingPos, gameFen[2], gameFen[1])
                        for m in moves:
                            moveChoices.append(m)

                    #--Append the possible en passant moves
                    if gameFen[3] != "-":
                        moves = self.enPassant(board, gameFen[3], gameFen[1])
                        for m in moves:
                            moveChoices.append(m)


            # Chose a move at random from the available moves
            moveChoiceIndex = random.randint(0, len(moveChoices)-1)
            chosenMove = moveChoices[moveChoiceIndex]
            stableBoard = self.parseFEN(gameFen[0])
            tempFen = []

            # The do-while loop that trims out moves that would result in a check
            castlingPairs = {"e1g1":"h1f1", "e1c1":"a1d1", "e8g8":"h8f8", "e8c8":"a8d8"}
            moveChoicesCounter = 0
            while True:
                # Generate a temp board of the result of your chosen move
                stableBoard = self.parseFEN(gameFen[0]) # The orignal board that the loop 'resets' to
                board = self.convertFromUCIandUpdateBoard(chosenMove, stableBoard)
                for castle in castlingPairs: # Move the rook if the chosen move was a castle
                    if chosenMove == castle:
                        board = self.convertFromUCIandUpdateBoard(castlingPairs[castle], board)
                tempFen.append(self.createFEN(board)) # create a fen representation of the new temp board
                if gameFen[1] == "w": tempFen.append("b") # add on who's turn would come next
                else: tempFen.append("w")

                # Generate all of the possible moves that your opponent could respond with
                postMoveOpponentChoices = self.generateOpponentMoves(board, tempFen)
                # Find the new hypothetical location of player's king
                for rank in range(8):
                    for file in range(8):
                        if board[rank][file] == "K" and gameFen[1] == "w":
                            kingPos = (self.convertToUCI(rank, file, "-", "-"))[0:2]
                        if board[rank][file] == "k" and gameFen[1] == "b":
                            kingPos = (self.convertToUCI(rank, file, "-", "-"))[0:2]
                # Again, find all of the moves putting player's king in
                # check in the new hypothetical future scenario
                for hypotheticalOppMove in postMoveOpponentChoices:
                    if hypotheticalOppMove[2:4] == kingPos:
                        yeah_HeWouldDieIfYouDidThis = True
                        break
                    else: yeah_HeWouldDieIfYouDidThis = False

                # If that move resulted in the opponent having the opportunity
                # to check, remove that move from the move set and pick a new one
                if yeah_HeWouldDieIfYouDidThis:
                    moveChoices.remove(chosenMove)
                    moveChoicesCounter -= 1
                if moveChoicesCounter < len(moveChoices):
                    chosenMove = moveChoices[moveChoicesCounter]
                    moveChoicesCounter += 1
                else:
                    break

            # Here we begin the MINIMAX searching.
            board = self.parseFEN(gameFen[0]) # Reinstantiate the state of the game board

            # moveChoiceIndex = random.randint(0, len(moveChoices)-1)
            # chosenMove = moveChoices[moveChoiceIndex]

            # minimaxDepth = 2
            timeRemaining  = self.player.time_remaining / 1000000000 # Converting from ns to s
            # while chosenMove not in self.game.history:
            moveChoicesCopy = moveChoices[:]
            chosenMove = self.alphaBetaSearch(moveChoices, board, timeRemaining, gameFen)
            # for i in range(len(moveChoices)):
            #     if chosenMove in self.game.history:
            #         # print("\t------RECHOSEN------")
            #         chosenMove = self.alphaBetaSearch(moveChoices, board, minimaxDepth, gameFen)
            #         # moveChoiceIndex = random.randint(0, len(moveChoices)-1)
            #         # chosenMove = moveChoices[moveChoiceIndex]
            
            print("Chosen Move:", chosenMove)

            # Print from the piece's list
            pieceMoveList = []
            for m in moveChoices:
                if m[0:2] == chosenMove[0:2]:
                    pieceMoveList.append(m)
            print("Chosen Piece's Move Choices:", pieceMoveList)
            return chosenMove
        except Exception as e:
            print("\n\t\tFINAL DIAGNOSTIC DATA")
            print("Chosen Move END:", chosenMove)
            print("Potential Move Choices END:", moveChoices)
            print("Pre Move Opponent Choices END:", preMoveOpponentChoices)
            print("Post Move Opponent Choices END:", postMoveOpponentChoices)
            print("\n")
            print(e)
            return ""
        # <<-- /Creer-Merge: makeMove -->> retMoves

    # <<-- Creer-Merge: functions -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
    # if you need additional functions for your AI you can add them here
    # White is uppercase, black is lowercase
    # Rank is the numbered rows, file is the lettered columns
    def parseFEN(self, gameLayout):
        board = [[], [], [], [], [], [], [], []] # The blank board
        boardFEN = gameLayout.split("/")
        for rank in range(8):
            for file in boardFEN[rank]:
                if not file.isdigit(): # if the position is a piece
                    board[rank].append(file)
                else:
                    for i in range(int(file)):
                        board[rank].append(" ")

        return board

    def createFEN(self, board):
        fen = ""
        spaceCounter = 0
        for rank in range(8):
            for file in range(8):
                try:
                    if board[rank][file] == " ":
                        spaceCounter += 1
                    else:
                        if spaceCounter > 0:
                            fen += str(spaceCounter)
                            spaceCounter = 0
                        fen += board[rank][file]
                except Exception as e:
                    print("createFEN error")
                    print(e)
            if spaceCounter > 0:
                fen += str(spaceCounter)
                spaceCounter = 0
            fen += "/"

        return fen

    # Is the space in front on the board and is empty
    def isEmpty(self, board, targetRank, targetFile):
        if self.moveOnBoard(targetRank, targetFile) and board[targetRank][targetFile] == " ": return True
        return False

    # Is it on the board and does the space in front have a piece of the other color?
    def killAvailable(self, board, targetRank, targetFile, colorMoving):
        if colorMoving.isupper(): # I'm checking if a white piece has a kill available
            if self.moveOnBoard(targetRank, targetFile) and (board[targetRank][targetFile]).islower(): return True
            return False
        elif colorMoving.islower(): # Otherwise, check if a black piece has a kill available
            if self.moveOnBoard(targetRank, targetFile) and (board[targetRank][targetFile]).isupper(): return True
            return False

    # Is the move in the bounds of the board?
    def moveOnBoard(self, targetRank, targetFile):
        if ((targetRank >= 0 and targetRank < 8) and (targetFile >= 0 and targetFile < 8)):
            return True
        return False

    def convertToUCI(self, rank, file, newRank, newFile): # Converts coordinates to UCI
        rankTranslation = {0:"8", 1:"7", 2:"6", 3:"5", 4:"4", 5:"3", 6:"2", 7:"1", "-":"-"}
        fileTranslation = {0:'a', 1:'b', 2:'c', 3:'d', 4:'e', 5:'f', 6:'g', 7:'h', "-":"-"}
        return (fileTranslation[file] + rankTranslation[rank] + fileTranslation[newFile] + rankTranslation[newRank])

    def convertFromUCIandUpdateBoard(self, move, board):
        rowTranslation = {'8':0, '7':1, '6':2, '5':3, '4':4, '3':5, '2':6, '1':7}
        colTranslation = {'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7}
        row, col, newRow, newCol = rowTranslation[move[1]], colTranslation[move[0]], rowTranslation[move[3]], colTranslation[move[2]]
        board[newRow][newCol] = board[row][col]
        board[row][col] = " "
        return board

    def generateOpponentMoves(self, board, gameFen):
        # print("The opponent I'm checking:", gameFen[1])
        opponentChoices = []
        for rank in range(8):
            for file in range(8):
                #--Find all possible OPPONENT PAWN moves
                if (board[rank][file] == "P" and gameFen[1] == "w") or (board[rank][file] == "p" and gameFen[1] == "b"):
                    moves = self.pawnMoves(board, rank, file, gameFen[1])
                    for m in moves:
                        opponentChoices.append(m)
                
                #--Find all possible OPPONENT ROOK moves
                if (board[rank][file] == "R" and gameFen[1] == "w") or (board[rank][file] == "r" and gameFen[1] == "b"):
                    moves = self.rookMoves(board, rank, file, board[rank][file])
                    for m in moves:
                        opponentChoices.append(m)
                
                #--Find all possible OPPONENT KNIGHT moves
                if (board[rank][file] == "N" and gameFen[1] == "w") or (board[rank][file] == "n" and gameFen[1] == "b"):
                    moves = self.knightMoves(board, rank, file, board[rank][file])
                    for m in moves:
                        opponentChoices.append(m)

                #--Find all possible OPPONENT BISHOP moves
                if (board[rank][file] == "B" and gameFen[1] == "w") or (board[rank][file] == "b" and gameFen[1] == "b"):
                    moves = self.bishopMoves(board, rank, file, board[rank][file])
                    for m in moves:
                        opponentChoices.append(m)

                #--Find all possible OPPONENT QUEEN moves
                if (board[rank][file] == "Q" and gameFen[1] == "w") or (board[rank][file] == "q" and gameFen[1] == "b"):
                    moves = self.queenMoves(board, rank, file, board[rank][file])
                    for m in moves:
                        opponentChoices.append(m)
                
                #--Find all possible OPPONENT KING moves
                if (board[rank][file] == "K" and gameFen[1] == "w") or (board[rank][file] == "k" and gameFen[1] == "b"):
                    moves = self.kingMoves(board, rank, file, board[rank][file])
                    for m in moves:
                        opponentChoices.append(m)

        return opponentChoices


#------STANDARD PIECE MOVES------
    def pawnMoves(self, board, rank, file, whosTurn):
        if whosTurn == "w":
            whosTurn = whosTurn.upper()
        possiblePawnMoves = []
        offset = {"W":-1, "b":1}
        promotionSet = ["Q", "B", "N", "R"]
        # print(board, rank, file)
        # print(rank)

        if self.isEmpty(board, rank+offset[whosTurn], file) and self.moveOnBoard(rank+offset[whosTurn], file): # The typical pawn move
            if rank+offset[whosTurn] == 8 and whosTurn == "W":
                for newPiece in promotionSet:
                    possiblePawnMoves.append(self.convertToUCI(rank, file, rank+offset[whosTurn], file)+newPiece)
            elif rank+offset[whosTurn] == 1 and whosTurn == "b":
                for newPiece in promotionSet:
                    possiblePawnMoves.append(self.convertToUCI(rank, file, rank+offset[whosTurn], file)+newPiece.lower())
            else:
                possiblePawnMoves.append(self.convertToUCI(rank, file, rank+offset[whosTurn], file))

            if self.isEmpty(board, rank+(offset[whosTurn]*2), file) and (rank == 6 or rank == 1): # Additional 2 ahead move for the first play
                possiblePawnMoves.append(self.convertToUCI(rank, file, rank+(offset[whosTurn]*2), file))

        if self.killAvailable(board, rank+offset[whosTurn], file+1, whosTurn): # Kill diagonal right?
            possiblePawnMoves.append(self.convertToUCI(rank, file, rank+offset[whosTurn], file+1))
        if self.killAvailable(board, rank+offset[whosTurn], file-1, whosTurn): # Kill diagonal left?
            possiblePawnMoves.append(self.convertToUCI(rank, file, rank+offset[whosTurn], file-1))

        return possiblePawnMoves

    def rookMoves(self, board, rank, file, colorMoving):
        dirOffSet = {
            "u":(-1,0),
            "l":(0,-1),
            "d":(1,0),
            "r":(0,1)
        }
        possibleRookMoves = []
        
        for dir in dirOffSet:
            for howFar in range(1, 8):
                targetRank = rank + (howFar * dirOffSet[dir][0])
                targetFile = file + (howFar * dirOffSet[dir][1])
                if self.killAvailable(board, targetRank, targetFile, colorMoving):
                    possibleRookMoves.append(self.convertToUCI(rank, file, targetRank, targetFile))
                    break
                elif self.isEmpty(board, targetRank, targetFile):
                    possibleRookMoves.append(self.convertToUCI(rank, file, targetRank, targetFile))
                elif not self.isEmpty(board, targetRank, targetFile): break

        return possibleRookMoves

    def knightMoves(self, board, rank, file, colorMoving):
        dirOffSet = {
            (-2,-1), #up2, left1 
            (-2,1), #up2, right1
            (1,2), #up1, right2
            (-1,2), #down1, right2
            (2,1), #down2, right1
            (2,-1), #down2, left1
            (1, -2), #up1, left2
            (-1, -2) #down1, left2
        }
        possibleKnightMoves = []

        for move in dirOffSet:
            if self.isEmpty(board, (rank+move[0]), (file+move[1])) or self.killAvailable(board, (rank+move[0]), (file+move[1]), colorMoving):
                possibleKnightMoves.append(self.convertToUCI(rank, file, (rank+move[0]), (file+move[1])))

        return possibleKnightMoves

    def bishopMoves(self, board, rank, file, colorMoving):
        dirOffSet = {
            "ur":(-1,1), #up+right
            "dl":(1,-1), #down+left
            "dr":(1,1), #down+right
            "ul":(-1,-1) #up+left
        }
        possibleBishopMoves = []
        
        for dir in dirOffSet:
            for howFar in range(1, 8):
                targetRank = rank + (howFar * dirOffSet[dir][0])
                targetFile = file + (howFar * dirOffSet[dir][1])
                if self.killAvailable(board, targetRank, targetFile, colorMoving):
                    possibleBishopMoves.append(self.convertToUCI(rank, file, targetRank, targetFile))
                    break
                elif self.isEmpty(board, targetRank, targetFile):
                    possibleBishopMoves.append(self.convertToUCI(rank, file, targetRank, targetFile))
                elif not self.isEmpty(board, targetRank, targetFile): break

        return possibleBishopMoves

    def queenMoves(self, board, rank, file, colorMoving):
        diagonalMoves = self.rookMoves(board, rank, file, colorMoving)
        levelMoves = self.bishopMoves(board, rank, file, colorMoving)
        possibleQueenMoves = []

        for m in diagonalMoves:
            possibleQueenMoves.append(m)
        for m in levelMoves:
            possibleQueenMoves.append(m)
            
        return possibleQueenMoves

    def kingMoves(self, board, rank, file, colorMoving):
        dirOffSet = {
            "u":(-1,0),
            "l":(0,-1),
            "d":(1,0),
            "r":(0,1),
            "ur":(-1,1), #up+right
            "dl":(1,-1), #down+left
            "dr":(1,1), #down+right
            "ul":(-1,-1) #up+left
        }
        possibleKingMoves = []

        for dir in dirOffSet:
            targetRank = rank + dirOffSet[dir][0]
            targetFile = file + dirOffSet[dir][1]
            if self.killAvailable(board, targetRank, targetFile, colorMoving) or self.isEmpty(board, targetRank, targetFile):
                possibleKingMoves.append(self.convertToUCI(rank, file, targetRank, targetFile))

        return possibleKingMoves

#------SPECIAL MOVES------
    def castle(self, board, preOppMoveSet, kingPos, availability, colorMoving):        
        castlablePieces = []
        for letter in availability:
            castlablePieces.append(letter)
    
        castlingMove = []

        for m in preOppMoveSet:
            for piece in castlablePieces:
                if piece == "K" and colorMoving == "w" and board[7][5] == " " and board[7][6] == " ":
                    if m[2:4] != kingPos and m[2:4] != board[7][5] and m[2:4] != board[7][6] and m[2:4] != board[7][7]:
                        castlingMove.append("e1g1")
                if piece == "Q" and colorMoving == "w" and board[7][3] == " " and board[7][2] == " " and board[7][1] == " ":
                    if m[2:4] != kingPos and m[2:4] != board[7][3] and m[2:4] != board[7][2] and m[2:4] != board[7][1] and m[2:4] != board[7][0]:
                        castlingMove.append("e1c1")
                if piece == "k" and colorMoving == "b" and board[0][5] == " " and board[0][6] == " ":
                    if m[2:4] != kingPos and m[2:4] != board[0][5] and m[2:4] != board[0][6] and m[2:4] != board[0][7]:
                        castlingMove.append("e8g8")
                if piece == "q" and colorMoving == "b" and board[0][3] == " " and board[0][2] == " " and board[0][1] == " ":
                    if m[2:4] != kingPos and m[2:4] != board[0][3] and m[2:4] != board[0][2] and m[2:4] != board[0][1] and m[2:4] != board[0][0]:
                        castlingMove.append("e8c8")
        
        return castlingMove

    def enPassant(self, board, enPassantMarker, colorMoving):
        enPassantMoves = []
        offset = {"w":-1, "b":1}
        colorPiece = {"w":"P", "b":"p"}
        rowTranslation = {'8':0, '7':1, '6':2, '5':3, '4':4, '3':5, '2':6, '1':7}
        colTranslation = {'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7}
        colOffset = [1, -1]

        for c in colOffset:
            if enPassantMarker != "-":
                rowToCheck = rowTranslation[enPassantMarker[1]] + offset[colorMoving]
                colToCheck = colTranslation[enPassantMarker[0]]+c
                if self.moveOnBoard(rowToCheck, colToCheck) and board[rowToCheck][colToCheck] == colorPiece[colorMoving]: # diagonal left
                    enPassantMoves.append(self.convertToUCI(rowToCheck, colToCheck, enPassantMarker[1], enPassantMarker[0]))
                # if board[rowToCheck][colTranslation[enPassantMarker[0]]+1] == colorPiece[colorMoving]: # diagonal right
                #     col = colTranslation[enPassantMarker[0]]+1
                #     enPassantMoves.append(self.convertToUCI(rowToCheck, col, enPassantMarker[1], enPassantMarker[0]))

        return enPassantMoves


#------GAME ASSIGNMENT 3 FUNCTIONS------
# NOTE: the heurstic evaluator function determines how many points a player still has on the board
# and creates the priority queue based off of that. The maximum points that a player can have on
# the board is 8(1)+2(3)+2(3)+2(5)+1(9) = 39
    #------Heuristic Evaluator
    def hVal(self, board, color):
        whitePoints = {"P":1, "B":3, "K":3, "R":5, "Q":9}
        blackPoints = {"p":1, "b":3, "k":3, "r":5, "q":9}
        remainingScore = 0
        for rank in board:
            for file in rank:
                if color == "w" and file in whitePoints:
                    remainingScore += whitePoints[file]
                if color == "b" and file in blackPoints:
                    remainingScore += blackPoints[file]
        return remainingScore

    #------Time-Limited Minimax with Alpha-Beta Pruning functions
    # Here we find every possible minimax score (heuristic) that we
    # could attain, selecting only the best one as our chosen move
    def alphaBetaSearch(self, moveChoices, board, timeLeft, currGameFen):
        castlingPairs = {"e1g1":"h1f1", "e1c1":"a1d1", "e8g8":"h8f8", "e8c8":"a8d8"}
        bestPotentialScore = -math.inf
        tieScoreList = []

        percentageOfTime = 0.022 # 2.2%
        d = 0
        t0 = calendar.timegm(time.gmtime())
        timeTurn = t0 + (timeLeft * percentageOfTime)

        while True:
            for m in moveChoices:
                bestMove = m
                # Generate a temp board of the result of your chosen move
                stableBoard = self.parseFEN(currGameFen[0]) # The orignal board that the loop 'resets' to
                board = self.convertFromUCIandUpdateBoard(m, stableBoard)
                for castle in castlingPairs: # Move the rook if the chosen move was a castle
                    if m == castle:
                        board = self.convertFromUCIandUpdateBoard(castlingPairs[castle], board)

                potential = self.minValue(board, d, -math.inf)
                
                # What if multiple moves have the same best hueristic?
                # This section resolves that by placing them into a list
                # of tied best moves and then later choosing one at random
                # so that the same one isn't chosen every game 
                if potential > bestPotentialScore:
                    bestPotentialScore = potential
                    bestMove = m
                    tieScoreList.clear()
                    tieScoreList.append(m)
                if potential == bestPotentialScore:
                    tieScoreList.append(m)
            d += 1
            t1 = calendar.timegm(time.gmtime())
            if t1 >= timeTurn:
                break
        
        # print("\t------alphaBetaSearch------")
        if len(tieScoreList) > 1:
            index = random.randint(0, len(tieScoreList)-1)
            bestMove = tieScoreList[index]
            return bestMove
        else: return bestMove
    
    # Opponent attempts to minimize the player's score
    def minValue(self, board, d, alpha, beta):
        oppositeDic = {"white":"b", "black":"w"}
        
        if d == 0: return self.hVal(board, self.player.color)

        stableBoard = board[:]
        tempFen = ["", oppositeDic[self.player.color]]

        # Generate all of the possible moves that the opponent could respond with
        opponentChoices = self.generateOpponentMoves(board, tempFen)
        # Find the move that the opponent might make that would minimize the player's score
        vMinValue = math.inf # I've instantiated this to just over the max possible score to avoid accientally returning the wrong value
        
        for o in opponentChoices:
            # Generate a temp board of the result of the opponent's chosen move
            board = self.convertFromUCIandUpdateBoard(o, stableBoard)

            potentialScore = self.maxValue(board, d-1, alpha, beta)
            if vMinValue <= alpha: return vMinValue
            beta = max(beta, vMaxValue)
            if potentialScore <= vMinValue:
                vMinValue = potentialScore
            
        # print("\t------MINVALUE------")
        return vMinValue

    # Player attempts to maximize their score
    def maxValue(self, board, d, alpha, beta):
        if d == 0: return self.hVal(board, self.player.color)

        stableBoard = board[:]
        tempFen = ["", self.player.color]

        # Generate all of the possible moves that the opponent could respond with
        respondingChoices = self.generateOpponentMoves(board, tempFen)
        # Find the move that the opponent might make that would minimize the player's score
        vMaxValue = -math.inf # I've instantiated this to just over the max possible score to avoid accientally returning the wrong value
        
        for r in respondingChoices:
            # Generate a temp board of the result of the opponent's chosen move
            board = self.convertFromUCIandUpdateBoard(r, stableBoard)

            potentialScore = self.minValue(board, d-1, alpha, beta)
            if vMaxValue <= beta: return vMaxValue
            alpha = max(alpha, vMaxValue)
            if potentialScore <= vMaxValue:
                vMaxValue = potentialScore
            
        # print("\t------MAXVALUE------")
        return vMaxValue

    # <<-- /Creer-Merge: functions -->>
