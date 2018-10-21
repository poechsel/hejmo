import React, { Component } from 'react';
import { StyleSheet, View } from 'react-native';
import { Title, Button, Text } from 'react-native-paper';

import GeniusButton from './GeniusButton'

export default function Genius(props) {
  return (
    <View style={styles.container}>
      <Title style={{ marginBottom: 25 }}>What do you want to do?</Title>
      <View style={{ alignItems: 'center' }}>
        <View style={styles.row}>
          <GeniusButton color="#7569ff" text="Find a restaurant" icon="material/restaurant-menu"></GeniusButton>
          <GeniusButton color="#d684ef" text="Go out for the night" icon="entypo/drink"></GeniusButton>
        </View>
        <View style={styles.row}>
          <GeniusButton color="#ffb769" text="See an exhibit" icon="material/account-balance"></GeniusButton>
          <GeniusButton color="#fa6b83" text="Surprise me!" icon="fa5/dice"></GeniusButton>
        </View>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    alignItems: 'center'
  },

  row: {
    marginBottom: 10,
    alignItems: 'center',
    flexDirection: 'row',
  },
});