# University Project
The projects aim is to analyse the scope and underlying mechanisms behind the phenomenon of social media bounty hunters who participate in the organization of astroturfing to spread disinformation about cryptocurrency asset investments to users across social media platforms. In this project the forum - **bitcointalk.org** will be analysed.
## Control Functions
### Topic (subject)
```
from control import control_topic

control_topic.populate_database(option)
```
#### Options:
    'one' - retrieve one page of posts
    'all' - retrieve all posts from all pages
    'update' - retrieve posts which have recieved additional comments from last scraping
    [id_2 (40), id_2 (80),...] - retrieve posts from id manually
    'yyyy/mm/dd - yyyy/mm/dd' or 'yyyy/mm/dd' - retrieve posts from a date or in a date range
### Comments (proof, participation, author)
```
from control import control_comments

control_comments.populate_database(option_1, option_2, reverse, tables)
```
#### Options:
#### option_1
    'one' - retrieve posts from one topic page
    'all' - retrieve posts form all topic pages
    'update' - retrieve posts that are in comments_update database (produced by updating topic)
    '[(id, url, author), (id, url, author) ...]' - manual mode
    'yyyy/mm/dd - yyyy/mm/dd' or 'yyyy/mm/dd' - retrieve posts from a date or in a date range
#### option_2
    'all' - retrieve all post pages
    number - retrieve posts form a specified number of pages
#### reverse
    True - start retrieving posts from the last page
    False - retrieve posts form the first page
#### tables
    ['proof', 'author', 'participation'] - select which tables to populate when scraping
### Author images (main topic post conversion from image to text)
```
from control import control_author_images

control_author_images.populate_database_author(option)
```
#### Options:
    'one' - extract data from the first entry in the topic database
    'all_new' - extracts only the entries that have not been extracted before
    'all_failed' - extracts all entries including the ones that failed before
### Google spreadsheets
```
from control import control_sheets

control_sheets.populate_database_sheets(option)
```
#### Options:
    'all' - create records of all Google sheets in the database
    number - create a specified amount of records in the database

# Packages

```Analysis``` - Cleaned data analysis functions <br/>
```Classes``` - Object classes <br/>
```Control``` - All the functions (scraping, cleaning) are combined here <br/>
```Database``` - Database creation and CRUD functions <br/>
```Image_to_text``` - Image conversion to text data <br/>
```Information cleaning``` - Prepare the scraped data for storing in database <br/>
```Values``` - Stores constants such as table names <br/>
```Web scraping``` - Retrieves data from the web

