<h1>RAILWAY_MANAGEMENT_SYSTEM</h1>
<h3>Installation and Setup</h3>

<h4>1. Install MySQL</h4>
<p>Install MySQL Server and MySQL Command Line Client:</p>
<ul>
    <li>Download MySQL Server from <a href="https://dev.mysql.com/downloads/mysql/">MySQL Official Website</a>.</li>
    <li>Follow the installation instructions for your operating system.</li>
    <li>Ensure MySQL server is running.</li>
</ul>

<h4>2. Install Python and Dependencies</h4>
<p>Ensure Python 3.x is installed. Install required Python packages:</p>
<pre>
pip install Flask Flask-MySQLdb Flask-JWT-Extended
    </pre>
<h3>Clone the Repository</h4>
    <p>Clone the project repository from GitHub:</p>
    <pre>git clone https://github.com/moulipasalapudi/API_RAILWAYS_TASK.git
</pre>
<pre>cd API_RAILWAYS_TASK</pre>

 <h3>Running the Application</h4>
    <p>Run the Flask application:</p>
    <pre>python app.py</pre>
  <h3>Accessing Endpoints</h3>
  <p>Make sure app.py is running on other terminal execute these scripts</p>
    <p>Use the following PowerShell scripts to interact with the application endpoints:</p>
    <h3>1.Script for Checking Whether Database is Accessible</h3>
    <pre>$response = Invoke-WebRequest -Uri http://localhost:5000/check/check_db -Method GET
$response.Content</pre>
    <h3>2.Script for Creating a User</h3>
    <pre>$headers = @{
    "Content-Type" = "application/json"
}

$body = @{
    "username" = "sameer"
    "password" = "sameer2345"
} | ConvertTo-Json

$response = Invoke-WebRequest -Uri http://localhost:5000/user/register -Method Post -Headers $headers -Body $body

$response.Content</pre>



<h3>3.Script to Login</h3>
    <pre>
$headers = @{
    "Content-Type" = "application/json"
}


$body = @{
    "username" = "ameer"
    "password" = "ameer2345"
} | ConvertTo-Json


$loginResponse = Invoke-RestMethod -Uri "http://localhost:5000/user/login" -Method POST -Headers $headers -Body $body


$loginResponse | ConvertTo-Json -Depth 10
</pre>
<p>This access token is used for accessing next endpoints </p>
<h3>4.Script for Availability of seats</h3>
    <pre>
$headers = @{
    "Content-Type" = "application/json"
    "Authorization" = "Bearer <token>"
}


$body = @{
    "source" = "Station A"
    "destination" = "Station B"
} | ConvertTo-Json


$response = Invoke-RestMethod -Uri "http://localhost:5000/booking/check_availability" -Method POST -Headers $headers -Body $body


$response | ConvertTo-Json -Depth 10
</pre></pre>


  
