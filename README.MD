# University Project

The projects aim is to analyse the scope and underlying mechanisms behind the phenomenon of social media bounty hunters who participate in the organization of astroturfing to spread disinformation about cryptocurrency asset investments to users across social media platforms. In this project the forum - **bitcointalk.org** will be analysed.

# Program Control Functions

```
Create a database table from the home page data:

control.populate_database_main_page('option')

"one" - create database records from the first page
"all" - create database records for all posts
```
```
Create a database table from the commen section data:

control.populate_database_comment_page('option', Reverse)

"one_one" - one post, once comment page
"one_all" - one post, all comment pages
"all_one" - all pages, one comment page
"all_all" - all posts, all comment pages

True (Reverse) - read comments from the last page first
False (Reverse) -  read comments from the first page
```

```
Create a database table from Google Sheets data:

control.populate_database_sheets('option')

"all" - create records from all topics
"any_number" - creates records of that many topics. I.e. number 3 would create records from 3 topics
```

# Packages

```Control``` - All the functions (scraping, cleaning) are combined here <br/>
```Database``` - Database creation and CRUD functions <br/>
```Information cleaning``` - Prepare the scraped data for storing in database <br/>
```Values``` - Stores constants such as table names <br/>
```Web scraping``` - Retrieves data from the web

