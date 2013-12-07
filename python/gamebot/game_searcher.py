import codescraper

DEBUGGING = True

class NoResultsException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class GameSearcher:
    '''The game searcher class provides a framework for searching Google for 
    swfs.'''
    _page_list = []
    _list_loc = 0
    _next_page = 0
    _game_query = ""
    _current_url = ""  #The current swf's url.
    max_recursion = 30  #Number of pages to search until saying there is no game
    current_recursion = 0
    
    def _clear_current_search(self):
        '''Clears the current game search.'''
        self._page_list = []
        self._list_loc = 0
        self._next_page = 0
        self._game_query = ""
    
    def _get_more_games(self):
        #Get google page, and get potential paths
        query = self._game_query + "&start=" + str(self._next_page)
        page_text = codescraper.fetch_page(query)
        
        #There are 10 results per page, so the next page should be 10 results further along.
        self._next_page += 10
        
        #This gets all the text between the tags given on the page.
        url_list = codescraper.return_between("<cite>", "</cite>", page_text)
        
        if url_list == []:
            raise NoResultsException, "No results found!"
            
        
        for a in url_list:
            #Google sometimes puts html tags in their cite tags like <b>
            #since these will become messy when you try to create urls from it
            #we need to remove them.
            a = codescraper.remove_HTML_tags(a)
            self._page_list.append(a)
            
    def _get_next_game_url(self):        
        '''Creates a url for the next game on the list.'''
        try:
            url = 'http://' + self._page_list[self._list_loc]
        except IndexError:  #Index out of bounds.
            self._get_more_games()
            return self._get_next_game_url()
        
        self._list_loc += 1
        
        return url
        
    def get_next_game(self):
        
        self.current_recursion += 1

        #Get the next game url
        url = self._get_next_game_url()
        if url == None:
            return None

        
        #Get the content type as told by the webserver.
        ct = codescraper.url_content_type(url)
        if ct in ["application/x-shockwave-flash", "text/html; charset=iso-8859-1"]:
            self._current_url = url  #Remember the current url.
            return url
            
        return self.get_next_game()
        
    def get_current_game(self):
        return self._current_url
        
    def search_for_games(self, query):
        '''Searches for games with the current query'''
        #Clean the current search
        self._clear_current_search()
        #Build google query
        query = query.replace("%20", "+")
        self._game_query = "http://www.google.com/search?q=" + query + "+filetype%3Aswf&hl=en&num=10"
        
        #Populate the list so the first request will be faster.
        self._get_more_games()

if __name__ == "__main__":
    print("Running breaking tests.")
    g = GameSearcher()
    g.search_for_games("blah blah all good things happen to great people hannah")
    
    while(g._list_loc < 1):
        print g.get_next_game()
    
    print("Running bubble tanks tests.")
    g.search_for_games("bubble%20tanks")
    
    while(g._list_loc < 1):
        print g.get_next_game()
