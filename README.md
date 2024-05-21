# Next

#### Video Demo: https://youtu.be/XQQy39gyflA

## Description

Next is a web application that helps users track games/sports that involve two teams or players competing against each other. The idea came about when I would be playing Volleyball with a lot of people, and someone would join and say that they will play next and then someone else comes later and says that they were next. This would create a lot of arguments and debate, so I saw an opportunity to create a simple app to solve this problem.

Essentially, this app allows users to create a game, or join an existing game. Both routes will lead the user to a game page that displays the game name, who is currently playing, who is up next, a game code so that others could join, and some actions. Those actions include adding users to the up next section, starting the next game through declaring the winner, and ending the entire game session. The app also allows users to create accounts and log in in order to create and keep track of multiple games at a time.

The app adopts a "winner stays on" approach, where the winning team/player would remain in the game and the next team/player would play against the current winner. I opted for this approach since it was the way my friends and I played all sports and video games.

#### Design Choice

As far as design goes, I chose to go with a very simple design to allow users to just focus on the data in front of them. I did not want any distractions in the app since its entire purpose was to provide information that solved confusion on the court.

#### Tech Stack

The app was built using Flask, meaning the languages I used were mainly python, html, css and some little javascript. Thus, this application includes a templates folder, a static folder, an app.py file, and a helpers.py file. For the database, I used SQLite3, since a table format was the best approach for the data storage. I also opted for bootstrap to provide some design tools.

### Templates Folder

In the templates folder is 8 html files that represent all the pages of the app.

#### layout.html

This file is the template file over which all the other files are built. It includes all the necessary links and tags to link the CSS file, and bootstrap. It also includes the html code for the navbar, which stays constant throughout the entire app. The title and body tags include jinja code to allow for the content of the other files.

#### index.html

This file represents the landing page, or what the user sees first thing after logging in. It includes the title of the app and two buttons that allow the user to create a new game, or join an existing one.

#### new.html

Upon clicking on create a new game, the user is then taken to this page, where they would fill a form that asks for the game title and the names of the two teams/players to play against each other.

#### join.html

This file displays a text input and a search button. Users would input the 6-digit code for the game they would like to join and click search. If the game exists, the user will be directed to the game. If not, an error code appears telling the user that the game does not exist.

#### mygames.html

This page simply displays all the games that the user has created. The user can click on a game and will be navigated to the game page of the respective game.

#### game.html

This is the main page of the entire app. It displays the name of the game, who is currently playing, who is up next, and the 6-digit code of this particular game. The page also allows users to add players to the up next section, end the current "match", declare the winner, and start a new one with whoever is next, and end the entire game session.

#### login.html

Displays a form that allows users to log in with their username and password.

#### register.html

Displays a form where users would create an account by typing the username, password, and confirm password.

### app.py

This is the python folder where most of the functionality is stored. For each of the previously outlined features, this file is where the logic is written.

### next.db

This is a SQLite3 database consisting of three tables: users, games, and players. The users table stores the id, username and the hash of each user. The games table stores the name of the 6-digit id of the game, its name, and the id of the user who created it. The players table stores the id of the player, their name, the id of the game they are playing, and a timestamp of when that player was created in order to properly place them in the up next section.

### helpers.py

This file only stores a function that requires users to log in before they access a certain route.
