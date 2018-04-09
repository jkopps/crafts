import sys
import formatter

def transpose(fname, nr, nc):
    with open(fname, 'r') as fh:
        raw = fh.read()
    chars = formatter.loadSolution(raw, nr, nc)
    trans = ['' for i in range(nr * nc)]
    for i in range(nr):
        for j in range(nc):
            x = i*nc + j
            y = j*nr + i
            trans[y] = chars[x]
    return trans

if __name__ == '__main__':
    fname = sys.argv[1]
    nr = int(sys.argv[2])
    nc = int(sys.argv[3])
    chars = transpose(fname, nr, nc)
    sys.stdout.write(reduce(lambda a, b: a + ',' + b, chars))
