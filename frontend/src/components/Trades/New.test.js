import React from 'react';
import { shallow } from 'enzyme';
import 'node-fetch';
import fetchMock from 'fetch-mock';

import New from './New';

const currencies = [{
  value: 'GBP',
  label: 'GBP - Pound Sterling',
}, {
  value: 'XXX',
  label: 'XXX - LABEL',
}];

describe('<App />', () => {
  it('should fetch list of trades', () => {
    fetchMock.get('/api/currencies/', { currencies });

    shallow(<New addTrade={() => {}} />);
    expect(fetchMock.called()).toBe(true);
  });
});
