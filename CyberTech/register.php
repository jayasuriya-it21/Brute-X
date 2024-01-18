<?php
// Retrieve form data
$username = $_POST['username'];
$password = $_POST['password'];
$email = $_POST['email'];

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
    $email = $_POST["email"];

    // Retrieve user from the database
    $sql = "SELECT * FROM users WHERE username='$username' or email='$email'";
    $result = $conn->query($sql);

    if ($result->num_rows == 1) {
        // Login successful, redirect to success.html
        echo "<script>alert('Username or Email is already registered');</script>";
        echo "<script>window.location.href = 'index.html';</script>";
        exit();
    } else {
        $sql = "INSERT INTO users (email, username, password) VALUES ('$email', '$username', '$password')";

        if ($conn->query($sql) === TRUE) {
            // Registration successful, redirect to success.html
            echo "<script>alert('Your Registration is successful');</script>";
            echo "<script>window.location.href = 'index.html';</script>";
            exit();
        } else {
            echo "Error: " . $sql . "<br>" . $conn->error;
        }
    }
}

// Insert data into the database


$conn->close();
?>
