#!/usr/bin/env node

/**
 * ETL Script: ArcGIS -> Firestore
 * Imports winter shelter data from ArcGIS to Firebase Firestore
 */

import fetch from 'node-fetch';
import admin from 'firebase-admin';
import dotenv from 'dotenv';
import fs from 'fs/promises';
import path from 'path';

// Load environment variables
dotenv.config();

// Initialize Firebase Admin
const serviceAccount = {
  projectId: process.env.FIREBASE_PROJECT_ID,
  privateKey: process.env.FIREBASE_PRIVATE_KEY?.replace(/\\n/g, '\n'),
  clientEmail: process.env.FIREBASE_CLIENT_EMAIL,
};

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
});

const db = admin.firestore();

/**
 * Fetch data from ArcGIS REST API
 * @param {string} url - ArcGIS REST API endpoint
 * @returns {Promise<Array>} - Array of features
 */
async function fetchArcGISData(url) {
  try {
    console.log(`Fetching data from: ${url}`);
    
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    
    if (!data.features) {
      throw new Error('No features found in ArcGIS response');
    }
    
    console.log(`Found ${data.features.length} features`);
    return data.features;
  } catch (error) {
    console.error('Error fetching ArcGIS data:', error);
    throw error;
  }
}

/**
 * Transform ArcGIS feature to shelter object
 * @param {Object} feature - ArcGIS feature object
 * @returns {Object} - Transformed shelter object
 */
function transformFeature(feature) {
  const attributes = feature.attributes || {};
  const geometry = feature.geometry || {};
  
  return {
    name: attributes.NAME || attributes.SHELTER_NAME || 'Unknown Shelter',
    address: attributes.ADDRESS || attributes.LOCATION || 'Address not available',
    phone: attributes.PHONE || attributes.CONTACT || null,
    capacity: parseInt(attributes.CAPACITY) || 0,
    available: parseInt(attributes.AVAILABLE) || 0,
    type: attributes.TYPE || attributes.SHELTER_TYPE || 'general',
    status: attributes.STATUS || 'open',
    coordinates: geometry.x && geometry.y ? {
      latitude: geometry.y,
      longitude: geometry.x
    } : null,
    hours: attributes.HOURS || null,
    restrictions: attributes.RESTRICTIONS || null,
    services: attributes.SERVICES ? attributes.SERVICES.split(',').map(s => s.trim()) : [],
    lastUpdated: new Date().toISOString(),
    source: 'arcgis_import'
  };
}

/**
 * Save shelter data to Firestore
 * @param {Array} shelters - Array of shelter objects
 */
async function saveToFirestore(shelters) {
  const batch = db.batch();
  const sheltersRef = db.collection('shelters');
  
  console.log(`Preparing to save ${shelters.length} shelters to Firestore...`);
  
  shelters.forEach((shelter, index) => {
    const docRef = sheltersRef.doc();
    batch.set(docRef, shelter);
    
    if ((index + 1) % 100 === 0) {
      console.log(`Processed ${index + 1} shelters...`);
    }
  });
  
  try {
    await batch.commit();
    console.log(`Successfully saved ${shelters.length} shelters to Firestore`);
  } catch (error) {
    console.error('Error saving to Firestore:', error);
    throw error;
  }
}

/**
 * Save data to local JSON file for testing
 * @param {Array} shelters - Array of shelter objects
 * @param {string} filename - Output filename
 */
async function saveToLocalFile(shelters, filename = 'winter_shelters.json') {
  try {
    const dataDir = path.join(process.cwd(), '..', 'data');
    const filePath = path.join(dataDir, filename);
    
    // Ensure data directory exists
    await fs.mkdir(dataDir, { recursive: true });
    
    const jsonData = JSON.stringify(shelters, null, 2);
    await fs.writeFile(filePath, jsonData);
    
    console.log(`Data saved to local file: ${filePath}`);
  } catch (error) {
    console.error('Error saving to local file:', error);
  }
}

/**
 * Clear existing shelter data from Firestore
 */
async function clearExistingData() {
  try {
    console.log('Clearing existing shelter data...');
    
    const snapshot = await db.collection('shelters').get();
    const batch = db.batch();
    
    snapshot.docs.forEach(doc => {
      batch.delete(doc.ref);
    });
    
    await batch.commit();
    console.log(`Cleared ${snapshot.docs.length} existing documents`);
  } catch (error) {
    console.error('Error clearing existing data:', error);
    throw error;
  }
}

/**
 * Main ETL function
 */
async function runETL() {
  const arcgisUrl = process.env.ARCGIS_SHELTERS_URL;
  
  if (!arcgisUrl) {
    console.error('ARCGIS_SHELTERS_URL environment variable is required');
    process.exit(1);
  }
  
  try {
    console.log('Starting ETL process...');
    
    // Fetch data from ArcGIS
    const features = await fetchArcGISData(arcgisUrl);
    
    // Transform features to shelter objects
    console.log('Transforming data...');
    const shelters = features.map(transformFeature);
    
    // Filter out invalid shelters
    const validShelters = shelters.filter(shelter => 
      shelter.name && shelter.name !== 'Unknown Shelter'
    );
    
    console.log(`Transformed ${validShelters.length} valid shelters`);
    
    // Save to local file for testing
    await saveToLocalFile(validShelters);
    
    // Clear existing data if requested
    if (process.argv.includes('--clear')) {
      await clearExistingData();
    }
    
    // Save to Firestore
    await saveToFirestore(validShelters);
    
    console.log('ETL process completed successfully!');
    
  } catch (error) {
    console.error('ETL process failed:', error);
    process.exit(1);
  } finally {
    process.exit(0);
  }
}

/**
 * Validate environment variables
 */
function validateEnvironment() {
  const required = [
    'FIREBASE_PROJECT_ID',
    'FIREBASE_PRIVATE_KEY',
    'FIREBASE_CLIENT_EMAIL',
    'ARCGIS_SHELTERS_URL'
  ];
  
  const missing = required.filter(key => !process.env[key]);
  
  if (missing.length > 0) {
    console.error('Missing required environment variables:', missing.join(', '));
    console.error('Please check your .env file');
    process.exit(1);
  }
}

// Run the script
if (import.meta.url === `file://${process.argv[1]}`) {
  validateEnvironment();
  runETL();
}

export { fetchArcGISData, transformFeature, saveToFirestore, saveToLocalFile };
