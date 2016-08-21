/** @jsx React.DOM */
    var Input = React.createClass({
        updateLabel: function(event){
            this.setState({value: event.target.value});
        },
        getInitialState: function(){
            return {
                value: ''
            }
        },
        componentWillMount: function(){
            this.setState({value: this.state.value})
        },
        render: function(){
            return (
                <div className="update-label">
                      <input type="text" placeholder="Enter text" onChange={this.updateLabel}/>
                    <Label value={this.state.value}/>
                </div>
        )
    }
});

var Label = React.createClass({
    render: function(){
        return (
        <div class="my-label">
        <h2>{this.props.value}</h2>
        </div>
        )
    }
});

React.render(<Input/>, document.getElementById('mount-point'));