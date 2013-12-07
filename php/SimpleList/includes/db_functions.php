<?php

require_once('global.php');
require_once('Mail.php');
require_once('Mail/mime.php');

/**
 * Encode Username
 */
function encode_user($name)
{
	return sha1($name);
}

/**
 * Encode Password
 */
function encode_pass($pass, $username)
{
	return sha1($pass.$username);
}


/**
 * True if the user is logged in, false otherwise.
 **/
function is_logged_in(){
	return (!empty ($_SESSION['auth'])) && $_SESSION['auth'] == "yes";
	
}

/**
 * True if the user is an admin, false otherwise.
 **/
function is_admin()
{
	if(isset($_SESSION['is_admin']))
		return $_SESSION['is_admin'];
	else
		return false;
}

/**
 * Returns a category name from a category id.
 */
function cat_name_from_id($id){
	$CID = mysql_escape_string($id);
	try {
		$result = exec_query("SELECT * FROM Categories WHERE cat_id = ".$CID);
	
		$row = mysql_fetch_array($result);
	
		return $row['cat_title'];
	} catch(Exception $ex) {}
	return null;
}

/**
 * Deletes an article if the current user is an admin or if they own the
 * article.
 * 
 * Returns a string, success or error.
 */
function delete_article($article_id)
{
	try
	{
		$article_id = mysql_real_escape_string($article_id);

		if(can_delete_article($article_id))
		{
			$result = exec_query("DELETE FROM Articles WHERE article_id = {$article_id}");
			return "Deleted article";
		}
		else
		{
			return "Permission Denied: You are not authorized to delete this article";
		}
			
	} catch(Exception $ex) {
		return "An error occured with the reference code: ".log_error("db_functions.php:delete_article()",$ex);
	}
}

/**
 * Returns true/false, whether or not the current user can delete the 
 * article with the given id.
 **/
 
function can_delete_article($article_id)
{
	if(isset($_SESSION['id']))
		return is_admin() || get_article_owner($article_id) == $_SESSION['id'];
	else
		return is_admin();
}


/**
 * Deletes a category if the current user is an admin.
 * 
 * Returns a string, success or error.
 */
function delete_category($cat_id)
{
	try
	{
		$cat_id = mysql_real_escape_string($cat_id);

		if(is_admin())
		{
			$result = exec_query("DELETE FROM Categories WHERE cat_id = {$cat_id}");
			return "Deleted category";
		}
		else
		{
			return "Permission Denied: You are not authorized to delete this category";
		}
			
	} catch(Exception $ex) {
		return "An error occured with the reference code: ".log_error("db_functions.php:delete_article()",$ex);
	}
}


/**
 * Gets the owner of the article, returns null if there was an error.
 */
function get_article_owner($article_id)
{
	try
	{
		$article_id = mysql_real_escape_string($article_id);
		$result = exec_query("SELECT author FROM Articles WHERE article_id = {$article_id}");
		$result = mysql_fetch_array($result);
		
		return $result['author'];
	}catch(Exception $ex){
		log_error("db_functions.php:get_article_owner()", $ex);
	}
	return null;
}


/**
 * Creates a new category with the given title and subtitle, returns the
 * result string.
 */
function create_category($title, $subtitle) {
	// Make sure the user can create a category.
	if(! is_admin())
		return "Permission Denied: You are not authorized create a category";
		
	
	// Verify all data.
	$title 		= mysql_real_escape_string(strip_tags($title));
	$subtitle	= mysql_real_escape_string(strip_tags($subtitle));
	
	
	// Check that everything that should be filled is.
	if($title == "")
		return "The category title cannot be blank.";
	
	
	// If nothing failed, try it out.
	try {
		exec_query("INSERT INTO Categories (cat_title, cat_subtitle) VALUES ('{$title}','{$subtitle}')");
		
		return "Your category has been created";
	} catch (Exception $ex) {
		$uid = log_error("db_functions.php new_category()", $ex);
		return "An error occured with a reference id of: {$uid}.";
	}
}

/**
 * Sets up a user with the given email and password, and sends a 
 * verification email to them. If they don't register they won't be let
 * in and their account will be removed after enough days.
 */
function register_user($email, $pass)
{
	global $BASE_SITE_PATH;
	try {
		$orig_email = $email;
		
		create_user($email, $pass);
		
		$usr_id = get_user_by_name($email);
		if($usr_id == null)
			return "An error occured while trying to create you as a new user.";
		
		$val_id = uniqid();
		
		exec_query("INSERT INTO Validations (val_usr, val_id) VALUES ('{$usr_id}','{$val_id}')");
		
		
		$ec = send_mail($orig_email, "Registration: Almost done!", "Complete your registration by clicking on this link: <a href='{$BASE_SITE_PATH}validate.php?id={$val_id}'>Validate</a><br><br>\n\nThanks!");
		
		if($ec != null)
			return "An error occured while trying to send you an email.";
		
		return "You will get an email soon to validate you own the email address you provided, you must validate before your account is activated.";
		
	} catch (Exception $ex) {
		$uid = log_error("db_functions register_user()", $ex);
		return "An error occured with a reference id of: {$uid}.";
	}
}

/**
 * Actually creates a user account.
 */
function create_user($raw_username, $raw_password, $is_admin=false, $is_validated=false, $id=null)
{
	$name = encode_user($raw_username);
	$pass = encode_pass($raw_password, $raw_username);
	
	$is_admin = ($is_admin)? "TRUE" : "FALSE";
	$is_validated = ($is_validated)? "TRUE" : "FALSE";
	
	if($id != null)
		exec_query("INSERT INTO Users (username, usr_password, is_admin, is_validated, usr_id) VALUES ('{$name}','{$pass}','{$is_admin}','{$is_validated}',{$id})");
	else
		exec_query("INSERT INTO Users (username, usr_password, is_admin, is_validated) VALUES ('{$name}','{$pass}','{$is_admin}','{$is_validated}')");
}

/**
 * Validates the user with the given validation ID
 */
function validate_user($id)
{
	$id = mysql_real_escape_string($id);
	
	// Get validation user by id
	$usr = get_user_by_validation_id($id);
	
	if ($usr == null)
		return "There was a problem validating";
	
	// Set validated.
	try
	{
		$result = exec_query("UPDATE Users SET is_validated=TRUE WHERE usr_id = {$usr}");
		// Delete validation.
		$result = exec_query("DELETE FROM Validations WHERE	 val_id = '{$id}'");
		
		// Send login
		return "You have been validated, you may now <a href='login.php'>log in</a>";
		
	} catch (Exception $ex) {
		$uid = log_error("db_functions validate_user()", $ex);
		return "An error occured with a reference id of: {$uid}.";
	}

}


/**
 * Returns a user id from their raw username, null if none exists or an 
 * error occured.
 **/
function get_user_by_name($raw_name)
{
	try
	{
		$name = encode_user($raw_name);
		$result = exec_query("SELECT usr_id FROM Users WHERE username = '{$name}'");
		$result = mysql_fetch_array($result);
		
		if(! isset($result['usr_id']))
			return null;
		
		return $result['usr_id'];
	}catch(Exception $ex){
		log_error("db_functions.php:get_user_by_name()", $ex);
	}
	return null;
}

/**
 * Returns true if the id is from the same user as the username and pass
 * belong to, false otherwise. (checks if the username and password 
 * belong to the user);
 **/
function is_same_user($id, $raw_user, $pass) {
	try
	{
		$user = encode_user($raw_user);
		$pass = encode_pass($pass, $raw_user);
		
		$result = exec_query("SELECT usr_id FROM Users WHERE username = '{$user}' and usr_password = '{$pass}'");
		$result = mysql_fetch_array($result);

		if(! isset($result['usr_id']))
			return false;
		
		return $result['usr_id'] == $id;
	
	} catch(Exception $ex){
		$uid = log_error("db_functions.php:grant_admin()", $ex);
		echo $ex;
		return false;
	}
	
	return false;
}

/**
 * Grants a user admin privliges.
 */
function make_admin($username, $password)
{	
	if(get_user_by_name($username) == null)
		return "No user exists with this username and password";
	
	$name = encode_user($username);
	$pass = encode_pass($password, $username);
	
	try
	{
		$result = exec_query("UPDATE Users SET is_admin = TRUE WHERE username = '{$name}' AND usr_password = '{$pass}'");
		return "Success";
	}catch(Exception $ex){
		$uid = log_error("db_functions.php:grant_admin()", $ex);
		return "An error occured with a reference id of: {$uid}.";
	}
	
	return "o_O Well shit, something went horribly wrong!";	
}


/**
 * Removes a user with the given ID, destroys the session if the id
 * is that of the current user.
 */
 
function delete_user($id)
{
	try
	{
		$id = mysql_real_escape_string($id);
		exec_query("DELETE FROM Users WHERE usr_id = {$id}");
		if($id === $_SESSION['id'])
			session_destroy();
		
		return "Success, the account has been wiped. Bye.";
	}catch(Exception $ex){
		$uid = log_error("db_functions.php:grant_admin()", $ex);
		return "An error occured with a reference id of: {$uid}.";
	}
}

/**
 * Changes the password for the current user.
 */
function update_password($newpass)
{
	$user = $_SESSION['raw_username'];
	$newpass = encode_pass($newpass, $user);
	$id = $_SESSION['id'];
	
	try {
		exec_query("UPDATE Users SET usr_password = '{$newpass}' WHERE usr_id = {$id}");
		return "Password changed.";
	} catch(Exception $ex) {
		$uid = log_error("db_functions.php:grant_admin()", $ex);
		return "An error occured with a reference id of: {$uid}.";
	}

}	
			

/**
 * Removes the user from the admin group.
 * Returns null if things went okay.
 */
function remove_admin($username, $password)
{
	if(get_user_by_name($username) != null)
		try
		{
			$name = encode_user($username);
			$pass = encode_pass($password, $username);
			$result = exec_query("UPDATE Users SET is_admin = FALSE WHERE username = '{$name}' AND usr_password = '{$pass}'");
			return null;
		}catch(Exception $ex){
			$uid = log_error("db_functions.php:grant_admin()", $ex);
			return "An error occured with a reference id of: {$uid}.";
		}
	
	log_error("DANGER WILL ROBINSON! Someone has attempted to delete an ADMIN that didn't exist.");
	return "Some funny business was logged.";
}

/**
 * Returns a userid from a validation id, null if none exists or an 
 * error occured.
 **/
function get_user_by_validation_id($id)
{
	try
	{
		$id = mysql_real_escape_string($id);
		$result = exec_query("SELECT val_usr FROM Validations WHERE val_id = '{$id}'");
		$result = mysql_fetch_array($result);
		
		if(! isset($result['val_usr']))
			return null;
		
		return $result['val_usr'];
	}catch(Exception $ex){
		log_error("db_functions.php:get_user_by_validation_id()", $ex);
	}
	return null;
}


/**
 * A handy function to check if one thing ended with another.
 */
function endsWith( $str, $sub ) {
   return ( substr( $str, strlen( $str ) - strlen( $sub ) ) === $sub );
}

/**
 * 
 * Checks whether people from the given domain are allowed to register
 * their email.
 *  (Using the $VALID_DOMAINS in global)
 * 
 */
function email_is_allowed($email_addr)
{
	global $VALID_DOMAINS;
	// If there are no valid domains, everyone is allowed.
	if($VALID_DOMAINS === array())
		return true;
	
	// If there are valid domains, iterate over them, and check if 
	// this email ends with one.
	foreach($VALID_DOMAINS as $domain)
		if(endsWith($email_addr, $domain))
			return true;
			
	// Domain not found, sorry :(
	return false;
}


/**
 * Sends mail to the person at the to address. The name of the site is
 * prepended to the message.
 * 
 * HTML is okay in these messages.
 * 
 * Returns null if everything went okay, a string otherwise.
 */
function send_mail($to, $subject, $body)
{
	global $SMTP_HOST, $SMTP_PASSWORD, $SMTP_PORT, $SMTP_USERNAME, $SITE_NAME;
	$subject = $SITE_NAME." - ".$subject;

	$headers = array (
		'From' => $SMTP_USERNAME,
		'To' => $to,
		'Subject' => $subject);
	$smtp = Mail::factory(
		'smtp',
		array (
			'host' => $SMTP_HOST,
			'port' => $SMTP_PORT,
			'auth' => true,
			'username' => $SMTP_USERNAME,
			'password' => $SMTP_PASSWORD));

	// Creating the Mime message
	$mime = new Mail_mime();

	// Setting the body of the email
	$mime->setTXTBody(strip_tags($body,"<a>")); // Strip out all but a tags for text
	$mime->setHTMLBody($body);
	$body = $mime->get();
	$headers = $mime->headers($headers);

	$mail = $smtp->send($to, $headers, $body);

	if (PEAR::isError($mail)) 
		return "An error occured with the reference code: ".log_error("db_functions.php:send_mail()",$mail->getMessage());

	return null;
}

?>
