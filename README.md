# feature/domain-model

This branch defines the ATS domain foundation:
- Applicant model + Status enum
- Request/response schemas (apply, admin, status update, errors)
- DTOs used by services/routes
- Shared validation constants
- Unit tests for schema validation

Notes:
- Duplicate email policy: reject (409 Conflict)
- Status values: Pending, Reviewed, Shortlisted, Accepted, Rejected

Run tests:
- `py -m pytest backend/tests/unit -q`
