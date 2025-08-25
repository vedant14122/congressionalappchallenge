import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';
import { LANGUAGES } from '../constants';

export interface LanguageToggleProps {
  currentLanguage: keyof typeof LANGUAGES;
  onLanguageChange: (language: keyof typeof LANGUAGES) => void;
  size?: 'small' | 'medium';
  showAll?: boolean;
}

export const LanguageToggle: React.FC<LanguageToggleProps> = ({
  currentLanguage,
  onLanguageChange,
  size = 'medium',
  showAll = false,
}) => {
  const languages = showAll ? Object.entries(LANGUAGES) : [
    ['en', LANGUAGES.en],
    ['es', LANGUAGES.es],
  ];

  const sizeStyles = {
    small: { paddingHorizontal: 8, paddingVertical: 4, fontSize: 12 },
    medium: { paddingHorizontal: 12, paddingVertical: 6, fontSize: 14 },
  };

  return (
    <View style={styles.container}>
      {languages.map(([code, name]) => (
        <TouchableOpacity
          key={code}
          style={[
            styles.button,
            {
              backgroundColor: currentLanguage === code ? '#3B82F6' : 'transparent',
              borderColor: currentLanguage === code ? '#3B82F6' : '#D1D5DB',
              ...sizeStyles[size],
            },
          ]}
          onPress={() => onLanguageChange(code as keyof typeof LANGUAGES)}
        >
          <Text
            style={[
              styles.text,
              {
                color: currentLanguage === code ? 'white' : '#6B7280',
                fontSize: sizeStyles[size].fontSize,
              },
            ]}
          >
            {name}
          </Text>
        </TouchableOpacity>
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
  button: {
    borderRadius: 8,
    borderWidth: 1,
    alignItems: 'center',
    justifyContent: 'center',
    minWidth: 60,
  },
  text: {
    fontWeight: '500',
    textAlign: 'center',
  },
});
