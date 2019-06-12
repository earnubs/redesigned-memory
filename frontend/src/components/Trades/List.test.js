import React from 'react';
import { shallow } from 'enzyme';

import List, { TableHead, TableBody } from './List';

import { trades } from './index.test.js';

describe('List components', () => {
  it('should render TableHead as expected', function() {
    const wrapper = shallow(<TableHead />);

    expect(wrapper).toMatchSnapshot();
  });

  it('should render TableBody as expected', function() {
    const wrapper = shallow(<TableBody trades={trades} />);

    expect(wrapper).toMatchSnapshot();
  });

  it('should render List as expected', function() {
    const wrapper = shallow(<List trades={trades} />);

    expect(wrapper).toMatchSnapshot();
  });
});
