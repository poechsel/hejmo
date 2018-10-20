import React, { Component } from 'react';
import { View, Image, StyleSheet } from 'react-native';
import Icon from 'react-native-vector-icons/MaterialIcons';

import { withTheme, Button, Card, Title, Text, Paragraph } from 'react-native-paper';

function PlaceCard(props) {
  const { theme, place, ...rest } = props;
  const { roundness } = theme;

  const rounding = {
    borderTopLeftRadius: roundness,
    borderTopRightRadius: roundness,
  };

  return (
    <Card style={styles.card}>
      <Image source={{ uri: place.photo_url }} style={[styles.image, rounding]} />
      <Card.Content>
        <Title style={styles.title}>{ place.name }</Title>
        <View style={styles.status}>
          <Icon style={styles.icons} name="place" size={20} />
          <Text>{place.location}</Text>
        </View>
        <View style={styles.status}>
          <Icon style={styles.icons} name="access-time" size={20} />
          <Text>{place.date_of_visit}</Text>
        </View>
        <Paragraph style={styles.description}>{place.description}</Paragraph>
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