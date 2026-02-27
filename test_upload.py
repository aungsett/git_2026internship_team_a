from backend.app.services.storage_service import StorageService

class DummyFile:
  def __init__(self):
    self.filename = "resume3.pdf"

  def read(self):
    return b"fake pdf content 2"
  
file = DummyFile()

service = StorageService()
url = service.upload_cv(file, 99999)

print("Uploaded to:", url)
