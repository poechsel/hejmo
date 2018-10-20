import React, { Component } from 'react';
import { View, Image, StyleSheet } from 'react-native';
import Icon from 'react-native-vector-icons/MaterialIcons';

import { withTheme, Button, Card, Title, Text, Paragraph } from 'react-native-paper';

function PlaceCard(props) {
  const { theme, src, ...rest } = props;
  const { roundness } = theme;

  const rounding = {
    borderTopLeftRadius: roundness,
    borderTopRightRadius: roundness,
  };

  return (
    <Card style={styles.card}>
      <Image source={{ uri: src }} style={[styles.image, rounding]} />
      <Card.Content>
        <Title style={styles.title}>Restaurant Higuma</Title>
        <View style={styles.status}>
          <Icon style={styles.icons} name="place" size={20} />
          <Text>Card content</Text>
        </View>
        <View style={styles.status}>
          <Icon style={styles.icons} name="access-time" size={20} />
          <Text>Card content</Text>
        </View>
        <Paragraph style={styles.description}>
          uisdfysidfu
        </Paragraph>
      </Card.Content>
    </Card>
  );
}

const styles = StyleSheet.create({
  card: {
    width: 320,
    elevation: 1,
  },

  image: {
    height: 200,
  },

  title: {
    marginVertical: 10,
  },

  status: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    marginVertical: 1,
  },

  icons: {
    color: '#333',
    marginRight: 6,
  },

  description: {
    marginTop: 10
  },
});

export default withTheme(PlaceCard);