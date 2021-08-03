# Telegram bot with django admin
This bot can:<br>
&emsp;Send random photo<br>
&emsp;Send temperature in the city at the moment<br>
&emsp;Send temperatures in the city every 10 seconds
## Django
From the first message, username and id of the chat are recorded in the PostgreSQL database. Also, the name is checked every message, if name changes, it will also be updated in the database.
You can check the name, chat id and the subscription to the mailing in the Django administrative panel.
