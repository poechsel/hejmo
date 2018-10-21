import React, { Component } from 'react';
import { StyleSheet, Text, View, ScrollView, ActivityIndicator } from 'react-native';
import { Title } from 'react-native-paper';
import Icon from 'react-native-vector-icons/AntDesign';

import Config from '../config.json';
import PlaceCard from '../components/PlaceCard'

const CATEGORY_NAMES = {
  '4d4b7105d754a06374d81259': 'a restaurant',
  '4d4b7105d754a06376d81259': 'somewhere to go out',
  '4bf58dd8d48988d181941735': 'an exhibit',
};

export default class HomeListing extends Component<{}> {
  constructor(props) {
    super(props);

    this.state = {matches: null};
    fetch(`${Config.API_URL}/recommendations/${Config.USER_ID}/${props.category}/52.236687/20.995437/0`)
      .then(resp => resp.json())
      .catch(error => { alert(error.message) })
      .then(data => {
        this.setState({ matches: data.recommendations });
      })
  }

  render() {
    if (!this.state.matches) {
      return <ActivityIndicator size="large" color="#ccc" style={{ flex: 1 }} />;
    }

    const cards = this.state.matches.map(match => 
      <PlaceCard key={match.place_id} place={match}></PlaceCard>);

    return (
      <View style={styles.container}>
        <View style={styles.wrapper}>
          <Title>Find {CATEGORY_NAMES[this.props.category]} nearby:</Title>
          <ScrollView style={{ flex: 1 }} contentContainerStyle={styles.scroll}>
            {cards}
          </ScrollView>
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
    margin: 20,
  },

  scroll: {
    alignItems: 'center',
  },
});