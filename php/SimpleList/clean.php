<?php include("includes/head.php");

// Check if there are any users, if not, add the one that has credentials
// for the sql database.

// Try adding user if possible.
try {
	
	create_user($DB_USER, $DB_PASSWORD, true, true, -1);
	//$result = exec_query("INSERT INTO Users (usr_id, username, usr_password, is_admin, is_validated) Values (-1, \"".$DB_USER."\", \"".$DB_PASSWORD."\", TRUE, TRUE)");
	echo "Default user created with username: '".$DB_USER."' and password: '".$DB_PASSWORD."'";
} catch(Exception $e) {}

// Delete the old articles.
$result = exec_query("DELETE FROM Articles WHERE begin_time < (NOW() - INTERVAL ".$MESSAGE_EXPIRE_DAYS." DAY)");
?>

<h1>The database for this site is done being cleaned.</h1>

<?php include("includes/tail.php");
