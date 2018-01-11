#!/usr/bin/env python3

from flask import Flask, request, redirect, url_for

import newsdb

app = Flask(__name__)

get_code_items = newsdb.get_items

query1 = """
      SELECT articles.title, pathnames.views
      FROM articles, pathnames
      WHERE pathnames.path
      LIKE CONCAT('%' , articles.slug ,'%')
      GROUP BY articles.title, pathnames.views
      ORDER BY pathnames.views DESC;
    """

query2 = """
      SELECT authors.name, SUM(view_popular_articles.views) AS views
      FROM view_popular_articles, authors
      WHERE authors.id = view_popular_articles.author
      GROUP BY authors.name ORDER BY views DESC
    """

query3 = """
    SELECT TO_CHAR(date,'Mon dd, YYYY') AS date, perc_error
    FROM view_error_log
    WHERE perc_error > 1
  """

# HTML template for the forum page
HTML_WRAP = '''\
<!DOCTYPE html>
<html>
  <head>
    <title>DB news Report</title>
    <style>
        h1 {
  text-align: center;
}

.container {
  max-width: 960px;
  margin: 0 auto;
}

.popular-section .title {
  font-size: 24px;
  color: red;
  margin: 0;
}

.popular-section .title small, h3 {
  color: blue;
}

.popular-section {
  margin: 10px;
  min-height: 50px;
}

.popular-section .articles-img {
  position: relative;
}

.popular-section .articles-img:after {
  background-repeat: no-repeat;
  background-position: center center;
  background-size: cover;
}

.popular-section .articles-img.books:after {
  content: "";
  position: absolute;
  width: 50px;
  height: 50px;
}

.popular-section .articles-img.authors:after {
  content: "";
  position: absolute;
  width: 40px;
  height: 40px;
}

.popular-section .articles-img.error-log:after {
  content: "";
  position: absolute;
  width: 30px;
  height: 30px;
  top: 8px;
}

.popular-section header {
  padding: 10px 50px;
  height: 50px;
}

nav > ul {
  list-style: none;
  padding: 0;
}

nav > ul > li {
  display: inline;
}

nav > ul > li a {
  text-decoration: none;
  padding: 5px 10px 10px 0;
}
</style>
  </head>
  <body>
      <div class="container">
        <main>
        <header>
             <h1>DB `news` Report</h1>
            <nav>
                <ul class="main-nav">
                    <li>
                        <a href="/">Popular Articles</a>
                    </li>
                    <li>
                        <a href="/popular-authors">Popular Authors</a>
                    </li>
                    <li>
                        <a href="/error-log">Error Log</a>
                    </li>
                </ul>
            </nav>
        </header>
            <!-- content will go here -->
            <div class="main-container">
                %s
            </div>
        </main>
      </div>
  </body>
</html>
'''

POPULAR_ARTICLES = '''
    <section class="popular-section">

        <div class="articles-img books"></div>
        <header>
            <h2 class="title">"%s"  - <small> %s views</small></h2>
        </header>

    </section>
'''

POPULAR_AUTHORS = '''
    <div class="popular-section">

        <div class="articles-img authors"></div>
        <header>
            <h2 class="title">%s  - <small> %s views</small></h2>
        </header>
    </div>
'''

POPULAR_ERROR_DATE = '''
    <div class="popular-section">
        <div class="articles-img error-log"></div>
        <header>
            <h2 class="title">Date where Errors occur more than 1%%: </h2>
            <h3>%s  - %s %% errors</h3>
        </header>
    </div>
'''


def get_popular_article_titles():
    popular_articles_titles_ = "".join(POPULAR_ARTICLES % (title, views) for
                                       title, views in get_code_items(query1))
    return popular_articles_titles_


def get_popular_authors_names():
    popular_authors_names = "".join(POPULAR_AUTHORS % (name, views) for
                                    name, views in get_code_items(query2))
    return popular_authors_names


def geterror_and_percent():
    popular_authors_names = "".join(POPULAR_ERROR_DATE % (date, percent)
                                    for date, percent in
                                    get_code_items(query3))
    return popular_authors_names


@app.route('/', methods=['GET'])
def popular_articles():
    names_popular_authors = get_popular_article_titles()
    html = HTML_WRAP % names_popular_authors
    return html


@app.route('/popular-authors', methods=['GET'])
def popular_authors():
    names_popular_authors_ = get_popular_authors_names()
    html = HTML_WRAP % names_popular_authors_
    return html


@app.route('/error-log', methods=['GET'])
def popular_error_log_day():
    names_popular_authors_2 = geterror_and_percent()
    html = HTML_WRAP % names_popular_authors_2
    return html

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
