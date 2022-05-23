# Ultimate cookbook
An async web-server based on sockets.
# Key Features:
Index with list of recipes and ingridients. On click on recipe, a post request is generated, a text file with recipes is accessed and matching recipe is rendered on html page. Together with that a search is made via Flickr API to find an image by name - tag of the recipe. 
Images are cached in the /images folder but yet cannot be accessed from file.
With click on ingridients a search is performed which returns all the recepies featuring given ingridient
Search returns all matching ingridients and recipes in table format.
Gallery loads all the images on file - *Currently does not work*
Feedback uses a form to leave feedback on page with a timestamp. Feedback is collected in text file.
