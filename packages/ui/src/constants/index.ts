export const SHELTER_CATEGORIES = {
  MEN: 'MEN',
  WOMEN: 'WOMEN',
  FAMILY: 'FAMILY',
  YOUTH: 'YOUTH',
  MIXED: 'MIXED',
} as const;

export const RESOURCE_TYPES = {
  FOOD: 'FOOD',
  SHOWER: 'SHOWER',
  HEALTH: 'HEALTH',
  LEGAL: 'LEGAL',
  EMPLOYMENT: 'EMPLOYMENT',
  HYGIENE: 'HYGIENE',
  COOLING: 'COOLING',
  WARMING: 'WARMING',
  SAFE_PARKING: 'SAFE_PARKING',
} as const;

export const STATUS_COLORS = {
  OPEN: '#10B981', // green
  LIMITED: '#F59E0B', // amber
  FULL: '#EF4444', // red
  UNKNOWN: '#6B7280', // gray
} as const;

export const STATUS_LABELS = {
  OPEN: 'Open',
  LIMITED: 'Limited',
  FULL: 'Full',
  UNKNOWN: 'Unknown',
} as const;

export const CATEGORY_LABELS = {
  MEN: 'Men',
  WOMEN: 'Women',
  FAMILY: 'Family',
  YOUTH: 'Youth',
  MIXED: 'Mixed',
} as const;

export const RESOURCE_LABELS = {
  FOOD: 'Food',
  SHOWER: 'Shower',
  HEALTH: 'Health',
  LEGAL: 'Legal',
  EMPLOYMENT: 'Employment',
  HYGIENE: 'Hygiene',
  COOLING: 'Cooling',
  WARMING: 'Warming',
  SAFE_PARKING: 'Safe Parking',
} as const;

export const LANGUAGES = {
  en: 'English',
  es: 'Español',
  ko: '한국어',
  hy: 'Հայերեն',
  tl: 'Tagalog',
  zh: '中文',
} as const;

export const LA_NEIGHBORHOODS = [
  'Skid Row',
  'Westlake/MacArthur Park',
  'Koreatown',
  'Hollywood',
  'Venice',
  'South LA',
  'San Fernando Valley',
  'San Pedro/Harbor',
] as const;
