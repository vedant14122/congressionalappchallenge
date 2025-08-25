import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { RESOURCE_TYPES } from '../constants';

export interface ResourceTypeIconProps {
  type: keyof typeof RESOURCE_TYPES;
  size?: 'small' | 'medium' | 'large';
  showLabel?: boolean;
}

export const ResourceTypeIcon: React.FC<ResourceTypeIconProps> = ({
  type,
  size = 'medium',
  showLabel = false,
}) => {
  const getIconAndColor = (resourceType: keyof typeof RESOURCE_TYPES) => {
    switch (resourceType) {
      case 'FOOD':
        return { icon: '🍽️', color: '#10B981' };
      case 'SHOWER':
        return { icon: '🚿', color: '#3B82F6' };
      case 'HEALTH':
        return { icon: '🏥', color: '#EF4444' };
      case 'LEGAL':
        return { icon: '⚖️', color: '#8B5CF6' };
      case 'EMPLOYMENT':
        return { icon: '💼', color: '#F59E0B' };
      case 'HYGIENE':
        return { icon: '🧴', color: '#06B6D4' };
      case 'COOLING':
        return { icon: '❄️', color: '#3B82F6' };
      case 'WARMING':
        return { icon: '🔥', color: '#EF4444' };
      case 'SAFE_PARKING':
        return { icon: '🚗', color: '#10B981' };
      default:
        return { icon: '📍', color: '#6B7280' };
    }
  };

  const { icon, color } = getIconAndColor(type);
  const label = type.replace('_', ' ').toLowerCase();

  const sizeStyles = {
    small: { fontSize: 16, containerSize: 24 },
    medium: { fontSize: 20, containerSize: 32 },
    large: { fontSize: 24, containerSize: 40 },
  };

  return (
    <View style={styles.container}>
      <View
        style={[
          styles.iconContainer,
          {
            backgroundColor: `${color}20`,
            width: sizeStyles[size].containerSize,
            height: sizeStyles[size].containerSize,
          },
        ]}
      >
        <Text style={[styles.icon, { fontSize: sizeStyles[size].fontSize }]}>
          {icon}
        </Text>
      </View>
      {showLabel && (
        <Text style={[styles.label, { color }]} numberOfLines={1}>
          {label}
        </Text>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    alignItems: 'center',
    justifyContent: 'center',
  },
  iconContainer: {
    borderRadius: 8,
    alignItems: 'center',
    justifyContent: 'center',
  },
  icon: {
    textAlign: 'center',
  },
  label: {
    fontSize: 10,
    fontWeight: '500',
    marginTop: 2,
    textAlign: 'center',
  },
});
