"""
This part will have a URLshortener class.


The class will take in the long_url and then use
the base62 encoding method to generate the shorter urls

base62  has:
The numbers 0-9 (10 characters)
The uppercase letters A-Z (26 characters)
The lowercase letters a-z (26 characters)

making the amount of combinations available much more than base10

For simplicity a dictionary could be used to map the long url with the short url, a database could be integrated later on.


The procedure: 
                Original Url is passed into .shorten_url() method, the method then checks if the url exists in the url map
                and either retrieves the id (which the counter being incremented from 1), or addes the key-value pair (original Url - id)
                , thus encoding the id using base62 encoding then attaching it to a base url (An example in this case only) and returning the shortened url.

                The .retrieve_original_url() method takes in the shortened url, decodes it to find the id, and then finds all instances of the original url
                within the disctionary that the value (id) matches the decoded id ----> So either  a list full of that url (if found) or an empty list (if not found)


For specifics :

                When encoding the divmod() function continously (via a while loop) divides the id (current counter) by 62 and finds the remainder
                that would then be used as an index in the full alphabet string attached "in reverse" to the base62 string.

                The decoding method flips the script. It multiplies the id by 62 then add the index of the specific characters in the shortened url.

                validators library can be used to check the validity of the url provided. 
                Custom aliases can be provided by the user as well (Note : Added to a different mapping as it conflicted with the original url map at first).

                Tests have been provided at the end.

Future Work:
                Implement persistent storage: Transitioning from a dictionary-based storage to a database system for scalability and persistence as mention before.

                Enhance error handling: Developing a more comprehensive error management to handle various edge cases and input errors.

                Optimize performance: Analyzing and optimizing the performance for handling a large number of URLs.

                Add user authentication and management: Introducing user accounts and personal URL management features.

Thank you for your time. 

"""

import string
import validators

class URLshortener:
    _alphabet = string.digits + string.ascii_letters # All characters and digites
    _base_url = "https://Fake.com/"  # Just an example that represents a domain (not real)

    def __init__(self):
        self._url_map = {}
        self._alias_map = {}
        self._counter = 1

    def _encode(self, id):
        base62 = ''
        while id > 0:
            id, remainder = divmod(id, 62)
            base62 = self._alphabet[remainder] + base62
        return base62

    def _decode(self, short_url):
        id = 0
        # Remove the base URL part before decoding
        short_url = short_url.replace(self._base_url, "")
        for char in short_url:
            id = id * 62 + self._alphabet.index(char)
        return id

    def shorten_url(self, original_url,alias = None):
        
        if not self.is_valid_url(original_url): # If the url is valid the not will prevent it from returning the statement
            return "Invalid URL"
        
        if alias:
            if alias in self._alias_map:
                return "Alias has already been used"
            self._alias_map[alias] = self._counter
        
        if original_url in self._url_map:
            return self._base_url + self._encode(self._url_map[original_url])

        current_id = self._alias_map.get(alias, self._counter) # If the URL is not in the _url_map and if an alias was provided, 
                                                               # it checks if this alias has a reserved ID in _alias_map; if not, it uses the current counter as the ID.
        self._url_map[original_url] = current_id
        short_url = self._base_url + self._encode(current_id)
        self._counter += 1  # Increments only if a new URL or alias is being added
        return short_url
    
        # CHATGPT enhanced respose
        """
        This separation and order of operations ensure that:

        The system maintains a clean mapping of URLs to their unique identifiers, whether those are derived from an alias or are auto-generated.
        Aliases are managed separately to allow them to be an optional, unique identifier that does not interfere with the primary URL-ID mapping.
        The system efficiently checks for and handles duplicates, which optimizes storage and retrieval while maintaining the integrity and uniqueness of shortened URLs.
        """


    def retrieve_original_url(self, short_url):
        id = self._decode(short_url)
        original_url = [url for url, index in self._url_map.items() if index == id]
        return original_url[0] if original_url else None

    def is_valid_url(self,url):
        return validators.url(url) # Checks the validity of the url
    








if __name__ == '__main__':

    shortener  = URLshortener()

    def test_duplicate_shortening(shortener):
        print("Testing Duplicate URL Shortening: ")
        url = "https://www.duplicate.com"
        first_shortened = shortener.shorten_url(url)
        second_shortened = shortener.shorten_url(url)
        print("First Shortened URL: ", first_shortened)
        print("Second Shortened URL: ", second_shortened)
        assert first_shortened == second_shortened, "The URLs should be the same."
        
    def test_url_validation(shortener):
        print("Testing URL Validation:")
        invalid_url = "htp://incorrect-format"
        valid_url = "https://www.example.com"
        print("Invalid URL Test: ", shortener.shorten_url(invalid_url))  # Expected: "Invalid URL"
        print("Valid URL Test: ", shortener.shorten_url(valid_url))  # Expected: Short URL

    def test_custom_aliasing(shortener):
        print("Testing Custom Aliasing:")
        url = "https://www.unique-domain.com"
        alias = "uniquealias"
        print("First use of alias: ", shortener.shorten_url(url, alias))  # Expected: New Short URL
        print("Reuse of alias: ", shortener.shorten_url(url, "uniquealias"))  # Expected: "Alias has already been used"

    def test_retrieval(shortener):
        print("Testing URL Retrieval:")
        url = "https://www.retrieve.com"
        shortened = shortener.shorten_url(url, "retrievealias")
        print("Shortened URL: ", shortened)
        print("Retrieved URL: ", shortener.retrieve_original_url(shortened))  # Expected: Original URL
    
    test_retrieval(shortener)
    test_duplicate_shortening(shortener)
    test_url_validation(shortener)
    test_custom_aliasing(shortener)
    


