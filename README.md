# pasturemap
Pasturmap Coding Test

No special instructions needed, just creates the database, update `DATABASES` settings and install the requirements.txt.

Once running, you can also navigate the API by creating an user, authenticating, and visiting http://localhost:8000/api/ to see the endpoints (custom POST endpoints will not be available from here).

I was not able to add Unit Tests for models given the time and having to leave, I've chosen to add the tests to the API endpoint, which use the model methods. But I consider the `calculate_weight` method of `Animal` class should have its own test.

Consulted information:
- https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.interp1d.html (first time use)
- http://www.django-rest-framework.org/


# API endpoints

## Animals API
- [GET | POST] `/api/animals/`
- [GET | POST | PATCH | DELETE] `/api/animals/<pid>/` (bonus: can update pid)
- [POST] `/api/animals/<pid>/add_weight/` (add a weigh to an animal)
- [POST] `/api/animals/total_weight/` (total animals weight)

## Herds API
- [GET | POST] `/api/herds/` (bonus: create new herds)
- [GET | POST | PATCH | DELETE]`/api/herds/<pid>/`
- [POST] `/api/herds/<pid>/add_animal/` (add animal to herd)

## Weight Entries API
- [GET | POST] `/api/weight_entries/` (bonus: add animal weigh)
- [GET | POST | PATCH | DELETE] `/api/weight_entries/<pk>/` (bonus: can update a weigh)



