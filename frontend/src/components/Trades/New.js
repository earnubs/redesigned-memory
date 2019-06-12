import React, { Component } from 'react';
import PropTypes from 'prop-types';
import numeral from 'numeral';

import CurrencySelector from './CurrencySelector';
import './New.css';

import { NUMBER_FORMAT } from './List';


class New extends Component {

  constructor(props) {
    super(props);

    this.state = {
      sellCurrency: null,
      buyCurrency: null,
      rate: null,
      amount: '1.00',
      options: [],
      isLoadingCurrencies: true,
    };

    this.handleBuyCurrencyChange = this.handleBuyCurrencyChange.bind(this);
    this.handleSellCurrencyChange = this.handleSellCurrencyChange.bind(this);
    this.handleAmountChange = this.handleAmountChange.bind(this);

    this.handleCreate = this.handleCreate.bind(this);
    this.handleCancel = this.handleCancel.bind(this);
  }

  componentDidMount() {
    this.fetchCurrencies();
  }

  async fetchCurrencies() {
    try {
      const response = await fetch('/api/currencies/');
      if (response.ok) {
        const { currencies } = await response.json();

        const commonOptions = [];
        const options = currencies.reduce((acc, currency) => {
          // XXX mock up doesn't appear to use label which is also returned, instead
          // the mock up is reusing the value
          const value = currency[0]; // FIXME array destructuring assignment in jest

          if (['USD', 'EUR', 'GBP'].indexOf(value) !== -1) {
            commonOptions.push({ value, label: value });
          } else {
            acc.push({ value, label: value });
          }


          return acc;
        }, []);

        this.setState({
          options: commonOptions.concat(options),
          isLoadingCurrencies: false,
        });

      } else {
        // TODO handle response not ok
      }
    } catch(err) {
      console.log(err);
    }
  }

  async fetchRates(buy, sell) {
    if (buy && sell) {
      try {
        const response = await fetch(`/api/rates/${buy}/${sell}`);
        if (response.ok) {
          const { rate } = await response.json();
          this.setState({
            rate,
          });
        } else {
          // TODO handle response not ok
          const error = await response.json();
          console.log(error);
        }
      } catch(err) {
        console.log(err);
      }
    }
  }

  handleSellCurrencyChange({ value }) {
    this.setState({ sellCurrency: value });
    this.fetchRates(this.state.buyCurrency, value);
  }

  handleBuyCurrencyChange({ value }) {
    this.setState({ buyCurrency: value });
    this.fetchRates(value, this.state.sellCurrency);
  }

  handleAmountChange(e) {
    this.setState({ amount: numeral(e.target.value, NUMBER_FORMAT).value() });
  }

  async handleCreate() {
    const { addTrade, history } = this.props;
    const { buyCurrency, sellCurrency, amount } = this.state;

    try {
      const response = await fetch('/api/trades/', {
        method: 'POST',
        body: JSON.stringify({
          sell_currency: sellCurrency,
          sell_amount: amount,
          buy_currency: buyCurrency,
        }),
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        const trade = await response.json();
        addTrade(trade);
        history.goBack();
      } else {
        // XXX handle response not ok
      }

    } catch(err) {
      alert(err);
    }
  }

  handleCancel() {
    const { history } = this.props;
    history.goBack();
  }

  render() {
    const {
      buyCurrency,
      sellCurrency,
      amount,
      rate,
      options,
      isLoadingCurrencies,
    } = this.state;

    const tradeAmount = numeral(numeral(amount).value() * rate).format(NUMBER_FORMAT);

    return (
      <div className="eb-Trades-New">
        <h2>New Trade</h2>
        <label>Sell Amount</label>
        <div className="eb-Select-currency">
          <CurrencySelector
            options={options}
            isLoadingCurrencies={isLoadingCurrencies}
            handleCurrencyChange={this.handleSellCurrencyChange}
          />
          <input
            type="number"
            className="eb-Trades-amount"
            onChange={this.handleAmountChange}
            defaultValue={'1.00'}
          />
        </div>
        <div>Rate</div>
        <div>
          { sellCurrency && buyCurrency && `${sellCurrency}${buyCurrency}`} { rate }
        </div>
        <label>Buy Amount</label>
        <div className="eb-Select-currency">
          <CurrencySelector
            options={options}
            isLoadingCurrencies={isLoadingCurrencies}
            handleCurrencyChange={this.handleBuyCurrencyChange}
          />
          <input className="eb-Trades-amount" disabled value={tradeAmount} />
        </div>
        <div onClick={this.handleCreate}>
          Create
        </div>
        <div onClick={this.handleCancel}>
          Cancel
        </div>
      </div>
    );
  }
}

New.defaultProps = {
  history: undefined,
};

New.propTypes = {
  addTrade: PropTypes.func.isRequired,
  history: PropTypes.object,
};

export default New;
