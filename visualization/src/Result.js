import React, { Component } from 'react';
import { RadioGroup, Radio } from 'react-radio-group';
import fetch from 'node-fetch';
import lodash from 'lodash';
import 'keen-dataviz/dist/keen-dataviz.js';
import 'keen-dataviz/dist/keen-dataviz.css';

// Import React Table
import ReactTable from "react-table";
import "react-table/react-table.css";

import transpose from './transpose'

const Keen = window.Keen;

class Result extends Component {
  state = {
    type: 'bar'
  }

  constructor(props) {
    super(props)
    this.renderGraph = lodash.throttle(this.renderGraph, 1000);
  }

  shouldComponentUpdate(nextProps, nextState) {
    if(this.state.type != nextState.type && this.props.query != nextProps.query) {
      return true;
    }
    if(this.state.data != nextProps.data) {
      return true;
    }
    return false;
  }

  componentDidUpdate(nextProps, nextState) {
    this.renderGraph();
  }

  renderGraph() {
    try {
      var chart = new Keen.Dataviz()
      .el('#dom-selector')
      .height(280)
      .title(this.props.query)
      .type(this.state.type)
      .prepare();
      
      // Fetch data from the API:
      //  Imaginary callback ...
      chart
        .data({
          result: this.props.data
        })
        .labels(this.props.labels.splice(1))
        .render();
      } catch(e) {
        return;
      }
  }

  handleRadio = (value) => {
    this.setState({
      type: value
    }, this.renderGraph)
  }

  parseData = () => {
    var parsedData = []
    for(var i = 0;i < this.props.data.length;i++) {
      let obj = {}
      for(var j = 0;j < this.props.data[i].length;j++) {
        obj[`${this.props.labels[j]}`] = this.props.data[i][j]        
      }
      parsedData.push(obj)
    }
    return parsedData
  }

  render() {
    return (
      <div className="App">
        <RadioGroup name="graph" selectedValue={this.state.type} onChange={this.handleRadio}>
          <Radio value="bar" />Bar Graph
          <Radio value="line" />Line Graph
        </RadioGroup>
        {this.props.data &&
          <div>
            {this.props.data.length > 1 ?
              <div id="dom-selector" />:
              <div>{JSON.stringify(this.props.data[0])}</div>
            }
            <ReactTable data={this.parseData()} columns={this.props.labels.map(i => ({Header:i, accessor: i}))}/>
          </div>
        }
      </div>
    );
  }
}

export default Result;
