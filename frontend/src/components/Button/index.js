import React from 'react';
import PropTypes from 'prop-types';
import classNames from 'classnames';

import './Button.css';

function Button({ children, mod, ...rest }) {
  const cx = classNames('eb-Button', {
    [`eb-Button--${mod}`]: mod,
  });

  return (
    <div className={cx} {...rest}>
      { children }
    </div>
  );
}

Button.defaultProps = {
  mod: undefined,
};

Button.propTypes = {
  mod: PropTypes.string,
  children: PropTypes.node.isRequired,
};

export default Button;
