<?php
	if (_GET["count"]){
		$ count _GET["count"]
		count = count + 1;	
	}
	else{
		count = 0;
	}
	echo count;
?>