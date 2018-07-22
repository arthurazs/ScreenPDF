from __future__ import absolute_import
from .screenpdf import ScreenPDF
import logging
import os.path as path
from re import compile as re_compile


class Converter:

    TRANSLATE = {
        'authors': 'auths',
        'informations': 'infos',
        'act': 'action',
        'dia': 'dialogue',
        'int': 'interior',
        'ext': 'exterior',
        'characters': 'chars'
    }

    def __init__(self):
        self._logger = logging.getLogger('screenpdf.convert')
        # TODO change charList and firstList to dict
        # e.g. {'{0}': {'name': 'arthur', 'first': True}, }
        self._charList = []
        self._firstList = []
        self._authList = []
        self._infoList = []
        self._titleString = ''
        self._pdf = None
        self._isDialogueBeingUsed = False  # Flag to print log only once
        self._re_findall_chars = re_compile(r'{\d+}').findall

    # TODO remove_bracket() for the replaces
    def _build_list(self, text, var):
        for item in text.replace('[', '').split(']')[:-1]:
            var.append(item)
            if var is self._charList:
                self._firstList.append(True)

    def chars(self, text):
        self._build_list(text, self._charList)

    def auths(self, text):
        self._build_list(text, self._authList)

    def infos(self, text):
        self._build_list(text, self._infoList)

    def title(self, text):
        self._titleString = text.replace(']', '').replace('[', '')

    def interior(self, text):
        self._pdf.scene('int. ' + text)

    def exterior(self, text):
        self._pdf.scene('ext. ' + text)

    def _replace_names(self, text, is_action=True):
        people = set(self._re_findall_chars(text))
        for person in people:
            index = int(person[1:-1])
            name = self._charList[index]
            if is_action and self._firstList[index]:
                text = text.replace(person, name.upper(), 1)
                self._firstList[index] = False
            text = text.replace(person, name)
        return text

    def action(self, text):
        self._pdf.action(self._replace_names(text))
        # TODO add underline

    def begin(self):
        self._pdf = ScreenPDF(
            self._titleString, self._authList, self._infoList)

    def savePdf(self):
        filename = self._titleString + '.pdf'
        self._pdf.save(filename)
        self._logger.info('PDF saved at ' + path.abspath(filename))

    def dialogue(self, text):
        # FIXME
        # What if " {1} hey are you going (there)? "
        speaker, line = text.split('}', 1)
        speaker = int(speaker.replace('{', ''))
        extension = ''
        if ']' in line:
            extension, line = line.split(']', 1)
            extension = extension.replace('[', '')
        char = self._charList[speaker]
        line = self._replace_names(line, False)
        self._pdf.dialogue(char, line, extension)

        if not self._isDialogueBeingUsed:
            self._isDialogueBeingUsed = True
            self._logger.warn('Dialogue still in beta')
