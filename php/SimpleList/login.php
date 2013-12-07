<?php include 'includes/head.php'; 

// A quick index to the last page the user was at.
$lastpage = "index.php";
if(isset($_GET['return']))
	$lastpage = urldecode($_GET['return']);
	
$needform = false; // true if the login form nees to be output.


echo "<div id='menu'><a class='choice' href='{$lastpage}'>&lt; back</a>";
register_link();
echo "</div>";

// User wants to log out
if(isset($_GET['logout']) && !isset($_POST['submit'])){
	session_destroy();
	echo "<p class='error'>You are now logged out: ".last_page_link()."</p>";
	$needform = true;
// User already logged in
} elseif(is_logged_in()) {
	echo "<div class='error'><p>You are already logged in.</p></div>";

// Validate and login
} elseif(isset($_POST['submit'])) {
	$user = encode_user($_POST['username']);
	$pass = encode_pass($_POST['password'], $_POST['username']);
	
	try{
		$result = exec_query("SELECT * FROM Users WHERE username='{$user}' AND usr_password = '{$pass}'");
		
		$result = mysql_fetch_array($result);
		
		if($result[0] == null || $result[0] == '')
			throw new Exception("problem");
		
		$_SESSION['id'] = $result[0];
		$_SESSION['auth'] = "yes";
		$_SESSION['username'] = $user;
		$_SESSION['raw_username'] = $_POST['username'];
		$_SESSION['is_admin'] = $result['is_admin'];
		
		//Check if the user is an admin or not.
		if( $_SESSION['is_admin'])
			echo "<p class='error'>You are an admin, be wise.</p>";
		
		echo "<p class='notification'>You are now logged in: ".last_page_link()."</p>";

	}catch(Exception $ex){
		echo "<p class='error'>Couldn't log you in, please try again.</p>";
		$needform = true;
	}
	
// The user wants to log in
} else {
	$needform = true;
}

if($needform){
?>
<form class='notification' method='post' action='<?php echo $_SERVER["REQUEST_URI"]?>'>
<table>
	<tr>
		<td>Username</td>
		<td><input type='text' name='username' /></td>
	</tr>
	<tr>
		<td>Password</td>
		<td><input type='password' name='password' /></td>
	</tr>
	<tr>
		<td></td>
		<td><input type='submit' name='submit' value='Log In'/></td>
	</tr>
</table>
</form>
<br>
<div class='notification'><p>If you lose a password, there is no way to recover it due to the <a href='about.php'>anonymous nature of the database</a>.</p></div>

<?php
}
include 'includes/tail.php';
?>
