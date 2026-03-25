# Patient Management System - Frontend 🏥

A responsive, mobile-friendly web frontend for the Patient Management API built with **pure HTML, CSS, and JavaScript**. Perfect for GitHub Pages hosting!

## 📱 Features

- ✅ **Fully Responsive Design** - Works perfectly on desktop, tablet, and mobile
- ✅ **Pure HTML/CSS/JavaScript** - No frameworks, GitHub Pages compatible
- ✅ **Tailwind CSS** - Beautiful, responsive UI with Tailwind's utility classes
- ✅ **Real-time Updates** - Instant feedback on all operations
- ✅ **Complete CRUD Operations** - Create, Read, Update, Delete patients
- ✅ **Advanced Search** - Find patients by ID or name
- ✅ **Smart Sorting** - Sort by height, weight, or BMI
- ✅ **BMI Visualization** - Color-coded health status badges
- ✅ **Smooth Animations** - Delightful UI interactions
- ✅ **Mobile-Optimized** - Touch-friendly interface

## 📁 File Structure

```
FRONTEND/
├── index.html       # Main HTML file with all modals and structure
├── main.js          # Complete API integration and functionality
├── styles.css       # Custom styling and animations
└── README.md        # This file
```

## 🚀 Quick Start

### Option 1: Local Development

1. **Clone or download the FRONTEND folder**

   ```bash
   cd FRONTEND
   ```

2. **Open in browser**
   - Double-click `index.html`, OR
   - Use a local server:

     ```bash
     python -m http.server 8000
     # Then open http://localhost:8000
     ```

### Option 2: Deploy to GitHub Pages

1. **Create a new GitHub repository** (e.g., `patient-management-frontend`)

2. **Clone or push the FRONTEND folder to GitHub**

   ```bash
   git clone https://github.com/YOUR_USERNAME/patient-management-frontend.git
   cd patient-management-frontend
   # Copy FRONTEND contents here
   git add .
   git commit -m "Initial commit: Patient Management Frontend"
   git push origin main
   ```

3. **Enable GitHub Pages**
   - Go to repository Settings → Pages
   - Select "Deploy from a branch"
   - Choose "main" branch → "/ (root)"
   - Click Save

4. **Access your frontend**
   - Your site will be live at: `https://YOUR_USERNAME.github.io/patient-management-frontend`
   - Alternatively: `https://YOUR_USERNAME.github.io/patient-management-frontend/index.html`

## 🔗 API Configuration

The frontend is configured to use the backend API at:

```
https://patient-management-app-rqjp.onrender.com
```

To change the API URL, edit `main.js`:

```javascript
const API_BASE_URL = 'https://your-api-url.com';
```

## 💻 Usage Guide

### 1. **Add a New Patient**

- Click the **"➕ Add Patient"** button
- Fill in all required fields:
  - Patient ID (e.g., P001)
  - Full Name
  - Age (1-119)
  - City
  - Gender
  - Height (in meters)
  - Weight (in kilograms)
- Click **"Save Patient"**
- BMI and health verdict are calculated automatically

### 2. **View All Patients**

- Click **"🔄 Refresh"** to reload
- All patients are displayed as cards
- Each card shows:
  - Patient name and ID
  - Age, city, weight, BMI
  - Health status with color-coded badge

### 3. **View Patient Details**

- Click the **"👁️ View"** button on any patient card
- See detailed information in a modal

### 4. **Edit Patient**

- Click the **"✏️ Edit"** button on any patient card
- Modify the information
- Click **"Update Patient"**
- BMI and verdict update automatically

### 5. **Delete Patient**

- Click the **"🗑️ Delete"** button
- Confirm deletion in the confirmation modal
- Patient is removed from the system

### 6. **Search Patients**

- Click **"🔍 Search"** button
- **Search by ID**: Enter Patient ID (e.g., P001)
- **Search by Name**: Enter full name
- Results appear instantly

### 7. **Sort Patients**

- Click **"📊 Sort"** button
- Select field: Height, Weight, or BMI
- Choose order: Ascending (⬆️) or Descending (⬇️)
- Results display sorted

## 🎨 UI Components

### Patient Cards

- Display patient summary with key metrics
- Color-coded BMI status badges
- Quick action buttons (View, Edit, Delete)
- Hover effects for better interactivity

### Modals

- **Add/Edit Patient Modal** - Form for patient data
- **Search Modal** - Search by ID or name
- **Sort Modal** - Configure sorting options
- **Patient Details Modal** - Full patient information
- **Delete Confirmation Modal** - Safety confirmation

### Alerts

- Green alerts for successful operations
- Red alerts for errors
- Auto-dismiss after 3 seconds

### Loading Indicator

- Shows during API calls
- Spinning animation
- Prevents user interaction during loading

## 📊 BMI Status Categories

| BMI Range | Verdict | Color |
|-----------|---------|-------|
| < 18.5 | 🟠 Underweight | Orange |
| 18.5 - 24.9 | 🟢 Normal | Green |
| 25 - 29.9 | 🟡 Overweight | Yellow |
| 30 - 34.9 | 🔴 Obese | Red |
| ≥ 35 | 🔴 Extremely Obese | Dark Red |

## 🛠️ Technologies Used

- **HTML5** - Semantic markup
- **CSS3** - Responsive design with Tailwind CSS
- **JavaScript (ES6+)** - Modern JavaScript for API integration
- **Tailwind CSS (CDN)** - Utility-first CSS framework
- **Fetch API** - For backend communication

## 📱 Browser Compatibility

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+
- Mobile browsers (iOS Safari, Chrome Mobile)

## 🔄 API Integration

The frontend communicates with the backend API using the Fetch API:

```javascript
// Example: Add new patient
fetch('https://patient-management-app-rqjp.onrender.com/new', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        id: 'P001',
        name: 'John Doe',
        age: 30,
        city: 'New York',
        gender: 'male',
        height: 1.75,
        weight: 75
    })
})
```

All API endpoints are fully implemented:

- ✅ GET /view - View all patients
- ✅ GET /patient/{id} - Search by ID
- ✅ GET /patient/name/{name} - Search by name
- ✅ GET /sort - Sort patients
- ✅ POST /new - Add patient
- ✅ PUT /update/{id} - Update patient
- ✅ DELETE /delete/{id} - Delete patient

## 🎯 Features Breakdown

### Search Functionality

- Real-time search with instant results
- Case-insensitive name search
- Quick access to patient details from search results

### Sorting Flexibility

- Sort by multiple fields
- Ascending/descending options
- Maintains all patient data during sorting

### Responsive Design

- Mobile-first approach
- Adaptive grid layouts
- Touch-friendly buttons and inputs
- Fast loading on all devices

### Error Handling

- Network error detection
- User-friendly error messages
- Automatic retry suggestions
- Graceful degradation

## 🚀 Performance

- Lightweight - No dependencies, minimal JavaScript
- Fast loading - Tailwind CSS from CDN
- Smooth animations - GPU-accelerated CSS transitions
- Efficient API calls - Batched operations when possible

## 📝 Notes

- All data is persisted in the backend (JSON file)
- Frontend is stateless - refresh friendly
- No local storage required
- Works offline with backend connectivity

## 🔐 Security Considerations

- No sensitive data stored locally
- All API calls use HTTPS (when deployed)
- Input validation on frontend (+ backend)
- CORS may need configuration on backend for GitHub Pages

## 🐛 Troubleshooting

### "Failed to load patients"

- Check internet connection
- Verify backend API is running
- Check console for CORS errors

### "API URL not found"

- Ensure `API_BASE_URL` in `main.js` is correct
- Verify backend is deployed and accessible
- Check browser console for specific errors

### Styles not loading

- Clear browser cache
- Hard refresh (Ctrl+Shift+R)
- Check browser console for CSS errors

### Buttons not responding

- Check JavaScript console for errors
- Verify API endpoint is accessible
- Ensure form fields are properly filled

## 📞 Support

For issues or questions:

1. Check console errors (F12 → Console)
2. Verify API URL is correct
3. Test API directly in Postman
4. Check backend logs for errors

## 🚀 Deployment Tips

### For GitHub Pages

1. Remove trailing slashes from paths
2. Ensure index.html is in repo root
3. Don't include build files
4. Test locally before deploying

### For Custom Domain

1. Add CNAME file with your domain
2. Update DNS records at registrar
3. Enable HTTPS in GitHub Pages settings

### For Better Performance

1. Minify CSS/JS (optional)
2. Optimize images if added
3. Use CDN for external resources
4. Enable caching headers

## 📚 Resources

- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [MDN Web Docs](https://developer.mozilla.org/)
- [GitHub Pages Guide](https://pages.github.com/)
- [Fetch API Guide](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API)

## 📄 License

This frontend is free to use and modify for your projects.

---

**Happy Patient Management! 🎉**

*Built with ❤️ using HTML, CSS, and JavaScript*

**Version:** 1.0.0  
**Last Updated:** March 2026
