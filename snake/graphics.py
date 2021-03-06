#!/usr/bin/env python

# graphics.py
#
# Copyright (C) 2013, 2014 Kano Computing Ltd.
# License:   http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#

import stage
import game
import theme
import curses
import gameloop
import parser

screen = None


def drawTile(x, y, tile='', color=None):
    color = color or theme.get_color('default')

    x = x * 2 + stage.padding[3] * 2 + stage.width / 2
    y += stage.padding[0] + stage.height / 2

    try:
        screen.addstr(y, x, tile, color)
        if (len(tile) < 2):
            screen.addstr(y, x + 1, tile, color)
    except:
        # This is not the built-in exit, rather the one declared later on
        exit()


def drawInitGame():
    drawTile(-5, -2, _("  Welcome to SNAKE "), theme.get_color('border'))
    drawTile(-4, 2, _(" Press [ENTER] "), theme.get_color('border'))
    left = u"\u2190"
    up = u"\u2191"
    down = u"\u2193"
    right = u"\u2192"
    drawTile(-5, 4, _(" Use [{0}{1}{2}{3}] to move ").format(left, up, down, right), theme.get_color('border'))


def drawGameOver():
    speed = gameloop.speed
    size = stage.passSize
    lives = game.lives
    sizeStr = ''
    speedStr = ''
    livesStr = str(lives)
    # set speed string
    if(speed == .2):
        speedStr = _('Slow')
    elif(speed == .12):
        speedStr = _('Medium')
    elif(speed == .07):
        speedStr = _('Fast')
    # set size string
    if(size == 's'):
        sizeStr = _('Small')
    elif(size == 'm'):
        sizeStr = _('Medium')
    elif(size == 'l'):
        sizeStr = _('Large')
    drawTile(-4, -10, _("  GAME OVER  "), theme.get_color('border'))
    drawTile(-3, -8, _("Score:") + str(game.score), theme.get_color('border'))
    drawTile(-3, -6, _("Speed:") + speedStr, theme.get_color('border'))
    drawTile(-3, -4, _("Size:") + sizeStr, theme.get_color('border'))
    drawTile(-3, -2, _("Lives:") + livesStr, theme.get_color('border'))

    if parser.args.tutorial:
        drawTile(-6, 2, _(" Press [ENTER] to exit "), theme.get_color('border'))
    else:
        drawTile(-7, 2, _(" Press [ENTER] to continue "), theme.get_color('border'))


def drawScore():
    score_formatted = str(game.score).zfill(2)
    drawTile(
        (stage.width / 2) - 1,
        (-stage.height / 2) - 1,
        score_formatted,
        theme.get_color('border')
    )


def drawLives():
    posx = (-stage.width / 2) + 3
    for x in xrange(1, game.lives + 1):
        posx += 1
        drawTile(
            posx,
            (-stage.height / 2) - 1,
            theme.get_tile('lives'),
            theme.get_color('lives')
        )
        posx += 1
        drawTile(
            posx,
            (-stage.height / 2) - 1,
            theme.get_tile('border-h'),
            theme.get_color('border')
        )


def drawSnake():
    for part in game.snake:
        drawTile(
            part[0],
            part[1],
            theme.get_tile('snake-body'),
            theme.get_color('snake')
        )
    # Clean last tile
    drawTile(
        game.lastPos[0],
        game.lastPos[1],
        theme.get_tile('bg'),
        theme.get_color('bg')
    )


def drawApples():
    for apple in game.apples:
        drawTile(
            apple[0],
            apple[1],
            theme.get_tile('apple'),
            theme.get_color('apple')
        )


def drawGame():
    for y in range(stage.boundaries['top'], stage.boundaries['bottom']):
        for x in range(stage.boundaries['left'], stage.boundaries['right']):
            drawTile(x, y, theme.get_tile('bg'), theme.get_color('bg'))
    drawBorders()
    drawText()


def drawBorders():
    tile_v = theme.get_tile('border-v')
    tile_h = theme.get_tile('border-h')
    tile_c = theme.get_tile('border-c')
    color = theme.get_color('border')

    x_left = stage.boundaries['left']
    x_right = stage.boundaries['right']

    y_top = stage.boundaries['top']
    y_bottom = stage.boundaries['bottom']

    for y in range(y_top, y_bottom):
        drawTile(x_left - 1, y, tile_v, color)
        drawTile(x_right, y, tile_v, color)

    for x in range(x_left, x_right):
        drawTile(x, y_top - 1, tile_h, color)
        drawTile(x, y_bottom, tile_h, color)

    drawTile(x_left - 1, y_top - 1, tile_c, color)
    drawTile(x_left - 1, y_bottom, tile_c, color)
    drawTile(x_right, y_top - 1, tile_c, color)
    drawTile(x_right, y_bottom, tile_c, color)


def drawText():
    color = theme.get_color('border')
    score_text = _("score:")
    drawTile((stage.width / 2) - (len(score_text) / 2) - 2, (-stage.height / 2) - 1, score_text, color)
    drawTile((-stage.width / 2), (-stage.height / 2) - 1, _("lives:"), color)
    drawTile(-5, (stage.height / 2), _(" Press Q to quit "), color)


def update():
    drawSnake()
    drawApples()
    drawScore()
    drawLives()


def init():
    global screen

    screen = curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    curses.start_color()
    screen.nodelay(1)


def exit():
    screen.clear()
    screen.keypad(0)
    curses.echo()
    curses.nocbreak()
    curses.endwin()
