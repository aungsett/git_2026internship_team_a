from mongoengine import Document, StringField, IntField

class Counter(Document):
    meta = {"collection": "counters"}

    name = StringField(required=True, unique=True)
    value = IntField(default=60000)