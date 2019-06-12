import React from 'react';
import PropTypes from 'prop-types';

import numeral from 'numeral';

import './Num.css';

function Num({ children }) {
  return (
    <div className="eb-Num">
      { numeral(children).format('0,0[.]00') }
    </div>
  );
}

Num.defaultProps = {};

Num.propTypes = {
  children: PropTypes.oneOfType([
    PropTypes.number,
    PropTypes.string,
  ]),
};

export default Num;
