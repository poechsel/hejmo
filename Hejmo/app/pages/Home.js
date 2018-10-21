import React, { Component } from 'react';
import { StyleSheet, Text, View } from 'react-native';

import HomeGenius from './HomeGenius';
import HomeListing from './HomeListing';

export default class Home extends Component<{}> {
  state = {
    page: 0,
  };

  render() {
    const PAGE_COMPS = [
      <HomeGenius onPageChange={page => this.setState({page})}></HomeGenius>,
      <HomeListing category="4d4b7105d754a06374d81259" onPageChange={page => this.setState({page})}></HomeListing>,
      <HomeListing category="4d4b7105d754a06376d81259" onPageChange={page => this.setState({page})}></HomeListing>,
      <HomeListing category="4bf58dd8d48988d181941735" onPageChange={page => this.setState({page})}></HomeListing>,
    ];

    return PAGE_COMPS[this.state.page];
  }
}