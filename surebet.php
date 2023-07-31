<?php
    $db = new SQLite3('found_opp.db');

    $results = $db->query('SELECT Match, Team1, Team2, Odd_team1_winning, Odd_equality, Odd_team2_winning, Team1_site, Equality_site, Team2_site, Returns, Date FROM opportunities_foot');

    echo "<table>";
    echo "<tr><th>Match</th><th>Team1</th><th>Team2</th><th>Odd_team1_winning</th><th>Odd_equality</th><th>Odd_team2_winning</th><th>Team1_site</th><th>Equality_site</th><th>Team2_site</th><th>Returns</th><th>Date</th></tr>";
    while ($row = $results->fetchArray()) {
        echo "<tr><td>".$row['Match']."</td><td>".$row['Team1']."</td><td>".$row['Team2']."</td><td>".$row['Odd_team1_winning']."</td><td>".$row['Odd_equality']."</td><td>".$row['Odd_team2_winning']."</td><td>".$row['Team1_site']."</td><td>".$row['Equality_site']."</td><td>".$row['Team2_site']."</td><td>".$row['Returns']."</td><td>".$row['Date']."</td></tr>";
    }
    echo "</table>";
    
?>

