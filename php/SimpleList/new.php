<?php 

include 'includes/head.php';

generate_menubar("category.php?cat={$_GET['cat']}");

?>

<h3><?php echo cat_name_from_id($_GET['cat']) ?></h3>

<?php
if (! is_logged_in()){
?>
	<p class='error'>You must be logged in to post an ad. <?php login_link();?></p>
<?php
/** If the ad has been made, post it. **/
} elseif(isset($_POST['submit'])) {
	
	// Verify all data.
	$title 		= mysql_real_escape_string(strip_tags( $_POST['title']));
	$text		= mysql_real_escape_string(strip_tags( $_POST['text'],	$TAGS_ALLOWED));
	$contact 	= mysql_real_escape_string(strip_tags($_POST['contact'], $TAGS_ALLOWED));
	$cat_id 	= mysql_real_escape_string($_GET['cat']);
	
	// Check that everything that should be filled is.
	if($title == "" || $text == "" || $cat_id == "" || cat_name_from_id($cat_id) == null)
	{
		echo "<p class='error'>Make sure you filled out your title and text and that you are
		posting in a valid category.</p>";
		$needtopost = 1;
	} else {
		
		// Try posting the query.
		try {
			
			exec_query("INSERT INTO Articles (title, text, contact_text, author, category) VALUES ('{$title}','{$text}','{$contact}',{$_SESSION['id']},{$cat_id})");
			
			echo "<p class='notification'>Your ad has been posted</p>";
		} catch (Exception $ex) {
			$uid = log_error("new.php", $ex);
			echo "<p class='error'>An error occured with a reference id of: {$uid}.</p>";
		}
	}

}else{
	$needtopost = 1;
}

if(isset($needtopost)) {
?>
	<form class='notification' method='post' action='<?php echo $_SERVER["REQUEST_URI"]?>'>
		<table>
			<tr>
				<td>Title (100 chars max)</td>
				<td><input type='text' maxlength='100' name='title' size='51'/></td>
			</tr>
			<tr>
				<td>Ad (1000 chars max)<br> ==Tags Allowed==<br><?php echo htmlspecialchars($TAGS_ALLOWED);?></td>
				<td><textarea maxlength='1000' rows='5' cols='70' name='text'></textarea></td>
			</tr>
			<tr>
				<td>Contact (500 chars max)<br>(Only shown to other members)</td>
				<td><textarea maxlength='500' rows='5' cols='70' name='contact'></textarea></td>
			</tr>
				<tr><td></td><td><input type='submit' value="submit" name='submit' /></td>
			</tr>
		</table>
	</form>
<?php
}

include 'includes/tail.php';

?>
