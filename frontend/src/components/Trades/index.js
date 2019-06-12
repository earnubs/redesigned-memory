import React from 'react';

import Layout from './Layout';
import List from './List';
import New from './New';


class App extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      trades: [],
    };

    this.addTrade = this.addTrade.bind(this);
  }

  addTrade(trade) {
    this.setState({
      trades: [trade].concat(this.state.trades),
    });
  }

  componentDidMount() {
    this.fetchTrades();
  }

  async fetchTrades() {
    try {
      const response = await fetch('/api/trades/');
      if (response.ok) {
        const trades = await response.json();

        this.setState({ trades });
      }
    } catch(err) {
      // XXX ErrorBoundary
      console.log(err);
    }
  }

  render() {
    const tradesList = (
      <List trades={this.state.trades} />
    );
    const newTrade = (
      <New addTrade={this.addTrade} />
    );

    return (
      <Layout
        tradesList={tradesList}
        newTrade={newTrade}
      />
    );
  }
}

export default App;
