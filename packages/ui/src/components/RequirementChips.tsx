import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

export interface RequirementChipsProps {
  requirements: {
    requiresId?: boolean;
    petFriendly?: boolean;
    adaAccessible?: boolean;
    lgbtqFriendly?: boolean;
    curfewTime?: string;
  };
  size?: 'small' | 'medium';
}

export const RequirementChips: React.FC<RequirementChipsProps> = ({
  requirements,
  size = 'medium',
}) => {
  const chips = [];

  if (requirements.requiresId) {
    chips.push({ label: 'ID Required', color: '#EF4444', icon: '🆔' });
  }

  if (requirements.petFriendly) {
    chips.push({ label: 'Pet Friendly', color: '#10B981', icon: '🐕' });
  }

  if (requirements.adaAccessible) {
    chips.push({ label: 'ADA Accessible', color: '#3B82F6', icon: '♿' });
  }

  if (requirements.lgbtqFriendly) {
    chips.push({ label: 'LGBTQ+ Friendly', color: '#8B5CF6', icon: '🏳️‍🌈' });
  }

  if (requirements.curfewTime) {
    chips.push({ label: `Curfew: ${requirements.curfewTime}`, color: '#F59E0B', icon: '⏰' });
  }

  if (chips.length === 0) {
    return null;
  }

  const sizeStyles = {
    small: { paddingHorizontal: 6, paddingVertical: 2, fontSize: 10 },
    medium: { paddingHorizontal: 8, paddingVertical: 3, fontSize: 12 },
  };

  return (
    <View style={styles.container}>
      {chips.map((chip, index) => (
        <View
          key={index}
          style={[
            styles.chip,
            {
              backgroundColor: `${chip.color}20`,
              borderColor: chip.color,
              ...sizeStyles[size],
            },
          ]}
        >
          <Text style={styles.icon}>{chip.icon}</Text>
          <Text
            style={[
              styles.label,
              { color: chip.color, fontSize: sizeStyles[size].fontSize },
            ]}
          >
            {chip.label}
          </Text>
        </View>
      ))}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 4,
  },
  chip: {
    flexDirection: 'row',
    alignItems: 'center',
    borderRadius: 12,
    borderWidth: 1,
    gap: 4,
  },
  icon: {
    fontSize: 12,
  },
  label: {
    fontWeight: '500',
  },
});
