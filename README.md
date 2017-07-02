# CS-C3170 Web Software Development Group Project - Project plan and Final Submission Notes (2016-2017)
Group members:
Antti Koskimäki - 51301B,
Sami Mahamoed - 544333,
Paula Minni - 62686F

# You can check our notes about the final submission at the end of the report in section 6

# 1 - Project Goals

The main goal of the project is to develop and deploy a web store service that sells Javascript games and more specifically access to them, so that the games are played through the shop website. We'll use the Django framework as a base for this web store. In addition to having authenticated users buy and play games, we'll enable developers to add games to the service and receive payments for sold games. You can see a rough sketch how the service would look in a browser in picture 1 below.

As we get the service up and running, we also aim to test the software and the service well throughout the project and also take into consideration possible security issues, as these are quite relevant with real life commercial services where money changes hands. Our goal is also to keep the modularity and reusability of the code in mind during the development process so it would be easier for the service to switch various components if needed.

Regarding the additional features, we aim to implement all of those that were presented in the assignment document. With the authentication part, we'll start with the Django's own authentication system and try to implement outside services if the timetable permits it.

![Layout plan](http://git.niksula.hut.fi/akoskima/cs-c3170_wsd_project_2016/raw/master/wsd_layout_plan_1a.jpg)
Picture 1 - Sketch of the storefront Layout

# 2 - Plan for the program structure and functionality
## 2.1 – Important classes in the models.py
As for the basic service structure, we aim to utilize the MTV paradigm when using the Django framework, where the main functionality of the service lies in Python files models.py and views.py that contain the relevant classes linked to system database and linkage and direction to the templates that are used to render the presented web pages to the end user. You can see the basic structure of our program in picture 2 below. For the basic customer case, the urls.py will direct the authenticated user initially to correct starting web page in the service, after which he/she can purchase and play games (in the case of a new user, there is a subscription process). The games are separate web pages that contain the Javascript code that makes the games work. These games can be accessed with the storefront iframe components that link to the particular game web page. One important feature with the games is that they can communicate back and forth with the parent web page via “window.postmessage”-type messaging.

![Project program structure](http://git.niksula.hut.fi/akoskima/cs-c3170_wsd_project_2016/raw/master/wsd_plan_1b.jpg)
Picture 2 - The basic program structure

## 2.2 – Important classes in the models.py
For basic store functionality, we plan to implement at least 3 classes in the models section that link to the database: User, Developer and Game

1. Class User – This class can contain personal information about the user (email, nickname, etc.), information about the possible store credit balance, which games are bought and can be accessed, saved game status data and various game achievements.

2. Class Developer – This class can contain data about the developer's games such as quantity of sold copies and credit balance in addition to having some personal information.

3. Class Game – This class can contain global game statistics such as high score lists and can also direct to the game's web page in the service.

## 2.3 - Web APIs
### 2.3.1    Cross-origin Messaging

The service will utilize windows.postMessage method for cross-origin communication with the game server.  The game server is expected to strictly follow the supported message structures described below.

The game server will send appropriate messages to the parent window to trigger different events on the service side. The parent window listening to Incoming messages will pass the data to the corresponding views via ajax call if the following conditions are satisfied.

1. The origin of the message is expected URL
2. The syntax for the message is verified.

Regarding outgoing messages will be handled by JavaScript function implementation linked to the corresponding parent page. This events will be triggered on window load event and if error occurs while processing incoming message.  

More description on each event is provided below.

#### 2.3.1.1              Req. Game Score message

In order to update global high score section of the page with new value. The game server can trigger SCORE event by sending score message to the current parent window. The expected message structure for SCORE message is as follows.

score_message = {
messageType: "SCORE",
score: value // Float
};

#### 2.3.1.2              Req. Game Save message

The game server can write the game state to the service database by triggering the SAVE event via save message.  The expected message structure for SAVE message is as follows.

save_message =  {
messageType: "SAVE",
gameState: {
playerItems: [],
score: value // Float
}
};

#### 2.3.1.3               Req. Game Load request message

The game server can request for game state from the service database via LOAD_REQUEST message.  The service will respond LOAD or ERROR message upon success or failure respectively. The expected message structure for LOAD_REQUEST message is as follows.

Load_request_message = {
messageType: "LOAD_REQUEST"
};


#### 2.3.1.4              Req. Game LOAD message

The service will send LOAD message to the game server as target origin. To load the recently saved state of the game on the game server side. The message structure for LOAD message is as follows.

Load_message = {
messageType: "LOAD",
gameState: {
playerItems: [],
score: value // Float
}
};


#### 2.3.1.5              Req. Game ERROR message

The service will send ERROR message to the game server. To notify error event during message exchange. The message structure for ERROR message is as follows.

error_message =  {
messageType: "ERROR",
info: " human-readable error description "
};


#### 2.3.1.6              Req. Game SETTING message

The game server can adjust different layout parameters on the parent window. However, in the current version only width and height parameters of the iframe can be adjusted.  The message structure for SETTING message is as follows.

setting_message =  {
messageType: "SETTING",
options: {
           "width": value, //Integer
      "height": value //Integer
}
};

### 2.3.2        Req. Payment Service API
The service will implement an external service named Simple Payment Service, to facilitate options where players can purchase games on the platform. The payment request will be generated from the view using POST request. Here, the purpose of the API is to handle the payment result. Thus, the api URL will be specified as success url, cancel url and error url on the payment form. And the API method implementation will process the result request form Simple Payment Service in such a way that: verify Checksum, update database and pass result message (success or failure) to the appropriate view.

### 2.3.3         Req. RESTful API
The service will provide various data access for external applications through this API implementation. For this purpose, the service will utilize Django REST framework.
In the current version available games, high scores and game sales for developers can be accessed as discussed below.   

#### 2.3.3.1             Games

External or internal applications can access available games data using the following API request URL format.

^/api/v1/games/ID

Here, the parameters year or ID can be omitted both or individually. Thus, if both are omitted the service will return all available games from database. If year only is specified all games published within the specified year will be returned. If ID is specified a single game with matching ID will be returned.

The GET parameters are all optional.  Similarly, if offset and limit parameters are specified the response data will be in the specified range otherwise no limit will be applied to the response.   

The response data structure is shown below.

{
{
      "ID": "Game ID"
"Title": "title",
"Developer": "Developer id",
"Year_Published": "YEAR",
"Number_Of_likes":"value"
"Total_number_Of_players": "value"
},
…
}

#### 2.3.3.2              High scores

External or internal applications can access High scores data using the following API request URL format.

^/api/v1/games/Scores/

Here, if ID is omitted all recorded scores will be returned. Thus, the response is High score data to specific game if the game ID is specified. Similarly hear, as in the previous case JSONP format response will be returned if callback function is specified.   

The response data structure is shown below.

{
      "Player Name": "Score",
}

#### 2.3.3.3              Sales

Internal applications can access sales data using the following API request URL format.

^/api/v1/games/Sales/developer?start=Date&end=Date  

Here, if developer id is omitted or developer is not authenticated Http 400 will be returned. The GET parameters start and end which indicate sales period are required. Thus if omitted Http400 will be returned.

The response data structure  is shown below.

{
      "Game ID": "ID",
"Sold Qty": "ID",
"Total price": "ID",
}

## 2.4 - Priorities
The application main priority will be **Security** followed by **functionality** followed by **appearance** followed by **features**.

# 3 - Working process and schedule for the project

The main thing about our project development is that large majority of the actual coding is done individually by each of us. The combined code is then kept in GitLab, where we then update it periodically as we move along in the development. Regarding communication, we aim to make a Trello project page to help with observing the coding advancements. For more immediate project-related discussions, we'll use whatsapp, and for some larger notifications about the project, we'll also try to send emails. We'll likely divide the workload so that Antti will do presentation side and some parts of the models and views, Sami will implement API for the system and Paula will handle implementation for authentication. This is just a rough plan, though, and we all will likely to various additional tasks during the development process.

Regarding the timetable, we'll aim to follow roughly the schedule below:

1. 21.12.2016 – Return the finished project plan    
2. 23.12.2016 – 2.1.2017 – Christmas break
3. 3.1.2017 – 15.1. 2017 – Start working on the basic framework of the project and deploy some usable code to Heroku at the end of this period to test that we have a working simple web service .
4. 16.1.2017 – 29.1.2017 – Finalize the models and views so that users/developers can be authenticated and some games could be added to the system, finish up more detailed layout for the presentation side, so we'll start to see functional web pages    
5. 30.1.2017 – 12.2.2017 – Try to have functioning service on the Heroku (so models and views should be almost done at this point), finish up visual presentation of the website, do testing for various things such as basic security and API functionality, code a simple game for the service if time permits    
6. 13.2.2017 – 19.2.2017 – Finishing touches, last minute testing and writing up the project report         
7. 19.2.2017 – Return the project and after this prepare for the demo session

# 4 - Testing

To verify the service implementation quality, manual and automated tests will be executed as part of the project. Here, the test cases will be identified during the project implementation. However, basically the tests we plan to perform can be classified into three types as described below.  

* Authorization and authentication Tests - Both manual and Automated test cases will be identified and performed to prevent security attacks such as unauthorized access, script injection, Privilege escalation, session fixation and other vulnerabilities. If time allows penetration test and vulnerability scanner software tools will be utilized to identify and improve the security of the application.

* Bug Tests - Python standard library unittest module will be utilized to identify logical errors within the code. Also Django testing tools will be used for testing database transaction behavior and correct template rendering.  

* Crash & idiot proof Tests - In this test, manual and automated stressful attempts will be made to explore the breaking point of the service, which can be used to identify possible amendments on software quality.

# 5 - Risk Analysis

The major risks of the webshop concerns security. In our project we rely on methodologies provided by the OWASP community to assess security. OWASP is a community that concentrates on web application security by providing information, tools and technologies regarding security.

On a high level security objectives can be divided into five topics: identity, financial, reputation, privacy and availability guarantees.

* Identity - Application must control that identity cannot be forged. This has two parts: preventing access to user accounts without authentication and preventing operations done by mimicking other users. For authentication we use Django authentication framework at the beginning and later 3rd party authentication methods (ie. Google or Facebook authentication). All operations done to user accounts and their contents must be verified to only access data the user is allowed to access. For example, developers should only be able to modify their own games. Users should not be able to mimic other users, for example by embedding scripts wherever user input is displayed on the application.

* Financial - Financial issues concern buying and selling the games. The web applications handles money transactions and they need to be highly secure. Transactions with the third party payment provider must be handled so that they can’t be forged, tampered, or replayed. The service won’t keep money balances for the users but the sums from sold games are probably used to pay the developers. Marking a game sold should only happen after a successful transaction from the payment provider. A log of transactions must be stored to prevent users from claiming they didn’t purchase a game. Major financial losses would happen if players would be able to play games they don’t own. This is of course possible by a user checking where the game is hosted and leaking this information. Preventing this particular threat is not in the scope of the application.

* Reputation - Reputation may not be easy to measure. But if the web application is seen as generally unsecure, developers may not want to sell their games in the webshop. On the other hand problems with privacy or payments can scare players away.

* Privacy - User data should be protected. The application does not gather a lot of sensitive data but one example of such could be the list of games people have bought or played. The list of games published by a developer can be public.

* Availability - There are no availability guarantees as such but we will of course test that the application won’t crash. Bad availability can hurt reputation in the long run but it is not a major security risk.

## Risk Assessment
For risk analysis it’s useful to identify the components that are most vulnerable for each threat category. For our application the major components are user authentication, payment integration and object ownership. Each component has its own threats which should be tested when developing the application.

# 6 - Final Submission Notes:

## 6-1 What Has Been Done and How Well?
### Authentication
For a base user identification and registration, we use the Django authentication framework with the build in user class and this used class is further extended with profile class to hold some non-authentication related data. In addition, when creating an account, email verification is required where the automatic email directs to a link which enables the new account. We think that this section is covered relatively well with our service so hopefully this warrants the maximum points or close to it.

### Basic player functionalities
The important thing here is that we have implemented the basic functionalities reasonably well. In our service players can view a list of available games, are able to view descriptions of those games and then are able to buy the games with the help of the course mockup payment service. Players can then view their games at the profile page and are able to access their games to play them either via the profile page or from the main games listing. Also user restrictions should work okay, as players can’t access games they have not bought, apart from viewing the description and highscore lists for those games. All the critical stuff regarding this section is done, so hopefully that warrants good points from this section.

### Basic developer functionalities
Every user can become a developer by simply adding their own game. The developed game is automatically added to developer’s own game listing and the developer is free to play the game. When adding a game you can add a name, description, url, image and price for the game. The game model defines which fields are required and which are optional. It also defines some default values, for example for the image.

Profile page lists all the games added by the developer. It also shows the sales of the games. The developer can also edit the game information or delete the game. We think that we offer the developers at least reasonable ways to add and modify games and also see some sales information, so hopefully this would warrant good points from this section.

### Game/service interaction
The game and service interact with each other as was instructed in the project description by using the postmessages from and to the game iframe using the required message types (SCORE, LOAD, SAVE etc.). The game service can the update the database to contain the player highscores and save/load the gamestate with our messaging scheme which is initially done between the game-playing page template, the actual game page (in frame) and then from the game-playing template to the views that manipulate the service database.

The views-template messaging is also done with ajax calls, so there is no need to refresh the whole page when for example loading a game. The messaging is successfully implemented as was instructed, so hopefully that warrants the 200 points or close to it from this section as the messaging was tested also with the course test game and seemed to work okay. Note that our implementation expects the settings to come in percentages which describe how large portion the iframe takes but nevertheless this could be changed easily to pixel input.

### Quality of Work
Regarding the structure of our code, we feel that our implementation is reasonably logical and additional features could be added easily (such as adding additional classes to models with additional message types to the messaging scheme and thus enabling some extra features so in that sense). We have also used the Django framework purposefully so there is a separation between the models, views and templates which enables for example switching to different page layouts without too much of a trouble. Regarding code comments, perhaps we could have done more with them, but as we use the Django framework and otherwise logical program structure and variable names, you can hopefully understand reasonably well what does what in the code, especially if you reference Django documentation when needed.

When discussing the UI of the service, we feel that the basic use of our service is quite straightforward and easy, as links lead to logical places, and buttons generally note what they do on themselves and so forth. The graphical layout of the service is also clear and not cluttered to facilitate the ease of use.

In regards to testing, this has perhaps not been done as well as we would have liked, but the basic functionalities of the service have been tested so that critical functions should work okay. These critical parts include checking for example that authentication works, game adding works, the cross service messaging works, games can be played, and that the database updates without problems via the views.py manipulation. All in all, there were perhaps some issues with this section, but hopefully we will still get decent points.

### Non-functional requirements in addition to the project plan and demo
For our workflow, you can check the git repository for what has been added
and when. Unfortunately we were late of the original planned schedule, but overall  the service code was built incrementally and in logical steps so there we no big additional problems.

Regarding teamwork, in addition of utilizing the project Git repository, we used Whatsapp for the immediate communication and used a Trello page to keep track of the programming tasks we needed to do and also who was doing what at which point. We worked mostly on our own, but we did have a few physical meetings to iron out some project details and to assign different tasks for different people.

We don’t know how much the demo session really affects this section at this point, but hopefully we would get decent points from here in addition to points got from the demo and from the initial project plan.

### Save/load and resolution feature
Save/load messaging is implemented as was suggested in the project description and it works decently, so hopefully this warrants the 100 points from this section or close to it.

### 3rd party login
We have added the possibility to login either via Facebook or via GitHub, so hopefully this warrants the available points from this section..

### RESTful API
We have implemented a straightforward RESTful API (which is the API app within the service) that can be used to get game, score and sales information from the service, where the sales data requires you authenticate. 



    The system will authenticates api requests using HMAC digest authentication method.
    The request should cointain authentication header with the following parameters
    username: secret id which can be accessed through profile page
    realm: any value with (string and number only, no special character)
    nonce:unix epoch timestamp generated as utc timezone
    response:checksum using MD5 algorithm
    password: secret key which can also be found via profile page

    the checksum will be caculated as follows
    #acceptable algorithm directive's value is "MD5 so we calculate HA1 as follows
    HA1=MD5(username:realm:password)

    #acceptable qop directive's value is null(unspecified), then HA2 is
    HA2=MD5(method:digestURI)

    #thus since the qop directive is unspecified,we calculate the response as follows
    response=MD5(HA1:nonce:HA2). Hopefully this implementation warrants good points from this section.

### Own game
We have implemented two games, one simple testing game for checking the cross service messaging and a bit more complex snake game that also supports the messaging fully (so it has save/load functionality). The game files are temporarily hosted within the game service so we wouldn’t require outside hosts for the project review and demo, but if the service was to be deployed for real, they would be hosted elsewhere. Hopefully the games we did warrant the 100 points or close to it from this section.

### Mobile Friendly
We utilize the bootstrap library for our service templates, which enables the pages to look okay with mobile devices. Hopefully this warrants some points from this section.

### Social media sharing
We implemented a possibility to share a game in Facebook. It shares a link to the game detail page where a user can play the game or they can register and then purchase the game themselves. Also the image of the game is also shared to Facebook. Hopefully this warrants decent points from this section.

## 6-2 Who Did What? (Task assignment)
Antti: Testing, project planning and management, developing the models, developing the cross site messaging, developing simple test game and more complex game for the service.

Paula: Testing, game adding, game editing and game deleting, listing all games in games page, scores page listing best 5 scores for all games, highscore listing in play page, personal highscore, social media sharing and some minor additions here and there.

Sami: Testing, project planning and management,setting up project frontend structure and base templates, setting up heroku environment, Payment handling,  RESTful API implimentation, Authentication system and email validation, profile page implementation, 3rd party login, game rating system, user registration and some minor additions here and there.   

## 6-3 Brief Instructions for the Service Use

Our service can be run in localhost and the Heroku deployment is available at:

https://awesome-game-shop.herokuapp.com/

(For localhost testing, check out the requirements.txt in the project repository root which tells the additional python modules that are needed for running the service.)

You can create a user account via the login link by clicking the register, but note that the process requires email validation. The email should give you a link to click, which enables your account and you can then log in with our user/password information.

First you are directed to the main page and from there you can check out the available games at the store via the “games” link at the top. You can also see top highscores for all the store games from the “scores” link at the top. Clicking a game in the game listing page leads you to a game description page, from which you can buy the game (this is done by utilizing the mockup payment service). You can then play the game by clicking the “play the game” button which directs you to a play page.

The play page is where the iframe gives you access to the game. In addition your current highscore, top overall highscores for the particular game, change to give rating to the game and also the share to Facebook-link are present there. You can click your username in the top right corner to access profile page where you see the games you have bought.

You can become a developer by just adding a game via the profile page to the system and this process you to form where you input the game name, it’s URL, description, icon picture and a price. The games you have inputted to the system are then displayed on your profile page and you can see their sale events and also the total amount of money you have accumulated from your game sales.

For localhost testing, you can flush the database for a clean slate, and then register users and with them you can add games. You can use the course test game and in addition you can check out our games that are hosted temporarily with the game service.

The simple game URL for localhost when adding a game to the service is:

http://localhost:8000/storefront/games/testgame1

The snake game URL for localhost is:

http://localhost:8000/storefront/games/snake

(If you're using the python manage.py runserver defaults)
