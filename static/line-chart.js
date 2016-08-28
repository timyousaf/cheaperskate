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
       <Line type="monotone" dataKey="uber" stroke="#5194EC" activeDot={{r: 5}}/>
       <Line type="monotone" dataKey="seamless" stroke="#DA907A" activeDot={{r: 5}}/>
       <Line type="monotone" dataKey="amazon" stroke="#60D394" activeDot={{r: 5}}/>
       <Line type="monotone" dataKey="foodanddrink" stroke="#FF5964" activeDot={{r: 5}}/>
      </LineChart>
    );
  }
})

var options = [
    { value: 'D', label: 'Day' },
    { value: 'W', label: 'Week' },
    { value: 'M', label: 'Month' }
];

function renderChart(url) {
  console.log("Rendering with URL " + url)
  ReactDOM.render(
  <SimpleLineChart url={url} />,
  document.getElementById('chartOne')
  );
}

function logChange(change) {
    var val = change.value
    console.log("Selected: " + val);
    renderChart("/data?bucket=" + val + "&days_ago=730")
}

ReactDOM.render(
  <Select
    name="form-field-name"
    value="one"
    options={options}
    onChange={logChange}
    />,
  document.getElementById('time-bucket-selector')
);

renderChart("/data?bucket=M&days_ago=730")
