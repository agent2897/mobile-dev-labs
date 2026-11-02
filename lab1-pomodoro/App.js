import React, { useState, useEffect, useRef } from 'react';
import { View, Text, TouchableOpacity, StyleSheet, StatusBar } from 'react-native';
import { vibrate } from './utils';
import TimeInput from './components/TimeInput';

const formatTime = (sec) => {
  const m = String(Math.floor(sec / 60)).padStart(2, '0');
  const s = String(sec % 60).padStart(2, '0');
  return `${m}:${s}`;
};

export default function App() {
  const [workMin, setWorkMin] = useState(25);
  const [breakMin, setBreakMin] = useState(5);
  const [mode, setMode] = useState('work'); // 'work' | 'break'
  const [secondsLeft, setSecondsLeft] = useState(25 * 60);
  const [running, setRunning] = useState(false);
  const intervalRef = useRef(null);

  // Відлік секунд
  useEffect(() => {
    if (running) {
      intervalRef.current = setInterval(() => {
        setSecondsLeft((s) => (s > 0 ? s - 1 : 0));
      }, 1000);
    }
    return () => clearInterval(intervalRef.current);
  }, [running]);

  // Досягнуто 00:00 — вібрація та перемикання режиму
  useEffect(() => {
    if (secondsLeft === 0 && running) {
      vibrate();
      const next = mode === 'work' ? 'break' : 'work';
      setMode(next);
      setSecondsLeft((next === 'work' ? workMin : breakMin) * 60);
    }
  }, [secondsLeft]);

  const reset = () => {
    setRunning(false);
    setMode('work');
    setSecondsLeft(workMin * 60);
  };

  const changeWork = (v) => {
    setWorkMin(v);
    if (!running && mode === 'work') setSecondsLeft(v * 60);
  };

  const changeBreak = (v) => {
    setBreakMin(v);
    if (!running && mode === 'break') setSecondsLeft(v * 60);
  };

  const isWork = mode === 'work';

  return (
    <View style={[styles.container, { backgroundColor: isWork ? '#d9534f' : '#2e8b57' }]}>
      <StatusBar barStyle="light-content" />
      <Text style={styles.mode}>{isWork ? 'Робота' : 'Перерва'}</Text>
      <Text style={styles.timer}>{formatTime(secondsLeft)}</Text>

      <View style={styles.buttons}>
        <TouchableOpacity
          style={styles.button}
          onPress={() => secondsLeft > 0 && setRunning(!running)}
        >
          <Text style={styles.buttonText}>{running ? 'Пауза' : 'Старт'}</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.button} onPress={reset}>
          <Text style={styles.buttonText}>Скинути</Text>
        </TouchableOpacity>
      </View>

      <TimeInput label="Робота:" value={workMin} onChange={changeWork} editable={!running} />
      <TimeInput label="Перерва:" value={breakMin} onChange={changeBreak} editable={!running} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, alignItems: 'center', justifyContent: 'center' },
  mode: { color: '#fff', fontSize: 32, fontWeight: 'bold', marginBottom: 10 },
  timer: { color: '#fff', fontSize: 80, fontWeight: '200', marginBottom: 30 },
  buttons: { flexDirection: 'row', marginBottom: 30 },
  button: {
    backgroundColor: 'rgba(255,255,255,0.25)', paddingVertical: 12,
    paddingHorizontal: 28, borderRadius: 30, marginHorizontal: 10,
  },
  buttonText: { color: '#fff', fontSize: 20, fontWeight: '600' },
});
