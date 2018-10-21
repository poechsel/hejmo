import React, { Component } from 'react';
import { StyleSheet, View } from 'react-native';
import { Text, TouchableRipple } from 'react-native-paper';

import EntypoIcon from 'react-native-vector-icons/Entypo';
import FontAwesome5Icon from 'react-native-vector-icons/FontAwesome5';
import MaterialIcon from 'react-native-vector-icons/MaterialIcons';

const ICON_COMPS = {
  'entypo': EntypoIcon,
  'fa5': FontAwesome5Icon,
  'material': MaterialIcon,
};

export default function GeniusButton(props) {
  const [type, icon] = props.icon.split('/');
  const IconComp = ICON_COMPS[type]

  return (
    <TouchableRipple
      style={[styles.outside, {backgroundColor: props.color}]}
      onPress={() => console.log('Pressed')}>
      <View style={styles.inside}>
        <IconComp name={icon} size={70} style={styles.icon}></IconComp>
        <Text style={styles.text}>{props.text}</Text>
      </View>
    </TouchableRipple>
  );
}

const styles = StyleSheet.create({
  outside: {
    height: 150,
    width: 155,
    borderRadius: 5,
    elevation: 1,
    marginHorizontal: 5,
  },

  inside: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
  },

  icon: {
    marginBottom: 10,
    color: '#fff',
  },

  text: {
    color: '#fff',
  }
});