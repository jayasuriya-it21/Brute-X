<?php
session_start();

// Retrieve form data
$username = $_POST['username'];
$password = $_POST['password'];

// Connect to the database
$host = 'localhost';
$user = 'root';
$pass = '';
$db = 'registration'; 

$conn = new mysqli($host, $user, $pass, $db);

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $username = $_POST["username"];
    $password = $_POST["password"];

    // Sanitize input to prevent SQL injection
    $username = $conn->real_escape_string($username);
    $password = $conn->real_escape_string($password);

    // Retrieve user from the database
    $sql = "SELECT * FROM users WHERE username='$username' AND password='$password'";
    $result = $conn->query($sql);

    if ($result->num_rows == 1) {
        // Login successful, create session and cookie
        $_SESSION['username'] = $username;

        // Set a cookie for username with a 24-hour expiration
        setcookie('username', $username, time() + (86400 * 1), "/"); // 1 day

        // Check if the request is from Python script or browser
        if (isset($_SERVER['HTTP_USER_AGENT']) && strpos($_SERVER['HTTP_USER_AGENT'], 'python-requests') !== false) {
            // Request is from Python script, return success response as JSON
            $response = array("success" => true);
            exit(json_encode($response));
        } else {
            // Request is from browser, redirect to success.html or any other page
            header("Location: ./site");
            exit();
        }
        
    } else {
        // Invalid username or password, display alert message
        echo "<script>alert('Invalid username or password.');</script>";
        echo "<script>window.location.href = '/';</script>";
        exit();


    }
}

$conn->close();
?>
