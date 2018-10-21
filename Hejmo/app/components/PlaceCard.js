import React, { Component } from 'react';
import { View, Image, StyleSheet } from 'react-native';
import Icon from 'react-native-vector-icons/MaterialIcons';
import { withTheme, Button, Card, Title, Text, Paragraph } from 'react-native-paper';
import timeago from 'timeago.js';

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
        {!!place.location && <View style={styles.status}>
          <Icon style={styles.icons} name="place" size={20} />
          <Text>{place.location}</Text>
        </View>}
        {!!place.date_of_visit && <View style={styles.status}>
          <Icon style={styles.icons} name="access-time" size={20} />
          <Text>{timeago().format(place.date_of_visit * 1000)}</Text>
        </View>}
        {!!place.distance && <View style={styles.status}>
          <Icon style={styles.icons} name="my-location" size={20} />
          <Text>{parseInt(place.distance)}m away</Text>
        </View>}
        {!!place.description && <Paragraph style={styles.description}>{place.description}</Paragraph>}
      </Card.Content>
    </Card>
  );
}

const styles = StyleSheet.create({
  card: {
    width: 320,
    elevation: 1,
    marginVertical: 10,
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