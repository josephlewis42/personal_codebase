<?php 

include 'includes/head.php';

generate_menubar("index.php");
?>

<?php
if (! is_admin())
{
	echo"<p class='error'>Permission Denied: You cannot grant a user admin privileges.</p>";	

/** If the category has been made, create it. **/
} elseif(isset($_POST['submit'])) {
	
	if($_POST['password'] == $_POST['password2'])
	
		$result = make_admin($_POST['username'], $_POST['password']);
	else
		$result = "Passwords did not match";
	
	echo"<p class='error'>{$result}</p>";
}else{
?>
	<h3>Grant Admin</h3>

	<form class='notification' method='post' action='<?php echo $_SERVER["REQUEST_URI"]?>'>
		<table>
			<tr>
				<td>Username of person you want to give admin to:</td>
				<td><input type='text' maxlength='100' name='username' size='51'/></td>
			</tr>
			<tr>
				<td>Password of person you want to give admin to:</td>
				<td><input type='password' maxlength='100' name='password' size='51'/></td>
			</tr>
			<tr>
				<td>Verify Password:</td>
				<td><input type='password' maxlength='100' name='password2' size='51'/></td>
			</tr>
			<tr>
				<td></td>
				<td><input type='submit' value='submit' name='submit' /></td>
			</tr>
		</table>
	</form>
<?php
}

include 'includes/tail.php';

?>
