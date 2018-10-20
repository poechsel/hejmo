import React, { Component } from 'react';
import { StyleSheet, Text, View, TouchableOpacity, Image } from 'react-native';
import CardStack, { Card } from 'react-native-card-stack-swiper';

import PlaceCard from '../components/PlaceCard';
import Icon from 'react-native-vector-icons/AntDesign';

// Mock data (the API calls will come later).
import mockReviews from '../mock/reviews.json';

export default class Review extends Component<{}> {
  constructor(props) {
    super(props);
    this.state = { empty: false };
    this.places = mockReviews;
  }

  removePlace = () => {
    this.places.splice(0, 1)
    if (this.places.length == 0) {
      this.setState({ empty: true });
    }
  }

  handleLeft = () => {
    // TODO(liautaud): API calls.
    this.removePlace()
  }

  handleRight = () => {
    // TODO(liautaud): API calls.
    this.removePlace()
  }

  handleTop = () => {
    // TODO(liautaud): API calls.
    // this.removePlace()
  }

  handleBottom = () => {
    // TODO(liautaud): API calls.
    this.removePlace()
  }

  renderFooter = () => (
    <View style={styles.footer}>
      <View style={styles.buttonContainer}>
        <TouchableOpacity
          style={[styles.button, styles.largeButton, styles.dislikeButton]}
          onPress={() => { this.swiper.swipeLeft(); }}>
            <Icon name="dislike1" size={32} color={DISLIKE_COLOR} />
        </TouchableOpacity>
        <View style={styles.centerButtonContainer}>
          <TouchableOpacity
            style={[styles.button, styles.smallButton, styles.commentButton]} 
            onPress={() => { this.swiper.swipeTop(); }}>
              <Icon name="edit" size={25} color={COMMENT_COLOR} />
          </TouchableOpacity>
          <TouchableOpacity
            style={[styles.button, styles.smallButton, styles.discardButton]}
            onPress={() => { this.swiper.swipeBottom(); }}>
              <Icon name="close" size={25} color={DISCARD_COLOR} />
          </TouchableOpacity>
        </View>
        <TouchableOpacity
          style={[styles.button, styles.largeButton, styles.likeButton]}
          onPress={() => { this.swiper.swipeRight(); }}>
            <Icon name="like1" size={32} color={LIKE_COLOR} />
        </TouchableOpacity>
      </View>
    </View>
  )

  render() {
    let cards = this.places.map(place => 
      <Card key={place.place_id}><PlaceCard place={place}></PlaceCard></Card>
    );

    if (!this.state.empty && this.places.length > 0) {
      return (
        <View style={{flex: 1, paddingVertical: 20}}>
          <CardStack
            style={styles.content}
            onSwipedLeft={this.handleLeft}
            onSwipedRight={this.handleRight}
            onSwipedTop={this.handleTop}
            onSwipedBottom={this.handleBottom}
            renderNoMoreCards={() => <Text></Text>}
            ref={swiper => { this.swiper = swiper }}>{ cards }</CardStack>
          {this.renderFooter()}
        </View>
      );
    } else {
      return (
        <View style={styles.empty}>
          <Icon size={80} name="star" color="#ddd"></Icon>
          <Text style={{ marginTop: 30 }}>You have no more places to review.</Text>
        </View>
      );
    }
  }
}

const LIKE_COLOR = '#00a86b';
const DISLIKE_COLOR = '#fd267d';
const COMMENT_COLOR = '#f6be42';
const DISCARD_COLOR = '#aaa';

const styles = StyleSheet.create({
  content:{
    flex: 5,
    alignItems: 'center',
    justifyContent: 'center',
  },

  label: {
    lineHeight: 400,
    textAlign: 'center',
    fontSize: 55,
    fontFamily: 'System',
    color: '#ffffff',
    backgroundColor: 'transparent',
  },

  footer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    marginTop: 10,
    marginBottom: 30,
  },

  empty: {
    flex: 1,
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center'
  },

  /* Container styles */
  buttonContainer: {
    width: 220,
    flexDirection: 'row',
    justifyContent: 'space-between',
  },

  centerButtonContainer: {
    marginHorizontal: 10
  },

  /* Button styles */
  button: {
    shadowColor: 'rgba(0,0,0,0.3)',
    shadowOffset: {
      width: 0,
      height: 1
    },
    elevation: 2,
    shadowOpacity:0.5,
    backgroundColor:'#fff',
    alignItems:'center',
    justifyContent:'center',
    zIndex: 0,
  },

  smallButton: {
    width: 55,
    height: 55,
    borderWidth: 4,    
    borderRadius:55,
    backgroundColor: '#fff',
  },

  largeButton: {
    width: 75,
    height: 75,
    borderWidth: 6,
    borderRadius: 75,
    backgroundColor: '#fff',
  },

  /* Specific button styles */
  commentButton: { borderColor: COMMENT_COLOR, marginTop: -22 },
  discardButton: { borderColor: DISCARD_COLOR, marginTop: 9 },
  likeButton: { borderColor: LIKE_COLOR },
  dislikeButton: { borderColor: DISLIKE_COLOR }
});
