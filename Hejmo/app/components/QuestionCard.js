import React, { Component } from 'react';
import { View, Image, StyleSheet } from 'react-native';
import Icon from 'react-native-vector-icons/MaterialIcons';

import { withTheme, Button, Card, Title, Text, Paragraph } from 'react-native-paper';
import ColorHash from 'color-hash';

function QuestionCard(props) {
  const { theme, question, ...rest } = props;
  const generator = new ColorHash({lightness: 0.45});
  
  return (
    <Card style={styles.card}>
      <Card.Content style={styles.cardContent}>
        <View style={[styles.imageBox, {backgroundColor: generator.hex(question.name)}]}>
          <Image source={{ uri: question.icon_url }} style={styles.image} />
        </View>
        <Text style={styles.question}>Are you interested in { question.name }?</Text>
      </Card.Content>
    </Card>
  );
}

const styles = StyleSheet.create({
  card: {
    width: 320,
    elevation: 1,
  },

  cardContent: {
    flexDirection: 'row',
    alignItems: 'center',
  },

  imageBox: {
    width: 50,
    height: 270,
    borderRadius: 5,
    marginRight: 25,
    alignItems: 'center',
    justifyContent: 'center',
  },

  image: {
    width: 45,
    height: 45,
  },

  question: {
    flex: 1,
    textAlign: 'center',
  }
});

export default withTheme(QuestionCard);