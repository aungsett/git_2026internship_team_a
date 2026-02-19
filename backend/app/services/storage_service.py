class StorageService:
    def upload_cv(self, file, applicant_id):
        if not file.filename.lower().endswith(".pdf"):
            raise ValueError("Only PDF allowed")
        return f"http://test.com/{applicant_id}/{file.filename}"
