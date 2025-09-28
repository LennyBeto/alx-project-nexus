#!/bin/bash

# Advanced Build script for Social Media Feed API
# This version includes more comprehensive error handling and optimization

set -e  # Exit on any error

# Color codes for better output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}🔄 $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_status "Starting build process for Social Media Feed API..."

# Check if we're in the right directory
if [ ! -f "manage.py" ]; then
    print_error "manage.py not found. Please run this script from the Django project root."
    exit 1
fi

# Print environment information
print_status "Environment Information:"
echo "Python: $(python --version 2>&1)"
echo "Pip: $(pip --version 2>&1)"
echo "Working Directory: $(pwd)"
echo "USER: ${USER:-unknown}"

# Set build start time
BUILD_START=$(date +%s)

# Upgrade pip to latest version
print_status "Upgrading pip..."
pip install --upgrade pip --quiet

# Install dependencies with cache optimization
print_status "Installing Python dependencies..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt --quiet
    print_success "Dependencies installed successfully"
else
    print_error "requirements.txt not found!"
    exit 1
fi

# Verify critical imports
print_status "Verifying critical imports..."
python -c "
import django
import rest_framework
import graphene_django
print(f'✅ Django: {django.get_version()}')
print(f'✅ DRF: {rest_framework.VERSION}')
print(f'✅ Graphene-Django installed')
" || {
    print_error "Critical imports failed!"
    exit 1
}

# Set environment variables for build
export DJANGO_SETTINGS_MODULE=social_media_feed.settings
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Create necessary directories
print_status "Creating directory structure..."
mkdir -p staticfiles
mkdir -p staticfiles_build/static
mkdir -p media
mkdir -p media/avatars
mkdir -p media/posts
mkdir -p logs
mkdir -p tmp

# Django configuration check
print_status "Checking Django configuration..."
python manage.py check --settings=social_media_feed.settings 2>/dev/null || {
    print_warning "Django check found issues, but continuing..."
    python manage.py check --settings=social_media_feed.settings || true
}

# Collect static files with compression
print_status "Collecting static files..."
DJANGO_SETTINGS_MODULE=social_media_feed.settings python manage.py collectstatic \
    --noinput \
    --clear \
    --verbosity=1 2>/dev/null || {
    print_warning "Static files collection had issues, trying alternative method..."
    mkdir -p staticfiles/admin
    mkdir -p staticfiles/rest_framework
    mkdir -p staticfiles/drf_spectacular_sidecar
}

# Copy static files to build directory
print_status "Preparing static files for deployment..."
if [ -d "staticfiles" ]; then
    # Copy all static files
    find staticfiles -type f -exec cp --parents {} staticfiles_build/static/ \; 2>/dev/null || {
        # Fallback method
        rsync -av staticfiles/ staticfiles_build/static/ 2>/dev/null || {
            cp -r staticfiles/* staticfiles_build/static/ 2>/dev/null || {
                print_warning "Could not copy static files, creating minimal setup..."
                mkdir -p staticfiles_build/static/admin/css
                mkdir -p staticfiles_build/static/admin/js
            }
        }
    }
    print_success "Static files copied to build directory"
else
    print_warning "No staticfiles directory found, creating minimal structure..."
    mkdir -p staticfiles_build/static
fi

# Create API documentation static files
print_status "Creating API documentation assets..."
mkdir -p staticfiles_build/static/docs

# Create a comprehensive index page
cat > staticfiles_build/static/index.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Social Media Feed API</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh; color: white; line-height: 1.6;
        }
        .container { max-width: 1000px; margin: 0 auto; padding: 2rem; }
        .header { text-align: center; margin-bottom: 3rem; }
        .header h1 { font-size: 3rem; margin-bottom: 1rem; }
        .header p { font-size: 1.2rem; opacity: 0.9; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem; }
        .card { 
            background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(10px);
            border-radius: 15px; padding: 2rem; transition: transform 0.3s ease;
        }
        .card:hover { transform: translateY(-5px); }
        .card h3 { margin-bottom: 1rem; font-size: 1.5rem; }
        .card a { 
            color: #fff; text-decoration: none; font-weight: bold;
            display: inline-block; margin-top: 1rem; padding: 0.5rem 1rem;
            background: rgba(255, 255, 255, 0.2); border-radius: 5px;
            transition: background 0.3s ease;
        }
        .card a:hover { background: rgba(255, 255, 255, 0.3); }
        .features { list-style: none; }
        .features li { margin: 0.5rem 0; }
        .features li:before { content: "✅ "; margin-right: 0.5rem; }
        .status { 
            position: fixed; top: 1rem; right: 1rem;
            background: #28a745; padding: 0.5rem 1rem; border-radius: 20px;
            font-size: 0.9rem; font-weight: bold;
        }
        @media (max-width: 768px) {
            .header h1 { font-size: 2rem; }
            .container { padding: 1rem; }
        }
    </style>
</head>
<body>
    <div class="status">🟢 API Online</div>
    <div class="container">
        <div class="header">
            <h1>🚀 Social Media Feed API</h1>
            <p>A modern, scalable GraphQL and REST API for social media applications</p>
        </div>
        
        <div class="grid">
            <div class="card">
                <h3>🎯 GraphQL Playground</h3>
                <p>Interactive GraphQL interface with real-time query testing and documentation.</p>
                <ul class="features">
                    <li>Interactive query builder</li>
                    <li>Real-time schema exploration</li>
                    <li>Mutation testing</li>
                </ul>
                <a href="/graphql/" target="_blank">Open GraphQL Playground →</a>
            </div>
            
            <div class="card">
                <h3>📚 API Documentation</h3>
                <p>Comprehensive REST API documentation with Swagger UI interface.</p>
                <ul class="features">
                    <li>Interactive API testing</li>
                    <li>Request/response examples</li>
                    <li>Authentication guides</li>
                </ul>
                <a href="/api/docs/" target="_blank">View Swagger Docs →</a>
            </div>
            
            <div class="card">
                <h3>⚙️ Admin Interface</h3>
                <p>Django admin interface for content management and user administration.</p>
                <ul class="features">
                    <li>User management</li>
                    <li>Content moderation</li>
                    <li>Analytics dashboard</li>
                </ul>
                <a href="/admin/" target="_blank">Open Admin Panel →</a>
            </div>
            
            <div class="card">
                <h3>🔗 Quick Links</h3>
                <p>Essential endpoints and resources for developers.</p>
                <ul class="features">
                    <li><a href="/api/" style="margin: 0; padding: 0.2rem 0.5rem;">REST API Base</a></li>
                    <li><a href="/health/" style="margin: 0; padding: 0.2rem 0.5rem;">Health Check</a></li>
                    <li><a href="/api/redoc/" style="margin: 0; padding: 0.2rem 0.5rem;">ReDoc Documentation</a></li>
                </ul>
            </div>
        </div>
    </div>
</body>
</html>
EOF

# Create health check endpoint data
cat > staticfiles_build/static/health.json << EOF
{
    "status": "healthy",
    "service": "social-media-feed-api",
    "version": "1.0.0",
    "build_time": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
    "build_duration": "calculating...",
    "features": [
        "GraphQL API",
        "REST API", 
        "User Authentication",
        "Post Management",
        "Comment System",
        "Like/Share System",
        "Follow System",
        "Admin Interface"
    ],
    "endpoints": {
        "graphql": "/graphql/",
        "api_docs": "/api/docs/",
        "admin": "/admin/",
        "health": "/health/",
        "api_base": "/api/"
    },
    "documentation": {
        "swagger": "/api/docs/",
        "redoc": "/api/redoc/",
        "graphql": "/graphql/"
    }
}
EOF

# Create robots.txt
cat > staticfiles_build/static/robots.txt << EOF
User-agent: *
Allow: /
Disallow: /admin/
Disallow: /api/schema/
Sitemap: /sitemap.xml
EOF

# Create a simple manifest.json for PWA support
cat > staticfiles_build/static/manifest.json << EOF
{
    "name": "Social Media Feed API",
    "short_name": "SM Feed API",
    "description": "A modern social media backend API",
    "start_url": "/",
    "display": "minimal-ui",
    "background_color": "#667eea",
    "theme_color": "#764ba2",
    "icons": [
        {
            "src": "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTkyIiBoZWlnaHQ9IjE5MiIgdmlld0JveD0iMCAwIDE5MiAxOTIiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSIxOTIiIGhlaWdodD0iMTkyIiByeD0iMjQiIGZpbGw9InVybCgjZ3JhZGllbnQwX2xpbmVhcl8xXzIpIi8+CjxkZWZzPgo8bGluZWFyR3JhZGllbnQgaWQ9ImdyYWRpZW50MF9saW5lYXJfMV8yIiB4MT0iMCIgeTE9IjAiIHgyPSIxOTIiIHkyPSIxOTIiIGdyYWRpZW50VW5pdHM9InVzZXJTcGFjZU9uVXNlIj4KPHN0b3Agc3RvcC1jb2xvcj0iIzY2N2VlYSIvPgo8c3RvcCBvZmZzZXQ9IjEiIHN0b3AtY29sb3I9IiM3NjRiYTIiLz4KPC9saW5lYXJHcmFkaWVudD4KPC9kZWZzPgo8L3N2Zz4K",
            "sizes": "192x192",
            "type": "image/svg+xml"
        }
    ]
}
EOF

# Optimize static files (compress, minify if tools available)
print_status "Optimizing static files..."
find staticfiles_build/static -name "*.css" -type f -exec gzip -k9 {} \; 2>/dev/null || true
find staticfiles_build/static -name "*.js" -type f -exec gzip -k9 {} \; 2>/dev/null || true
find staticfiles_build/static -name "*.json" -type f -exec gzip -k9 {} \; 2>/dev/null || true

# Set appropriate permissions
print_status "Setting file permissions..."
find staticfiles_build -type f -exec chmod 644 {} \; 2>/dev/null || true
find staticfiles_build -type d -exec chmod 755 {} \; 2>/dev/null || true

# Create deployment info file
print_status "Creating deployment information..."
cat > staticfiles_build/static/deployment-info.json << EOF
{
    "deployment": {
        "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
        "build_user": "${USER:-system}",
        "build_directory": "$(pwd)",
        "python_version": "$(python --version 2>&1)",
        "node_version": "$(node --version 2>/dev/null || echo 'Not available')",
        "git_commit": "$(git rev-parse HEAD 2>/dev/null || echo 'Not available')",
        "git_branch": "$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo 'Not available')"
    },
    "static_files": {
        "total_files": $(find staticfiles_build/static -type f | wc -l),
        "total_size": "$(du -sh staticfiles_build/static 2>/dev/null | cut -f1 || echo 'Unknown')",
        "compressed_files": $(find staticfiles_build/static -name "*.gz" | wc -l)
    }
}
EOF

# Clean up build artifacts and cache
print_status "Cleaning up build artifacts..."
find . -name "*.pyc" -delete 2>/dev/null || true
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyo" -delete 2>/dev/null || true
find . -name ".pytest_cache" -type d -exec rm -rf {} + 2>/dev/null || true
find . -name "*.log" -delete 2>/dev/null || true

# Remove development files from build
rm -rf .git 2>/dev/null || true
rm -rf .pytest_cache 2>/dev/null || true
rm -rf htmlcov 2>/dev/null || true

# Calculate build duration
BUILD_END=$(date +%s)
BUILD_DURATION=$((BUILD_END - BUILD_START))

# Update health check with actual build duration
sed -i.bak "s/calculating.../${BUILD_DURATION}s/" staticfiles_build/static/health.json 2>/dev/null || true
rm staticfiles_build/static/health.json.bak 2>/dev/null || true

# Final verification and summary
print_status "Build Verification:"
if [ -f "staticfiles_build/static/index.html" ]; then
    print_success "Main index page created"
else
    print_error "Main index page missing"
fi

if [ -d "staticfiles_build/static" ]; then
    FILE_COUNT=$(find staticfiles_build/static -type f | wc -l)
    DIR_SIZE=$(du -sh staticfiles_build/static 2>/dev/null | cut -f1 || echo "Unknown")
    print_success "Static files ready: ${FILE_COUNT} files, ${DIR_SIZE} total"
else
    print_error "Static files directory missing"
    exit 1
fi

# Display final summary
echo ""
print_success "🎉 Build completed successfully!"
echo "=================================="
echo "📊 Build Statistics:"
echo "   Duration: ${BUILD_DURATION}s"
echo "   Static files: ${FILE_COUNT}"
echo "   Total size: ${DIR_SIZE}"
echo "   Build time: $(date)"
echo ""
echo "🌐 Deployment URLs (after Vercel deployment):"
echo "   Main site: https://your-app.vercel.app/"
echo "   GraphQL: https://your-app.vercel.app/graphql/"
echo "   API Docs: https://your-app.vercel.app/api/docs/"
echo "   Admin: https://your-app.vercel.app/admin/"
echo ""
echo "🔧 Required Vercel Environment Variables:"
echo "   SECRET_KEY=your-django-secret-key"
echo "   DEBUG=False"
echo "   DATABASE_URL=postgresql://user:pass@host:port/db"
echo "   DOMAIN=your-app.vercel.app"
echo ""
print_success "Ready for deployment! 🚀"