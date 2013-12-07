<?php 
/**
 * This page is passed the GET param, article or category.
 * article is the article_id of the article to delete.
 * category is the cat_id of the category to delete
 */

include 'includes/head.php';

$error = "No post/category has been selected";
if(isset($_GET['article'])) 
	$error = delete_article($_GET['article']);

if(isset($_GET['category']))
	$error = delete_category($_GET['category']);

generate_menubar("index.php");

echo "<p class='error'>{$error}</p>";

include 'includes/tail.php';
?>
