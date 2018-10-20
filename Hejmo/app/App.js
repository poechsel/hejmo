import React, { Component } from 'react';
import { DefaultTheme, Provider as PaperProvider } from 'react-native-paper';
import { BottomNavigation, Text } from 'react-native-paper';

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
import ReviewPage from './pages/Review';
import ProfilePage from './pages/Profile';

const HomeRoute = () => <HomePage></HomePage>;
const ReviewRoute = () => <ReviewPage></ReviewPage>;
const ProfileRoute = () => <ProfilePage></ProfilePage>;

export default class App extends Component<{}> {
  state = {
    index: 1,
    routes: [
      { key: 'home', title: 'Home', icon: 'home' },
      { key: 'review', title: 'Review', icon: 'star' },
      { key: 'profile', title: 'Profile', icon: 'person' },
    ],
  };

  handleIndexChange = index => this.setState({ index });

  renderScene = BottomNavigation.SceneMap({
    home: HomeRoute,
    review: ReviewRoute,
    profile: ProfileRoute,
  });

  render() {
    return (
      <PaperProvider theme={theme}>
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