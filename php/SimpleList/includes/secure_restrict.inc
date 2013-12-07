<?php
/**
 * This script checks if the user is logged in or not using the SESSION
 * variable 'auth', this script should be included first thing on _all_
 * secure pages. If the user is not auth then send them to the login
 * page.
 * 
 *      Copyright 2010 Joseph Lewis III <joehms22@gmail.com>
 */
session_start();
if (empty ($_SESSION['auth']) || $_SESSION['auth'] != "yes") 
{
     header("location: /login.php");
}
?>
