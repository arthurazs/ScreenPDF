from __future__ import absolute_import
from .screenpdf import ScreenPDF
import logging


class Converter(object):

    def __init__(self):
        self._logger = logging.getLogger('screenpdf.convert')
        self._functions = {
            'chars': self._chars,       # try to use screenpdf here
            'characters': self._chars,
            'authors': self._auths,
            'informations': self._infos,
            'infos': self._infos,
            'title': self._title,
            'int': self._int,
            'ext': self._ext,
            'action': self._action,
            'act': self._action,
            'begin': self._begin,
            'dia': self._dialogue,
            'dialogue': self._dialogue
        }
        self._charList = []
        self._firstList = []
        self._authList = []
        self._infoList = []
        self._titleString = ''
        self._pdf = None

    def get_all(self):
        return self._functions

    # TODO remove_bracket() for the replaces
    def _build_list(self, text, var):
        for item in list(
                filter(None, text.replace('[', '').split(']'))):
            var.append(item)
            if (var == self._charList):
                self._firstList.append(True)

    def _chars(self, text):
        self._build_list(text, self._charList)

    def _auths(self, text):
        self._build_list(text, self._authList)

    def _infos(self, text):
        self._build_list(text, self._infoList)

    def _title(self, text):
        self._titleString = text.replace(']', '').replace('[', '')

    def _int(self, text):
        self._pdf.scene('int. ' + text)

    def _ext(self, text):
        self._pdf.scene('ext. ' + text)

    def _action(self, text):
        for i in range(len(self._charList)):
            person = '{' + str(i) + '}'
            name = self._charList[i]
            if self._firstList[i]:
                if person in text:
                    name = name.upper()
                    self._firstList[i] = False
            text = text.replace(person, name)
        self._pdf.action(text)
        # TODO add underline

    def _createPdf(self):
        self._pdf = ScreenPDF(
            self._titleString, self._authList, self._infoList)

    def _savePdf(self):
        self._pdf.save(self._titleString + '.pdf')

    def generatePdf(self):
        self._createPdf()
        self._savePdf()

    def _begin(self, text):
        self._createPdf()

    def _dialogue(self, text):
        # FIXME
        # What if " {1} hey are you going (there)? "
        speaker, line = text.split('}', 1)
        speaker = int(speaker.replace('{', ''))
        extension = ''
        parenthetical = ''
        if ']' in line:
            extension, line = line.split(']', 1)
            extension = extension.replace('[', '')
        if ')' in line:
            parenthetical, line = line.split(')', 1)
            parenthetical = parenthetical.replace('(', '')
        char = self._charList[int(speaker)].strip()
        line = line.strip()
        extension = extension.strip()
        parenthetical = parenthetical.strip()
        for num, name in enumerate(self._charList):
            person = '{' + str(num) + '}'
            line = line.replace(person, name)
        self._pdf.dialogue(
            char, line,
            extension, parenthetical)
        self._logger.info('Dialogue still in beta')
