# CivicPulse
This Repository is for the PVM projects for Tech Associates Hackathon

## Overview of the Project

CivicPulse is a comprehensive civic engagement platform designed to bridge the gap between citizens and government services. It provides an intuitive interface for citizens to submit service requests, track their progress, and receive timely updates from relevant government departments.

## Problem Statement
Many citizens face difficulties when trying to report issues or interact with government services due to bureaucratic delays, lack of transparency, or inaccessible platforms.

## Vision
CivicPulse aims to modernize public service delivery by enabling transparent, responsive, and efficient interaction between citizens and government agencies.

## Demo Video

[![Watch Demo](https://img.icons8.com/clouds/100/000000/video-playlist.png)](https://drive.google.com/file/d/1xKLkbcs1PpLFmOQpjEyypRgrTY9JEWh6/view?usp=sharing)


Click the image above to watch the video demo.


## Sample System Pages
### Home Page
![image](https://github.com/user-attachments/assets/f4ccaa47-5921-458f-8e51-c8ce38272e7c)

### Admin Dashboard

**Credential for Admin Login**: Username: admin, password: admin@123
![image](https://github.com/user-attachments/assets/7e8b6920-dda1-43be-ace6-4dc53f03213b)

![image](https://github.com/user-attachments/assets/91916ec3-ebbe-4873-bf05-364ae911d1e6)

### Staff Dashboard(Government Department)
**Credential for Staff Login**: Username: esther, password: Kirehe@2019 / this is sample staff user
![image](https://github.com/user-attachments/assets/6e60f73a-c4c0-4781-a0d1-84168733cffc)

![image](https://github.com/user-attachments/assets/acc49642-1d6a-4f8e-8382-8703aa9aa950)

![image](https://github.com/user-attachments/assets/4987d341-2880-4193-92f6-53aa02f0b494)

### User Dashboard(Citizen)
**Credential for citizen Login**: Username: philos, password: Kirehe@2019 / this is sample citizen user
![image](https://github.com/user-attachments/assets/c4bfd56b-eb5f-4cd0-976d-d27f4c70f95a)

![image](https://github.com/user-attachments/assets/0c85c599-5862-44e7-96ba-acdc7d4657a2)

![image](https://github.com/user-attachments/assets/e9bd0f39-ce78-454e-a252-f7028b5a1e21)

## Features

### For Citizens
- **Request Submission**: Easily submit service requests to various government departments
- **Request Tracking**: Monitor the status and progress of submitted requests
- **Timeline View**: Visualize the journey of each request through different stages
- **Notifications**: Receive updates when there's progress on your requests

### For Government Staff
- **Request Management**: Efficiently handle and respond to citizen requests
- **Department Assignment**: Route requests to appropriate departments
- **Status Updates**: Provide transparent updates on request progress
- **Analytics Dashboard**: Access insights on request volumes, resolution times, and department performance

### For Administrators
- **User Management**: Manage citizen and staff accounts
- **Department Configuration**: Set up and configure government departments
- **Category Management**: Create and manage service request categories
- **System Monitoring**: Monitor system performance and usage statistics

## Technology Stack

- **Backend**: Django (Python)
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Database**: SQLite (development), PostgreSQL (production)
- **Authentication**: Django Authentication System
- **Deployment**: Docker, Heroku/AWS

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Virtual environment (recommended)
- import database (**civicpulse_db**) in project folder


### Custom Settings
Additional configuration options can be found in `civicpulse/settings.py`.

## Data Models

- **User**: Extended Django User model with additional profile information
- **Department**: Government departments that handle service requests
- **Category**: Types of service requests (linked to departments)
- **Ticket**: Service requests submitted by citizens
- **TicketResponse**: Responses from staff to tickets
- **Timeline**: Tracking the progress stages of tickets

## Security

- Django's built-in security features (CSRF protection, SQL injection prevention)
- Password hashing and secure authentication
- Permission-based access control
- Form validation and sanitization

## Getting Started

```bash
#Clone the repo
git clone https://github.com/your-ndikubwimana12/civicpulse.git
cd civicpulse

# Create a virtual environment
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start the server
python manage.py runserver
```

##  Developer

- [NDIKUBWIMANA Eric](https://github.com/ndikubwimana12) - Project Lead,Backend Developer and Frontend Developer

##  Contact

For questions or support, please contact (ndikubwimanaeric2019@gmail.com).

## Acknowledgements

- [Django](https://www.djangoproject.com/)
- [Bootstrap](https://getbootstrap.com/)
- [Font Awesome](https://fontawesome.com/)



