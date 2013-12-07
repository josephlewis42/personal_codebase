<?php

/**
 * This software requires that you install the PEAR PHP Mail package, and
 * the Mail_Mime package.
 * 
 * The configuration here allows you to setup the email address that
 * SimpleList's emails are coming from.
 */
#$SMTP_HOST = "ssl://smtp.example.com"; # For SSL
$SMTP_HOST = "mail.example.com";
$SMTP_USERNAME = "smtp_username";
$SMTP_PASSWORD = "smtp_password";
#$SMTP_PORT = "465"; # For SSL
$SMTP_PORT = "25"; 


// These are shown throughout the site.
$SITE_NAME = "SimpleList";	// i.e. "Not Craigslist"
$SITE_TAGLINE = "A listing site for humans";	// i.e. "The best place to post not craigslist ads"
$SITE_IMG_PATH = "";	// i.e. "/resources/imgs/small_img.png"

// This is the location that all links should point to for the install,
// useful if you do re-writing.
$BASE_SITE_PATH = "localhost/SimpleList/";

// This is the information to conenct to the database, be sure to edit it properly.
$DB_USER = "www-data";
$host = "localhost";
$DB_PASSWORD = "password";
$database = "test2";



// This information is used to validate email addresses people come from
// If you wish to restrict who can use this applicaiton, i.e. only people
// who have @yoursite.com domain email addresses, you would add yoursite.com
// An empty list means anyone can join.
// Because this application is built around communities and trust within them
// it is recommended you are exclusive. I originally wrote this site to try
// out student -> student book resales within my college.

//$VALID_DOMAINS = array("gmail.com","yahoo.com");
$VALID_DOMAINS = array();  // Default registration is array() == anyone.

$login_msg = "Please log in to see this.";	// Shown at places where the user needs to be logged in to see, i.e. contact info.


// Control over the length of messages goes here, the default amount of time to show them
// is 30 days.
$MESSAGE_EXPIRE_DAYS = 30;


// Tags allowed in posts and contact info slots, not titles however.
$TAGS_ALLOWED = "<img><b><i><u><a>";

function throwException($message = null,$code = null) {
    throw new Exception($message,$code);
}

/**
 * A simple function to connect to the Database and execute the query given
 * returns the result of the query or throws an exception.
**/
$connection = mysql_connect($host,$DB_USER,$DB_PASSWORD) 
		or die ("Couldn't connect to server.");

function exec_query($query){
	global $host, $DB_USER, $DB_PASSWORD, $database, $connection;
	//$connection = mysql_connect($host,$DB_USER,$DB_PASSWORD) 
	
	$db = mysql_select_db($database,$connection) 
		or die ("Couldn't select db.");
	$result = mysql_query($query)
		or throwException(mysql_error(),111);
	return $result;
}




include "db_functions.php";

function login_link($logintext="[login]", $logouttext="[logout]"){
	$enc = urlencode($_SERVER["REQUEST_URI"]);
	if(is_logged_in()){
		echo "<a class='choice' href='login.php?logout=true&return={$enc}'>{$logouttext}</a>";
	}else{
		echo "<a class='choice' href='login.php?return={$enc}'>{$logintext}</a>";
	}
}


function register_link(){
	if(is_logged_in())
		return;
	
	$enc = urlencode($_SERVER["REQUEST_URI"]);
	echo "<a class='choice' href='signup.php?return={$enc}'>[sign up]</a>";
}

function admin_link(){
	if(is_admin())
		echo "<a class='choice' href='new_admin.php'>[grant admin]</a>";
}

function settings_link(){
	if(is_logged_in())
		echo "<a class='choice' href='user_settings.php'>[settings]</a>";
}

/**
 * echos a [return] link that directs to the
 * last page if a "return=" get param is passed.
 * 
 * returns the param (default:/index.php) if no return
 * is made.
 */
function last_page_link($lastpage = "/index.php"){
	if(isset($_GET['return']))
		$lastpage = urldecode($_GET['return']);
		
	return "<a href='{$lastpage}'>[return]</a>";
}

/**
 * Logs an error to the system log, including a ticket number that a 
 * user can use to reference the error.
 */
 
function log_error($from_whence_the_error_came, $error){
	
	$uid = uniqid();
	error_log("SimpleList ".$from_whence_the_error_came." error ref id: ".$uid." description: ".$error);
	
	return $uid;
}


/**
 * Generates a standard toolbar, includes the links given as well.
 * 
 * each variable is an array of key--> value pairs, where the keys are
 * the text and the values are the links, save for back_loc which is 
 * a simple string.
 * 
 * ex: generate_menubar("my_last_page.php", array('new' => 'new.php'));
 * 
 * The values of logged in will be shown if the user is logged in
 * otheritems will always be shown
 * admin_items will only be shown to admins.
 */
function generate_menubar($back_loc=null, $logged_in=null, $otheritems=null, $admin_items = null)
{
	echo "<div id='menu'>";
	
	// Back button
	if($back_loc != null)
		echo "<a class='choice' href='{$back_loc}'>&lt; back</a>";
	
	// Login Button
	login_link();
	
	// Register Button (if not logged in)
	register_link();
	
	// Settings button
	settings_link();
	
	// Generates a new admin user.
	admin_link();
	
	if(is_logged_in() && $logged_in != null)
		foreach(array_keys($logged_in) as $key)
			echo "<a class='choice' href='{$logged_in[$key]}'>[{$key}]</a>";

	
	if($otheritems != null)
		foreach(array_keys($otheritems) as $key)
			echo "<a class='choice' href='{$otheritems[$key]}'>[{$key}]</a>";
	
	if(is_admin() && $admin_items != null)
		foreach(array_keys($admin_items) as $key)
			echo "<a class='choice' href='{$admin_items[$key]}'>[{$key}]</a>";

	
	echo "</div>";
}
	
?>
