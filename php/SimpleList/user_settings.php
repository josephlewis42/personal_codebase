<?php 

include 'includes/head.php';

generate_menubar("index.php");
?>

<?php
if (! is_logged_in())
{
	echo"<p class='error'>You must log in to edit your settings.</p>";	

/** If the category has been made, create it. **/
} elseif(isset($_POST['delete']) || isset($_POST['drop_admin']) || isset($_POST['change_pass'])) {
	
	$pass = $_POST['password'];
	$user = $_SESSION['raw_username'];
	
	if(!is_same_user($_SESSION['id'], $user, $pass))
		$return =  "<p class='error'>The password you provided does not match your account, nothing was done.</p>";
	
    else
		if(isset($_POST['delete']))
			$return = delete_user($_SESSION['id']);
			
		elseif(isset($_POST['drop_admin']))
			if(($return = remove_admin($user, $pass)) == null){
				$_SESSION['is_admin'] = false;
				$return = "Success";
			} else { $return = "Failure"; }
			
		else
			if($_POST['new_password'] == $_POST['new_password2'])
				$return = update_password($_POST['new_password']);
			else
				$return = "Your new passwords didn't match.";

	
	echo "<p class='error'>{$return}</p>";

}else{
?>
	<h3>Delete Account &amp; All Postings</h3>

	<form class='notification' method='post' action='<?php echo $_SERVER["REQUEST_URI"]?>'>
		<table>
			<tr>
				<td>Enter your password:</td>
				<td><input type='password' maxlength='100' name='password' size='51'/></td>
			</tr>
			<tr>
				<td></td>
				<td><input type='submit' value='submit' name='delete' /></td>
			</tr>
		</table>
	</form>
	
	<h3>Change Password</h3>

	<form class='notification' method='post' action='<?php echo $_SERVER["REQUEST_URI"]?>'>
		<table>
			<tr>
				<td>Enter your password:</td>
				<td><input type='password' maxlength='100' name='password' size='51'/></td>
			</tr>
			<tr>
				<td>Enter your new password:</td>
				<td><input type='password' maxlength='100' name='new_password' size='51'/></td>
			</tr>
			<tr>
				<td>Repeat your new password:</td>
				<td><input type='password' maxlength='100' name='new_password2' size='51'/></td>
			</tr>
			<tr>
				<td></td>
				<td><input type='submit' value='submit' name='change_pass' /></td>
			</tr>
		</table>
	</form>
<?php
	if(is_admin())
	{
	?>
		<h3>Drop Admin</h3>

		<form class='notification' method='post' action='<?php echo $_SERVER["REQUEST_URI"]?>'>
			<table>
				<tr>
					<td>Enter your password:</td>
					<td><input type='password' maxlength='100' name='password' size='51'/></td>
				</tr>
				<tr>
					<td></td>
					<td><input type='submit' value='submit' name='drop_admin' /></td>
				</tr>
			</table>
		</form>
	<?php
	}
}

include 'includes/tail.php';

?>
