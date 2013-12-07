<?php include 'includes/head.php'; 
/**
 * This page is passed the GET param, article.
 * article is the article_id of the article
 * 
 * The return path is set to the category id of the article, if no
 * article is chosen, index.php is returned.
 */

$error = null; // Any error text that will be thrown.
try {
	// Do the query for the page.
	if(isset($_GET['article']))
	{
		$artid = mysql_real_escape_string($_GET['article']);
		$result = exec_query("SELECT * FROM Articles WHERE article_id = {$artid}");
				
		$result = mysql_fetch_array($result);
		
		$title = $result['title'];
		$post = $result['text'];
		$contact = $result['contact_text'];
		$cat = $result['category'];
		$date = $result['begin_time'];
		$author = $result['author'];
		
	}else{
		$error = "No post has been selected";
	}
}catch(Exception $ex){
	$error = "An error occured, reference id: ".log_error("view.php", $ex);
}



/** Do the menubar **/


// A quick index to the last page the user was at.
$lastpage = "/index.php";
if(isset($cat))
	$lastpage = 'category.php?cat='.$cat;

$logged_in = array();
if(can_delete_article($_GET['article']))
	$logged_in['delete'] = "delete.php?article={$_GET['article']}";

generate_menubar($lastpage,$logged_in);


if($error != null) {
	echo "<p class='error'>{$error}</p>";
}

?>
<div class='article'>
	<div class='header'>
		<h3><?php echo $title; ?></h3>
		<h4><?php echo $date; ?></h4>
	</div>
	<p><?php echo $post; ?></p>
	<?php
		if(is_logged_in())
		{
			echo "<p>".$contact."</p>";	
		}else{
			echo "<div class='error'><p>You must log in to view contact details</p></div>";
		}
	?>
</div>

<?php
	include 'includes/tail.php';
?>
