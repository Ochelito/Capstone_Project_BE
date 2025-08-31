# Capstone_Project_BE
Final Backend Web Development Project — Compulsory for Graduation

## SkillShare Marketplace API
This repository contains the backend API for a **SkillShare Marketplace** application where local community users can learn practical skills from experts.  
The backend is built with **Django** and **Django REST Framework**, using **MySQL** as the database.

---

## Table of Contents
1. [Project Overview](#project-overview)  
2. [Features](#features)  
3. [Technology Stack](#technology-stack)  
4. [Project Structure](#project-structure)  
5. [Installation](#installation)  
6. [Configuration](#configuration)  
7. [Running the Project](#running-the-project)  
8. [API Endpoints](#api-endpoints)  
9. [Authentication](#authentication)  
10. [Postman Setup](#postman-setup)  
11. [Contributing](#contributing)  
12. [License](#license)  

---

## Project Overview
The **SkillShare Marketplace API** allows:  
- **Mentors** to register and offer lessons on their skills.  
- **Learners** to browse skills, book lessons, and leave reviews.  
- **Admins** to manage users, skills, lessons, bookings, and reviews.  

---

## Features
- User roles: **Mentor**, **Learner**, or **Both**  
- JWT authentication and optional OAuth (Google, Facebook, etc.)  
- Skill management by mentors  
- Lesson creation under skills  
- Booking system for learners  
- Review system for lessons  
- Permission system ensuring only authorized actions  

---

## Technology Stack
- **Python 3.11**  
- **Django 5.x**  
- **Django REST Framework**
- **MySQL**  
- **Postman** for API testing  
- **JWT** for authentication

  ---

## API Endpoints

| Endpoint                | Method       | Description                |
|-------------------------|-------------|----------------------------|
| `/api/users/register/`  | POST        | Register a new user        |
| `/api/auth/login/`      | POST        | Obtain JWT token           |
| `/api/auth/refresh/`    | POST        | Refresh JWT token          |
| `/api/skills/`          | GET, POST   | List or create skills      |
| `/api/lessons/`         | GET, POST   | List or create lessons     |
| `/api/bookings/`        | GET, POST   | List or create bookings    |
| `/api/reviews/`         | GET, POST   | List or create reviews     |

**Note:** All endpoints requiring authentication must include the header: 

## Authentication
- JWT authentication is implemented using **rest_framework_simplejwt**.  
- Obtain a token via `/api/auth/login/` and include it in the Authorization header for protected endpoints.

---

## Postman Setup
1. Create an environment called **SkillShareAPI**.  
2. Define variables:
3. Create a collection **SkillShareAPI** with folders:  
- Users  
- Skills  
- Lessons  
- Bookings  
- Reviews  
4. Add requests in order:  
`Register → Login → Create Skill → Create Lesson → Create Booking → Create Review`  
5. Use Post-request scripts to automatically save IDs and tokens for subsequent requests.*MySQL**  
- **Postman** for API testing  
- **JWT** for authentication 
