Field names and formats 

- applicant_id: int
- full_name: string (max 100)
- dob: YYYY-MM-DD
- email: valid email string
- degree: string
- experience_years: int >= 0
- preferred_course: string
- location_country, location_state: optional string
- comments: optional string
- status: one of ["Pending","Reviewed","Shortlisted","Accepted","Rejected"]
- cv_filename: original filename
- cv_url: storage URL
- submitted_at: ISO datetime
- Default page size: 25
- Duplicate policy: reject duplicates (409 Conflict)
