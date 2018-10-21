import React, { Component } from 'react';
import { StyleSheet, Text, View, TouchableOpacity, Image } from 'react-native';
import { Banner } from 'react-native-paper';
import Icon from 'react-native-vector-icons/AntDesign';

import Genius from '../components/Genius';

export default class HomeGenius extends Component<{}> {
  state = {
    visible: true,
  };

  render() {
    return (
      <View style={styles.container}>
        <Banner
          visible={this.state.visible}
          actions={[
            {
              label: 'Dismiss',
              onPress: () => this.setState({ visible: false }),
            },
            {
              label: 'Open Reviews',
              onPress: () => this.setState({ visible: false }),
            },
          ]}
          image={({ size }) => <Icon size={20} name="star" color="#ddd"></Icon>}
        >
          You have 3 new places to review!
        </Banner>
        <View style={styles.wrapper}>
          <Genius onPageChange={(page) => {this.props.onPageChange(page)}}></Genius>
        </View>
      </View>
    );
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    flexDirection: 'column',
  },

  wrapper: {
    flex: 1,
    flexDirection: 'column',
    justifyContent: 'center',
    margin: 20,
  }
});