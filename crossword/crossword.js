var nrows = 32;
var ncols = 48;
var dirAcross = 0;
var dirDown = 1;
var direction = dirDown;

function setDirection(d) {
    direction = d;
    if (direction == 0) {
        document.getElementById("dirbutton").value = "Across";
    }
    else {
        document.getElementById("dirbutton").value = "Down";
    }
}

function changeDirection() {
    setDirection(direction ^ 1);
}

function error(s) {
    document.getElementById("debug").innerHTML = "ERROR: " + s;
}

function id2n(id) {
    if (id.slice(0,5) != "entry") {
	error("invalid id name");
	return 1;
    }
    return new Number(id.slice(5))
}

function n2id(n) {
    return "entry" + n.toString();
}

function getNextId(current, nsteps) {
    n = id2n(current);
    n += nsteps * ((1-direction)*1 + (direction)*ncols);
    if (n < 0) {
	n = 0;
    }
    if (n >= ncols * nrows) {
	n = ncols * nrows - 1;
    }
    return n2id(n);
}

function handler(node, event) {
    // todo: Does not handle tab, space or return well
    var x = document.getElementById(node.id);
    var code = event.which;
    var next, nsteps;

    x.value = x.value.slice(0,1);
    x.value = x.value.toUpperCase();

    switch (code) {
    case 8: // backspace
	x.value = '';
	setDirection(dirAcross);
	next = getNextId(node.id, -1);
	break;
    case 9: // tab
	setDirection(dirAcross);
	next = getNextId(node.id, 1);
	break;
    case 13: // enter
	changeDirection();
	next = node.id;
    case 37: // left
	setDirection(dirAcross);
	next = getNextId(node.id, -1);
	break;
    case 38: // up
	setDirection(dirDown);
	next = getNextId(node.id, -1);
	break;
    case 39: // right
	setDirection(dirAcross);
	next = getNextId(node.id, 1);
	break;
    case 40: // down
	setDirection(dirDown);
	next = getNextId(node.id, 1);
	break;
    default:
	next = getNextId(node.id, 1);
	break;
    }

    document.getElementById(next).focus();
    document.getElementById(next).setSelectionRange(0,0);
    document.getElementById("debug").innerHTML = event.which
}

function doExport() {
    var x = "";
    var i, j;
    for (i=0; i < nrows; i++) {
	for (j=0; j < ncols; j++) {
            var id = n2id(i*ncols + j);
            var z = document.getElementById(id).value;
            x += z + ",";
	}
    }
    document.getElementById("export").value = x;
}

function doImport() {
    var x = document.getElementById("import").value.split(",");
    var i, j;
    for (i=0; i < nrows*ncols; i++) {
        var id = "entry" + i;
	if (i < x.length) {
	    document.getElementById(id).value = x[i];
	}
	else {
            document.getElementById(id).value = '';
        }
    }
}

setDirection(dirAcross);

var grid = document.getElementById("grid");
var x = "", i, j;
for (i=0; i < nrows; i++) {
    for (j=0; j < ncols; j++) {
        var id = n2id(i*ncols + j);
        x = x + '<input type="text" class="gridbox" maxlength="2" size="1" id="' + id
	    + '" onkeyup="handler(this, event)"/>';
    }
    x = x + '<br/>';
}
grid.innerHTML = x;
