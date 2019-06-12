import React from 'react';
import PropTypes from 'prop-types';
import { Route } from 'react-router-dom';

import './Layout.css';

export function Box({ children, ...rest }) {
  return (
    <div className="eb-Layout-Box" { ...rest }>
      { children }
    </div>
  );
}

Box.propTypes = {
  children: PropTypes.node.isRequired,
};

function Layout({ tradesList, newTrade }) {
  return (
    <div className="eb-Layout">
      <Box style={{width: 860 }}>
        { tradesList}
      </Box>
      <Route exact path="/new" render={props => (
        <div className="eb-Layout-screen">
          <Box style={{
            width: 400,
            position: 'absolute',
            top: '50%',
            left: '50%',
            transform: 'translate(-50%, -50%)',
          }}>
            { React.cloneElement(newTrade, props) }
          </Box>
        </div>
      )} />
    </div>
  );
}

Layout.defaultProps = {};

Layout.propTypes = {
  tradesList: PropTypes.element.isRequired,
  newTrade: PropTypes.element.isRequired,
};

export default Layout;
