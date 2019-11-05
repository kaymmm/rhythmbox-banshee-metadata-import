# rhythmbox-banshee-metadata-import
Import metadata from Banshee into Rhythmbox

* Forked from a [script](https://code.google.com/archive/p/rhythmbox-banshee-import/) that was originally released by Wolfgang Steitz in 2009.
* Added the ability to import the `LastPlayedStamp` (date a file was last played) from Banshee.
* Maintains the ability to import the `PlayCount` and `Rating` fields.
* Instead of adding Banshee playcount to Rhythmbox count, it uses the greater of the two so that subsequent executions of the script don't keep increasing the playcounts.
* Added default paths for the Rhythmbox and Banshee database files
* Cleaned up the process of accessing the Rhythmbox database
* Fixed broken Banshee database access (it wasn't working for me with the `try` statement used previously)
* Added the ability to import the `DateAddedStamp` from Banshee into Rhythmbox's `last-seen`, if it was earlier.
