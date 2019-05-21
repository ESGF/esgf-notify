## Info

Currently contains two modules `db` and `notify`. 

### db
The `db` module, along with its execution script `db_setup.py` is the beginnings of using a single module to deploy all ESGF database tables and schemas. It should be used with care as it can easily drop entire schemas if misused.

### notify
The `notify` module, along with its execution script `main.py` are the core of detecting changes within a given amount of time in the ESGF Solr Index. It will eventually require a database connection (see `db.models.notify`) and a system for actually sending the notifications. It is really more of a weekly newsletter system. 