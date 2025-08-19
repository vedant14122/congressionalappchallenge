#!/usr/bin/env node

/**
 * Test ETL Script (without Firestore)
 * Demonstrates the ETL process using local JSON data
 */

import fs from 'fs/promises';
import path from 'path';

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
 * Save shelter data to local file
 * @param {Array} shelters - Array of shelter objects
 */
async function saveToLocalFile(shelters) {
  try {
    const outputPath = path.join(process.cwd(), 'data', 'processed_shelters.json');
    await fs.writeFile(outputPath, JSON.stringify(shelters, null, 2));
    console.log(`Data saved to local file: ${outputPath}`);
  } catch (error) {
    console.error('Error saving to local file:', error);
    throw error;
  }
}

/**
 * Main ETL function
 */
async function runTestETL() {
  try {
    console.log('Starting Test ETL process...');
    
    // Load from local JSON file
    const localDataPath = path.join(process.cwd(), 'data', 'winter_shelters.json');
    const shelters = await loadFromLocalFile(localDataPath);
    
    // Filter out invalid shelters
    const validShelters = shelters.filter(shelter => 
      shelter.name && shelter.name !== 'Unknown Shelter'
    );
    
    console.log(`Processing ${validShelters.length} valid shelters`);
    
    // Display shelter information
    console.log('\nShelter Details:');
    validShelters.forEach((shelter, index) => {
      console.log(`${index + 1}. ${shelter.name}`);
      console.log(`   Address: ${shelter.address}`);
      console.log(`   Capacity: ${shelter.capacity}, Available: ${shelter.available}`);
      console.log(`   Type: ${shelter.type}, Status: ${shelter.status}`);
      console.log(`   Services: ${shelter.services.join(', ')}`);
      console.log('');
    });
    
    // Save to local file for testing
    await saveToLocalFile(validShelters);
    
    console.log('✅ Test ETL process completed successfully!');
    console.log('📊 Summary:');
    console.log(`   - Total shelters processed: ${validShelters.length}`);
    console.log(`   - Data saved to: data/processed_shelters.json`);
    console.log('\n💡 To enable Firestore upload, enable the Firestore API at:');
    console.log('   https://console.developers.google.com/apis/api/firestore.googleapis.com/overview?project=congressionalappchalleng-7916f');
    
  } catch (error) {
    console.error('❌ Test ETL process failed:', error);
    process.exit(1);
  }
}

// Run the script
if (import.meta.url === `file://${process.argv[1]}`) {
  runTestETL();
}
