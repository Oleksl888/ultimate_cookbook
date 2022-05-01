# Lost_and_found
Final product is the website were user can create ads for items that they have lost or that they have found. 
Key features:
Website must be able to display three differen instances based on the user:
Guest - display the index page without login. No input is allowed from the user, read-only version
User - abilities of Guest version + user can create ads, edit exisiting ads, view the phone numbers in other ads, send messages to other users
Admin - abilities of User + can delete the ads of other users, can block the account of other users, can see the admin panel which shows totals of how many visits there has been to the website, list of all users with different statistics.

-Database schema-:
Table users:
USER ID - Unique, Username - Unique, Email - Unique, Phone - Unique, Password - Unique, Admin - True/False, First Name, Last Name.
Table ads:
USER ID - Unique(reference USER ID - link to users table), AD ID - Unique, AD Title NOT NULL(SET maximum symbols), AD BODY NOT NULL(SET maximum symbols), AD CATEGORY - (link to another table), AD Location - (Link to another table - use API), AD BLOB for storing images (1 per user for now)
Table Category:
CATEGORY ID, CATEGORY NAME
Table Location:
Location ID, Location Name
Table statistics:
USER ID, number of Sign Ins, number of ads created total, number of active ads, number of deleted ads
-Maybe just use sql requsts to get statistics on admin panel

-Register Function-:
Must be able to take input from user using html forms.
Info from user: Username - Unique(Neccessary), Email - Unique(Neccessary), Phone - Unique(Neccessary), Password - Unique(Neccessary), First Name - Optional, Last Name - Optional.
Input must be stored in the sql database. Database must be set up to have appropriate fields.
Password must be hashed before placed into the database (Hash function must be created or borrowed)
Register function must check if the required fields are unique and password is appropriate length  - return errors in case if something wrong
Optionally add confirmation of the email or phone verification (use APIs)
If info is correct - create entry in the database and commit changes.
Send a request to render a page with reply

-Sign in Function-:
Must be able to take input from user using html forms.
Info from user: Username, Password.
Input must be checked vs the sql database.
Password must be hashed before placed into the database (Hash function must be created or borrowed)
Function must check username/password are matching. If info is correct - update statistics entry in the database and render page based on user priveleges.

Website features:
No Login: 
Display index with top10 most recent ads
Search by name 
View ads by categories
View ads by location

User login:
All above + create, delete, edit personal ads
Account page - where you can view all the active ads
Ability to change details of account
Reset password via email function
Function to send messages to other users

Admin login:
All above + admin panel functionality
View list of all users registered with statistics
Function to disable ad
Function to disable account

--Ads Management--

--Create Ad--:

--Delete Ad--:

--Edit Ad--:

Website server must be created






