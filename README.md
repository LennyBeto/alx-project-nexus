# Social Media Feed Backend

A modern, scalable, and feature-rich social media backend API built with Django, offering both GraphQL and REST interfaces. Perfect for building social media applications, community platforms, and content management systems.

 ✨ Features
🔧 Core Functionality

📝 Post Management - Create, edit, delete posts with rich content support
💬 Comment System - Nested comments and replies with threading
❤️ Like System - Like posts and comments with real-time counters
🔄 Share System - Share posts with optional custom messages
👥 Follow System - Follow users and personalized feeds
👤 User Profiles - Extended profiles with bio, location, and statistics

🎯 API Interfaces

🚀 GraphQL API - Flexible querying with GraphQL Playground
📊 REST API - Full CRUD operations with DRF
📚 Interactive Documentation - Swagger UI and ReDoc
🔐 Authentication Ready - JWT and session-based auth
🌐 CORS Configured - Frontend integration ready

⚡ Performance & Scalability

🗃️ Optimized Database - Strategic indexes and denormalized counters
🧮 Efficient Queries - Prefetch and select_related optimization
📄 Pagination - Built-in pagination for large datasets
🗑️ Soft Delete - Data integrity with recoverable deletions
📊 Real-time Counters - Automatic like/comment/follow counting

🛠️ Developer Experience

🎨 Admin Interface - Enhanced Django admin with custom views
🧪 Sample Data - Management command for realistic test data
📈 Health Monitoring - Built-in health checks and status endpoints
🔄 Signal Handlers - Automatic data consistency maintenance
📝 Comprehensive Logging - Detailed logging and error tracking

🌐 Deployment Ready

☁️ Vercel Optimized - Production-ready deployment configuration
🐳 Docker Support - Containerized development and deployment
🔒 Security Hardened - Production security settings configured
📦 Static Files - Optimized static file handling with WhiteNoise

🏗️ Technology Stack
ComponentTechnologyPurposeBackend FrameworkDjango 4.2.7Web framework and ORMAPI LayerDjango REST FrameworkREST API endpointsGraphQLGraphene-DjangoGraphQL API implementationDatabasePostgreSQL / SQLiteData persistenceAuthenticationDjango Auth + JWTUser authenticationDocumentationdrf-spectacularOpenAPI/Swagger docsFile HandlingPillow + WhiteNoiseImage processing and static filesCORSdjango-cors-headersCross-origin resource sharingDeploymentVercelCloud deployment platform
📁 Project Structure
alx-project-nexus/
├── 📁 social_media_feed/          # Django project configuration
│   ├── ⚙️ settings.py             # Django settings with environment support
│   ├── 🌐 urls.py                 # Main URL routing
│   └── 🚀 wsgi.py                 # WSGI application
├── 📁 feed/                       # Main application
│   ├── 🗃️ models.py               # Database models with optimizations
│   ├── 🎯 schema.py               # GraphQL schema and queries
│   ├── 🔄 mutations.py            # GraphQL mutations
│   ├── 🎨 types.py                # GraphQL type definitions
│   ├── 📊 serializers.py          # REST API serializers
│   ├── 🌐 api_views.py            # REST API views
│   ├── 🔗 urls.py                 # App URL routing
│   ├── 👨‍💼 admin.py                # Enhanced admin interface
│   ├── ⚡ signals.py              # Database signal handlers
│   └── 📁 management/commands/    # Custom management commands
│       └── 🎭 create_sample_data.py
├── 📋 requirements.txt            # Python dependencies
├── ⚙️ .env.example               # Environment configuration template
├── 🔧 vercel.json                # Vercel deployment config
├── 🏗️ build_files.sh             # Build script for deployment
├── 🐳 Dockerfile                 # Docker configuration (optional)
└── 📖 README.md                  # Project documentation

🚀 Quick Start
1️⃣ Clone and Setup
bash# Clone the repository
git clone https://github.com/LennyBeto/alx-project-nexus.git
cd alx-project-nexus

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
2️⃣ Environment Configuration
bash# Copy environment template
cp .env.example .env

# Edit with your settings (essential variables)
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=  # Leave empty for SQLite development
3️⃣ Database Setup
bash# Create and apply migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser for admin access
python manage.py createsuperuser

# Generate sample data (optional)
python manage.py create_sample_data --users 10 --posts 50 --comments 100
4️⃣ Launch Development Server
bash# Start the development server
python manage.py runserver

# Server will be available at http://localhost:8000/
🌍 API Endpoints
🏠 Main Endpoints
EndpointDescriptionDocumentation/API information and statusLanding page with links/health/Health check endpointService status/admin/Django admin interfaceContent management
🎯 GraphQL API
EndpointDescriptionFeatures/graphql/GraphQL PlaygroundInteractive queries, schema exploration
graphql# Example: Get posts with author info
query GetPosts {
  posts(limit: 10) {
    id
    content
    createdAt
    likesCount
    commentsCount
    author {
      username
      profile {
        bio
        followersCount
      }
    }
    isLikedByUser
  }
}

# Example: Create a post
mutation CreatePost {
  createPost(content: "Hello, GraphQL world!") {
    success
    message
    post {
      id
      content
      author {
        username
      }
    }
  }
}
📊 REST API Endpoints
MethodEndpointDescriptionAuth RequiredGET/api/posts/List posts with pagination❌POST/api/posts/Create new post✅GET/api/posts/{id}/Get specific post❌PUT/api/posts/{id}/Update post (owner only)✅DELETE/api/posts/{id}/Delete post (owner only)✅POST/api/posts/{id}/like/Toggle like on post✅GET/api/posts/{id}/comments/Get post comments❌POST/api/posts/{id}/comments/Add comment to post✅GET/api/feed/Get personalized feed✅GET/api/trending/Get trending posts❌GET/api/users/List users❌POST/api/users/{id}/follow/Toggle follow user✅GET/api/profile/Get own profile✅PUT/api/profile/Update own profile✅
📚 API Documentation
EndpointDescriptionFeatures/api/docs/Swagger UIInteractive API testing/api/redoc/ReDoc documentationClean API reference/api/schema/OpenAPI schemaMachine-readable spec
🗃️ Database Models
👤 User & Profile Models

User - Django's built-in user model
UserProfile - Extended profile (bio, location, avatar, counters)

📝 Content Models

Post - User posts with content, images, engagement counters
Comment - Comments with nested reply support
Like - Flexible like system for posts and comments
Share - Post sharing with optional messages
Follow - User following relationships

🔢 Key Features

Soft Delete - Recoverable content deletion
Denormalized Counters - Fast engagement metrics
Database Indexes - Optimized query performance
Signal Handlers - Automatic counter maintenance
Constraints - Data integrity enforcement

🎭 Sample Data
Generate realistic test data for development:
bash# Generate sample data with custom parameters
python manage.py create_sample_data \
    --users 20 \
    --posts 100 \
    --comments 200 \
    --clear  # Optional: clear existing data

# Quick setup with defaults
python manage.py create_sample_data

# The command creates:
# - Users with realistic profiles (names, bios, locations)
# - Posts with varied content types
# - Comments and nested replies
# - Random likes, follows, and shares
# - Realistic engagement patterns
🔐 Authentication
🎫 Available Methods

Session Authentication - Web-based authentication
Token Authentication - API token-based auth
JWT Ready - JSON Web Token support configured

🔓 Usage Examples
REST API with Session Auth:
bash# Login via Django admin first, then:
curl -H "Content-Type: application/json" \
     -X POST \
     -d '{"content": "My first API post!"}' \
     http://localhost:8000/api/posts/
GraphQL with Authentication:
graphql# After logging in via admin interface
mutation {
  createPost(content: "GraphQL post with auth") {
    success
    message
    post {
      id
      content
    }
  }
}
🚀 Deployment
☁️ Vercel Deployment (Recommended)

Prepare Database:

bash   # Get PostgreSQL database URL from:
   # - Supabase: https://supabase.com/
   # - Railway: https://railway.app/
   # - ElephantSQL: https://www.elephantsql.com/

Deploy to Vercel:

bash   # Install Vercel CLI
   npm i -g vercel
   
   # Login and deploy
   vercel login
   vercel --prod

Set Environment Variables in Vercel Dashboard:

bash   SECRET_KEY=your-production-secret-key
   DEBUG=False
   DATABASE_URL=postgresql://user:pass@host:port/db
   DOMAIN=your-app.vercel.app
   ALLOWED_HOSTS=your-app.vercel.app

Run Initial Setup:

bash   # After deployment, run migrations via your database management tool
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py create_sample_data  # Optional
🐳 Docker Deployment
bash# Build and run with Docker
docker build -t social-media-api .
docker run -p 8000:8000 social-media-api

# Or use Docker Compose
docker-compose up --build
🌐 Production Checklist

✅ Set DEBUG=False
✅ Configure secure SECRET_KEY
✅ Set proper ALLOWED_HOSTS
✅ Configure production database
✅ Enable HTTPS settings
✅ Set restrictive CORS origins
✅ Configure email backend
✅ Set up error monitoring (Sentry)
✅ Configure static file serving
✅ Set up regular backups

🧪 Testing & Development
🔍 API Testing
GraphQL Playground:
http://localhost:8000/graphql/
REST API Testing:
bash# Get posts
curl http://localhost:8000/api/posts/

# Get API documentation
curl http://localhost:8000/api/docs/

# Health check
curl http://localhost:8000/health/
Interactive Testing:

Swagger UI: http://localhost:8000/api/docs/
ReDoc: http://localhost:8000/api/redoc/
Django Admin: http://localhost:8000/admin/

🛠️ Development Commands
bash# Database operations
python manage.py makemigrations
python manage.py migrate
python manage.py dbshell

# Create users
python manage.py createsuperuser
python manage.py create_sample_data

# Development server
python manage.py runserver
python manage.py runserver 0.0.0.0:8000  # Allow external connections

# Static files
python manage.py collectstatic
python manage.py findstatic admin/css/base.css

# Shell access
python manage.py shell
python manage.py shell_plus  # If django-extensions installed

# Check configuration
python manage.py check
python manage.py check --deploy  # Production readiness
🎨 Customization
🔧 Adding New Features

Create new models in feed/models.py:

python   class NewModel(models.Model):
       # Your fields here
       pass

Add GraphQL types in feed/types.py:

python   class NewModelType(DjangoObjectType):
       class Meta:
           model = NewModel

Create mutations in feed/mutations.py:

python   class CreateNewModel(graphene.Mutation):
       # Your mutation logic
       pass

Add REST serializers in feed/serializers.py:

python   class NewModelSerializer(serializers.ModelSerializer):
       class Meta:
           model = NewModel
           fields = '__all__'
⚙️ Environment Configuration
The project supports multiple environments:

Development: SQLite, debug mode, permissive CORS
Production: PostgreSQL, security settings, restrictive CORS
Docker: Container-optimized settings
Testing: Isolated test database, fast settings

🤝 Contributing
We welcome contributions! Here's how to get started:

Fork the Repository

bash   git fork https://github.com/LennyBeto/alx-project-nexus.git

Create Feature Branch

bash   git checkout -b feature/amazing-feature

Make Changes and Test

bash   python manage.py test
   python manage.py check

Commit with Conventional Commits

bash   git commit -m "feat: add amazing new feature"
   git commit -m "fix: resolve authentication issue"
   git commit -m "docs: update API documentation"

Push and Create PR

bash   git push origin feature/amazing-feature
📝 Commit Message Format

feat: - New features
fix: - Bug fixes
docs: - Documentation updates
style: - Code style changes
refactor: - Code refactoring
perf: - Performance improvements
test: - Adding tests
chore: - Maintenance tasks

🐛 Troubleshooting
Common Issues and Solutions
🔴 ModuleNotFoundError:
bash# Ensure __init__.py files exist
touch social_media_feed/__init__.py
touch feed/__init__.py
touch feed/management/__init__.py
touch feed/management/commands/__init__.py
🔴 Database Connection Error:
bash# For SQLite (development)
DATABASE_URL=  # Leave empty in .env

# For PostgreSQL
DATABASE_URL=postgresql://user:pass@host:port/db
🔴 Static Files Not Loading:
bashpython manage.py collectstatic --noinput
chmod +x build_files.sh
./build_files.sh
🔴 CORS Issues:
python# In .env file
CORS_ALLOW_ALL_ORIGINS=True  # Development only
CORS_ALLOWED_ORIGINS=https://your-frontend.com  # Production
🔴 Migration Issues:
bash# Reset migrations (development only)
rm -rf feed/migrations/
python manage.py makemigrations feed
python manage.py migrate
📊 Performance & Monitoring
🚀 Performance Features

Database Indexing - Strategic indexes on frequently queried fields
Query Optimization - Prefetch and select_related usage
Denormalized Counters - Fast engagement metrics
Pagination - Efficient large dataset handling
Caching Ready - Redis integration support

📈 Monitoring Endpoints

/health/ - Health check with system status
/api/ - API information and statistics
Django Admin - Built-in analytics and user management

🔍 Logging Configuration
python# Configured log levels and outputs
# - Console logging for development
# - File logging for production
# - Error tracking with Sentry (optional)
# - Request/response logging
# - Database query logging (development)
📄 License
This project is licensed under the MIT License - see the LICENSE file for details.
🙏 Acknowledgments

Django - The web framework for perfectionists with deadlines
Django REST Framework - Powerful and flexible toolkit for building Web APIs
Graphene-Django - GraphQL framework for Django
PostgreSQL - The world's most advanced open source database
Vercel - The platform for frontend developers (and full-stack too!)

📞 Support & Community

📧 Issues: GitHub Issues
💬 Discussions: GitHub Discussions
📖 Wiki: Project Wiki
🐛 Bug Reports: Use GitHub Issues with bug template
💡 Feature Requests: Use GitHub Issues with feature template

🗺️ Roadmap
🎯 Version 1.1 (Planned)

 WebSocket support for real-time notifications
 Advanced search with full-text search capabilities
 Image upload and processing
 Content moderation system
 Rate limiting and throttling
 Email notifications

🎯 Version 1.2 (Future)

 Mobile push notifications
 Advanced analytics and insights
 Content recommendation engine
 Multi-language support
 Advanced privacy controls
 API versioning


<div align="center">
🚀 Ready to build the next great social platform?
⭐ Star this repository • 🍴 Fork it • 📖 Read the Docs
Made with ❤️ by LennyBeto
</div>
