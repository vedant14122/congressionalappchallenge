import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { LA_NEIGHBORHOODS } from '../constants';

export interface NeighborhoodChipProps {
  neighborhood: string;
  size?: 'small' | 'medium';
  variant?: 'filled' | 'outlined';
}

export const NeighborhoodChip: React.FC<NeighborhoodChipProps> = ({
  neighborhood,
  size = 'medium',
  variant = 'outlined',
}) => {
  const getNeighborhoodColor = (name: string): string => {
    const normalizedName = name.toLowerCase();
    
    if (normalizedName.includes('skid row') || normalizedName.includes('dtla')) {
      return '#EF4444'; // red
    }
    if (normalizedName.includes('koreatown') || normalizedName.includes('ko')) {
      return '#3B82F6'; // blue
    }
    if (normalizedName.includes('hollywood')) {
      return '#8B5CF6'; // purple
    }
    if (normalizedName.includes('venice')) {
      return '#10B981'; // green
    }
    if (normalizedName.includes('south la') || normalizedName.includes('south los angeles')) {
      return '#F59E0B'; // amber
    }
    if (normalizedName.includes('san fernando') || normalizedName.includes('valley')) {
      return '#06B6D4'; // cyan
    }
    if (normalizedName.includes('san pedro') || normalizedName.includes('harbor')) {
      return '#6366F1'; // indigo
    }
    if (normalizedName.includes('westlake') || normalizedName.includes('macarthur')) {
      return '#EC4899'; // pink
    }
    
    return '#6B7280'; // gray default
  };

  const color = getNeighborhoodColor(neighborhood);
  const backgroundColor = variant === 'filled' ? color : 'transparent';
  const textColor = variant === 'filled' ? 'white' : color;

  const sizeStyles = {
    small: { paddingHorizontal: 6, paddingVertical: 2, fontSize: 10 },
    medium: { paddingHorizontal: 8, paddingVertical: 3, fontSize: 12 },
  };

  return (
    <View
      style={[
        styles.container,
        {
          backgroundColor,
          borderColor: color,
          borderWidth: variant === 'outlined' ? 1 : 0,
          ...sizeStyles[size],
        },
      ]}
    >
      <Text
        style={[
          styles.text,
          {
            color: textColor,
            fontSize: sizeStyles[size].fontSize,
          },
        ]}
        numberOfLines={1}
      >
        {neighborhood}
      </Text>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    borderRadius: 12,
    alignItems: 'center',
    justifyContent: 'center',
    maxWidth: 120,
  },
  text: {
    fontWeight: '500',
    textAlign: 'center',
  },
});
