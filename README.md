# Winter Shelter Finder

A comprehensive web application for finding and managing winter shelters, built for the Congressional App Challenge.

## 🏗️ Project Structure

```
congressionalappchallenge/
├─ .env                          # secrets & config (local)
├─ package.json
├─ server/
│  └─ server.js                  # Express API (GET/POST)
├─ web/
│  ├─ public.html                # public resource finder
│  └─ admin.html                 # shelter staff panel
├─ scripts/
│  └─ etl_winter.mjs             # ArcGIS -> Firestore ETL
├─ firestore.rules               # lock down direct writes
├─ data/
│  └─ winter_shelters.json       # optional local dump for testing
└─ README.md
```

## 🚀 Quick Start

### Prerequisites

- Node.js (v16 or higher)
- Firebase project with Firestore enabled
- ArcGIS API access (optional, for data import)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd congressionalappchallenge
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   # Firebase Configuration
   FIREBASE_PROJECT_ID=your-project-id
   FIREBASE_PRIVATE_KEY=your-private-key
   FIREBASE_CLIENT_EMAIL=your-client-email
   
   # API Keys (if needed)
   ARCGIS_API_KEY=your-arcgis-api-key
   ARCGIS_SHELTERS_URL=https://your-arcgis-endpoint/query
   
   # Server Configuration
   PORT=3000
   NODE_ENV=development
   ```

4. **Start the server**
   ```bash
   cd server
   node server.js
   ```

5. **Access the application**
   - Public interface: `http://localhost:3000/public.html`
   - Admin panel: `http://localhost:3000/admin.html`

## 📋 Features

### Public Interface (`public.html`)
- **Search & Filter**: Find shelters by location, type, and availability
- **Real-time Data**: Live shelter capacity and status updates
- **Responsive Design**: Works on desktop and mobile devices
- **Accessibility**: Designed for users with diverse needs

### Admin Panel (`admin.html`)
- **Dashboard**: Overview of shelter statistics and capacity
- **Shelter Management**: Add, edit, and remove shelter information
- **Real-time Updates**: Monitor shelter status and availability
- **Data Export**: Generate reports and analytics

### Backend API (`server/server.js`)
- **RESTful Endpoints**: GET/POST operations for shelter data
- **Firebase Integration**: Secure data storage with Firestore
- **CORS Support**: Cross-origin resource sharing enabled
- **Error Handling**: Comprehensive error management

## 🔧 Configuration

### Firebase Setup

1. Create a Firebase project at [Firebase Console](https://console.firebase.google.com/)
2. Enable Firestore Database
3. Generate a service account key:
   - Go to Project Settings > Service Accounts
   - Click "Generate new private key"
   - Download the JSON file
4. Update your `.env` file with the credentials

### Firestore Security Rules

The `firestore.rules` file provides:
- Public read access to shelter data
- Restricted write access (admin-only)
- Secure data protection

Deploy rules to Firebase:
```bash
firebase deploy --only firestore:rules
```

## 📊 Data Import (ETL)

### ArcGIS Integration

The ETL script (`scripts/etl_winter.mjs`) can import shelter data from ArcGIS:

```bash
# Run ETL script
node scripts/etl_winter.mjs

# Clear existing data and import
node scripts/etl_winter.mjs --clear
```

### Manual Data Entry

Shelters can be added manually through the admin panel or by updating the `data/winter_shelters.json` file.

## 🛠️ Development

### Adding New Features

1. **Frontend**: Modify files in the `web/` directory
2. **Backend**: Update `server/server.js` for new API endpoints
3. **Data**: Use the ETL script or admin panel for data management

### Testing

- **Local Testing**: Use the sample data in `data/winter_shelters.json`
- **API Testing**: Test endpoints using tools like Postman or curl
- **Frontend Testing**: Open browser developer tools for debugging

### Deployment

1. **Firebase Hosting** (Recommended):
   ```bash
   npm install -g firebase-tools
   firebase login
   firebase init hosting
   firebase deploy
   ```

2. **Other Platforms**: The application can be deployed to any Node.js hosting platform

## 🔒 Security Considerations

- **Environment Variables**: Never commit `.env` files to version control
- **Firebase Rules**: Regularly review and update Firestore security rules
- **API Keys**: Rotate API keys regularly and use least-privilege access
- **HTTPS**: Always use HTTPS in production

## 📱 Mobile Support

The application is fully responsive and works on:
- iOS Safari
- Android Chrome
- Mobile browsers

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is created for the Congressional App Challenge.

## 🆘 Support

For support or questions:
- Check the documentation
- Review the code comments
- Contact the development team

## 🔄 Updates

- **v1.0.0**: Initial release with basic shelter finder functionality
- **v1.1.0**: Added admin panel and ETL capabilities
- **v1.2.0**: Enhanced security and mobile responsiveness

---

**Built with ❤️ for the Congressional App Challenge**
