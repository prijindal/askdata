import React, { Component } from 'react';
import { RadioGroup, Radio } from 'react-radio-group';
import fetch from 'node-fetch';
import 'keen-dataviz/dist/keen-dataviz.js';
import 'keen-dataviz/dist/keen-dataviz.css';
import './App.css';

const Keen = window.Keen;

class App extends Component {
  componentDidMount() {
    this.fetchData()
  }

  state = {
    data: null,
    query: 'Literacy rate of females in Punjab vs Tamil Nadu',
    type: 'bar'
  }

  fetchData = async () => {
    let sqlbody = await fetch('http://localhost:3000/sql.txt');
    sqlbody = await sqlbody.text();
    let body = {SQL: sqlbody}

    
    let resp = await fetch('http://localhost:5000', {
      method: 'POST',
      headers: {
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(body)
    })
    resp = await resp.json()
    this.setState({
      data: resp.data,
      labels: resp.field_names
    }, this.renderGraph)
  }

  renderGraph() {
    var chart = new Keen.Dataviz()
    .el('#dom-selector')
    .colors(['red', 'orange', 'green'])    
    .height(280)
    .title(this.state.query)
    .type(this.state.type)
    .prepare();
    
    // Fetch data from the API:
    //  Imaginary callback ...
    chart
      .data({
        result: this.state.data
      })
      .labels(this.state.labels.splice(1))
      .render();
  }

  handleRadio = (value) => {
    this.setState({
      type: value
    }, this.renderGraph)
  }

  render() {
    return (
      <div className="App">
        <RadioGroup name="graph" selectedValue={this.state.type} onChange={this.handleRadio}>
          <Radio value="bar" />Bar Graph
          <Radio value="line" />Line Graph
        </RadioGroup>
        <div id="dom-selector" />
      </div>
    );
  }
}

export default App;
