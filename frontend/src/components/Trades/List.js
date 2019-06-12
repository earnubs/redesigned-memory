import React from 'react';
import PropTypes from 'prop-types';
import { Link } from 'react-router-dom';
import numeral from 'numeral';

import './List.css';

export const NUMBER_FORMAT = '0,0.00';

export function TableHead() {
  return (
    <thead>
      <tr className="eb-TradesList-head">
        <th>
            Sell CCY
        </th>
        <th>
            Sell amount
        </th>
        <th>
            Buy CCY
        </th>
        <th>
            Buy amount
        </th>
        <th>
            Rate
        </th>
        <th>
            Date booked
        </th>
      </tr>
    </thead>
  );
}

export function TableBody({ trades }) {
  return (
    <tbody>
      {
        trades.length ?
          trades.map(trade => (
            <tr key={trade.id} className="eb-TradesList-row">
              <td className="eb-TradesList--lighter">
                {trade.sell_currency}
              </td>
              <td>
                {numeral(trade.sell_amount).format(NUMBER_FORMAT)}
              </td>
              <td className="eb-TradesList--lighter">
                {trade.buy_currency}
              </td>
              <td>
                {numeral(trade.buy_amount).format(NUMBER_FORMAT)}
              </td>
              <td>
                {trade.rate}
              </td>
              <td>
                { trade.date_booked }
              </td>
            </tr>
          )) : null
      }
    </tbody>
  );
}

TableBody.defaultProps = {
  trades: [],
};

TableBody.propTypes = {
  trades: PropTypes.array,
};

export function List({ trades }) {
  return (
    <div>
      <h2>Booked Trades</h2>
      <Link to="/new">[plus icon] New Trade</Link>
      <table className="eb-Trades-List">
        <TableHead />
        <TableBody trades={ trades } />
      </table>
    </div>
  );
}

List.propTypes = {
  trades: PropTypes.array.isRequired,
};

export default List;
