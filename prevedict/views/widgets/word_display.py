from PySide6.QtGui import QFont, QTextBlockFormat, QTextCharFormat, QTextCursor
from PySide6.QtWidgets import QTextEdit

from prevedict.conf import UIText
from prevedict.conf.settings import Settings
from prevedict.model.dictionary import WordTranslation
from prevedict.model.thesaurus import WordDescription


class WordDisplay(QTextEdit):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setReadOnly(True)
        self.word = None
        self.writer = DescriptionWriter(self.textCursor())

    def configure(self, settings: Settings) -> None:
        self.setFont(settings.fonts.general.qfont)
        self.writer.configure(settings)

        if self.word:
            self.display(self.word)

    def display(self, details: WordDescription | WordTranslation) -> None:
        match details:
            case WordDescription():
                self.display_description(details)
            case WordTranslation():
                self.display_translation(details)
            case _:
                raise ValueError(
                    "Only WordDescription and WordTranslation types allowed"
                )
        self.word = details

    def display_loading(self) -> None:
        self.setText(UIText.LOADING)

    def display_not_found(self) -> None:
        self.setText(UIText.NOT_FOUND)

    def display_description(self, details: WordDescription) -> None:
        self.clear()

        self.writer.set_heading(details.word, details.transcription)

        for meaning in details.meanings:
            self.writer.write(
                f"({meaning.partOfSpeech.lower()})\n", bold=True, italic=True
            )

            definitions = []
            for i, definition in enumerate(meaning.definitions, 1):
                definitions.append(f"{i}. {definition.definition}")
            def_str = "\n".join(definitions)

            self.writer.write(def_str)

            if meaning.synonyms:
                self.writer.write("\n┃Synonyms: ", bold=True)
                synonyms = ", ".join(meaning.synonyms)
                self.writer.write(synonyms, italic=True, underline=True)

            self.writer.write("\n\n")

        self.writer.delete_from_back(2)

    def display_translation(self, details: WordTranslation) -> None:
        self.clear()

        self.writer.set_heading(details.word, details.transcription)
        self.writer.write(details.translation)
        self.writer.delete_from_back(1)


class DescriptionWriter:
    def __init__(self, cursor: QTextCursor) -> None:
        self.cursor = cursor

    def configure(self, settings: Settings) -> None:
        fonts = settings.fonts

        regular_font = fonts.general.qfont

        bold_font = QFont(regular_font)
        bold_font.setBold(True)

        italic_font = QFont(regular_font)
        italic_font.setItalic(True)

        self.word_fmt = QTextCharFormat()
        self.word_fmt.setFont(fonts.heading.qfont)
        self.word_fmt.setFontCapitalization(QFont.AllUppercase)

        self.trscpt_fmt = QTextCharFormat()
        self.trscpt_fmt.setFont(fonts.transcription.qfont)

        self.bold_fmt = QTextCharFormat()
        self.bold_fmt.setFont(bold_font)

        self.italic_fmt = QTextCharFormat()
        self.italic_fmt.setFont(italic_font)

        self.regular_fmt = QTextCharFormat()
        self.regular_fmt.setFont(regular_font)

        self.fmt = QTextCharFormat()
        self.fmt.setFont(regular_font)

    def set_heading(self, word: str, transcription: str) -> None:
        self.cursor.insertText(word, self.word_fmt)
        if transcription:
            self.cursor.insertText("\n" + transcription, self.trscpt_fmt)
        self.__insert_hr()

    def __insert_hr(self) -> None:
        self.cursor.insertHtml("<hr>")
        self.cursor.insertBlock()
        fmt = self.cursor.blockFormat()
        fmt.clearProperty(QTextBlockFormat.BlockTrailingHorizontalRulerWidth)
        self.cursor.setBlockFormat(fmt)

    def write(
        self,
        text: str,
        *,
        bold: bool = False,
        italic: bool = False,
        underline: bool = False,
    ) -> None:
        self.__set_style(bold, italic, underline)
        self.cursor.insertText(text, self.fmt)

    def __set_style(self, bold: bool, italic: bool, underline: bool) -> QTextCharFormat:
        if bold:
            self.fmt.setFontWeight(QFont.Bold)
        else:
            self.fmt.setFontWeight(QFont.Normal)

        self.fmt.setFontItalic(italic)
        self.fmt.setFontUnderline(underline)

        return self.fmt

    def delete_from_back(self, char_count: int) -> None:
        self.cursor.movePosition(QTextCursor.End)
        self.cursor.movePosition(QTextCursor.Left, QTextCursor.KeepAnchor, char_count)
        self.cursor.removeSelectedText()
