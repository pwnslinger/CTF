<?php

error_reporting(E_ALL & ~E_NOTICE);
ini_set('display_errors', 0);

const FILE_DIRECTORY = '../append/';
const PROTECTED_FIELDS = 'ssn,password';

// Make sure this is set to false except when testing!
$isAdmin = false;

/////////// Main code ////////////

echo "Welcome to our secure database system!";

if (checkAdmin())
{
	echo "You are an admin!";
}

// Load files from the database
foreach(array_diff(scandir(FILE_DIRECTORY), ['.', '..']) AS $_fileName)
{
	$$_fileName = json_decode(file_get_contents(FILE_DIRECTORY . $_fileName), true);
}

// Route request
if (isset($_GET['method']))
{
	switch ($_GET['method'])
	{
		case 'adminAccessFile':
			adminAccessFile(sanitize($_GET['fileName']));
			break;
		case 'storeProtectedRecord':
			storeProtectedRecord($_GET['fileName'], $_GET['password'], $_GET['name'], $_GET['ssn']);
			break;
		case 'userAccessField':
			userAccessField(${sanitize($_GET['fileName'])}, $_GET['key'], $_GET['password']);
			break;
		default:
			echo "Invalid request!";
			break;
	}
}

die();

/////////// System functions ////////////

function storeProtectedRecord($fileName, $password, $name = '', $ssn = '')
{
	if (sanitize($fileName) != $fileName)
	{
		die('File name can only be alphanumeric!');
	}

	if ($filename == "_GET")
	{
		die('you cannot DOS me.');
	}
	
	$newRecord = [
		'name' => $name, 
		'password' => $password, 
		'ssn' => $ssn
	];
	
	$target = FILE_DIRECTORY . $fileName;
	
	if (!file_exists($target))
	{
		file_put_contents($target, json_encode($newRecord));
		die('File successfully written!');
	}
	else
	{
		die("File $fileName already exists!");
	}
}

function adminAccessFile($fileName)
{
	if (checkAdmin())
	{
		echo "Authenticated as admin: retrieving $fileName";
		system('cat ' . escapeshellarg($fileName));
		die();
	}
	else
	{
		die("You're not an admin!");
	}
}

function userAccessField($data, $key, $password = NULL)
{
	if (empty($data))
	{
		die("File $fileName does not exist!");
	}

	// Only display sensitive fields if password is valid!
	if (in_array($key, explode(',', PROTECTED_FIELDS)) && $password != $data['password'])
	{
		echo "Sorry, field $key requires a password!";		
	}
	else
	{
		echo "Value for field $key is: <br />";		
		echo var_export($data[$key], true);
	}
}

function sanitize($val)
{
	return preg_replace('[^a-zA-Z0-9\.]', '', $val); 
}

function checkAdmin()
{
	return isset($GLOBALS['isAdmin']) && $GLOBALS['isAdmin'] == true;
}
