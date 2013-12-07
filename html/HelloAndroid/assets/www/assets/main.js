const DBNAME = 'WikiWrite';
const DBVER = '1.1';
const DBEASY = 'WikiWrite Wiki Database';
const DBSIZE = 5000000; // 5MB should be big enough for any file, right?

var db;
var noteOpen = false;
var noteID = -1;

var DEBUGGING = false;

/**
 * Toggles the debugging messages on or off then alerts the user of
 * the current status.
 */
function toggleDebug() {
	DEBUGGING = !DEBUGGING;
    var dbgvalue = (DEBUGGING)? 'On':'Off';
	alert("Debugging: "+dbgvalue);
}

/**
 * Displays a message if debugging is on.
 */
function dbgMsg(text) {
    if(DEBUGGING)
        alert("Debug:\n" + text);
    else
        console.log("Debug: " + text);
}

function onDeviceReady() {
	db = window.openDatabase(DBNAME, DBVER, DBEASY, DBSIZE);
	db.transaction(populateDB, 
					dbgClose("Program database already set up"), 
					dbgClose("Program database created."));
                    
    document.getElementById("wiki_in").onkeyup = dewiki;
	document.getElementById("wiki_in").onkeydown = resize_textarea;
	
	// Do init to start things up on load.
	dewiki();
	resize_textarea();   
    
	generate_main();
}

// Populate the database
function populateDB(tx) {
	 tx.executeSql('CREATE TABLE IF NOT EXISTS documents (name, page, id INTEGER PRIMARY KEY AUTOINCREMENT)', [], dbgClose("Created documents table."), dbgClose("Couldn't create documents table."));
}


// Transaction error callback
function errorCB(err) {
	alert("Error processing SQL: " + err.code + " " + err.message);
}

/**
 * Creates functions that will alert the user of an error when called.
 */
function errClose(errtext) {
    return function() { 
        alert("Error: \n" + errtext); 
    }
}

/**
 * Creates functions that will alert the user if debugging is enabled.
 */
function dbgClose(dbgText) {
    return function() {
        dbgMsg(dbgText);
    }
}

// Cleans up a name according to a regex.
function cleanName(name) {
	return name.replace(/[^a-zA-Z0-9\-:;\s]+/g, '');
}


/**
 * Renames a document to the given name.
 */
function renameDocument(name, id) {
    dbgMsg("Renaming document: "+id+" to: "+name);
    
    name = escape(name); // Escape the name to avoid problems.
    
	db.transaction(function(tx){
			tx.executeSql('UPDATE documents SET name="'+ name +'" WHERE id='+noteID);
	}, errorCB);
}

/**
 * Renames the open document.
 */
function renameOpenDocument() {
    var currName = $('#document_name').html();
    var name = prompt("Enter the new document name:", currName);

    if (name != null) {
        name = cleanName(name);
	    if (name != '') {
		    renameDocument(name, noteID);
            $('#document_name').html(name); //Rename here.
            generate_main(); //Rename in main.
        }
            
    }
}


// Adds a new document to the database.
function addDocument(name, callback) {
    dbgMsg("Adding Document");
	db.transaction(function(tx){
        
            var d = (new Date()).getTime();
            
            tx.executeSql('INSERT INTO documents (name, page, id) VALUES ("'+name+'", "", '+d+')', [], dbgClose('New Document OK'), errClose('New Document Bad!'));
		}, errorCB, callback);
}

//Removes the document based upon the id.
function removeDocument(id) {
	db.transaction(function(tx){
			tx.executeSql('DELETE FROM documents WHERE id="'+id+'"');
		}, errorCB, generate_main);
}


//Loads the document by ID
function loadDocument(id) {
    dbgMsg("Loading document with id: " + id);
	function success(tx, results) {
		$('#wiki_in').val( unescape(results.rows.item(0).page) );
		dewiki();
	}
	db.transaction(function(tx){
			tx.executeSql('SELECT name, page FROM documents WHERE id='+id, [], success, errorCB);
		}, errorCB);
}

/**
 * Saves the currently open document to the database.
 */
function saveDocument() {
    dbgMsg("Saving open document.");
	db.transaction(function(tx){
			page = escape( $('#wiki_in').val() );
			//name = $('#document_name').html();
			
			dbgMsg("Saving note: " + noteID + " Page Data: " + page);

			tx.executeSql('UPDATE documents SET page="'+ page +'" WHERE id='+noteID, [], dbgClose('Save good.'), errorCB);
	}, errorCB);
}


//Returns a dict of id -> name pairs for the documents the user
//has saved. 
function getWikiNames(callback) {
	function queryDB(tx) {
		tx.executeSql('SELECT * FROM documents ORDER BY name', [], querySuccess, errClose("Couldn't fetch wiki names"));
	}

	function querySuccess(tx, results) {
		var j = {};
		var len = results.rows.length;
		for (var i=0; i<len; i++) {
			j[results.rows.item(i).id] = unescape(results.rows.item(i).name);
        }
		callback(j);
        
        return false;

	}
	db.transaction(queryDB, errorCB);
}

/**
 * Creates an ISO formatted date from the current time.
 * 
 * Stolen from:
 * https://developer.mozilla.org/en/JavaScript/Reference/Global_Objects/Date#Example.3a_ISO_8601_formatted_dates
 */
function ISODate() {
    var d = new Date();

    function pad(n){
        return n < 10 ? '0'+n : n
    }
    return d.getUTCFullYear()+'-'
    + pad(d.getUTCMonth()+1)+'-'
    + pad(d.getUTCDate())+' '
    + pad(d.getUTCHours())+':'
    + pad(d.getUTCMinutes())+':'
    + pad(d.getUTCSeconds())
}


// Creates a new note.
function new_note() {
	var name = prompt("Enter the new document name:", "Untitled Document " + ISODate() );

    dbgMsg("Unedited Name: "+name);
    if (name != null)
        name = cleanName(name);
    dbgMsg("Edited Name: "+name);

	if (name != null && name != '') {
		addDocument(name, function(){generate_main();});
	}
}

//Write the changes to the db if a note is open.
function saveNote() {
	if(noteOpen)
		saveDocument();
	else
		dbgMsg("Note not open, not saving.");
}

function open_note(id, name) {
	// Save current note if one is open.
	saveNote();

    // Set up globals.
	noteOpen = true;
	noteID = id;
    noteName = name;
	
	$("#document_name").html(noteName);
	
	
	// Grab content and stick it in the textarea.
	loadDocument(id);
	
    // Make sure we are on the right page.
	dbgMsg("loading the editor");
	window.location = '#editor';
}

function closeNote() {
	dbgMsg("Closing "+noteName);
	history.back();
	saveNote();
	noteOpen = false;
	noteName = '';
    noteID = -1;
}

/**
Generates the main list of files that can be opened.
**/
function generate_main() {
    dbgMsg("Generating main list");
	getWikiNames(function(entries){
		var internal = "";
        var curr_init = "";

		for (id in entries) {
			
			name = entries[id];
            
            if(name.substr(0,1) != curr_init) {
                curr_init = name.substr(0,1);
                internal += "<li data-role='list-divider'>"+curr_init+"</li>";
            }
			
			internal += "<li><a href='javascript:open_note(\"" + id + "\", \"" + name + "\")';>" + name + "</a>";
			internal += "<a href='javascript:delete_item(\"" + id + "\", \"" + name + "\")';>Delete Item</a>";
		}
		$('#doclist').html(internal);
		$('#doclist').listview('refresh');
        
        return false;
	
	});
}



function resize_textarea() {
	var str = $("#wiki_in").val();
	var linecount = 0;
	str.split("\n").length;
	
	$('#wiki_in').attr('rows', linecount + 1);
 }
 
//Sets up the wiki.
function dewiki() {
	$('#output_area').html( $('#wiki_in').val().wiki2html());
}

// Starts when the page is loaded.
function init() {
	onDeviceReady();
    /**
    var tid = setInterval(saveTimer, 500);
    var lasthash = '';
    function saveTimer() {
        dbgMsg("checking hash");
        if(window.location.hash != lasthash) {
            lasthash = window.location.hash;
            saveNote();
            dbgMsg("Hash changed");
        }
    }
    **/
    window.onhashchange = function () { 
        saveNote();
        dbgMsg('hash changed');            
    }         

}

//Confirms that the user wants to delete the document.
function delete_item(docid, name) {
	var ans = confirm("Delete the document "+name+"?");
	if(ans)
		removeDocument(docid);
}