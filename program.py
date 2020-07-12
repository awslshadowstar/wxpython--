import wx
import wx.adv
import random
from PIL import Image

ID_EASY = wx.NewId()
ID_NORMAL = wx.NewId()
ID_HARD = wx.NewId()
ID_LUNATIC = wx.NewId()
diffchoice = "NORMAL"


class Tetris(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, size=(360, 760),
                          style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER ^ wx.MAXIMIZE_BOX)
        self.InitUI()
        self.initFrame()

    def InitUI(self):

        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        fileItem1 = fileMenu.Append(ID_EASY, 'EASY')
        fileItem2 = fileMenu.Append(ID_NORMAL, 'NORMAL')
        fileItem3 = fileMenu.Append(ID_HARD, 'HARD')
        fileItem4 = fileMenu.Append(ID_LUNATIC, 'LUNATIC')

        menubar.Append(fileMenu, '&Difficuity')

        self.Bind(wx.EVT_MENU, self.difficuity, fileItem1)
        self.Bind(wx.EVT_MENU, self.difficuity, fileItem2)
        self.Bind(wx.EVT_MENU, self.difficuity, fileItem3)
        self.Bind(wx.EVT_MENU, self.difficuity, fileItem4)

        helpmenu = wx.Menu()
        helpItem = helpmenu.Append(wx.ID_ANY, 'help')
        menubar.Append(helpmenu, 'help')
        self.Bind(wx.EVT_MENU, self.morehelp, helpItem)
        self.SetMenuBar(menubar)

        self.icon = wx.Icon('ico/icon.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.icon)

    def difficuity(self, e):
        eid = e.GetId()
        if eid == ID_EASY:
            Board.Speed = 500
            diffchoice = "EASY"
            self.SetTitle("Tetris "+diffchoice+" MODE")
        elif eid == ID_NORMAL:
            Board.Speed = 300
            diffchoice = "NORMAL"
            self.SetTitle("Tetris "+diffchoice+" MODE")
        elif eid == ID_HARD:
            Board.Speed = 200
            diffchoice = "HARD"
            self.SetTitle("Tetris "+diffchoice+" MODE")
        elif eid == ID_LUNATIC:
            Board.Speed = 50
            diffchoice = "LUNATIC"
            self.SetTitle("Tetris "+diffchoice+" MODE")

    def initFrame(self):

        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetStatusText('0')
        self.board = Board(self)
        self.board.SetFocus()
        self.board.start()
        self.board.help()

        self.SetTitle("Tetris "+diffchoice+" MODE")
        self.Centre()

    def morehelp(self, e):
        msg = '''
        俄罗斯方块 by shadowstar
        共计六张福利图
        单击Difficuty选择难度
        按键介绍：
        A：向左
        D：向右
        W：翻转
        S：加速下落
        SPACE：直接到达底部
        P：开始/暂停/解除暂停
        注意：请在暂停模式下选择难度否则无法生效
        '''
        wx.MessageBox(msg, '玩法介绍',
                      wx.OK | wx.ICON_INFORMATION)


class Board(wx.Panel):

    BoardWidth = 10
    BoardHeight = 22
    Speed = 300
    ID_TIMER = 1

    def __init__(self, *args, **kw):

        super(Board, self).__init__(*args, **kw)

        self.initBoard()

    def initBoard(self):

        self.timer = wx.Timer(self, Board.ID_TIMER)
        self.isWaitingAfterLine = False
        self.curPiece = Shape()
        self.nextPiece = Shape()
        self.curX = 0
        self.curY = 0
        self.numLinesRemoved = 0
        self.board = []

        self.isStarted = False
        self.isPaused = False

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        self.Bind(wx.EVT_TIMER, self.OnTimer, id=Board.ID_TIMER)

        self.clearBoard()

    def shapeAt(self, x, y):

        return self.board[(y * Board.BoardWidth) + x]

    def setShapeAt(self, x, y, shape):

        self.board[(y * Board.BoardWidth) + x] = shape

    def squareWidth(self):

        return self.GetClientSize().GetWidth() // Board.BoardWidth

    def squareHeight(self):

        return self.GetClientSize().GetHeight() // Board.BoardHeight

    def start(self):

        if self.isPaused:
            return

        self.isStarted = True
        self.isWaitingAfterLine = False
        self.numLinesRemoved = 0
        self.clearBoard()

        self.newPiece()
        self.timer.Start(Board.Speed)

    def pause(self):

        if not self.isStarted:
            return

        self.isPaused = not self.isPaused
        statusbar = self.GetParent().statusbar

        if self.isPaused:
            self.timer.Stop()
            statusbar.SetStatusText(
                'pause')
        else:
            self.timer.Start(Board.Speed)
            statusbar.SetStatusText(str(self.numLinesRemoved))

        self.Refresh()

    def help(self):
        if not self.isStarted:
            return

        self.isPaused = not self.isPaused
        statusbar = self.GetParent().statusbar

        if self.isPaused:
            self.timer.Stop()
            statusbar.SetStatusText(
                'enter L to get licence')
        else:
            self.timer.Start(Board.Speed)
            statusbar.SetStatusText(str(self.numLinesRemoved))

        self.Refresh()

    def gethelp(self):
        self.OnAboutBox()

    def OnAboutBox(self):

        description = """俄罗斯方块粗制版，超过20分有福利(正经向)
        点击菜单栏的难度和帮助选择难度查看难度和规则
        """

        licence = """手签license，你值得拥有
        """

        info = wx.adv.AboutDialogInfo()

        info.SetIcon(wx.Icon('./ico/icon.png', wx.BITMAP_TYPE_PNG))
        info.SetName('万华镜')
        info.SetVersion('1.0')
        info.SetDescription(description)
        info.SetCopyright('(C) 2020 - 2020 July Shen')
        info.SetWebSite('https://github.com/awsl1784597340')
        info.SetLicence(licence)
        info.AddDeveloper('Shadowstar Shen')
        info.AddDocWriter('Shadowstar Shen')
        info.AddArtist('Shadowstar Shen')
        info.AddTranslator('Shadowstar Shen')

        wx.adv.AboutBox(info)

    def clearBoard(self):

        for i in range(Board.BoardHeight * Board.BoardWidth):
            self.board.append(Tetrominoes.NoShape)

    def OnPaint(self, event):

        dc = wx.PaintDC(self)

        size = self.GetClientSize()
        boardTop = size.GetHeight() - Board.BoardHeight * self.squareHeight()

        for i in range(Board.BoardHeight):
            for j in range(Board.BoardWidth):

                shape = self.shapeAt(j, Board.BoardHeight - i - 1)

                if shape != Tetrominoes.NoShape:
                    self.drawSquare(dc,
                                    0 + j * self.squareWidth(),
                                    boardTop + i * self.squareHeight(), shape)

        if self.curPiece.shape() != Tetrominoes.NoShape:

            for i in range(4):

                x = self.curX + self.curPiece.x(i)
                y = self.curY - self.curPiece.y(i)

                self.drawSquare(dc, 0 + x * self.squareWidth(),
                                boardTop + (Board.BoardHeight -
                                            y - 1) * self.squareHeight(),
                                self.curPiece.shape())

    def OnKeyDown(self, event):

        if not self.isStarted or self.curPiece.shape() == Tetrominoes.NoShape:
            event.Skip()
            return

        keycode = event.GetKeyCode()

        if keycode == ord('P') or keycode == ord('p'):
            self.pause()
            return

        if keycode == ord('l') or keycode == ord('L'):
            self.gethelp()
            return

        if self.isPaused:
            return

        elif keycode == ord('a')or keycode == ord('A'):
            self.tryMove(self.curPiece, self.curX - 1, self.curY)

        elif keycode == ord('d')or keycode == ord('D'):
            self.tryMove(self.curPiece, self.curX + 1, self.curY)

        elif keycode == ord('w')or keycode == ord('W'):
            self.tryMove(self.curPiece.rotatedLeft(), self.curX, self.curY)

        elif keycode == wx.WXK_SPACE:
            self.dropDown()

        elif keycode == ord('S') or keycode == ord('s'):
            self.oneLineDown()

        else:
            event.Skip()

    def OnTimer(self, event):

        if event.GetId() == Board.ID_TIMER:

            if self.isWaitingAfterLine:
                self.isWaitingAfterLine = False
                self.newPiece()

            else:
                self.oneLineDown()

        else:
            event.Skip()

    def dropDown(self):

        newY = self.curY

        while newY > 0:
            if not self.tryMove(self.curPiece, self.curX, newY - 1):
                break
            newY -= 1

        self.pieceDropped()

    def oneLineDown(self):

        if not self.tryMove(self.curPiece, self.curX, self.curY - 1):
            self.pieceDropped()

    def pieceDropped(self):

        for i in range(4):

            x = self.curX + self.curPiece.x(i)
            y = self.curY - self.curPiece.y(i)
            self.setShapeAt(x, y, self.curPiece.shape())

        self.removeFullLines()

        if not self.isWaitingAfterLine:
            self.newPiece()

    def removeFullLines(self):

        numFullLines = 0

        statusbar = self.GetParent().statusbar

        rowsToRemove = []

        for i in range(Board.BoardHeight):
            n = 0
            for j in range(Board.BoardWidth):
                if not self.shapeAt(j, i) == Tetrominoes.NoShape:
                    n = n + 1

            if n == 10:
                rowsToRemove.append(i)

        rowsToRemove.reverse()

        for m in rowsToRemove:
            for k in range(m, Board.BoardHeight):
                for l in range(Board.BoardWidth):
                    self.setShapeAt(l, k, self.shapeAt(l, k + 1))

            numFullLines = numFullLines + len(rowsToRemove)

            if numFullLines > 0:

                self.numLinesRemoved = self.numLinesRemoved + numFullLines
                statusbar.SetStatusText(str(self.numLinesRemoved))
                self.isWaitingAfterLine = True
                self.curPiece.setShape(Tetrominoes.NoShape)
                self.Refresh()

    def newPiece(self):

        self.curPiece = self.nextPiece
        statusbar = self.GetParent().statusbar
        self.nextPiece.setRandomShape()

        self.curX = Board.BoardWidth // 2 + 1
        self.curY = Board.BoardHeight - 1 + self.curPiece.minY()

        if not self.tryMove(self.curPiece, self.curX, self.curY):

            self.curPiece.setShape(Tetrominoes.NoShape)
            self.timer.Stop()
            self.isStarted = False
            statusbar.SetStatusText('Game over')
            if self.numLinesRemoved >= 20:
                wx.MessageBox('恭喜恭喜，老绅士了！', '恭喜',
                              wx.OK | wx.ICON_INFORMATION)
                num = random.randint(1, 6)
                image = Image.open('ico/image{}.jpg'.format(num))
                image.show()
            else:
                wx.MessageBox('你太菜了，哪来的福利?再见！', '哈哈哈哈哈',
                              wx.OK | wx.ICON_INFORMATION)

    def tryMove(self, newPiece, newX, newY):

        for i in range(4):

            x = newX + newPiece.x(i)
            y = newY - newPiece.y(i)

            if x < 0 or x >= Board.BoardWidth or y < 0 or y >= Board.BoardHeight:
                return False

            if self.shapeAt(x, y) != Tetrominoes.NoShape:
                return False

        self.curPiece = newPiece
        self.curX = newX
        self.curY = newY
        self.Refresh()

        return True

    def drawSquare(self, dc, x, y, shape):

        colors = ['#000000', '#CC6666', '#66CC66', '#6666CC',
                  '#CCCC66', '#CC66CC', '#66CCCC', '#DAAA00']

        light = ['#000000', '#F89FAB', '#79FC79', '#7979FC',
                 '#FCFC79', '#FC79FC', '#79FCFC', '#FCC600']

        dark = ['#000000', '#803C3B', '#3B803B', '#3B3B80',
                '#80803B', '#803B80', '#3B8080', '#806200']

        pen = wx.Pen(light[shape])
        pen.SetCap(wx.CAP_PROJECTING)
        dc.SetPen(pen)

        dc.DrawLine(x, y + self.squareHeight() - 1, x, y)
        dc.DrawLine(x, y, x + self.squareWidth() - 1, y)

        darkpen = wx.Pen(dark[shape])
        darkpen.SetCap(wx.CAP_PROJECTING)
        dc.SetPen(darkpen)

        dc.DrawLine(x + 1, y + self.squareHeight() - 1,
                    x + self.squareWidth() - 1, y + self.squareHeight() - 1)
        dc.DrawLine(x + self.squareWidth() - 1,
                    y + self.squareHeight() - 1, x + self.squareWidth() - 1, y + 1)

        dc.SetPen(wx.TRANSPARENT_PEN)
        dc.SetBrush(wx.Brush(colors[shape]))
        dc.DrawRectangle(x + 1, y + 1, self.squareWidth() - 2,
                         self.squareHeight() - 2)


class Tetrominoes(object):

    NoShape = 0
    ZShape = 1
    SShape = 2
    LineShape = 3
    TShape = 4
    SquareShape = 5
    LShape = 6
    MirroredLShape = 7


class Shape(object):

    coordsTable = (
        ((0, 0),     (0, 0),     (0, 0),     (0, 0)),
        ((0, -1),    (0, 0),     (-1, 0),    (-1, 1)),
        ((0, -1),    (0, 0),     (1, 0),     (1, 1)),
        ((0, -1),    (0, 0),     (0, 1),     (0, 2)),
        ((-1, 0),    (0, 0),     (1, 0),     (0, 1)),
        ((0, 0),     (1, 0),     (0, 1),     (1, 1)),
        ((-1, -1),   (0, -1),    (0, 0),     (0, 1)),
        ((1, -1),    (0, -1),    (0, 0),     (0, 1))
    )

    def __init__(self):

        self.coords = [[0, 0] for i in range(4)]
        self.pieceShape = Tetrominoes.NoShape

        self.setShape(Tetrominoes.NoShape)

    def shape(self):

        return self.pieceShape

    def setShape(self, shape):

        table = Shape.coordsTable[shape]
        for i in range(4):
            for j in range(2):
                self.coords[i][j] = table[i][j]

        self.pieceShape = shape

    def setRandomShape(self):

        self.setShape(random.randint(1, 7))

    def x(self, index):

        return self.coords[index][0]

    def y(self, index):

        return self.coords[index][1]

    def setX(self, index, x):

        self.coords[index][0] = x

    def setY(self, index, y):

        self.coords[index][1] = y

    def minX(self):

        m = self.coords[0][0]
        for i in range(4):
            m = min(m, self.coords[i][0])

        return m

    def maxX(self):

        m = self.coords[0][0]
        for i in range(4):
            m = max(m, self.coords[i][0])

        return m

    def minY(self):

        m = self.coords[0][1]
        for i in range(4):
            m = min(m, self.coords[i][1])

        return m

    def maxY(self):

        m = self.coords[0][1]

        for i in range(4):
            m = max(m, self.coords[i][1])

        return m

    def rotatedLeft(self):

        if self.pieceShape == Tetrominoes.SquareShape:
            return self

        result = Shape()
        result.pieceShape = self.pieceShape

        for i in range(4):
            result.setX(i, self.y(i))
            result.setY(i, -self.x(i))

        return result


def main():

    app = wx.App()
    ex = Tetris(None)
    ex.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()
