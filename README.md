# 💅 Chun's Nail Polish Finder

A beautiful web application that helps you find the perfect nail polish by selecting any color! Built with Flask, modern CSS animations, and real-time Amazon product scraping.

## ✨ Features

- 🎨 Interactive color picker with real-time color name conversion
- 🌈 Beautiful gradient animations and particle effects
- 🔍 Live Amazon product search
- 📱 Fully responsive design
- ✨ Modern UI with smooth animations
- 🛍️ Shows 18 matching nail polish products
- 💫 Feminine aesthetic with elegant typography

## 🚀 Tech Stack

- **Backend:** Python with Flask
- **Frontend:** HTML5, CSS3, JavaScript
- **Styling:** Custom CSS with animations
- **Color Names:** ntc.js (Name That Color)
- **Scraping:** BeautifulSoup4
- **Design:** Bootstrap 5

## 📁 Project Structure

```
amazon/
├── app.py                 # Flask application
├── amazon_scraper.py      # Amazon scraping functionality
├── requirements.txt       # Python dependencies
├── ntc.js                # Color name conversion library
├── static/
│   ├── css/
│   │   └── style.css     # Custom styling and animations
│   └── js/
│       ├── app.js        # Main frontend logic
│       ├── ntc.js        # Color naming functionality
│       └── particles.js   # Background particle animations
└── templates/
    └── index.html        # Main HTML template
```

## 🛠️ Setup & Installation

1. Clone the repository:
```bash
git clone https://github.com/Chungus1310/chuns-nailpolish-finder.git
cd chuns-nailpolish-finder
```

2. Install required Python packages:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and visit:
```
http://localhost:5000
```

## 📦 Key Components

### Backend (Python)

#### `app.py`
- Main Flask application
- Serves the frontend
- Handles API endpoints
- Returns 18 product results per search

#### `amazon_scraper.py`
- Scrapes Amazon for nail polish products
- Uses rotating user agents
- Extracts product details:
  - Title
  - Price
  - Rating
  - Reviews count
  - Image URL
  - Product URL

### Frontend

#### `templates/index.html`
- Modern, responsive layout
- Integration with Bootstrap
- Custom fonts (Playfair Display, Poppins, Dancing Script)
- Dynamic color picker interface

#### `static/css/style.css`
- Custom animations and transitions
- Gradient backgrounds
- Glassmorphism effects
- Responsive design
- Hover effects and micro-interactions

#### `static/js/app.js`
- Color picker functionality
- Real-time color name updates
- Product grid management
- Loading states
- Smooth scrolling

#### `static/js/particles.js`
- Interactive background particles
- Mouse-following effects
- Floating animations

## 🎨 UI Features

- Animated gradient background
- Interactive color picker with glow effect
- Floating particles with mouse interaction
- Elegant typography with mixed fonts
- Product cards with hover animations
- Loading spinner with gradient effect
- Smooth transitions and fade effects
- Responsive grid layout

## 🔄 How It Works

1. User selects a color using the color picker
2. Color is converted to a name using ntc.js
3. Backend scrapes Amazon for matching products
4. Results are displayed in a responsive grid
5. Users can click products to view on Amazon

## 📱 Responsive Design

- Works on all screen sizes
- Mobile-friendly color picker
- Adaptive grid layout
- Touch-friendly interface
- Optimized loading states

## 🤝 Contributing

Feel free to:
- Open issues
- Submit pull requests
- Suggest new features
- Report bugs
- Improve documentation

## 📝 Notes

- The scraper respects Amazon's terms of service
- Color names are approximate
- Product availability may vary
- Requires active internet connection

## 🎉 Credits

- **Author:** Chun
- Color naming: [ntc.js](http://chir.ag/projects/ntc/)
- Icons: Bootstrap Icons
- Fonts: Google Fonts
- Particles Effect: Custom implementation

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---
Made with ❤️ by Chun
