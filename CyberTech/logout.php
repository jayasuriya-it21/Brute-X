<?php
session_start();

// Unset session variables
session_unset();

// Destroy the session
session_destroy();

// Delete the username cookie
setcookie('username', '', time() - 3600, "/");



// Redirect to the login page
header("Location: /");
exit();
?>
