<?php 

include 'includes/head.php';

generate_menubar("index.php");
?>

<?php
if (! is_admin())
{
	echo"<p class='error'>Permission Denied: You cannot create a category.</p>";	

/** If the category has been made, create it. **/
} elseif(isset($_POST['submit'])) {
	
	// Verify all data.
	$title 		= mysql_real_escape_string(strip_tags($_POST['title']));
	$subtitle	= mysql_real_escape_string(strip_tags($_POST['subtitle']));
	
	$result = create_category($title, $subtitle);
	echo"<p class='error'>{$result}</p>";
}else{
?>
	<h3>New Category</h3>

	<form class='notification' method='post' action='<?php echo $_SERVER["REQUEST_URI"]?>'>
		<table>
			<tr>
				<td>Title</td>
				<td><input type='text' maxlength='100' name='title' size='51'/></td>
			</tr>
			<tr>
				<td>Subtitle</td>
				<td><input type='text' maxlength='100' name='subtitle' size='51'/></td>
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
