import 'react-native-gesture-handler';
import React, { useEffect, useMemo, useState } from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import AsyncStorage from '@react-native-async-storage/async-storage';
import LoginScreen from './src/screens/LoginScreen';
import SignUpScreen from './src/screens/SignUpScreen';
import HomeScreen from './src/screens/HomeScreen';
import NewsListScreen from './src/screens/NewsListScreen';
import NewsDetailScreen from './src/screens/NewsDetailScreen';
import { AuthContext } from './src/context/AuthContext';
import JobsSearchScreen from './src/screens/JobsSearchScreen';
import ChatServiceScreen from './src/screens/ChatServiceScreen';

const Stack = createNativeStackNavigator();

export default function App() {
  const [token, setToken] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    (async () => {
      try {
        const t = await AsyncStorage.getItem('token');
        if (t) setToken(t);
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  const auth = useMemo(() => ({
    token,
    signIn: async (t) => { await AsyncStorage.setItem('token', t); setToken(t); },
    signOut: async () => { await AsyncStorage.removeItem('token'); setToken(null); },
  }), [token]);

  if (loading) return null;

  return (
    <AuthContext.Provider value={auth}>
      <NavigationContainer>
        <Stack.Navigator>
          {token ? (
            <>
              <Stack.Screen name="Home" component={HomeScreen} options={{ headerShown: false }} />
              <Stack.Screen name="NewsList" component={NewsListScreen} options={{ title: 'All News' }} />
              <Stack.Screen name="NewsDetail" component={NewsDetailScreen} options={{ title: 'Article' }} />
              <Stack.Screen name="JobsSearch" component={JobsSearchScreen} options={{ title: 'Jobs' }} />
              <Stack.Screen name="ServiceChat" component={ChatServiceScreen} options={{ title: 'Chat' }} />
            </>
            
          ) : (
            <>
              <Stack.Screen name="Login" component={LoginScreen} options={{ title: 'Login', headerShown:false }} />
              <Stack.Screen name="SignUp" component={SignUpScreen} options={{ title: 'Create Account', headerShown:false }} />
            </>
          )}
        </Stack.Navigator>
      </NavigationContainer>
    </AuthContext.Provider>
  );
}
