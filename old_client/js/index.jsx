var FormRow = React.createClass({
    render: function () {
        return (
                <Row>
                    {Object.keys(this.state.item).map(function (key) {
                        <Col>
                            {cloneComponent(
                                this.props.renderers(this.state.item[key]),
                                {
                                    onChange: function (event) {
                                        var val = event.target.value;
                                        var newItem = this.state.item;
                                        newItem[key] = val;
                                        var newValidation = this.state.validation;
                                        validation = this.props.fields[key].validator(val);
                                        this.setState({ item: newItem, validation: newValidation });
                                    },
                                    bsStyle: this.state.validation[key]
                                }
                            )}
                        </Col>
                    })}
                    <Button bsStyle="danger"  onClick={this.deleteItem}>✗</Button>
                    <Button bsStyle="success" onClick={this.postItem}  >✓</Button>
                </Row>
        );
    }
});

var TableView = React.createClass({
    mixins: [ReactFireMixin],
    componentWillMount: function () {
        this.bindAsArray(this.props.firebase.child(this.props.tableName), "items");
    },
    render: function () {
        return (
            <Table responsive>
                <thead>
                    <tr>
                        {this.props.headers.map(function (header) {
                            return <th>{header}</th>;
                        })}
                        <th>Delete</th>
                        <th>Update</th>
                    </tr>
                </thead>
                <tbody>
                    {this.state.items.map(function (item) {
                        return (
                            <tr>
                                <FormRow item={item} /* TODO */ />
                            </tr>
                        );
                    })}
                    <tr>
                        <NewRow /* TODO */ />
                    </tr>
                </tbody>
            </Table>
        );
    }
});

var App = React.createClass({
    componentWillMount: function () {
        this.tabs = [
            {name: 'Debates',      view: <TableView /* TODO */>},
            {name: 'Teams',        view: <TableView /* TODO */>},
            {name: 'Debaters',     view: <TableView /* TODO */>},
            {name: 'Judges',       view: <TableView /* TODO */>},
            {name: 'Teachers',     view: <TableView /* TODO */>},
            {name: 'Score Debate', view: <DebateScorer />      }
        ];
    },
    getInitialState: function () {
        return {firebase: new Firebase(FIREBASE_ROOT)};
    }
    render: function () {
        return (
            <TabbedArea defaultActiveKey={1} animation={false}>
                this.tabs.map(function (tab, index) {
                    return <TabPane eventKey={index} tab={tab.name}>{tab.view}</TabPane>;
                });
            </TabbedArea>
        );
    }
});

React.render(<App />, document.getElementById('body'))
