import re
import sys
from math import sqrt

class PuzzleGrid:
    def __init__(self, chars, nr, nc):
        self.chars = chars[:]
        self.nr = nr
        self.nc = nc
        # Assign count numbers
        self.numbers = {}
        self.counts = [None for i in range(nr*nc)]
        self.acrossClues = []
        self.downClues = []
        t = 0
        for i in range(nr):
            for j in range(nc):               
                if self.chars[i*nc + j] == '':
                    continue
                across = ''
                down = ''
                # starts an across clue?
                if ((j+1 < self.nc) and 
                    (self.chars[i*nc+j+1] != '') and 
                    (j == 0 or self.chars[i*nc+j-1] == '')):
                    for k in range(self.nc - j):
                        if self.chars[i*nc + j + k] == '':
                            break
                        across += self.chars[i*nc + j + k]
                    
                # starts a down clue?
                if ((i+1 < self.nr) and
                    (self.chars[(i+1)*nc + j] != '') and
                    (i == 0 or self.chars[(i-1)*nc + j] == '')):
                    for k in range(self.nr - i):
                        if self.chars[(i+k)*nc + j] == '':
                            break
                        down += self.chars[(i+k)*nc + j]
                if across != '' or down != '':
                    t += 1
                    self.counts[i*nc+j] = t
                    if across:
                        self.acrossClues.append((t, across))
                        self.numbers[across] = '%d across' % t
                    if down:
                        self.downClues.append((t, down))
                        self.numbers[down] = '%d down' % t

    def _validate(self, i, j):
        if not (0 <= i < self.nr and 0 <=j < self.nc):
            raise ValueError()
        
    def getChar(self, i, j):
        self._validate(i, j)
        return self.chars[i*nc+j]

    def getCount(self, i, j):
        self._validate(i, j)
        return self.counts(i, j)

    def get(self, i, j):
        self._validate(i, j)
        return (self.chars[i*self.nc+j], self.counts[i*self.nc+j])

    def getWord(self, i, j):
        self._validate(i, j)
        raise NotImplemented()

    def getClue(self, word):
        return self.numbers.get(word, None)

def loadSolution(raw, nr, nc):
    raw = raw.strip()
    chars = raw.split(',')
    assert len(chars) >= nr * nc, "Input dimensions incorrect!"
    if len(chars) < nr * nc:
        sys.stderr.write('Excess characters provided: ignoring')
    return chars[0:nr*nc]

def formatPuzzle(chars, nr, nc, clues):
    ret = ''
    grid  = PuzzleGrid(chars, nr, nc)
    ret += '\\begin{Puzzle}{%d}{%d}\n' % (nr, nc)
    for i in range(nr):
        for j in range(nc):
            c,t = grid.get(i, j)
            if t != None:
                n = '[%d] ' % t
            else:
                n = ''
            if c == '':
                c = '*'
            ret += '|%s %s ' % (n,c)
        ret += '|.\n'
    ret += '\\end{Puzzle}\n'

    ret += '\\newcommand{\\blank}{\\rule[-0.1pt]{15pt}{0.5pt}\\ }\n\n'
    ret += '\\begin{PuzzleClues}{\\textbf{Across}}\\\\\n'
    for (n, w) in grid.acrossClues:
        cl = clues[w]
        m = re.search('[#]([A-Z]+)', cl)
        if m != None:
            ref = m.groups()[0]
            try:
                assert grid.getClue(ref) != None, 'Referenced clue "%s" missing!' % ref
                cl = cl.replace('#' + ref, grid.getClue(ref))
            except:
                pass
        ret += '    \\Clue{%d}{%s}{%s}\\\\\n' % (n, w, cl)
    ret += '\\end{PuzzleClues}\n'

    ret += '\\begin{PuzzleClues}{\\textbf{Down}}\\\\\n'
    for (n, w) in grid.downClues:
        cl = clues[w]
        m = re.search('[#]([A-Z]+)', cl)
        if m != None:
            ref = m.groups()[0]
            cl = cl.replace('#' + ref, grid.getClue(ref))
        ret += '    \\Clue{%d}{%s}{%s}\\\\\n' % (n, w, cl)
    ret += '\\end{PuzzleClues}\n'

    # generate list of words
    if False:
        words = set()
        for (n, w) in grid.downClues + grid.acrossClues:
            words.add(w)
        for w in sorted(list(words)):
            sys.stderr.write('%s (%s)\n' % (w, w))
    
    return ret

def loadClues(fname):
    clues = {}
    with open(fname, 'r') as fh:
        for line in fh:
            line = line.strip()
            if line == '':
                continue
            i = line.index(' ')
            word = line[0:i]
            clue = line[i+1:]
            clues[word] = clue
    return clues

def cut(chars, nr, nc, cutRow=None, cutCol=None):
    ret = []
    rows = range(nr)
    cols = range(nc)
    if cutRow != None:
        rows.remove(cutRow)
    if cutCol != None:
        cols.remove(cutCol)
    for i in rows:
        for j in cols:
            ret.append(chars[i*nc + j])
    return ret

def isRowEmpty(chars, nr, nc, t):
    for j in range(nc):
        if chars[t*nc + j] != '':
            return False
    return True

def isColEmpty(chars, nr, nc, t):
    for i in range(nr):
        if chars[i*nc + t] != '':
            return False
    return True

def trim(chars, nr, nc):
    while True:
        if not isRowEmpty(chars, nr, nc, 0):
            break
        chars = cut(chars, nr, nc, cutRow=0)
        nr -= 1
    while True:
        if not isRowEmpty(chars, nr, nc, nr-1):
            break
        chars = cut(chars, nr, nc, cutRow=nr-1)
        nr -= 1
    while True:
        if not isColEmpty(chars, nr, nc, 0):
            break
        chars = cut(chars, nr, nc, cutCol=0)
        nc -= 1
    while True:
        if not isColEmpty(chars, nr, nc, nc-1):
            break
        chars = cut(chars, nr, nc, cutCol=nc-1)
        nc -= 1
    assert len(chars) == nr*nc
    return chars, nr, nc

def transpose(chars, nr, nc):
    trans = ['' for i in range(nr * nc)]
    for i in range(nr):
        for j in range(nc):
            x = i*nc + j
            y = j*nr + i
            trans[y] = chars[x]
    return trans, nc, nr

if __name__ == '__main__':
    clues = loadClues('clues.txt')

    fname = sys.argv[1]
    nr = int(sys.argv[2])
    nc = int(sys.argv[3])
    with open(fname, 'r') as fh:
        raw = fh.read()

    chars = loadSolution(raw, nr, nc)
    chars, nr, nc = trim(chars, nr, nc)
    chars, nr, nc = transpose(chars, nr, nc)

    formatted = formatPuzzle(chars, nr, nc, clues)
    sys.stdout.write(formatted)
