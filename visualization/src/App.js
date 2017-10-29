import React, { Component } from 'react';
import { RadioGroup, Radio } from 'react-radio-group';

import Result from './Result';
import './App.css';

class App extends Component {
  state = {
    query: null,
    submittedQuery: null,
    submitted: false,
    data: null,
    labels: null,
  }

  fetchData = async () => {
    let body = {query: this.state.query}
    
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
      submittedQuery: this.state.query,
      data: resp.data,
      labels: resp.field_names
    })
  }

  onSubmit = (e) => {
    e.preventDefault()
    this.setState({
      submitted: true,
    }, this.fetchData)
  }

  handleInput = (e) => {
    this.setState({
      query: e.target.value
    })
  }

  render() {
    return (
      <div className="App">
        <form onSubmit={this.onSubmit}>
          <input type="text" onChange={this.handleInput}/>
        </form>
        {this.state.submitted &&
          <Result query={this.state.submittedQuery} data={this.state.data} labels={this.state.labels}/>
        }
      </div>
    )
  }
}

export default App;
