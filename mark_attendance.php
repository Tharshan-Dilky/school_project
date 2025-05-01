<?php
$db = new SQLite3('attendance.db');
date_default_timezone_set("Asia/Kolkata");
$student_id = $_GET['id'] ?? '';
$date = date('Y-m-d');
$time = date('H:i:s');

if ($time <= "08:00:00") {
    $status = "Present";
} else {
    $status = "Absent";
    // Optionally trigger SMS here
}

$stmt = $db->prepare("INSERT INTO attendance (student_id, student_name, date, status) VALUES (?, ?, ?, ?)");
$stmt->bindValue(1, $student_id, SQLITE3_INTEGER);
$stmt->bindValue(2, 'Student Name Placeholder'); // Fetch from students table if needed
$stmt->bindValue(3, $date);
$stmt->bindValue(4, $status);
$stmt->execute();

echo "Marked " . $status;
?>
