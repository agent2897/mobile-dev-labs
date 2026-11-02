import { Vibration } from 'react-native';

// змушує телефон вібрувати
export const vibrate = () => Vibration.vibrate([500, 500, 500]);
