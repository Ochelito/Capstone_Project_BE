# Capstone_Project_BE
Final Backend Web Development Project. Compulsory for graduation

# SkillShare Marketplace API
This repository contains the backend API for a SkillShare Marketplace application where local community users can learn practical skills from experts. The backend is built with Django and Django REST Framework, using MySQL as the database.

# Table of Contents
Project Overview
Features
Technology Stack
Project Structure
Installation
Configuration
Running the Project
API Endpoints
Authentication
Postman Setup
Contributing
License

# Project Overview
The SkillShare Marketplace API allows: 
- Mentors to register and offer lessons on their skills.
- Learners to browse skills, book lessons, and leave reviews.
- Admins to manage users, skills, lessons, bookings, and reviews.

# Features
-User roles: Mentor, Learner, or Both
-JWT authentication and optional OAuth (Google, Facebook, etc.)
-Skill management by mentors
-Lesson creation under skills
-Booking system for learners
-Review system for lessons
-Permission system ensuring only authorized actions

# Technology Stack
-Python 3.11
-Django 5.x
-Django REST Framework
-MySQL
-Postman for API testing
-JWT for authentication

# API Endpoints
Endpoint Method Description
/api/users/register/ POST Register a new user
/api/auth/login/ POST Obtain JWT token
/api/auth/refresh/ POST Refresh JWT token
/api/skills/ GET, POST List or create skills
/api/lessons/ GET, POST List or create lessons
/api/bookings/ GET, POST List or create bookings
/api/reviews/ GET, POST List or create reviews
Note: All endpoints requiring authentication must include Authorization: Bearer
<access_token> header.

# Authentication
JWT Authentication is implemented using rest_framework_simplejwt .
Obtain a token via /api/auth/login/ , then pass in Authorization header.

# Postman Setup
-Create an environment SkillShareAPI .
-Define variables: base_url , access_token , mentor_id , skill_id , lesson_id ,
booking_id , review_id .
-Create collection SkillShareAPI and folders: Users, Skills, Lessons, Bookings, Reviews.
-Add requests in order: Register → Login → Create Skill → Create Lesson → Create Booking → Create Review.
-Use Post-request scripts to automatically save IDs and tokens for subsequent requests.

