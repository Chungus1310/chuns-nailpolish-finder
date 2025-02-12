# 🛍️ Multi-Market Product Finder

A beautiful web application that helps you find products across multiple marketplaces! Built with Flask, modern CSS animations, and real-time product scraping from Amazon and Yandex Market.

# Demo



https://github.com/user-attachments/assets/527bf45c-9aff-4b63-97fb-7cd9cbbe5856



## ✨ Features

- 🎨 Interactive color picker with real-time color name conversion
- 🌈 Beautiful gradient animations and particle effects
- 🔍 Live product search on multiple marketplaces:
  - Amazon
  - Yandex Market
- 📱 Fully responsive design
- ✨ Modern UI with smooth animations
- 🛍️ Shows matching products with color context
- 💫 Elegant aesthetic with modern typography

## 🚀 Tech Stack

- **Backend:** Python with Flask
- **Frontend:** HTML5, CSS3, JavaScript
- **Styling:** Custom CSS with animations
- **Color Names:** ntc.js (Name That Color)
- **Scraping:** BeautifulSoup4, Google Translator
- **Design:** Bootstrap 5

## 📁 Project Structure

```
amazon/
├── app.py                 # Flask application
├── amazon_scraper.py      # Amazon scraping functionality
├── yandex_scraper.py      # Yandex Market scraping functionality
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
- Handles API endpoints for multiple marketplaces
- Returns product results per search

#### `amazon_scraper.py`
- Scrapes Amazon for products
- Uses rotating user agents
- Extracts product details:
  - Title
  - Price
  - Rating
  - Reviews count
  - Image URL
  - Product URL

#### `yandex_scraper.py`
- Scrapes Yandex Market for products
- Translates search queries to Russian
- Extracts similar product details
- Handles international market specifics

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
3. User can choose between Amazon or Yandex Market
4. Backend scrapes selected marketplace for matching products
5. Results are displayed in a responsive grid
6. Users can click products to view on respective marketplace

## 📱 Responsive Design

- Works on all screen sizes
- Mobile-friendly color picker
- Adaptive grid layout
- Touch-friendly interface
- Optimized loading states

## 🌍 International Support

- Multi-marketplace integration
- Automatic query translation for Yandex Market
- Support for different currencies and formats
- Cross-border product discovery

## 🤝 Contributing

Feel free to:
- Open issues
- Submit pull requests
- Suggest new features
- Report bugs
- Improve documentation

## 📝 Notes

- The scrapers respect marketplace terms of service
- Color names are approximate
- Product availability may vary by region
- Requires active internet connection
- Yandex Market results are translated from Russian

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
````
