Build container with:
<br>
``docker build --tag little_john:latest .``
<br>
Run it afterwards with:
<br>
``docker run --name little_john -d -p 8080:8080 little_john:latest``
<br>
Run local tests with:  ``python3 manage.py test``
<br>
Available endpoints are:
<br>
Getting the Swagger Documentation of API by accessing server: ``127.0.0.1:8080``
<br>
Registering a new user: GET - ``/admin/register_user/ ``
<br>
Getting the current prices of users watchlist: GET - ``/tickers/`` with basic auth
<br>
Getting the price history for a ticker symbol: GET/POST - ``/tickers/<TICKER>/history/`` with basic auth
<br>
