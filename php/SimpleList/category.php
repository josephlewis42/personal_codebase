<?php include 'includes/head.php'; 

generate_menubar("index.php",array("new" => "new.php?cat={$_GET['cat']}"),null,array("delete category" => "delete.php?category={$_GET['cat']}"));

?>

<div class='listings'>
	<?php
		$CID = mysql_real_escape_string($_GET['cat']);
		$result = exec_query("SELECT * FROM Articles WHERE category = {$CID} ORDER BY begin_time DESC");
		$last_date = "";
		
		while($row = mysql_fetch_array($result))
		{
			if($last_date != substr($row['begin_time'],0,10)) {
				$last_date = substr($row['begin_time'],0,10);
				echo "<h3>{$last_date}</h3>";
			}
		
		echo "<div><a href='view.php?article={$row['article_id']}' >{$row['title']}</a></div>";
		}
		
		// If there was no date, meaning no row
		if($last_date == "")
			echo "<h3>Nothing in this category yet</h3>";		
	?>
</div>

<?php
include 'includes/tail.php';
?>
