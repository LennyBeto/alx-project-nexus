# feed/auth_mutations.py 
import graphene
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from graphql import GraphQLError
import jwt
from django.conf import settings
from datetime import datetime, timedelta
from .types import UserType

class RegisterUser(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        first_name = graphene.String()
        last_name = graphene.String()
    
    success = graphene.Boolean()
    message = graphene.String()
    user = graphene.Field(UserType)
    token = graphene.String()
    
    def mutate(self, info, username, email, password, first_name=None, last_name=None):
        # Check if user already exists
        if User.objects.filter(username=username).exists():
            raise GraphQLError('Username already exists')
        
        if User.objects.filter(email=email).exists():
            raise GraphQLError('Email already exists')
        
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name or '',
            last_name=last_name or ''
        )
        
        # Generate JWT token
        payload = {
            'user_id': user.id,
            'username': user.username,
            'exp': datetime.utcnow() + timedelta(days=7)
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        
        return RegisterUser(
            success=True,
            message='User registered successfully',
            user=user,
            token=token
        )

class LoginUser(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
    
    success = graphene.Boolean()
    message = graphene.String()
    user = graphene.Field(UserType)
    token = graphene.String()
    
    def mutate(self, info, username, password):
        user = authenticate(username=username, password=password)
        
        if not user:
            raise GraphQLError('Invalid credentials')
        
        # Generate JWT token
        payload = {
            'user_id': user.id,
            'username': user.username,
            'exp': datetime.utcnow() + timedelta(days=7)
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        
        return LoginUser(
            success=True,
            message='Login successful',
            user=user,
            token=token
        )

class UpdateProfile(graphene.Mutation):
    class Arguments:
        first_name = graphene.String()
        last_name = graphene.String()
        email = graphene.String()
    
    success = graphene.Boolean()
    message = graphene.String()
    user = graphene.Field(UserType)
    
    def mutate(self, info, first_name=None, last_name=None, email=None):
        user = info.context.user
        if not user.is_authenticated:
            raise GraphQLError('Authentication required')
        
        if first_name is not None:
            user.first_name = first_name
        if last_name is not None:
            user.last_name = last_name
        if email is not None:
            if User.objects.filter(email=email).exclude(id=user.id).exists():
                raise GraphQLError('Email already exists')
            user.email = email
        
        user.save()
        
        return UpdateProfile(
            success=True,
            message='Profile updated successfully',
            user=user
        )
