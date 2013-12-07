<?php
/* set the cache limiter to 'private' */
session_cache_limiter('private');
session_start();
header("Cache-Control: no-cache");

include 'global.php';
?>
<!DOCTYPE html>

<!--
Find a security flaw? Be an U83R K3W1 D00D and tell us about it.
Your name/pseudonym/handle/short message will be added to our
contributors list.

This is HTML5/CSS3, no need to include any slow/nasty JS. Sorry IE6
-->

<html lang="en">
    <head>
	<meta charset="utf-8" />
	<title><?php echo $SITE_NAME." - ".$SITE_TAGLINE; ?> </title>
	<link href="assets/style.css" rel="stylesheet" />
    </head>
<body>

<div id="HEADER">
	<h1><a href='index.php'><?php echo $SITE_NAME; ?></a></h1>
	<h2><?php echo $SITE_TAGLINE; ?></h2>
</div>
