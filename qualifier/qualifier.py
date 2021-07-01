from typing import Any, Dict, List, Optional


def make_table(rows: List[List[Any]], labels: Optional[List[Any]] = None, centered: bool = False) -> str:
    # sourcery skip: merge-nested-ifs
    """
    :param rows: 2D list containing objects that have a single-line representation (via `str`).
    All rows must be of the same length.
    :param labels: List containing the column labels. If present, the length must equal to that of each row.
    :param centered: If the items should be aligned to the center, else they are left aligned.
    :return: A table representing the rows passed in.
    """
    MAX_ROWS = len(rows)
    MAX_COLUMNS = len(rows[0])
    EXTRA_SPACES = 2
    COL_LENGTHS = [max(len(str(row[i])) for row in rows) for i in range(MAX_COLUMNS)]
    labels_length = list(map(len,map(str,labels))) if labels != None else [0]*MAX_COLUMNS # also labels count for cell's width
    COL_LENGTHS = [max(COL_LENGTHS[i],labels_length[i]) for i in range(MAX_COLUMNS)]

    border = {
        "h": '─',
        "v": '│',
        "tl": '┌', "tc": '┬', "tr": '┐',
        "ml": '├', "mc": '┼', "mr": '┤',
        "bl": '└', "bc": '┴', "br": '┘',
    }

    # Create the first line (the upper border)
    _table = firstLine(COL_LENGTHS, border, EXTRA_SPACES) + "\n"
    # If there are labels, then create the header of the table
    if labels != None:
        if len(labels) > 0:
            _table += createHeaderLines(labels, COL_LENGTHS, border, centered, EXTRA_SPACES)
    # Create the parts of the table about the words
    _table += createWordsLines(rows, COL_LENGTHS, border, centered, EXTRA_SPACES)
    # Create the last line of the table (the lower border)
    _table += lastLine(COL_LENGTHS, border, EXTRA_SPACES)
    return _table


######################################
######## Draw Table Line by Line
######################################
def createHeaderLines(labels: List[str], col_lengths: List[int], border: Dict[str, str], centered: bool, extra_spaces: int = 2) -> str:
    """ Creates the table header as a multiline string.
    Args:
        labels (List[str]): The list of the labels (column names) of the table.
        col_lengths (List[int]): The char length of each comlumn as a list of int.
        border (Dict[str, str]): The border dictionary.
        centered (bool): If the words are centered in their cells.
        extra_spaces (int, optional): The extra length added to each column's length. Defaults to 2.
    Returns:
        str: The table header as a multiline string
    """
    words = list(map(str, labels))
    _lines = wordsLine(col_lengths, border, words, centered, extra_spaces) + "\n"
    _lines += headerBotLine(col_lengths, border, extra_spaces) + "\n"
    return _lines

def createWordsLines(wordsTable: List, col_lengths: List[int], border: Dict[str, str], centered: bool, extra_spaces: int = 2) -> str:
    """ Creates the part of table with the words as a multiline string.
    Args:
        wordsTable (List):  The list of the words of the whole table.
        col_lengths (List[int]): The char length of each comlumn as a list of int.
        border (Dict[str, str]): The border dictionary.
        centered (bool): If the words are centered in their cells.
        extra_spaces (int, optional): The extra length added to each column's length. Defaults to 2.
    Returns:
        str: The part of table with the words as a multiline string.
    """
    _lines = ""
    for row in wordsTable:
        words = list(map(str, row))
        _lines += wordsLine(col_lengths, border, words, centered, extra_spaces)
        _lines += "\n"
    return _lines

def firstLine(col_lengths: List[int], border: Dict[str, str], extra_spaces: int = 2) -> str:
    """ Create the first line of the table (the upper border)
    Args:
        col_lengths (List[int]): the char length of each comlumn as a list of int.
        border (Dict[str, str]): the border dictionary.
        extra_spaces (int, optional): The extra length added to each column's length. Defaults to 2.
    Returns:
        str: The first line of the table (the upper border).
    """
    # sourcery skip: inline-immediately-returned-variable, simplify-len-comparison
    if len(col_lengths) < 1:
        return ""
    _line = border["tl"]
    for col_length in col_lengths:
        _line += border["h"] * (col_length + extra_spaces)
        _line += border["tc"]
    # now replace the right corner with the appropriate one
    _line = _line[:-1] + border["tr"]
    return _line


def headerBotLine(col_lengths: List[int], border: Dict[str, str], extra_spaces: int = 2) -> str:
    """ Create the line just after the table header (the lower border of the table header)
    Args:
        col_lengths (List[int]): The char length of each comlumn as a list of int.
        border (Dict[str, str]): The border dictionary.
        extra_spaces (int, optional): The extra length added to each column's length. Defaults to 2.
    Returns:
        str: The line just after the table header (the lower border of the table header).
    """
    _line = firstLine(col_lengths, border, extra_spaces) # it is almost the same as first line
    _line = _line.replace(border["tl"], border["ml"])    # with just some replacements
    _line = _line.replace(border["tc"], border["mc"])
    _line = _line.replace(border["tr"], border["mr"])
    return _line


def wordsLine(col_lengths: List[int], border: Dict[str, str], words: List[str], centered: bool, extra_spaces: int = 2) -> str:
    """ Create a line with padded words separated by given borders.
    Args:
        col_lengths (List[int]): The char length of each comlumn as a list of int.
        border (Dict[str, str]): The border dictionary.
        words (List[str]): The list of the word for this line.
        centered (bool): If the words are centered in their cells.
        extra_spaces (int, optional): The extra length added to each column's length. Defaults to 2.
    Returns:
        str: A line with padded words separated by given borders.
    """
    # sourcery skip: simplify-len-comparison
    if len(col_lengths) < 1:
        return ""
    _line = border["v"]
    for i, col_length in enumerate(col_lengths):
        word = words[i]
        _line += paddedWord(word, col_length, centered, extra_spaces)
        _line += border["v"]
    return _line


def lastLine(col_lengths: List[int], border: Dict[str, str], extra_spaces: int = 2) -> str:
    """ Returns the last line of the table. It is just the lower border of the table.
    Args:
        col_lengths (List[int]): The char length of each comlumn as a list of int.
        border (Dict[str, str]): The border dictionary.
        extra_spaces (int, optional): The extra length added to each column's length. Defaults to 2.
    Returns:
        str: The last line of the table (just the lower border).
    """
    _line = firstLine(col_lengths, border, extra_spaces) # it is almost the same as first line
    _line = _line.replace(border["tl"], border["bl"])    # with just some replacements
    _line = _line.replace(border["tc"], border["bc"])
    _line = _line.replace(border["tr"], border["br"])
    return _line


def paddedWord(word: str, max_length: int, centered: bool = False, extra_spaces:int = 2) -> str:
    """ Just adds spaces around the given word.
    Args:
        word (str): Word to add padding.
        max_length (int): Essentially the legth of the largest word.
        centered (bool): If the word should be centered within it's cell.
        extra_spaces (int): It requires at least one space on either side for the wider item.
    Returns:
        str: Word with added padding.
    """
    total_length = max_length + extra_spaces
    if centered:
        return word.center(total_length, " ")
    
    _word = word.rjust(min(int(extra_spaces/2)+len(word), total_length), " ")
    return _word.ljust(total_length, " ")
