# MARKET HELPER (CAPSTONE PROJECT)
#### Video Demo:  https://youtu.be/huy1yYy5d4I
#### Distinctiveness and Complexity:
My web application is not based on any other project, neither Pizza project nor social network nor e-commerce-site.

It includes 3 Django models, one of which has a foreign key to another one, JavaScriptwise the project utilize asynchronous content delivery (ajax queries),
updatable calendar (working via FullCalendar library) and some quality of life features such as displaying/undisplaying needed blocks and sections of html page
on clicks.

None of the positioning is absolute, which makes the application mobile responsive: pages looks the same on any device.
#### Description:
Overview:

Market Helper is a tool that 1) helps to keep track of your stock portfolio and easily double check information given by your brocker as well as 2) add customizable info on your shares such as notes, ratings and events.

1) Keeping track part implemented with the idea of regular comparison of the two numbers: amount of money you deposited and actual current worth of all your holdings. Some of the processes are automated: for example, application utilizes IEX Cloud's API to update share's price if possible (and if not, application will say so by highlighting the unsuccessful shares). But at the same time some things are intentionally not automated: when buying share (via buy form) application doesn't check the quote for the share, you have to manually put the price instead. Another not-so-obvious thing is that web application doesn't check if you have enough money to purchase something and there are two reasons:
first is the idea to put in the exact prices your broker provided you with on an operation to keep track of how much exactly you paid for it and not for average price stock was selling at at that time
second is I'm from Russia and, as I created application for myself, sums that app compares are in RUB, which once again creates the necessity of precision: app needs to know not only what price my broker asked me for the stock, but what was broker's USD to RUB ratio at that time.

2) Notes and rating are just fields in the Share model, nothing too interesting, just to put down things to not memorize them. Events at the same time are using its own model with a foreign key to a share (might be blank too) and accessible either on a calendar page or on the share's page.

Backend of the application made with Python's framework Django, frontend made with JavaScript.

#### Files:

Besides automatically created Django files (manage.py, admin.py, settings.py, urls.py models.py etc), project contains SQLite database (controled with Django models), static folder which has 2 subfolders: one for FullCalendar library and one project's JavaScript, CSS and design (icon and background svg) and templates folder with the
templates for each of the page.

#### How to run:

Navigate to the project folder in your terminal (as via cd) and execute "python manage.py runserver".

#### Additional information:

For me personally, I consider it a better design to use a dark mode style when creating a text/numbers-info based applications, which helps to work with more comfort,
that is the reason my application is soft-black/beige.
