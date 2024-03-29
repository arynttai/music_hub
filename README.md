# Music Hub

Welcome to the documentation for the "Music Hub" project – an innovative platform designed to bring together music enthusiasts, creative performers, and event organizers. "Music Hub" goes beyond providing music services; it becomes a center where user convenience and comfort are prioritized.

## Overview

"Music Hub" aims to be an integral part of organizing diverse events, facilitating musician bookings, and easing individual music sessions. It is more than just a platform; it's a space where music lovers and creative performers converge, where notes and requests blend to create a unique experience in the world of sounds and emotions.

The main goal of the project is not just to offer music services but to automate them for maximum user convenience. The service addresses the needs of professionals and becomes a reliable ally for individuals or companies seeking music-related services, including event organization, regular musician bookings, and individual music sessions.

"Music Hub" offers unique features such as service ratings and selection based on reviews, a recommendation panel for easy searching, the ability to create personal service-seeking advertisements, a unique payment system, and time savings.

## Project Details

### 1. Tools Used

In the "Music Hub" project, we utilized a blend of technologies learned during training and explored new ones during development. Here are some specific examples:

#### Frontend
- HTML, CSS, JavaScript
  - Semantic HTML5 and CSS3 standards
  - Balanced use of semantic elements
  - Minimal use of tables
  - Preferential use of Flex technology
  - Optimization for browser window resolutions: 1280 px, 768 px, 320 px

#### Backend
- FastAPI Framework
  - Fast, efficient, and simple web application development in Python
  - Automatic API interface generation based on type data annotations
  - Use of Uvicorn, psycopg2 for database communication, Jinja2 templates, CORS, and other tools for working with the FastAPI asynchronous application.

## Getting Started

To set up and run the "Music Hub" project locally, follow these steps:

1. Clone the repository.
2. Install dependencies using `requirements.txt`.
3. Configure the backend settings.
4. Run the application.

# Music Hub Database

## 1.2 Database Structure

The "Music Hub" database is designed to comprehensively cover all aspects of the project, ensuring efficient storage and manipulation of data. The key tables include:

### 1. Table: Users
   - Contains all user information.

### 2. Tables: Bands and Events
   - Stores id and name for each band and event request.

### 3. Tables: Band_Details and Event_Details
   - Holds complete information about bands and events.

### 4. Tables: Band_Orders and Event_Orders
   - Connective tables for order execution.

## Figure 1.1: Database Tables
![Database Tables](dbmusichub.png)

Feel free to explore the codebase and documentation to understand the project structure and contribute to its development.

Thank you for choosing "Music Hub"!
