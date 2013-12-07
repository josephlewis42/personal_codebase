<?php 
/**
 * This page alerts users about the software.
 */

include 'includes/head.php';
?>

<div class='text'>
	<h1>About</h1>
	<p>This website is built on the SimpleList framework, which allows a fully
	customizable community to be built around users creating and posting
	articles.</p>


	<h2>Authors/Contributors</h2>
	<ul>
	<li>Joseph Lewis &lt;joehms22 gmail com&gt;</li>
	</ul>

	<h2>Security (also: Why can't I recover my password?)</h2>
	<p>Most web databases store user's information in plaintext, meaning 
	the text can be read and easily updated by the database software. This 
	also means that anyone that "hacks" the database can easily tell who was
	part of it.</p>

	<p>SimpleList (the software that runs this website) uses a different
	database ideology. SimpleList sends your username and password through
	a one way cryptographic hashing algorithm, meaning it is impossible to 
	say for certain who is in the database. This does make some things 
	inconvenient, like password recovery, but overall provides a large
	amount of privacy to our users.</p>

	<p>The only information SimpleList keeps is session information while 
	you are logged in and information that is backed up by whoever is 
	running this instance, along with any information you post in articles/
	ads you write.</p>

	<p>If a "hacker" does indeed get in all that will be found of your 
	username and password is meaningless alphanumeric sequences like: 
	5baa61e4c9b93f3f0682250b6cf8331b7ee68fd8</p>

</div>
<?php
include 'includes/tail.php';
?>
