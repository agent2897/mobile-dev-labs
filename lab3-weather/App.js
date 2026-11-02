import 'react-native-gesture-handler';
import React from 'react';
import { Provider } from 'react-redux';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { Ionicons } from '@expo/vector-icons';
import { store } from './store';
import SearchScreen from './screens/SearchScreen';
import FavoritesScreen from './screens/FavoritesScreen';
import WeatherScreen from './screens/WeatherScreen';
import SettingsScreen from './screens/SettingsScreen';

const Tab = createBottomTabNavigator();
const SearchStack = createStackNavigator();
const FavStack = createStackNavigator();

const stackOptions = {
  headerStyle: { backgroundColor: '#4a90e2' },
  headerTintColor: '#fff',
  cardStyle: { flex: 1 },
};

// Стек вкладки «Пошук»: список міст -> прогноз
function SearchStackScreen() {
  return (
    <SearchStack.Navigator screenOptions={stackOptions}>
      <SearchStack.Screen name="Search" component={SearchScreen} options={{ title: 'Пошук міста' }} />
      <SearchStack.Screen name="Weather" component={WeatherScreen} />
    </SearchStack.Navigator>
  );
}

// Стек вкладки «Обране»
function FavStackScreen() {
  return (
    <FavStack.Navigator screenOptions={stackOptions}>
      <FavStack.Screen name="Favorites" component={FavoritesScreen} options={{ title: 'Обрані міста' }} />
      <FavStack.Screen name="Weather" component={WeatherScreen} />
    </FavStack.Navigator>
  );
}

const TAB_ICONS = { SearchTab: 'search', FavTab: 'star', SettingsTab: 'settings' };

export default function App() {
  return (
    <Provider store={store}>
      <NavigationContainer>
        <Tab.Navigator
          screenOptions={({ route }) => ({
            tabBarIcon: ({ color, size }) => <Ionicons name={TAB_ICONS[route.name]} size={size} color={color} />,
            tabBarActiveTintColor: '#4a90e2',
            tabBarStyle: { height: 64, paddingTop: 4 },
            tabBarLabelStyle: { fontSize: 12, marginBottom: 6 },
            headerShown: false,
          })}
        >
          <Tab.Screen name="SearchTab" component={SearchStackScreen} options={{ title: 'Пошук' }} />
          <Tab.Screen name="FavTab" component={FavStackScreen} options={{ title: 'Обране' }} />
          <Tab.Screen
            name="SettingsTab"
            component={SettingsScreen}
            options={{ title: 'Налаштування', headerShown: true, ...stackOptions }}
          />
        </Tab.Navigator>
      </NavigationContainer>
    </Provider>
  );
}
