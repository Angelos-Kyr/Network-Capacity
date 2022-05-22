# Network Capacity
#### Description:
The Network Capacity program is made to facilitate everyday life and meet the needs of a company that gives IP to users. Until now the company was calculating the capacity that each network had and its occupancy manually and you could not have a clear and quick picture of its occupancy so that it is 100% stable to the users , so what we need is an API that calculates the occupancy with the possibility of filters and a search bar because such companies have to deal with too many networks . As a first step we have to copy an excel file that has all the trials that the company provides this will start from the month of November but to have a better future use we will use the whole last quarter , so we create our database from which our table will then get all the necessary information. To solve such a problem we will use Python as the main programming language to meet the backend needs just like we did in week 9 and Flask with Html for the frontend needs. With this API we can calculate with the help of "Linear Regression" methods the first quarter of the new year and thus avoid the dissatisfaction of our users from any Overlord . Our API has as a first image all the trials has a search bar and has 4 buttons , the first one is "All" with which we can see all the trials regardless of their occupancy, the second one is "<5%" where here we can use our first filter limiting only the trials that have less than 5 percent free IP, as third we have the "<10%" where we filter and show us the networks that have less than 10 percent free IP and our last button is the "Preview" where by pressing this button we can see the most likely occupancy of all the networks and using the exact same buttons we can again put our filters to see which networks are likely to be more loaded and by pressing the "back" button we can again return to our home page. For more information I am at your disposal. Before closing this text I would like to thank you for beautiful videos and the many insights you have given me .

The Project consists of:
Static Folder: contains style.css which is used to format the HTML document and describes how those elemnts should be displayed.

Template Folder: contains two HTML files which create the "backbone" of our table.

Database.py: is used to create, connect and manage the Databases

Helper.py: is used to manage and parse the configurations needed from the program and to enable users credentials validation. The "configparser" module from Python's standard library defines functionality for reading and writing configuration files and "getpass" module prompts users to enter their credentials.

Linear_regression.py: with SciPy library help we can calculate the future network load, up to three months.

Main.py: here can be found the whole structure of the table and the project is being initialised. For time calculation the "datetime library" is being used. To read and write in Excel files we are using "openpyxl" library. Urlib3 is a dynamic library that is being used for better and friendlier HTTP operation.

Web.py: is providing HTML template with the appropriate network capacity information. To create a "finished" web application we are using Framework Flask. NumPy library is used to handle Lists and Arrays and Pandas library is used to manage high load of Data in columns and lines.

The final version packets that are being used in the project, please check requirements.txt