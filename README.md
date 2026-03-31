# ATS Website

A simple Applicant Tracking System built with Flask for applicant submissions and admin review.

Live site: [https://ats-website-team-a.onrender.com/](https://ats-website-team-a.onrender.com/)

## Features

- Applicant form with CV upload
- MongoDB storage for applicant data
- Cloudinary storage for resumes
- Firebase-based admin login
- Admin dashboard with filters, status updates, notes, CSV export, and applicant detail view

## Tech Stack

- Backend: Flask, MongoEngine
- Frontend: HTML, Tailwind CSS, vanilla JavaScript
- Database: MongoDB Atlas
- File storage: Cloudinary
- Admin auth: Firebase Authentication

## Local Setup

1. Create a `.env` file with your project credentials.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Start the app:

```bash
py -m backend.app.main
```

4. Open:
- `/` for the landing page
- `/apply` for the applicant form
- `/admin-login` for admin access

## Notes

- New applicants are saved with default status `Pending`.
- Resume filenames and file types are preserved in storage and download flow.
- Submission times in the admin UI are shown in JST.

## Deployment

This project can be deployed on Render using:

- Build command: `pip install -r requirements.txt`
- Start command: `gunicorn "backend.app.main:create_app()"`

Set all required environment variables in Render, including MongoDB, Cloudinary, and Firebase credentials.
