var ArrayEditor = React.createClass({displayName: "ArrayEditor",

  mixins: [ReactForms.RepeatingFieldsetMixin],

  onFocus: function(idx, e) {
    var value = this.value();
    if (value.value.length - 1 === idx) {
      this.onValueUpdate(value.add());
    }
  },

  onRemoveItem: function(idx) {
    var value = this.value();
    if (idx === 0 && value.value.length === 1) {
      this.onValueUpdate(value.updateValue([null]));
    } else {
      this.onValueUpdate(value.remove(idx));
    }
  },

  decorate: function(item) {
    item = React.addons.cloneWithProps(
      item,
      {onFocus: this.onFocus.bind(null, item.props.name)}
    )
    return (
      React.createElement("div", {key: item.props.name, className: "rf-repeating-fieldset-item"}, 
        item, 
        React.createElement("button", {
          onClick: this.onRemoveItem.bind(null, item.props.name), 
          tabIndex: "-1", 
          type: "button", 
          className: "rf-repeating-fieldset-remove"}, "×"
        )
      )
    )
  },

  render: function() {
    var fields = this.renderFields().map(this.decorate)
    return this.transferPropsTo(React.createElement("div", {className: "ArrayEditor"}, fields))
  }

})

var Values = (
  React.createElement(List, {component: ArrayEditor}, 
    React.createElement(Property, null)
  )
)

React.renderComponent(
  React.createElement(Form, {schema: Values, value: ['focus on me!']}),
  document.getElementById('example')
)
