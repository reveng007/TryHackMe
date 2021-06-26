Task1: How websites work
-------------------------

By the end of this room, you'll know how websites are created and will be introduced to some basic security issues.

When you visit a website, your browser (_like Safari or Google Chrome_) makes a request to a web server asking for information about the page you're visiting. It will respond with data that your browser uses to show you the page; a web server is just a dedicated computer somewhere else in the world that handles your requests.

There are two major components that make up a website:

1. Front End (**Client-Side**) - the way your browser renders a website.
2. Back End (**Server-Side**) - a server that processes your request and returns a response.


**NOTE**:
There are many other processes involved in your browser making a request to a web server, but for now, you just need to understand that you make a request to a server, and it responds with data your browser uses to render information to you.


1. What term describes the way your browser renders a website?   

--> Front End


Task2: HTML
------------

Websites are primarily created using:

1. HTML, to build websites and define their structure
2. CSS, to make websites look pretty by adding styling options
3. JavaScript, implement complex features on pages using interactivity

**HyperText Markup Language (HTML)** is the language websites are written in. Elements (also known as tags) are the building blocks of HTML pages and tells the browser how to display content.

The code snippet below shows a simple HTML document, the structure of which is the same for every website:

```html
<!DOCTYPE html>
<html>
	<head>
		<title>Page Title</title>
	</head>
	<body>
		<h1>Example Heading</h1>
		<p>Example paragraph..</p>
	</body>
</html>
```

- `<!DOCTYPE html>` defines that **page is a HTML5 document**. This helps with standardisation across different browsers and tells the browser to use HTML5 tp interpret the page.

- The `<html>` element is the **root element of the HTML page - all other elements come after this element**.

- The `<head>` element contains **infos. about the page(such as the page title) - Actually the name that can be seen in the tab portion**

- The `<body>` element defines the **HTML document's body; only content inside of the body is shown in the browser**(separate panel)

- The `<h1>` element defines a **large heading**

- The `<p>` element defines a **paragraph**

- There are many other elements (tags) used for different purposes.
For example, there are tags for buttons (`<button>`), images (`<img>`), lists, and much more.


#### NOTE:

Tags can contain attributes such as the **class attribute** which can be used to **style an element** 
e.g.**`make the tag a different color`** --> `<p class="bold-text">` 

or the **src attribute** which is used on images to **`specify the location of an image`** 
--> 
```html
<img src="img/cat.jpg">
```
An element can have multiple attributes each with its own unique purpose, 
e.g., 
```html
<p attribute1="value1" attribute2="value2">
```

Elements can also have an **id attribute** (`<p id="example">`), which is **unique to the element**.
Unlike the class attribute, where multiple elements can use the same class, an element must have different id's to identify them uniquely. Element id's are used for styling and to identify it by JavaScript.

You can view the HTML of any website by right-clicking and selecting "View Page Source" (Chrome) / "Show Page Source" (Safari).


1. One of the images on the cat website is broken - fix it, and the image will reveal the hidden text answer!

--> HTMLHERO

2. Add a dog image to the page by adding another img tag (`<img>`) on line 11. The dog image location is img/dog-1.png

--> DOGHTML


Task3: JavaScript
------------------

- **JavaScript (JS) is one of the most popular coding languages in the world** and allows pages to become **`interactive`**. **HTML** is used to create the _website structure and content_, while **JavaScript** is used to _control the functionality of web pages_ - **without JavaScript, a page would not have interactive elements and would always be static**. 

- **JS** can **`dynamically update the page in real-time`**, giving functionality to change the style of a button when a particular event on the page occurs (such as when a user clicks a button) or to display moving animations.


JavaScript is added within the page source code and can be either loaded within **`<script> tags`** (When directly adding js to the HTML code) or can be included remotely with the src attribute: **`<script src="/location/of/javascript_file.js"></script>`**(adding js from another js file, just like importing)


The following JavaScript code finds a HTML element on the page with the id of "demo" and changes the element's contents to "Hack the Planet"

```javascript
document.getElementById("demo").innerHTML = "Hack the Planet";
```

HTML elements can also have events, such as **`"onclick"`** or **`"onhover"`** that execute JavaScript when the event occurs. 

The following code changes the text of the element with the demo ID to Button Clicked: 
```
<button onclick='document.getElementById("demo").innerHTML = "Button Clicked";'>Click Me!</button>
```

- onclick events can also be defined inside the JavaScript script tags, and not on elements directly. 

1. Click the "View Site" button on this task. On the right-hand side, add JavaScript that changes the demo element's content to "Hack the Planet"

--> JSISFUN


Task4: Sensitive Data Exposure
-------------------------------

**`Sensitive Data Exposure`** occurs when a website _doesn't properly protect (or remove) sensitive_ **clear-text information to the end-user**; usually found in a _site's frontend source code_.

We now know that websites are built using many HTML elements (tags), all of which we can see simply by "viewing the page source". A website developer may have forgotten to remove login credentials, hidden links to private parts of the website or other sensitive data shown in HTML or JavaScript.

**Sensitive information** can be potentially leveraged to further an attacker's access within different parts of a web application.
For example, there could be **`HTML comments with temporary login credentials`**, and if you viewed the page's source code and found this, you could use these _credentials to log in elsewhere on the application (or worse, used to access other backend components of the site)_.

#### NOTE:

Whenever you're assessing a web application for security issues:

One of the **first things** you should do is **`review the page source code`** to see if you can find any exposed login credentials or hidden links.


Task5: HTML Injection
----------------------

HTML Injection is a vulnerability that occurs when:

1. **Unfiltered user input is displayed on the page**. 

2. If a website fails to **sanitise user input (filter any "malicious" text that a user inputs into a website)**, and that _input is used on the page_, an **attacker can inject HTML code into a vulnerable website**.

![](https://github.com/reveng007/TryHackMe/blob/main/_SUBSCRIPTION_/paths/Complete%20Beginner/04.Web%20Hacking%20Fundamentals/01.How%20websites%20work/login_panel1.png?raw=true)


![](https://github.com/reveng007/TryHackMe/blob/main/_SUBSCRIPTION_/paths/Complete%20Beginner/04.Web%20Hacking%20Fundamentals/01.How%20websites%20work/login_panel2.png?raw=true)


##### Login panel front end code:
```html

<!DOCTYPE html>
<html>

<head>
    <title>How websites work</title>
    <link rel="stylesheet" href="css/style.css"></link>
</head>

<body>
    <div id='html-code-box'>
        <div id='html-bar'>
            <span id='html-url'>https://vulnerable-site.com</span>
        </div>
        <div class='theme' id='html-code'>
            <p id='welcome-msg'></p>
            <form id='form' autocomplete="off">
                <div class='form-field'>
                    <input class="input-text" type="text" id="name" placeholder="Whats your name?">
                </div>
                <button onclick="sayHi()" type='button' class='login'>Say Hi</button>
            </form>
        </div>
    </div>
    <script src='js/script.js'></script>
    <script>
        function sayHi() {
            const name = document.getElementById('name').value
            document.getElementById("welcome-msg").innerHTML = "Welcome " + name
            setTimeout(checkAnswer, 100)
        }
    </script>
</body>

</html>
```
We can see that **name** is not **sanitized!**, _directly inputed strings are used here_.

1. View the website on this task and inject HTML so that a malicious link to http://hacker.com is shown.

Malicious Input:
```
<a href="http://hacker.com">
```

--> `HTML_INJ3CTI0N`


