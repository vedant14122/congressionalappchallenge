const express = require('express');
const cors = require('cors');
const admin = require('firebase-admin');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;

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

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static('../web'));

// GET endpoint to fetch shelter data
app.get('/api/shelters', async (req, res) => {
  try {
    const sheltersRef = db.collection('shelters');
    const snapshot = await sheltersRef.get();
    const shelters = [];
    
    snapshot.forEach(doc => {
      shelters.push({
        id: doc.id,
        ...doc.data()
      });
    });
    
    res.json(shelters);
  } catch (error) {
    console.error('Error fetching shelters:', error);
    res.status(500).json({ error: 'Failed to fetch shelters' });
  }
});

// POST endpoint to add/update shelter data
app.post('/api/shelters', async (req, res) => {
  try {
    const shelterData = req.body;
    const docRef = await db.collection('shelters').add(shelterData);
    
    res.json({ 
      id: docRef.id, 
      message: 'Shelter added successfully' 
    });
  } catch (error) {
    console.error('Error adding shelter:', error);
    res.status(500).json({ error: 'Failed to add shelter' });
  }
});

// GET endpoint to fetch specific shelter
app.get('/api/shelters/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const doc = await db.collection('shelters').doc(id).get();
    
    if (!doc.exists) {
      return res.status(404).json({ error: 'Shelter not found' });
    }
    
    res.json({
      id: doc.id,
      ...doc.data()
    });
  } catch (error) {
    console.error('Error fetching shelter:', error);
    res.status(500).json({ error: 'Failed to fetch shelter' });
  }
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
