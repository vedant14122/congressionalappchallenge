import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { STATUS_COLORS, STATUS_LABELS } from '../constants';

export interface StatusPillProps {
  status: keyof typeof STATUS_COLORS;
  size?: 'small' | 'medium' | 'large';
  variant?: 'filled' | 'outlined';
}

export const StatusPill: React.FC<StatusPillProps> = ({
  status,
  size = 'medium',
  variant = 'filled',
}) => {
  const backgroundColor = variant === 'filled' ? STATUS_COLORS[status] : 'transparent';
  const borderColor = STATUS_COLORS[status];
  const textColor = variant === 'filled' ? 'white' : STATUS_COLORS[status];

  const sizeStyles = {
    small: { paddingHorizontal: 8, paddingVertical: 2, fontSize: 12 },
    medium: { paddingHorizontal: 12, paddingVertical: 4, fontSize: 14 },
    large: { paddingHorizontal: 16, paddingVertical: 6, fontSize: 16 },
  };

  return (
    <View
      style={[
        styles.container,
        {
          backgroundColor,
          borderColor,
          borderWidth: variant === 'outlined' ? 1 : 0,
          ...sizeStyles[size],
        },
      ]}
    >
      <Text style={[styles.text, { color: textColor, fontSize: sizeStyles[size].fontSize }]}>
        {STATUS_LABELS[status]}
      </Text>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    borderRadius: 16,
    alignItems: 'center',
    justifyContent: 'center',
    minWidth: 60,
  },
  text: {
    fontWeight: '600',
    textAlign: 'center',
  },
});
