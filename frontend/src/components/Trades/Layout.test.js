import React from 'react';
import { shallow } from 'enzyme';

import Layout, { Box } from './Layout';

describe('Layout components', () => {
  it('should render <Box/> as expected', () => {
    const wrapper = shallow(<Box>Test</Box>);

    expect(wrapper).toMatchSnapshot();
  });

  it('should render <Layout /> as expected', () => {
    const wrapper = shallow(
      <Layout
        tradesList={<div>List</div>}
        newTrade={<div>New</div>}
      />
    );

    expect(wrapper).toMatchSnapshot();
  });
});
