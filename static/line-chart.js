const {LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend} = Recharts;

const SimpleLineChart = React.createClass({
    getInitialState: function() {
        return {data: []};
    },
    componentDidMount: function() {
        $.ajax({
          url:  this.props.url,
          dataType: 'json',
          cache: false,
          success: function(data) {
            console.log("got some data")
            console.log(this)
            this.setState({data: data});
          }.bind(this),
          error: function(xhr, status, err) {
            console.error(this.props.url, status, err.toString());
          }.bind(this)
        });
    },
    render () {
    return (
        <LineChart width={800} height={400} data={this.state.data}
            margin={{top: 5, right: 30, left: 20, bottom: 5}}>
       <XAxis dataKey="date"/>
       <YAxis/>
       <Tooltip/>
       <Legend />
       <Line type="monotone" dataKey="Uber" stroke="#5194EC" activeDot={{r: 5}}/>
       <Line type="monotone" dataKey="Seamless" stroke="#DA907A" activeDot={{r: 5}}/>
       <Line type="monotone" dataKey="Amazon" stroke="#60D394" activeDot={{r: 5}}/>
       <Line type="monotone" dataKey="FoodAndDrink" stroke="#FF5964" activeDot={{r: 5}}/>
      </LineChart>
    );
  }
})

ReactDOM.render(
  <SimpleLineChart url="/api/uber" />,
  document.getElementById('chartOne')
);