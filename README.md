# Applicant Tracking System (ATS)

## Overview
This project is a simple web-based Applicant Tracking System (ATS) built for the Human Resocia internship project.

Applicants can submit an application form with a CV. The backend validates the data, stores applicant metadata in MongoDB Atlas, stores CV files in Firebase Storage, and provides admin-only functionality for reviewing applicants.

## Core Features
### Applicant (Public)
- Submit application form with required fields
- Upload CV file (.pdf, .doc, .docx)
- Server-side validation
- Duplicate email detection (duplicates rejected with 409 Conflict)
- Submission returns an applicant_id and confirmation message

### Admin (Protected)
- Admin authentication using Firebase Authentication
- View paginated list of applicants
- Search and filters (name/email, degree, experience range, preferred course, status)
- View applicant detail including CV URL
- Update applicant status (Pending, Reviewed, Shortlisted, Accepted, Rejected)
- Export filtered applicant list to CSV

## Tech Stack
- Backend: Python (Flask)
- Database: MongoDB Atlas
- Authentication: Firebase Authentication (admin)
- File Storage: Firebase Storage
- Deployment: Render

## Project Structure
- `backend/app/` contains the Flask application
- `backend/app/routes/` contains API routes/controllers
- `backend/app/services/` contains business logic
- `backend/app/repositories/` contains database queries
- `backend/app/models/`, `schemas/`, `dtos/` define domain objects and validation
- `tests/` contains unit and integration tests

## Environment Variables
Environment variables are stored in `.env` and must not be committed.

Key variables include:
- MongoDB connection URI
- Firebase service account credentials path
- Firebase storage bucket name
- Secret key
- Upload size limit

## Collaboration Workflow
This project uses a feature-branch workflow.

- `main`: stable integration branch
- Feature branches:
  - `feature/domain-model`
  - `feature/database-setup`
- etc

Changes can be merged into `main` via Pull Requests.

