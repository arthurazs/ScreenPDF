# coding: utf-8
from __future__ import absolute_import
from fpdf import FPDF
import os.path as path


class Pages:
    # Margins size
    leftMarginSize = 1.5
    topMarginSize = 1
    rightMarginSize = 1
    bottomMarginSize = 1
    headerMarginSize = 0.5

    # Page Margins
    height = 11
    width = 8.5
    leftMargin = leftMarginSize
    topMargin = topMarginSize
    rightMargin = width - rightMarginSize
    bottomMargin = height - bottomMarginSize
    headerMargin = headerMarginSize

    # Font
    font = '10Pitch'
    font_path = path.abspath(
        path.join(path.dirname(__file__), 'courier10pitch'))
    fontSize = 12
    textHeight = 0.17

    # Element Margin
    # Transition
    transitionLeftSize = 4
    transitionLeftMargin = transitionLeftSize + leftMarginSize
    # Character
    characterLeftSize = 2
    characterLeftMargin = characterLeftSize + leftMarginSize
    # Parenthetical
    parentheticalLeftMarginSize = 1.5
    parentheticalLeftMargin = parentheticalLeftMarginSize + leftMarginSize
    parentheticalRightMarginSize = 2
    parentheticalRightMargin = parentheticalRightMarginSize + rightMarginSize
    # Dialogue
    dialogueLeftMarginSize = 1
    dialogueLeftMargin = dialogueLeftMarginSize + leftMarginSize
    dialogueRightMarginSize = 1.5
    dialogueRight = dialogueRightMarginSize + rightMarginSize

    # Borders
    textBorder = False
    border = False


class ScreenPDF(FPDF):

    def header(self):
        if(self.page_no() > 2):
            self.set_y(Pages.headerMargin)
            self.multi_cell(
                0, Pages.textHeight, str(self.page_no() - 1) + '.',
                Pages.textBorder, 'R', False)
            self.set_y(Pages.topMargin)

    def footer(self):
        if (Pages.border):
            self._printMargins()

    def _printMargins(self):
        # header
        self.line(
            Pages.leftMargin, Pages.headerMargin,
            Pages.rightMargin, Pages.headerMargin)
        self.line(
            Pages.leftMargin, Pages.headerMargin + Pages.textHeight,
            Pages.rightMargin, Pages.headerMargin + Pages.textHeight)
        self.line(
            Pages.leftMargin, Pages.headerMargin, Pages.leftMargin,
            Pages.headerMargin + Pages.textHeight)
        self.line(
            Pages.rightMargin, Pages.headerMargin, Pages.rightMargin,
            Pages.headerMargin + Pages.textHeight)
        # top
        self.line(
            Pages.leftMargin, Pages.topMargin,
            Pages.rightMargin, Pages.topMargin)
        # left
        self.line(
            Pages.leftMargin, Pages.topMargin,
            Pages.leftMargin, Pages.bottomMargin)
        # right
        self.line(
            Pages.rightMargin, Pages.topMargin,
            Pages.rightMargin, Pages.bottomMargin)
        # bottom
        self.line(
            Pages.leftMargin, Pages.bottomMargin,
            Pages.rightMargin, Pages.bottomMargin)

    def __init__(self, title, authors, informations):
        self._sceneCount = 0        # Scene count
        self._subsceneCount = 0     # Subscene count
        self._authors = authors
        self._informations = informations
        self._title = title
        super(ScreenPDF, self).__init__(
            'Portrait', 'in', (Pages.width, Pages.height)
        )
        self.add_font(
            '10Pitch', '',
            path.join(
                Pages.font_path, 'Courier10PitchBT-Roman.ttf'),
            True)
        self.add_font(
            '10Pitch', 'B',
            path.join(
                Pages.font_path, 'Courier10PitchBT-Bold.ttf'),
            True)
        self.add_font(
            '10Pitch', 'I',
            path.join(
                Pages.font_path, 'Courier10PitchBT-Italic.ttf'),
            True)
        self.add_font(
            '10Pitch', 'BI',
            path.join(
                Pages.font_path, 'Courier10PitchBT-BoldItalic.ttf'),
            True)
        self._titlePage()
        self._lastCharacter = (None, None)

    def newPage(self):
        self.set_margins(
            Pages.leftMarginSize, Pages.topMarginSize,
            Pages.rightMarginSize)
        self.set_auto_page_break(True, Pages.bottomMarginSize)
        self.set_font(Pages.font, '', Pages.fontSize)
        self.add_page('Portrait')

    def _titlePage(self):
        self.newPage()
        self.set_y((Pages.height / 2) - Pages.textHeight)
        quote = u'\N{QUOTATION MARK}'.decode('utf-8', 'strict')
        test = '{0}{1}{0}'.format(quote, self._title.upper())
        line = test.encode('utf-8', 'strict')
        self._writep(line, 'C')

        self._writep('written by', 'C')
        author = ''
        for a in self._authors:
            author += a + ' & '
        self._writep(author[:-3], 'C')

        self.set_y(
            (Pages.bottomMargin - Pages.textHeight) -
            (len(self._informations) * Pages.textHeight)
        )

        self.ln()
        for i in self._informations:
            self._write(i, 'R')
        self.newPage()
        self._fadeIn()
        # PDF's details
        self.set_author(self._authors[0])
        self.set_keywords('screenplay script')
        self.set_creator('ScreenPdf')
        self.set_subject('Screenplay')
        self.set_title(self._title)

    def _fadeIn(self):
        self._writep('FADE IN:')

    def _fadeOut(self):
        self.transition('fade out.')
        self.ln()
        self.set_font(Pages.font, 'U', Pages.fontSize)
        self._write('THE END', 'C')
        self.set_font('')

    def scene(self, text):
        self._sceneCount += 1
        self._subsceneCount = 0
        self.ln()
        self._writep(text.upper())

    def subscene(self, text):
        self._subsceneCount += 1
        self._writep(text.upper())

    def _write(self, text, align='L', margin=Pages.leftMarginSize):
        self.set_left_margin(margin)
        self.ln(0)
        self.multi_cell(
            0, Pages.textHeight, text,
            Pages.textBorder, align, False)

    def _writep(self, text, align='L', margin=Pages.leftMarginSize):
        self._write(text, align, margin)
        self.ln()

    def transition(self, text):
        self._writep(text.upper(), 'R', Pages.transitionLeftMargin)
        self.ln()

    def action(self, text):
        self._writep(text)

    def _character(self, name, extension):
        char = name.upper()
        if (extension != ''):
            char += ' (' + extension.upper() + ')'
        self._write(char, 'L', Pages.characterLeftMargin)

    def _parenthetical(self, text):
        par = '(' + text + ')'
        self.set_right_margin(Pages.parentheticalRightMargin)
        self._write(par, 'L', Pages.parentheticalLeftMargin)
        self.set_right_margin(Pages.rightMarginSize)

    def _sameCharacter(self, name):
        previous = self._lastCharacter
        current = (name, self._sceneCount)
        if (previous == current):
            return True
        self._lastCharacter = current
        return False

    def dialogue(self, name, text, extension='', parenthetical=''):
        if (self._sameCharacter(name)):
            self._character(name + ' (CONT\'D)', extension)
        else:
            self._character(name, extension)
        if (parenthetical != ''):
            self._parenthetical(parenthetical)
        self.set_right_margin(Pages.dialogueRight)
        self._writep(text, 'L', Pages.dialogueLeftMargin)
        self.set_right_margin(Pages.rightMarginSize)
        # if (self._sameCharacter(name)):
        #     self._character(name + ' (CONT\'D)', extension)
        # else:

    def save(self, name):
        self._fadeOut()
        self.output(name, 'F')
