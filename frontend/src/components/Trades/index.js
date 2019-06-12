import React from 'react';
import format from 'date-fns/format';
import parseISO from 'date-fns/parseISO';
import compareAsc from 'date-fns/compareAsc';

import Layout from './Layout';
import List from './List';
import New from './New';

const DATE_FORMAT = 'dd/MM/yyyy hh:mm';

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

  async componentDidMount() {
    try {
      const response = await fetch('/api/trades/');
      if (response.ok) {
        const trades = await response.json();

        const sortedTrades = trades.map(trade => {
          trade.date_booked = format(parseISO(trade.date_booked), DATE_FORMAT);
          return trade;
        }).sort(() => compareAsc);

        this.setState({ trades: sortedTrades });
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
