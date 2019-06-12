import React from 'react';
import PropTypes from 'prop-types';
import Select from 'react-select';

const styles = {
  container: (provided, state) => ({
    ...provided,
    width: 155,
    zIndex: state.isFocused ? 10 : 'initial',
    color: '#556468',
  }),
  control: (provided, state) => ({
    ...provided,
    borderColor: state.isFocused ? '#00bef0' : '#84959a',
    boxShadow: state.isFocused ? '0 0 0 1px #00bef0' : 'none',
    borderTopRightRadius: 0,
    borderBottomRightRadius: 0,
  }),
  singleValue: provided => ({
    ...provided,
    color: '#556468',
  }),
  indicatorSeparator: () => ({
    display: 'none',
  }),
  menu: provided => ({
    ...provided,
    zIndex: 1000000,
  }),
  menuPortal: provided => ({
    ...provided,
    zIndex: 1000000,
  }),
  menuList: provided => ({
    ...provided,
    zIndex: 1000000,
  }),
};

export default class CurrencySelector extends React.Component {

  render() {
    const {
      options,
      isLoadingCurrencies,
      handleCurrencyChange,
    } = this.props;

    return (
      <Select
        styles={styles}
        placeholder={null}
        isSearchable
        isLoading={isLoadingCurrencies}
        options={options}
        onChange={handleCurrencyChange}
        maxMenuHeight={128}
      />
    );
  }
}

CurrencySelector.defaultProps = {
  options: [],
  isLoadingCurrencies: true,
};

CurrencySelector.propTypes = {
  options: PropTypes.arrayOf(
    PropTypes.shape({
      value: PropTypes.string,
      label: PropTypes.string,
    }),
  ),
  isLoadingCurrencies: PropTypes.bool,
  handleCurrencyChange: PropTypes.func.isRequired,
};
