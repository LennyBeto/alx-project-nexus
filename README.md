# Social Media Feed Backend

A scalable GraphQL-based backend for social media applications built with Django and PostgreSQL.

## 🚀 Features 

- **GraphQL API**: Flexible querying with GraphQL and Graphene-Django
- **Post Management**: Create, read, update, and delete posts
- **User Interactions**: Like, comment, and share posts
- **Social Features**: Follow/unfollow users, personalized feeds
- **Real-time Data**: Optimized queries for high-traffic applications
- **Admin Interface**: Django admin for content management
- **Database Optimization**: Indexed fields and denormalized counters for performance

## 🛠 Technologies Used

- **Backend**: Django 4.2.7
- **Database**: PostgreSQL (production) / SQLite (development)
- **API**: GraphQL with Graphene-Django
- **Deployment**: Vercel
- **Additional**: CORS support, WhiteNoise for static files

## 📊 Database Schema

### Models

- **Post**: User posts with content, images, and interaction counters
- **Comment**: Comments and replies on posts
- **Like**: Like system for posts and comments
- **Share**: Post sharing functionality
- **Follow**: User following relationships

## 🏃‍♂️ Quick Start

### Local Development

1. **Clone the repository**
```bash
git clone <repository-url>
cd social_media_backend
```

2. **Set up virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
# Create .env file
cp .env.example .env
# Edit .env with your database credentials
```

5. **Set up database**
```bash
# For PostgreSQL (recommended for production-like testing)
createdb social_media_db

# For SQLite (quick setup), uncomment SQLite config in settings.py
```

6. **Run migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

7. **Create superuser**
```bash
python manage.py createsuperuser
```

8. **Create sample data (optional)**
```bash
python manage.py create_sample_data --users 10 --posts 50 --comments 100
```

9. **Start development server**
```bash
python manage.py runserver
```

10. **Access GraphQL Playground**
Visit: `http://localhost:8000/graphql/`

## 🚀 Deployment on Vercel

### Prerequisites
- Vercel account
- PostgreSQL database (recommend: Railway, Supabase, or ElephantSQL)

### Steps

1. **Prepare your database**
   - Create a PostgreSQL database
   - Note the DATABASE_URL connection string

2. **Deploy to Vercel**
```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy
vercel --prod
```

3. **Configure environment variables in Vercel**
   - Go to your Vercel project dashboard
   - Add these environment variables:
     - `DATABASE_URL`: Your PostgreSQL connection string
     - `SECRET_KEY`: Django secret key
     - `DEBUG`: `False`

4. **Run initial setup**
   After deployment, run migrations:
```bash
# You may need to run these commands via Vercel CLI or database management tool
python manage.py migrate
python manage.py createsuperuser
python manage.py create_sample_data
```

## 🔍 API Usage

### GraphQL Endpoint
- **Development**: `http://localhost:8000/graphql/`
- **Production**: `https://your-app.vercel.app/graphql/`

### Sample Queries

#### Get Posts
```graphql
query GetPosts {
  posts(limit: 10) {
    id
    content
    createdAt
    likesCount
    commentsCount
    author {
      username
      fullName
    }
  }
}
```

#### Create Post
```graphql
mutation CreatePost {
  createPost(content: "Hello, World!") {
    success
    message
    post {
      id
      content
      createdAt
    }
  }
}
```

#### Like Post
```graphql
mutation LikePost {
  likePost(postId: 1) {
    success
    message
  }
}
```

### Authentication
Currently, the API uses Django's built-in authentication. For production, consider implementing JWT or session-based authentication.

## 🔧 Development Commands

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Create sample data
python manage.py create_sample_data

# Run development server
python manage.py runserver

# Collect static files
python manage.py collectstatic

# Access Django admin
# Visit: http://localhost:8000/admin/
```

## 📈 Performance Optimization

- **Database Indexes**: Strategic indexes on frequently queried fields
- **Denormalized Counters**: Likes, comments, and shares counts stored directly on posts
- **Query Optimization**: Prefetch and select_related for efficient database queries
- **Pagination**: Built-in pagination for large datasets

## 🧪 Testing

Access the GraphQL Playground to test all queries and mutations interactively:
- Development: `http://localhost:8000/graphql/`
- Production: Your deployed URL + `/graphql/`

## 📝 Git Workflow

Follow the commit message format:
- `feat:` - New features
- `fix:` - Bug fixes
- `perf:` - Performance improvements
- `docs:` - Documentation updates
- `refactor:` - Code refactoring
- `test:` - Adding tests

### Example Commits
```bash
git add .
git commit -m "feat: set up Django project with PostgreSQL"
git commit -m "feat: create models for posts, comments, and interactions"
git commit -m "feat: implement GraphQL API for querying posts and interactions"
git commit -m "feat: integrate and publish GraphQL Playground"
git commit -m "perf: optimize database queries for interactions"
git commit -m "docs: update README with API usage"
```

## 🔐 Security Considerations

- **CORS**: Properly configured for frontend integration
- **Environment Variables**: Sensitive data stored in environment variables
- **Database**: Prepared statements prevent SQL injection
- **Authentication**: Ready for JWT or session-based auth integration

## 📊 API Endpoints

| Endpoint | Description |
|----------|-------------|
| `/` | API status and information |
| `/graphql/` | GraphQL API endpoint with Playground |
| `/admin/` | Django admin interface |
| `/health/` | Health check endpoint |

## 🏗 Project Structure

```
social_media_backend/
├── social_media_feed/           # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── feed/                   # Main application
│   ├── models.py          # Database models
│   ├── types.py           # GraphQL types
│   ├── queries.py         # GraphQL queries
│   ├── mutations.py       # GraphQL mutations
│   ├── schema.py          # Main GraphQL schema
│   ├── admin.py           # Django admin config
│   └── management/        # Custom management commands
├── requirements.txt       # Python dependencies
├── vercel.json           # Vercel deployment config
├── build_files.sh        # Build script for Vercel
└── README.md             # This file
```

## 🚨 Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Verify DATABASE_URL in environment variables
   - Check PostgreSQL server is running
   - Ensure database exists

2. **GraphQL Schema Errors**
   - Run `python manage.py migrate` to ensure all models are synced
   - Check for syntax errors in schema files

3. **Static Files Not Loading**
   - Run `python manage.py collectstatic`
   - Verify STATIC_URL and STATIC_ROOT settings

4. **Vercel Deployment Issues**
   - Check build logs in Vercel dashboard
   - Verify all environment variables are set
   - Ensure PostgreSQL database is accessible from Vercel

## 📚 Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [GraphQL Documentation](https://graphql.org/learn/)
- [Graphene-Django Documentation](https://docs.graphene-python.org/projects/django/)
- [Vercel Documentation](https://vercel.com/docs)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and commit: `git commit -m "feat: add new feature"`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter any issues or have questions:
1. Check the troubleshooting section above
2. Review the GraphQL Playground for API testing
3. Check the Django admin interface for data management
4. Open an issue in the repository

---

**Happy coding! 🚀**
