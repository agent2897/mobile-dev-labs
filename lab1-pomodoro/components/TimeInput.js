import React from 'react';
import PropTypes from 'prop-types';
import { View, Text, TextInput, StyleSheet } from 'react-native';

// Поле для введення тривалості (у хвилинах)
export default function TimeInput({ label, value, onChange, editable }) {
  return (
    <View style={styles.row}>
      <Text style={styles.label}>{label}</Text>
      <TextInput
        style={[styles.input, !editable && styles.disabled]}
        keyboardType="numeric"
        value={String(value)}
        editable={editable}
        onChangeText={(text) => {
          const n = parseInt(text.replace(/[^0-9]/g, ''), 10);
          onChange(Number.isNaN(n) ? 0 : Math.min(n, 999));
        }}
      />
      <Text style={styles.label}>хв</Text>
    </View>
  );
}

TimeInput.propTypes = {
  label: PropTypes.string.isRequired,
  value: PropTypes.number.isRequired,
  onChange: PropTypes.func.isRequired,
  editable: PropTypes.bool,
};

TimeInput.defaultProps = { editable: true };

const styles = StyleSheet.create({
  row: { flexDirection: 'row', alignItems: 'center', marginVertical: 6 },
  label: { color: '#fff', fontSize: 18, marginHorizontal: 8 },
  input: {
    backgroundColor: '#fff', borderRadius: 8, width: 70, paddingVertical: 6,
    textAlign: 'center', fontSize: 18,
  },
  disabled: { opacity: 0.5 },
});
