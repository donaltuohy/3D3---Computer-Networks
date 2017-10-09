<h1>Proxy Server</h1>

<p>The repository contains the python code written to create a proxy server the management console used to control the blacklist. 
The proxy is implemented using sockets. Here is the process in which the proxy runs:</p>

<ul>
 <li>The browser sends a get request to the proxy through a socket.</li>
 <li>The proxy takes this get request a creates a thread which will deal with this get request individually. </li> 
 <li>In this thread, the get request is parsed so that the essential information such as the web server address, the url and the port, are stored in variables in python. This way, they are easy to access.</li>
 <li>The url is then checked against the blacklist. If it should be blocked, a html page which says that the page is blocked is sent back to the browser through the browser socket.</li>
 <li>If the url is not blocked, the cache directory is checked. If the site is cached and the cache is not too old, a flag is set.</li>
 <li>If there is no existing cache, a socket is opened up with the corresponding  web server and the get request is sent through it. The reply received is then sent back to the browser and also cached in the cache directory for future use.</li>
<li>If the site is cached, the cached data is sent back to browser which makes the process much shorter.</li>
<li>The thread is now finished so the sockets are closed the page should have loaded on the browser. </li>
<li>The management console works dynamically by using a series of functions which open a close a the blacklist file.</li>
</ul>


