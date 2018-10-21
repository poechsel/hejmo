import React, { Component } from 'react';
import { StyleSheet, Animated, Easing, Dimensions } from 'react-native';
import { View, ActivityIndicator, Image } from 'react-native';
import { Text } from 'react-native-paper';

import ColorHash from 'color-hash';
import Config from '../config.json';

export default class BarChart extends Component<{}> {
  constructor(props) {
    super(props);

    const {width, height} = Dimensions.get('window');

    this.state = {
      categories: null,
      animations: null,
    };

    fetch(Config.API_URL + '/profile_summary/' + Config.USER_ID)
      .then(resp => resp.json())
      .catch(error => { alert(error.message) })
      .then(categories => {
        const animations = categories.map(_ => new Animated.Value(-width))
        this.setState({categories, animations})

        // Animate the appearance of the bars.
        Animated.stagger(100, 
          animations.map(a => Animated.timing(a, {
            toValue: 0,
            duration: 600,
            easing: Easing.quad,
          })
        )).start();
      })
  }

  render() {
    const generator = new ColorHash({lightness: 0.45});

    if (!this.state.categories) {
      return <ActivityIndicator size="large" color="#ccc" />;
    } else {
      const bars = this.state.categories.map((c, i) =>
        <Animated.View
          key={c.category_id}
          style={{
            ...styles.bar,
            width: (c.interest * 80 + 10) + '%',
            backgroundColor: generator.hex(c.display_name),
            marginLeft: this.state.animations[i],
          }}>
          <Text style={styles.barName}>{c.display_name}</Text>
          <Image style={styles.barIcon} source={{ uri: c.icon_url }}></Image>
        </Animated.View>
      );

      return <View>{ bars }</View>;
    }
  }
}

const styles = StyleSheet.create({
  bar: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'flex-end',
    padding: 5,
    borderTopRightRadius: 8,
    borderBottomRightRadius: 8,
    marginBottom: 7,
    elevation: 1,
  },

  barName: {
    color: '#fff',
  },

  barIcon: {
    width: 20,
    height: 20,
    marginLeft: 3,
  },
});