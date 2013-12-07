<?php 

include 'includes/head.php';

$return = "index.php";
if(isset($_GET['return']))
	$return = $_GET['return'];

generate_menubar($return);
?>

<?php
if (is_logged_in())
{
	echo"<p class='error'>You are already a user.</p>";	

/** Create a user with the given username and password. **/
} elseif(isset($_POST['submit'])) {

	// Verify all data.
	$email 	= $_POST['username'];
	$pass	= $_POST['password'];
	$pass2	= $_POST['password2'];

	
	if($pass != $pass2)
		$result = "Your passwords do not match";
		
	elseif(! email_is_allowed($email))
		$result = "People from your domain are not being accepted right now.";
	else
		$result = register_user($email, $pass);
		
	echo"<p class='error'>{$result}</p>";
}else{
?>
	<h3>Sign Up</h3>

	<form class='notification' method='post' action='<?php echo $_SERVER["REQUEST_URI"]?>'>
		<table>
			<tr>
				<td>Email Address (Username)</td>
				<td><input type='text' maxlength='100' name='username'/></td>
			</tr>
			<tr>
				<td>Password</td>
				<td><input type='password' maxlength='100' name='password'/></td>
			</tr>
			<tr>
				<td>Repeat Password</td>
				<td><input type='password' maxlength='100' name='password2'/></td>
			</tr>
				<tr><td>
				<td><input type='submit' value='submit' name='submit' /></td>
			</tr>
		</table>
	</form>
<?php
}

include 'includes/tail.php';

?>
