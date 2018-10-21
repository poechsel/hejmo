import React, { Component } from 'react';
import { DefaultTheme, Provider as PaperProvider } from 'react-native-paper';
import { BottomNavigation, Text, Appbar } from 'react-native-paper';

/* Theming */
const theme = {
  ...DefaultTheme,
  // roundness: 2,
  colors: {
    ...DefaultTheme.colors,
    // primary: '#3498db',
    // accent: '#f1c40f',
  }
};

/* Routing */
import HomePage from './pages/Home';
import ReviewsPage from './pages/Reviews';
import ProfilePage from './pages/Profile';

const HomeRoute = () => <HomePage></HomePage>;
const ReviewsRoute = () => <ReviewsPage></ReviewsPage>;
const ProfileRoute = () => <ProfilePage></ProfilePage>;

export default class App extends Component<{}> {
  state = {
    index: 0,
    routes: [
      { key: 'home', title: 'Home', icon: 'home' },
      { key: 'reviews', title: 'Reviews', icon: 'star' },
      { key: 'profile', title: 'Profile', icon: 'person' },
    ],
  };

  handleIndexChange = index => this.setState({ index });

  renderScene = BottomNavigation.SceneMap({
    home: HomeRoute,
    reviews: ReviewsRoute,
    profile: ProfileRoute,
  });

  render() {
    return (
      <PaperProvider theme={theme}>
        <Appbar.Header>
          <Appbar.Content title={this.state.routes[this.state.index].title} />
          <Appbar.Action icon="more-vert" />
        </Appbar.Header>
        <BottomNavigation
          navigationState={this.state}
          onIndexChange={this.handleIndexChange}
          renderScene={this.renderScene}
          activeColor={theme.colors.primary}
          inactiveColor={theme.colors.disabled}
          barStyle={{backgroundColor: '#fff'}}
        />
      </PaperProvider>
    );
  }
}