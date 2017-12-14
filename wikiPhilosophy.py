import argparse
import urllib2
import sqlite3
from sqlite3 import Error
from bs4 import BeautifulSoup, SoupStrainer, Tag, NavigableString



class getting_to_philosophy:

   def __init__(self):
      self.div_id = "mw-content-text"
      self.content_tags = ['p', 'ul', 'ol']


   def get_philosophy_link(self, url):
      self.set_page(url)
      self.page_name = return_wiki_page_name(url)

      if self.page == False or self.page_name == False:
         return False

      self.soup = self.set_parser()
      return self.philosophy_link()


   def set_page(self,url):
      self.url = url
      self.page = follow_url(self.url)

   def set_parser(self):
      strained = SoupStrainer('div', id=self.div_id)
      return BeautifulSoup(self.page, parse_only=strained)


   def seek_to_first_paragraph(self):

      first_link_containing_element = self.soup.find('p')

      while is_in_table(first_link_containing_element):
         first_link_containing_element = first_link_containing_element.find_next('p')

      if first_link_containing_element == None:
         first_link_containing_element = soup.find(self.content_tags)

      return first_link_containing_element


   def philosophy_link(self):
      current_page_element = self.seek_to_first_paragraph()

      while current_page_element != None:
         no_parenthesized_links = remove_parenthesized_links(current_page_element)
         all_links = no_parenthesized_links.find_all('a')
         for link in all_links:
            if link['href'].startswith("/wiki/"):
               full_link = "http://en.wikipedia.org" + link['href']
               is_wiki = is_wiki_url(full_link)
               is_special = is_special_wiki_page(full_link) # check if the page is a Help page, File page,...
               is_same_page = return_wiki_page_name(full_link) == self.page_name
               italicized = is_italicized(link)
               if is_wiki and not is_special and not italicized and not is_same_page:
                  return full_link

         current_page_element = current_page_element.find_next(self.content_tags)

      return False


def remove_parenthesized_links(tag):
   without_parens = []
   in_parens = False

   subtree_list = tag_subtree_as_list(tag)

   in_anchor = False
   in_parens = False
   for element in subtree_list:
      in_tag = False
      if element.startswith("<"):
         in_tag = True
         if element.startswith("<a"):
            in_anchor = True
         elif element.startswith("</a>"):
            in_anchor = False


      if not in_tag:
         for char in element:
            if char == "(":
               in_parens = True
            elif char == ")":
               in_parens = False

      if (not in_anchor or (in_anchor and not in_parens)):
         without_parens.append(element)

   return BeautifulSoup("".join(without_parens))


def tag_subtree_as_list(tag):


   pretty = tag.prettify()

   pretty_list = []
   for element in pretty.splitlines():
      pretty_list.append(element.lstrip())

   return pretty_list

def is_italicized(tag):
   return tag.find_parent().name == "i"

def is_in_table(tag):
   for parent in tag.parents:
      if parent.name == 'td' or parent.name == 'tr' or parent.name == 'table':
         return True
   return False

def is_special_wiki_page(url):
   is_red = is_red_link(url)
   is_help = is_help_page(url)
   is_special = is_special_page(url)
   is_file = is_file_page(url)
   return (is_red or is_help or is_special or is_file)


def is_red_link(url):
   if "redlink=1" in url:
      return True
   return False

def is_help_page(url):
   if "Help:" in url:
      return True
   return False

def is_special_page(url):
   if "Special:" in url:
      return True
   return False

def is_file_page(url):
   if "File:" in url:
      return True
   return False

def is_wiki_url(url):
   valid_http_start = url.startswith("http://en.wikipedia.org/wiki/")
   valid_https_start = url.startswith("https://en.wikipedia.org/wiki/")
   if valid_http_start or valid_https_start:
      return True
   return False

def return_wiki_page_name(wiki_url):
   if is_wiki_url(wiki_url):
      url_split = wiki_url.split("/wiki/")
      page_name = url_split[1]
      return page_name
   return False

def follow_url(url):
   try:
      page = urllib2.urlopen(url)
      return page
   except (ValueError, urllib2.URLError) as e:
      print e
      return False

# Create database connection object

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(db_file)
        print("Connection created...")
        return conn
    except Error as e:
        print(e)
        print("Error creating connection...")

    return None

# Create table within database
def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
        print("Table created...")
    except Error as e:
        print(e)
        print("Error creating table...")

# Insert paths and objects into Database
def create_path(conn, paths):
    sql = ''' INSERT INTO paths(name, pathListString, hops)
    VALUES(?,?,?) '''

    cur = conn.cursor()
    cur.execute(sql, paths)
    return cur.lastrowid

# Function to create table
def main(start_page_name, pathListString, hops):
    database = "pythonsqlite.db"

    sql_create_paths_table =  """CREATE TABLE IF NOT EXISTS paths (
    id integer PRIMARY KEY,
    name text NOT NULL,
    pathListString text,
    hops integer
    ); """

    conn = create_connection(database)
    print(hops)
    print(start_page_name)

    with conn:
        paths = (start_page_name, pathListString, hops);
        print(paths)
        path_id = create_path(conn, paths)


def hop_to_wiki_url(start_wiki_url, destination_wiki_url, limit):
   start_page_name = return_wiki_page_name(start_wiki_url)
   end_page_name = return_wiki_page_name(destination_wiki_url)

   pathList = [start_wiki_url]


   if start_page_name == end_page_name:
      print "Looks like we started at our destination page:",start_wiki_url
      print "0 hops"
      return


   philosophy_links = getting_to_philosophy()


   next_url = philosophy_links.get_philosophy_link(start_wiki_url)

   hops = 0
   print start_wiki_url

   while next_url != False and hops < limit:
      print next_url
      page_name = return_wiki_page_name(next_url)
      pathList.append(next_url)
      hops = hops + 1

      if page_name == end_page_name:
         print "Arrived."
         print hops,"hops"
         pathListString = ' '.join(pathList)
         main(start_page_name,pathListString, hops)
         return

      next_url = philosophy_links.get_philosophy_link(next_url)


   print "Looks like we hit our page-limit, a dead-end, a loop, or a bad link."
   print "Unknown # hops."
   return




################
# "Main":
################
if __name__ == "__main__":
   # build command-line parser
   parser = argparse.ArgumentParser(description='Getting to phiolosophy on Wikipedia.')
   parser.add_argument('STARTING_LINK', help='Link to English Wikipedia page to start hopping (http://en.wikipedia.org/wiki/some_page).')


   args = parser.parse_args()



   first_wiki = follow_url(args.STARTING_LINK)

   if first_wiki == False:
      print "Error folling given link."
      print "Please enter a valid (English wikipedia) URL, http://en.wikipedia.org/wiki/some_page"
      print "Exiting..."
      exit()



   if not is_wiki_url(args.STARTING_LINK):
      print "Starting link must be some to wikipedia page."
      print "Please enter a valid (English wikipedia) URL, http://en.wikipedia.org/wiki/some_page"
      print "Exiting..."
      exit()


   destination_wiki = "http://en.wikipedia.org/wiki/Philosophy"
   limit = 100
   hop_to_wiki_url(args.STARTING_LINK, destination_wiki, limit)
   #main()
