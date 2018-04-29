# pasturemap
Pasturmap Coding Test

No special instructions needed, just creates the database, update DATABASES and install the requirements.txt.

Once running, you can also navigate the API by creating and user, authenticating, and visiting http://localhost:8000/api/ to see the endpoints (custom POST endpoints will not be available from here).

I was not able to add Unit Tests for models given the time and having to leave, I've chosen to add the tests to the API endpoint, which use the model methods. But I consider the `calculate_weight` method of `Animal` class should have its own test.

Consulted information:
- https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.interp1d.html

