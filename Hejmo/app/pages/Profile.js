import React, { Component } from 'react';
import { StyleSheet, Text, View, TouchableOpacity, Image } from 'react-native';
import { Divider, Title, Surface, List, IconButton } from 'react-native-paper';

import Icon from 'react-native-vector-icons/Ionicons';

const IMAGE_URI = 'https://scontent-lhr3-1.xx.fbcdn.net/v/t1.0-9/31719881_10214351038884093_19545721854230528_n.jpg?_nc_cat=110&_nc_ht=scontent-lhr3-1.xx&oh=6413fde5f59edd9a99f883961319283c&oe=5C500132'

export default function Profile(props) {
  return (
    <View>
      <View style={styles.avatarContainer}>
        <Image style={styles.avatar} source={{ uri: IMAGE_URI }}></Image>
        <View>
          <Text style={{ fontSize: 16 }}>Anna Logacheva</Text>
          <View style={{ flexDirection: 'row' }}>
            <View style={styles.badge}>
              <Icon size={15} name="ios-trophy" style={{ marginRight: 5 }}></Icon>
              <Text>Super Reviewer</Text>
            </View>
            <View style={styles.badge}>
              <Icon size={15} name="ios-trophy" style={{ marginRight: 5 }}></Icon>
              <Text>Parisian</Text>
            </View>
          </View>
        </View>
      </View>
      <Divider></Divider>
      <View style={styles.profileContainer}>
        <Title>My profile</Title>
        <Title>My past reviews</Title>
        <Surface style={styles.reviews}>
          <List.Item
            title="First Item"
            description="Item description"
            right={props => <IconButton {...props} icon="edit" />}
          />
          <List.Item
            title="First Item"
            description="Item description"
            right={props => <IconButton {...props} icon="edit" />}
          />
          <List.Item
            title="First Item"
            description="Item description"
            right={props => <IconButton {...props} icon="edit" />}
          />
        </Surface>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
    avatarContainer: {
        padding: 20,
        backgroundColor: '#fff',
        flexDirection: 'row',
        alignItems: 'center',
    },

    avatar: {
        width: 65,
        height: 65,
        borderRadius: 65,
        marginRight: 20,
    },

    badge: {
      marginTop: 9,
      marginRight: 5,
      paddingVertical: 4,
      paddingHorizontal: 10,
      flexDirection: 'row',
      alignItems: 'center',
      fontSize: 11,
      backgroundColor: '#ffdb72',
      borderRadius: 15,
    },

    profileContainer: {
      padding: 20,
    },

    reviews: {
      marginTop: 10,
      borderRadius: 5,
      elevation: 1,
    }
});