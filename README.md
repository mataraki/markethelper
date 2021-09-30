# I MUST
#### Video Demo:  https://youtu.be/6EiNbg_nrbs
#### Description:
Overview:

I Must is the web application made in Flask using JavaScript, Python and SQL 
with the help of libraries such as jQuery and Bootstrap.

For the realisation I borrowed some helper-functions used for the CS50's pset9,
basically the whole register-login-logout mechanics, hope that's ok since
implemented it myself there.

My web application keeps track of the things you want/need to do: so called
mustdo, mustbuy, mustread and mustwatch things, storing them in corresponding
tables in the SQL database. The users table is also there.

User can customize his experience a bit in the settings tab by using the page
loading for them by default via / route. That preference is stored in the
users table.

I also got expired by the David's ajax example from the Flask lecture and
implemented that - the "Watch" page suggests the name of the show using specific 
imdb table from the table in thelocal database and adds the rating automatically 
if the movie was found in it.

I made some cool visual style too: font, boldness of the name of the current
page in the navigation bar, background picture on the bottom of each page,
themed colors and some more.

Enjoy

File-by-file:

application.py is the main file that contains and defines every route

helpers.py contains login_required function, which keeps track that the user is
logged in while trying to access the routes where it needed
apology function is also inside: it generates the page with the picture on
server errors

imust.db contains six tables: users with the username, hash and preferenced
page; imdb with the name and rating of the shows; buy, do, read and watch
with all the information about those entries

requirements.txt contains the names of all necessary libraries

In static foulder there are logo and background image as well as css styles

And in templates there are htmls for layout and all the routes:

main and unloginned for the main page with and without session which has some
information about the features

login and register for corresponding actions with all thefields marked as 
required (that's the way i treated all the necessary inputs in all the forms)

settings, where user can choose they preferenced page loaded via "/" route

buy, do, read and watch with the access to corresponding tables in database
rendered as the interactive tables with the sort, search and pagination (thanks
to the Datatables library) and the forms to fill the tables, delete option is 
there too;
watchpage also has the autocompletion (not forced, more of an autosuggestion) 
with the help of ajax

And lastly i borrowed the apology page as an hommage to CS50 even though it's
almost impossible to visit it now via any route with the "required" properties
on necessary fields and reloads with error messages on errors. I chose this
option instead of the apology page because I think that it's the better user
exprerience: to not be redirected from the page you got error on, but get the
error message on that page instead