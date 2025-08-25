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

// Initialize Firebase Admin (robust: supports GOOGLE_APPLICATION_CREDENTIALS, FIREBASE_SERVICE_ACCOUNT, or individual env vars)

function parseInlineServiceAccount(jsonStr){
  try {
    const obj = JSON.parse(jsonStr);
    return obj;
  } catch (e) {
    throw new Error(`FIREBASE_SERVICE_ACCOUNT is set but not valid JSON: ${e.message}`);
  }
}

async function loadServiceAccountFromFile(filePath){
  const raw = await fs.readFile(filePath, 'utf8');
  return JSON.parse(raw);
}

async function initFirebase(){
  let svc = null;

  // Option A: Full JSON in FIREBASE_SERVICE_ACCOUNT
  if (process.env.FIREBASE_SERVICE_ACCOUNT) {
    svc = parseInlineServiceAccount(process.env.FIREBASE_SERVICE_ACCOUNT);
  }

  // Option B: GOOGLE_APPLICATION_CREDENTIALS points to a JSON file
  if (!svc && process.env.GOOGLE_APPLICATION_CREDENTIALS) {
    svc = await loadServiceAccountFromFile(process.env.GOOGLE_APPLICATION_CREDENTIALS);
  }

  // Option C: Individual env vars (FIREBASE_PROJECT_ID, FIREBASE_CLIENT_EMAIL, FIREBASE_PRIVATE_KEY)
  if (!svc && process.env.FIREBASE_PROJECT_ID && process.env.FIREBASE_CLIENT_EMAIL && process.env.FIREBASE_PRIVATE_KEY) {
    svc = {
      type: 'service_account',
      project_id: process.env.FIREBASE_PROJECT_ID,
      client_email: process.env.FIREBASE_CLIENT_EMAIL,
      private_key: process.env.FIREBASE_PRIVATE_KEY.replace(/\\n/g, '\n'),
    };
  }

  // Initialize
  if (svc) {
    if (!admin.apps.length) {
      admin.initializeApp({
        credential: admin.credential.cert(svc),
        projectId: svc.project_id || process.env.FIREBASE_PROJECT_ID,
      });
    }
  } else {
    // Fall back to ADC if available (gcloud auth application-default login)
    if (!admin.apps.length) {
      admin.initializeApp({
        credential: admin.credential.applicationDefault(),
      });
    }
  }

  // Sanity check
  try {
    return admin.firestore();
  } catch (e) {
    console.error('\n🔥 Firebase credential error:', e.message);
    console.error('Fix by either:');
    console.error('  1) Set GOOGLE_APPLICATION_CREDENTIALS to a *service account key* JSON file, or');
    console.error('  2) Set FIREBASE_SERVICE_ACCOUNT to the full JSON, or');
    console.error('  3) Set FIREBASE_PROJECT_ID, FIREBASE_CLIENT_EMAIL, FIREBASE_PRIVATE_KEY env vars.');
    throw e;
  }
}

const db = await initFirebase();

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
  
  const capacity = Number.parseInt(attributes.CAPACITY) || 0;
  const available = Number.parseInt(attributes.AVAILABLE) || 0;
  const occupied = Math.max(capacity - available, 0);

  return {
    name: attributes.NAME || attributes.SHELTER_NAME || 'Unknown Shelter',
    address: attributes.ADDRESS || attributes.LOCATION || 'Address not available',
    phone: attributes.PHONE || attributes.CONTACT || null,
    type: attributes.TYPE || attributes.SHELTER_TYPE || 'shelter',
    status: attributes.STATUS || 'unknown',
    location: (geometry.x && geometry.y) ? { lat: geometry.y, lng: geometry.x } : null,
    hours_text: attributes.HOURS || null,
    notes: attributes.RESTRICTIONS || attributes.NOTES || null,
    populations: ['all'],
    ada: /ada|accessible|wheelchair/i.test(attributes.NOTES || attributes.HOURS || '') || false,
    pets_ok: /pet|animal/i.test(attributes.NOTES || '') || false,

    // Primary fields your UI expects
    totalBeds: capacity,
    occupiedBeds: occupied,

    // Keep raw numbers for reference/debug
    _raw_capacity: capacity,
    _raw_available: available,

    last_verified_at: new Date().toISOString(),
    source: 'arcgis_import'
  };
}

/**
 * Save shelter data to Firestore
 * @param {Array} shelters - Array of shelter objects
 */
async function saveToFirestore(shelters) {
  const batch = db.batch();
  const sheltersRef = db.collection(process.env.FIRESTORE_COLLECTION || 'places');
  
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
    const dataDir = path.join(process.cwd(), 'data');
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
    
    const snapshot = await db.collection(process.env.FIRESTORE_COLLECTION || 'places').get();
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
 * Load data from local JSON file
 * @param {string} filePath - Path to JSON file
 * @returns {Promise<Array>} - Array of shelter objects
 */
async function loadFromLocalFile(filePath) {
  try {
    console.log(`Loading data from local file: ${filePath}`);
    const data = await fs.readFile(filePath, 'utf8');
    const shelters = JSON.parse(data);
    console.log(`Loaded ${shelters.length} shelters from local file`);
    return shelters;
  } catch (error) {
    console.error('Error loading from local file:', error);
    throw error;
  }
}

/**
 * Main ETL function
 */
async function runETL() {
  const arcgisUrl = process.env.ARCGIS_SHELTERS_URL || process.env.WINTER_LAYER_URL;
  const useLocalFile = process.argv.includes('--local') || !arcgisUrl || arcgisUrl.includes('example.com');
  
  try {
    console.log('Starting ETL process...');
    
    let shelters;
    
    if (useLocalFile) {
      // Load from local JSON file
      const localDataPath = path.join(process.cwd(), 'data', 'winter_shelters.json');
      shelters = await loadFromLocalFile(localDataPath);
    } else {
      // Fetch data from ArcGIS
      const features = await fetchArcGISData(arcgisUrl);
      
      // Transform features to shelter objects
      console.log('Transforming data...');
      shelters = features.map(transformFeature);
    }
    
    // Filter out invalid shelters
    const validShelters = shelters.filter(shelter => 
      shelter.name && shelter.name !== 'Unknown Shelter'
    );
    
    console.log(`Processing ${validShelters.length} valid shelters`);
    
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
    'FIREBASE_CLIENT_EMAIL'
  ];
  
  const missing = required.filter(key => !process.env[key]);
  
  if (missing.length > 0) {
    console.error('Missing required environment variables:', missing.join(', '));
    console.error('Please check your .env file');
    process.exit(1);
  }
  
  // Warn if ArcGIS URL is not set (but don't fail)
  if (!process.env.ARCGIS_SHELTERS_URL) {
    console.log('ARCGIS_SHELTERS_URL not set, will use local JSON file');
  }
}

// Run the script
if (import.meta.url === `file://${process.argv[1]}`) {
  validateEnvironment();
  runETL();
}

export { fetchArcGISData, transformFeature, saveToFirestore, saveToLocalFile };
