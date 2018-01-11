# Log Analysis

This project consists of answering these 3 basic questions

* What are the most popular three articles of all time?
* Who are the most popular article authors of all time?
* On which days did more than 1% of requests lead to errors?

The database consist of three tables

* authors
* articles
* log

## Running the project

* download a virtual machine from [https://www.vagrantup.com/downloads.html] vagrant
* After installing, run the command `vagrant up` in a terminal
* When vagrant up is finished running, you will get your shell prompt back. At this point, you can run `vagrant ssh` to log in to your newly installed Linux VM!
* connect to the news db `psql -d news -f newsdata.sql`

## Setting up the db for queries

* once connected to the db run the following queries

```
    CREATE OR REPLACE VIEW pathnames as SELECT log.path,
    count(log.path) AS views
    FROM log
    WHERE log.path LIKE '%article%'::text
    GROUP BY log.path
    ORDER BY (count(log.path)) DESC
    LIMIT 3;
```

```
    CREATE OR REPLACE VIEW view_popular_articles
    AS SELECT title, author, COUNT(*) AS views
    FROM articles,log
    WHERE log.path LIKE concat('%', articles.slug)
    GROUP BY articles.title, articles.author
    ORDER BY views DESC;
```

```
    CREATE OR REPLACE VIEW view_error_log
    AS SELECT DATE(time),
    ROUND(100.0 * SUM(CASE log.status WHEN '200 OK' THEN 0 ELSE 1 END) / COUNT(log.status), 2)
    AS perc_error
    FROM log GROUP BY DATE(time)
    ORDER BY perc_error DESC;
```

## View the results

* on the termoinal disconnect from the database `\q`
* navigate to the vagrant folder `cd /vagrant`
* navigate to the news folder `cd news`
* run the python file `python news.py`

* open up your browser to http://localhost:8000/
* click "Popular Articles" to answer question 1
* click "Popular Authors" to answer question 2
* click "Error Log" to answer question 3
