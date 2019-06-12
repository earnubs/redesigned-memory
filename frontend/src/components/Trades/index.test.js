import React from 'react';
import { shallow } from 'enzyme';
import 'node-fetch';
import fetchMock from 'fetch-mock';

import App from './index.js';

export const trades = [{
  id:'TR3W659X2',
  sell_currency:'USD',
  sell_amount:'100.00',
  buy_currency:'GBP',
  buy_amount:'87.81',
  rate:'0.878085',
  date_booked:'2019-06-10T20:06:57.313042Z',
}];

describe('<App />', () => {
  it('should fetch list of trades', () => {
    fetchMock.get('/api/trades/', trades);

    shallow(<App />);
    expect(fetchMock.called()).toBe(true);
  });
});
