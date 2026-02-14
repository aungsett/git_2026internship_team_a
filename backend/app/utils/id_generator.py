from models.counter import Counter

def generate_applicant_id():
    counter = Counter.objects(name="applicant_id").modify(
        upsert=True,
        new=True,
        inc__value=1
    )
    return counter.value
