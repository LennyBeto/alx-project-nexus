import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction
from faker import Faker
from feed.models import Post, Comment, Like, Share, Follow, UserProfile

fake = Faker()


class Command(BaseCommand):
    help = 'Create sample data for testing the social media feed'

    def add_arguments(self, parser):
        parser.add_argument(
            '--users',
            type=int,
            default=10,
            help='Number of users to create'
        )
        parser.add_argument(
            '--posts',
            type=int,
            default=50,
            help='Number of posts to create'
        )
        parser.add_argument(
            '--comments',
            type=int,
            default=100,
            help='Number of comments to create'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before creating new data'
        )

    def handle(self, *args, **options):
        users_count = options['users']
        posts_count = options['posts']
        comments_count = options['comments']
        clear_data = options['clear']

        if clear_data:
            self.stdout.write(
                self.style.WARNING('Clearing existing data...')
            )
            with transaction.atomic():
                Follow.objects.all().delete()
                Share.objects.all().delete()
                Like.objects.all().delete()
                Comment.objects.all().delete()
                Post.objects.all().delete()
                UserProfile.objects.all().delete()
                User.objects.filter(is_superuser=False).delete()

        self.stdout.write(f'Creating {users_count} users...')
        users = self.create_users(users_count)

        self.stdout.write(f'Creating {posts_count} posts...')
        posts = self.create_posts(posts_count, users)

        self.stdout.write(f'Creating {comments_count} comments...')
        self.create_comments(comments_count, users, posts)

        self.stdout.write('Creating likes...')
        self.create_likes(users, posts)

        self.stdout.write('Creating follows...')
        self.create_follows(users)

        self.stdout.write('Creating shares...')
        self.create_shares(users, posts)

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created sample data:\n'
                f'- {users_count} users\n'
                f'- {posts_count} posts\n'
                f'- {comments_count} comments\n'
                f'- Random likes, follows, and shares'
            )
        )

    def create_users(self, count):
        """Create sample users with profiles"""
        users = []
        for i in range(count):
            username = fake.user_name()
            # Ensure unique usernames
            while User.objects.filter(username=username).exists():
                username = fake.user_name()

            user = User.objects.create_user(
                username=username,
                email=fake.email(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                password='testpass123'
            )

            # Create or update profile
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.bio = fake.text(max_nb_chars=200)
            profile.location = fake.city()
            profile.birth_date = fake.date_of_birth(minimum_age=18, maximum_age=65)
            profile.save()

            users.append(user)

        return users

    def create_posts(self, count, users):
        """Create sample posts"""
        posts = []
        for _ in range(count):
            author = random.choice(users)
            content_options = [
                fake.text(max_nb_chars=200),
                fake.sentence(nb_words=10),
                fake.paragraph(nb_sentences=3),
                f"Just had an amazing {fake.word()}! #life #awesome",
                f"Thinking about {fake.catch_phrase()}",
                f"Beautiful day in {fake.city()}! 🌞",
                f"Working on {fake.bs()} project today",
                f"Quote of the day: '{fake.sentence()}'"
            ]

            post = Post.objects.create(
                author=author,
                content=random.choice(content_options)
            )
            posts.append(post)

        return posts

    def create_comments(self, count, users, posts):
        """Create sample comments and replies"""
        comments = []
        
        # Create top-level comments
        for _ in range(int(count * 0.7)):  # 70% top-level comments
            post = random.choice(posts)
            author = random.choice(users)
            
            comment_options = [
                fake.sentence(nb_words=8),
                f"Great post! {fake.sentence()}",
                f"I {random.choice(['agree', 'disagree', 'love this', 'think'])}, {fake.sentence()}",
                fake.text(max_nb_chars=100),
                f"Thanks for sharing! {fake.word()}",
                "👍👍👍",
                f"{random.choice(['Amazing', 'Awesome', 'Cool', 'Nice'])}!"
            ]

            comment = Comment.objects.create(
                post=post,
                author=author,
                content=random.choice(comment_options)
            )
            comments.append(comment)

        # Create replies
        for _ in range(int(count * 0.3)):  # 30% replies
            if comments:  # Only if we have comments to reply to
                parent_comment = random.choice(comments)
                author = random.choice(users)
                
                reply_options = [
                    fake.sentence(nb_words=6),
                    f"@{parent_comment.author.username} {fake.sentence()}",
                    f"I agree! {fake.sentence()}",
                    fake.text(max_nb_chars=80),
                    "Exactly my thoughts!",
                    "Thanks for the reply!",
                    "🔥🔥"
                ]

                Comment.objects.create(
                    post=parent_comment.post,
                    author=author,
                    parent=parent_comment,
                    content=random.choice(reply_options)
                )

    def create_likes(self, users, posts):
        """Create random likes for posts and comments"""
        # Like posts
        for post in posts:
            # Each post gets liked by 0-80% of users
            likers = random.sample(users, random.randint(0, int(len(users) * 0.8)))
            for user in likers:
                Like.objects.get_or_create(user=user, post=post)

        # Like comments
        comments = list(Comment.objects.all())
        for comment in comments:
            # Each comment gets liked by 0-50% of users
            likers = random.sample(users, random.randint(0, int(len(users) * 0.5)))
            for user in likers:
                Like.objects.get_or_create(user=user, comment=comment)

    def create_follows(self, users):
        """Create random follow relationships"""
        for user in users:
            # Each user follows 0-60% of other users
            potential_follows = [u for u in users if u != user]
            follows = random.sample(
                potential_follows, 
                random.randint(0, int(len(potential_follows) * 0.6))
            )
            
            for follow_user in follows:
                Follow.objects.get_or_create(
                    follower=user,
                    following=follow_user
                )

    def create_shares(self, users, posts):
        """Create random shares"""
        for post in posts:
            # Each post gets shared by 0-20% of users
            sharers = random.sample(users, random.randint(0, int(len(users) * 0.2)))
            for user in sharers:
                share_messages = [
                    "",  # No message
                    fake.sentence(nb_words=5),
                    f"Check this out! {fake.word()}",
                    "Thought you'd like this",
                    f"Great content from @{post.author.username}",
                    fake.text(max_nb_chars=50)
                ]
                
                Share.objects.get_or_create(
                    user=user,
                    post=post,
                    defaults={'content': random.choice(share_messages)}
                )