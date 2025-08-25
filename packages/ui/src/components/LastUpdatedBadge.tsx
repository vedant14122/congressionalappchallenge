import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

export interface LastUpdatedBadgeProps {
  lastUpdated: Date;
  size?: 'small' | 'medium';
}

export const LastUpdatedBadge: React.FC<LastUpdatedBadgeProps> = ({
  lastUpdated,
  size = 'medium',
}) => {
  const getTimeAgo = (date: Date): string => {
    const now = new Date();
    const diffInMinutes = Math.floor((now.getTime() - date.getTime()) / (1000 * 60));
    
    if (diffInMinutes < 1) return 'Just now';
    if (diffInMinutes < 60) return `${diffInMinutes}m ago`;
    
    const diffInHours = Math.floor(diffInMinutes / 60);
    if (diffInHours < 24) return `${diffInHours}h ago`;
    
    const diffInDays = Math.floor(diffInHours / 24);
    if (diffInDays < 7) return `${diffInDays}d ago`;
    
    return 'Over a week ago';
  };

  const isStale = (date: Date): boolean => {
    const now = new Date();
    const diffInHours = (now.getTime() - date.getTime()) / (1000 * 60 * 60);
    return diffInHours > 12;
  };

  const timeAgo = getTimeAgo(lastUpdated);
  const stale = isStale(lastUpdated);

  const sizeStyles = {
    small: { paddingHorizontal: 6, paddingVertical: 2, fontSize: 10 },
    medium: { paddingHorizontal: 8, paddingVertical: 3, fontSize: 12 },
  };

  return (
    <View
      style={[
        styles.container,
        {
          backgroundColor: stale ? '#FEF3C7' : '#F3F4F6',
          borderColor: stale ? '#F59E0B' : '#D1D5DB',
          ...sizeStyles[size],
        },
      ]}
    >
      <Text
        style={[
          styles.text,
          {
            color: stale ? '#92400E' : '#6B7280',
            fontSize: sizeStyles[size].fontSize,
          },
        ]}
      >
        {stale ? '⚠️ ' : '🕒 '}Updated {timeAgo}
      </Text>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    borderRadius: 12,
    borderWidth: 1,
    alignItems: 'center',
    justifyContent: 'center',
  },
  text: {
    fontWeight: '500',
  },
});
