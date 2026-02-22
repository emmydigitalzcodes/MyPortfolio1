# Django Developer Portfolio

A modern, professional portfolio website built with Django to showcase your skills as a Django web developer.

![Django Version](https://img.shields.io/badge/django-4.x-green)
![Python Version](https://img.shields.io/badge/python-3.8+-blue)
![License](https://img.shields.io/badge/license-MIT-yellow)

## Features

### Core Features
- **Home Page** - Hero section with animated background, skills showcase, featured projects, services, testimonials, and blog preview
- **About Page** - Detailed about section with experience timeline, education, certifications, and skills
- **Projects Showcase** - Grid view with filtering by category/technology, search functionality, and detailed project pages
- **Blog/Articles** - Full-featured blog with categories, tags, search, and newsletter subscription
- **Contact Form** - Contact form with email notifications, FAQs, and social links

### Technical Features
- Responsive design with Bootstrap 5
- Dark/Light mode toggle
- Smooth animations with AOS
- SEO optimization (meta tags, sitemap, robots.txt)
- Google Analytics integration
- reCAPTCHA spam protection
- Custom Django admin interface
- Contact form with email notifications

## Tech Stack

- **Backend**: Django 4.x
- **Frontend**: Bootstrap 5, Font Awesome, AOS Animation
- **Database**: SQLite (development), PostgreSQL (production)
- **Deployment**: WhiteNoise for static files, Gunicorn

## Installation

### Prerequisites
- Python 3.8+
- pip
- virtualenv (recommended)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/django-portfolio.git
   cd django-portfolio
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create environment variables**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` file with your settings:
   ```
   DJANGO_SECRET_KEY=your-secret-key-here
   DJANGO_DEBUG=True
   DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
   
   # Email settings (optional)
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password
   
   # reCAPTCHA (optional)
   RECAPTCHA_PUBLIC_KEY=your-recaptcha-site-key
   RECAPTCHA_PRIVATE_KEY=your-recaptcha-secret-key
   
   # Google Analytics (optional)
   GOOGLE_ANALYTICS_ID=G-XXXXXXXXXX
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Collect static files**
   ```bash
   python manage.py collectstatic
   ```

8. **Run development server**
   ```bash
   python manage.py runserver
   ```

9. **Access the site**
   - Website: http://127.0.0.1:8000/
   - Admin: http://127.0.0.1:8000/admin/

## Project Structure

```
portfolio/
├── home/                   # Home app (about, skills, experience)
│   ├── models.py          # Skill, Experience, Education models
│   ├── views.py           # Home, About views
│   └── admin.py           # Admin configuration
├── projects/              # Projects app
│   ├── models.py          # Project, Technology models
│   ├── views.py           # Project list/detail views
│   └── admin.py           # Admin configuration
├── blog/                  # Blog app
│   ├── models.py          # Post, Category, Tag models
│   ├── views.py           # Blog list/detail views
│   └── admin.py           # Admin configuration
├── contact/               # Contact app
│   ├── models.py          # ContactMessage, FAQ models
│   ├── forms.py           # Contact form
│   └── views.py           # Contact view
├── templates/             # HTML templates
├── static/                # CSS, JS, images
├── media/                 # User-uploaded files
├── portfolio/             # Project settings
│   ├── settings.py
│   ├── urls.py
│   └── sitemaps.py
└── manage.py
```

## Configuration

### Adding Your Information

1. **Personal Info**: Go to Django Admin > Home > Personal Info
   - Add your name, title, bio, profile photo, resume
   - Configure social links (GitHub, LinkedIn, Twitter)

2. **Site Configuration**: Go to Django Admin > Home > Site Configuration
   - Set site name, tagline, description
   - Enable/disable features (dark mode, blog, contact form)

3. **Contact Info**: Go to Django Admin > Contact > Contact Info
   - Add email, phone, address
   - Configure social media links

### Adding Content

#### Skills
- Go to Django Admin > Home > Skill Categories
- Create categories (e.g., Backend, Frontend, DevOps)
- Add skills with proficiency levels

#### Projects
- Go to Django Admin > Projects > Projects
- Add projects with screenshots, descriptions, technologies
- Set featured status for homepage display

#### Blog Posts
- Go to Django Admin > Blog > Posts
- Create posts with categories and tags
- Set featured status for homepage display

#### Experience
- Go to Django Admin > Home > Experience
- Add work history with dates and descriptions

#### Education & Certifications
- Go to Django Admin > Home > Education/Certifications
- Add academic background and professional certifications

## Deployment

### Deploying to PythonAnywhere

1. Create a PythonAnywhere account
2. Upload your code via Git or ZIP
3. Create a virtual environment and install dependencies
4. Set up environment variables in `.env`
5. Configure the WSGI file
6. Collect static files
7. Set up the database

### Deploying to Heroku

1. Install Heroku CLI and login
2. Create a `Procfile`:
   ```
   web: gunicorn portfolio.wsgi
   ```
3. Create a `runtime.txt`:
   ```
   python-3.11.0
   ```
4. Deploy:
   ```bash
   heroku create your-app-name
   git push heroku main
   heroku run python manage.py migrate
   heroku run python manage.py createsuperuser
   ```

### Production Settings

Update `settings.py` for production:
- Set `DEBUG = False`
- Configure `ALLOWED_HOSTS`
- Set up PostgreSQL database
- Configure AWS S3 or similar for media files
- Set up SSL/HTTPS

## Customization

### Changing Colors
Edit `static/css/main.css` and modify CSS variables:
```css
:root {
    --primary-color: #your-color;
    --secondary-color: #your-color;
    /* ... */
}
```

### Adding New Pages
1. Create view in appropriate `views.py`
2. Add URL pattern in `urls.py`
3. Create template in `templates/`

### Modifying Templates
All templates use Bootstrap 5 classes. Edit files in `templates/` directory.

## SEO Optimization

The portfolio includes:
- Meta tags for all pages
- Open Graph tags for social sharing
- Twitter Card support
- XML sitemap at `/sitemap.xml`
- Robots.txt at `/robots.txt`
- Canonical URLs
- Structured data ready for implementation

## Performance

- Static files served with WhiteNoise
- Optimized images with lazy loading
- Minified CSS and JS
- Database query optimization with `select_related` and `prefetch_related`

## Security

- CSRF protection enabled
- XSS prevention
- Secure file uploads
- Environment variables for sensitive data
- HTTPS enforcement in production

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, email your-email@example.com or open an issue on GitHub.

## Acknowledgments

- Bootstrap 5 for the UI framework
- Font Awesome for icons
- AOS for scroll animations
- Django community for the amazing framework
