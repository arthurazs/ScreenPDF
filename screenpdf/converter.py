from __future__ import absolute_import
from .screenpdf import ScreenPDF
import logging
import os.path as path


class Converter:

    TRANSLATOR = {
        'authors': 'auths',
        'informations': 'infos',
        'act': 'action',
        'dia': 'dialogue',
    }

    def __init__(self):
        self._logger = logging.getLogger('screenpdf.convert')
        self._charList = []
        self._firstList = []
        self._authList = []
        self._infoList = []
        self._titleString = ''
        self._pdf = None
        self._isDialogueBeingUsed = False  # Flag to print log only once

    # TODO remove_bracket() for the replaces
    def _build_list(self, text, var):
        for item in list(
                filter(None, text.replace('[', '').split(']'))):
            var.append(item)
            if (var == self._charList):
                self._firstList.append(True)

    def chars(self, text):
        self._build_list(text, self._charList)

    def auths(self, text):
        self._build_list(text, self._authList)

    def infos(self, text):
        self._build_list(text, self._infoList)

    def title(self, text):
        self._titleString = text.replace(']', '').replace('[', '')

    def int(self, text):
        self._pdf.scene('int. ' + text)

    def ext(self, text):
        self._pdf.scene('ext. ' + text)

    def action(self, text):
        for i in range(len(self._charList)):
            person = '{' + str(i) + '}'
            name = self._charList[i]
            if self._firstList[i]:
                if person in text:
                    text = text.replace(person, name.upper(), 1)
                    self._firstList[i] = False
            text = text.replace(person, name)
        self._pdf.action(text)
        # TODO add underline

    def _createPdf(self):
        self._pdf = ScreenPDF(
            self._titleString, self._authList, self._infoList)

    def savePdf(self):
        filename = self._titleString + '.pdf'
        self._pdf.save(filename)
        self._logger.info('PDF saved at ' + path.abspath(filename))

    def generatePdf(self):
        self._createPdf()
        self._savePdf()

    def begin(self, text):
        self._createPdf()

    def dialogue(self, text):
        # FIXME
        # What if " {1} hey are you going (there)? "
        speaker, line = text.split('}', 1)
        speaker = int(speaker.replace('{', ''))
        extension = ''
        if ']' in line:
            extension, line = line.split(']', 1)
            extension = extension.replace('[', '')
        char = self._charList[int(speaker)].strip()
        line = line.strip()
        extension = extension.strip()
        for num, name in enumerate(self._charList):
            person = '{' + str(num) + '}'
            line = line.replace(person, name)
        self._pdf.dialogue(
            char, line,
            extension)

        if not self._isDialogueBeingUsed:
            self._isDialogueBeingUsed = True
            self._logger.warn('Dialogue still in beta')
