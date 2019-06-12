import React from 'react';
import { shallow } from 'enzyme';

import CurrencySelector from './CurrencySelector';


describe('<CurrencySelector />', () => {
  it('should render as expected', () => {
    const wrapper = shallow(<CurrencySelector handleCurrencyChange={() => {}} />);
    expect(wrapper).toMatchSnapshot();
  });

  it('should call passed onChange handler', () => {
    const spy = jest.fn();
    const wrapper = shallow(<CurrencySelector handleCurrencyChange={spy} />);
    wrapper.prop('onChange')();
    expect(spy).toHaveBeenCalledTimes(1);
  });
});
