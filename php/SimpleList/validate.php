<?php 
/**
 * This page is passed the GET param, 'id'.
 * 'id' corresponds to the id of the value in the database
 */

include 'includes/head.php';

$error = "No ID has been provided for the validation";
if(isset($_GET['id'])) 
	$error = validate_user($_GET['id']);

generate_menubar("login.php");

echo "<p class='error'>{$error}</p>";

include 'includes/tail.php';
?>
