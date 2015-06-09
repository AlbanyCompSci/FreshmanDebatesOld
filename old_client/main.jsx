/** @jsx React.DOM */

/*
 * init
 *  - mounts   : Component -> FB -> ()
 *  - unmounts : Component -> FB -> ()
 * header
 *  - headers : List<String>
 * row
 *  - render : Component -> a -> List<HTML>
 *  - read   : List<String> -> Maybe<a>
 * new
 *  - default : a
 * bulk
 */

var FIREBASE_ROOT = 'https://ahs-freshman-renewal.firebaseio.com';

var Menu = React.createClass({
    render: function () {
        <Logo onClick={this.props.home.view)} />
        <ul>
            this.props.views.map(function (view) {
                return <li onClick=/* TODO */>{view.title}</li>;
            });
            <li onClick={this.props.fb.unauth}>Logout</li>
        </ul>
    },
});

var HomeView = React.createClass({
    render: function () {
        return <h1>Welcome to the Albany High School Freshman Renewal Debates!</h1>;
    },
});

/*
 * firebaseRef : Firebase
 * headers : [String]
 * render : a -> [Field]
 * read : HTML -> a
 * default : a
 */
var TableView = React.createClass({
    componentWillMount: function () {
        this.props.firebaseRef.on('value', function (snap) {
            this.setState({items: snap});
        });
    },
    put: function (event) {
        var item = this.props.read(event.target)
        var key = event.target.getAttribute('key');
        this.props.firebaseRef.child(key).set(item, function (resp) {
            if (resp) { console.log('PUT: ' + resp); }
            else { console.log('Failed to PUT: ' + resp); }
        });
    },
    post: function (event) {
        var item = this.props.read(event.target);
        this.props.firebaseRef.push(item, function (resp) {
            if (resp) { console.log('POST: ' + resp); }
            else { console.log('Failed to POST: ' + resp); }
        });
    },
    delete: function (event) {
        var key = event.target.getAttribute('key');
        this.props.firebaseRef.child(key).remove(function (resp) {
            if (resp) { console.log('DELETE: ' + resp); }
            else { console.log('Failed to DELETE: ' + resp); }
        });
    },
    render: function () {
        return (
            <table>
                <tr>
                    { this.props.headers.map(function (h) { return <th>h</th>; }) }
                    <th>Update/Create</th>
                    <th>Delete</th>
                </tr>
                { this.state.items.map(function (i) {
                    return (
                        <tr>
                            { this.props.render(i).map(function (f) { return <td>f</td>; }); }
                            <td onClick={this.put}>✓</td>
                            <td onClick={this.delete}>✗</td>
                        </tr>
                    );
                }); }
                <tr>
                    { this.props.render(this.props.default).map(function (f) { return <td>f</td>; }); }
                    <td onClick={this.post}>✓</td>
                    <td></td> // No need to delete a new entry
                </tr>
                /* TODO: Bulk Upload Button */
            </table>
        );
    },
});

var mkSelect = function (opts, selected) {
    return opts.map(function (opt) {
        if (opt === selected) {
var mkMultiSelect = function (opts, selected) {
    return opts.map(function (opt) {
        if (typeof selected === 'list' || typeof selected === 'array') {

var DebatesView  = function (firebaseRef) {
    var debatesHeaders = ['Name', 'Email'];
    var debatesRender = function (debate) {
        return [ <input type="text" defaultValue={debate.title}></input>
               , <input type="text" defaultValue={debate.location}></input>
               , <input type="datetime" defaultValue={debate.time}></input>
               , mkMultiSelect(this.state.judges, debate.judges)
               , mkSelect(this.state.teams, debate.affTeam)
               , mkSelect(this.state.teams, debate.negTeam)
               , mkMultiSelect(this.state.scores, debate.affScores)
               , mkMultiSelect(this.state.scores,)
               ];
    };
    var debatesRead = function (row) {
        /* TODO */
    };
    var debatesDefault = { title: null
                         , location: null
                         , time: null
                         , judges: []
                         , affTeam: null
                         , negTeam: null
                         , affScores: []
                         , negScores: []
                         };
    return (
        <TableView firebaseRef={firebaseRef.child('debates')}
                   headers={debatesHeaders}
                   render={debatesRender}
                   read={debatesRead}
                   default={debatesDefault}
        >
    );
};

var TeamsView    = function (firebaseRef) {
    var teamsHeaders = ['Teachers', 'Debaters'];
    var teamsRender = function (team) {
        /* TODO */
    };
    var teamsRead = function (row) {
        /* TODO */
    };
    var teamsDefaults = { teachers: []
                        , debaters: []
                        };
    return (
      <TableView firebaseRef={firebaseRef.child('teams')}
                 headers={teamsHeaders}
                 render={teamsRender}
                 read={teamsRead}
                 default={teamsDefault}
      >
    );
};


var usersHeaders = ['Name', 'Email'];
var usersRender = function (user) {
    /* TODO */
};
var usersRead = function (row) {
    /* TODO */
};
var usersDefault = { name: null
                   , email: null
                   };
var DebatersView = function (firebaseRef) {
    return (
      <TableView firebaseRef={firebaseRef.child('debaters')}
                 headers={usersHeaders}
                 render={usersRender}
                 read={usersRead}
                 default={usersDefault}
      >
    );
}

var JudgesView   = function (firebaseRef) {
    return (
      <TableView firebaseRef={firebaseRef.child('judges')}
                 headers={usersHeaders}
                 render={usersRender}
                 read={usersRead}
                 default={usersDefault}
      >
    );
}

var TeachersView = function (firebaseRef) {
    return (
      <TableView firebaseRef={firebaseRef.child('teachers')}
                 headers={usersHeaders}
                 render={usersRender}
                 read={usersRead}
                 default={usersDefault}
      >
    );
}

var ScoreDebateView = React.createClass({
    /* TODO */
});

var App = React.createClass({
    getInitialState: function () {
        return AppStore.getState();
    },
    _onChange: function () {
        this.setState(AppStore.getState());
    },
    componentWillMount: function () {
        AppStore.addChangeListener(this._onChange);
        this.fb = new Firebase(FIREBASE_ROOT);
        this.fb.onAuth(function (authData) {
            if (authData) {
                user = fb.once
                this.setState({ view : homeView, user : fb.once});
            } else {
                fb.authWithPopup("google", function(error, authData) {
                    if (error) {
                        alert("Authentication failed");
                        console.log("Authentication failed:", error);
                    } else {
                        console.log("Authentication succeeded for:", authData);
                    }
                }, {'scope': 'email'});
            }
        });
    },
    componentWillUnmount: function () {
        this.removeChangeListener(this._onChange);
        this.firebaseRef.off();
    },
    render: function () {
        var homeView = { title : 'Home', view : <HomeView fb={this.fb}> };
        var allViews = [ { title : 'Debates',      view : <ViewTable fb={this.fb} view={debatesView}>  }
                       , { title : 'Teams',        view : <ViewTable fb={this.fb} view={teamsView}>    }
                       , { title : 'Debaters',     view : <ViewTable fb={this.fb} view={debatersView}> }
                       , { title : 'Judges',       view : <ViewTable fb={this.fb} view={judgesView}>   }
                       , { title : 'Teachers',     view : <ViewTable fb={this.fb} view={teachersView}> }
                       , { title : 'Score Debate', view : <ScoreDebateView fb={this.fb}>               }
                       ];
        <div>
            <Menu home=homeView views=allViews />
            {this.state.view}
        </div>
    },
});
