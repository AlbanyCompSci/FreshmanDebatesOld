var api_root = '/api';

function Table(listing) {
    this.listing   = listing;
    this.table     = null;
    this.counter   = 0;
    this.render = function (container) {
        container.append('<table id="table"></table>');
        this.table = container.children('#table');
        this.table.empty();
        this.listing.header(this.newRow());
        data = this.listing.all();
        for (var r in data) {
            this.listing.render(r, this.newRow());
        }
        this.addCreator();
    };
    this.remove = function () {
        this.table.remove();
        delete this;
    }
    this.addCreator = function () {
        this.table.append('<tr id="new_row"></tr>');
        this.table.children('#new_row').click(function () {
            this.listing.default(this.newRow());
        });
    }
    this.newRow = function (row) {
        this.table.append('<tr id="' + String(this.counter) + '">' + row + '</tr>');
        row = this.table.children('#' + this.counter);
        this.counter++;
        return row;
    };
    this.empty = function () {
        this.table.empty();
        this.counter = 0;
    };
};

var getJson = function (url) {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open('GET', url, true);
    xmlHttp.send();
function Listing(type) {
    this.type    = type;
    this.all     = function () {
        return getJson(this.type.root);
    };
    this.header  = this.type.header;
    this.render  = function (item, row) {
        this.type.renderer(item, row);
        addPut(row);
        addDelete(row);
        addDelete(row)
    };
    this.default = function (row) {
        row.append(this.type.renderer(this.type.defaults));
        addPost(row);
    };
    var addPut = function (row) {
        row.append('<td class="put">PUT</td>');
        row.children('.put').click(function () {
            resp = this.type.putter(row);
            if (resp.err) {
                alert(resp.err);
            }
        });
    };
    var addPost = function (row) {
        row.append('<td class="post">POST</td>');
        row.children('.post').click(function () {
            resp = this.type.poster(row);
            if (resp.id) {
                removePost(row());
                addPut(row());
                addDelete(row());
            } else {
                alert(resp.err);
            }
        });
    };
    var addDelete = function (row) {
        row.append('<td class="delete">DELETE</td>');
        row.children('.delete').click(function () {
            resp = this.type.deletor(row);
            if (resp.err) {
                alert(resp.err);
            }
        });
    };
};

var options = function (list, def) {
    var mkOpt = function (o) {
        return '<option value="' + o + '">' + o + '</option>'
    };
    return '<td><select selected="' + def + '">' + _.map(list, mkOpt) + '</select></td>';
}

var objectList = function (list, defs) {};

var object = function (list, def) {};

var debates =
    { root     : api_root + '/debates'
    , defaults : { url       : null
                 , time      : null
                 , location  : null
                 , judges    : []
                 , affTeam   : null
                 , negTeam   : null
                 , affScores : []
                 , negScores : []
                 }
    , header   : function (row) {
        row.append('<td>Time</td>');
        row.append('<td>Location</td>');
        row.append('<td>Judges</td>');
        row.append('<td>Affirmative Team</td>');
        row.append('<td>Affirmative Scores</td>');
        row.append('<td>Negative Team</td>');
        row.append('<td>Negative Scores</td>');
    }
    , renderer : function (item, row) {
        row.append('<td><input type=datetime>' + item.time + '</input></td>');
        row.append(options(locOpts, item.location))
        row.append(options(judgeOpts, item.judges));
    }
    , putter   : function (row) {}
    , poster   : function (row) {}
    , deletor  : function (row) {}
    }

$(document).ready(function () {
    var switchTo = function (table) {
        $('#body').empty();
        table.render($('#body'));
    };
    var mkTable = function (type) {
        listing = new Listing(type);
        table = new Table(listing);
        switchTo(table);
    };
    $('#debates').click(mkTable(debates));
    // $('#teams').click(mkTable(teams));
    // $('#debaters').click(debaters);
    // $('#judges').click(mkTable(judges));
    // $('#teachers').click(mkTable(teachers));
});
