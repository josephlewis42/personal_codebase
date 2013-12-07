<?php include 'includes/head.php'; 

generate_menubar(null,null,null,array("new category" => "new_category.php"));

$result = exec_query("SELECT * FROM Categories");

echo "<div class='category'>";

while($row = mysql_fetch_array($result))
{
?>
	
		<a href="category.php?cat=<?php echo $row['cat_id']?>">
			<h3><?php echo $row['cat_title']?></h3>
			<h4><?php echo $row['cat_subtitle']?></h4>
		</a>
<?php
}

echo "	</div>";
include 'includes/tail.php';
?>
