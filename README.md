#Underwatch
Underwatch is a utility for tracking changes to the ini and save files for Undertale.

The core functionality of the Underwatch utility was created by DMNh.

#Tools Used
* Python (3.4)
* configparser is used for managing the config file.
* Clint is used for coloured output.
* cx_free is used to create the windows executable.


#Tidazi's Changes
##Underwatch 0.4
* Fixed the bug where files are reported as modified but none of the values have changed.
* When a file is modified, the number of changes detected is displayed.
* Configuration is now handled by a single underwatch.ini file.
* Created a simple icon for Underwatch.

	

#Coming Soon...
* Add descriptions to "Undertale.ini" change reports.
* More robust support for timestamps.


#Underwatch Reports
By default, any changes are printed out to the terminal in the following format:

	file0 had 3 changes detected.
	(56) 4349  >> 4351  (Skipped count)
	(493) 1  >> 2  (unknown)
	(549) 673344  >> 673637  (Play time)

	file9 had 3 changes detected.
	(56) 4349  >> 4351  (Skipped count)
	(493) 1  >> 2  (unknown)
	(549) 673344  >> 673637  (Play time)

	undertale.ini had 1 change detected.
	[General]
	Time: 673344.000000 >> 673637.000000


Changes to the save file include the line number and a description if one is known.

Descriptions were largely taken from the Traveler's Guide to the Underland:

https://docs.google.com/document/d/1h_vdEFZMtefD-nkCZ7ODzArp7BRbGgN0_7HQ1XjTT8Y/edit#heading=h.a5d6q4uvp7b8


The descriptions for save file lines are stored in _saveFile and can be modified and added to.

On first run, Underwatch will create the config file (underwatch.ini) with default options.

It will also confirm the directory for Undertale data, and create the default directory for output files.

-----

#Configuration Options

	[Undertale]
		savePath 
			The directory that the Undertale save files are stored in.
			This is usually C:\Users\<username>\AppData\Local\UNDERTALE.

	[Underwatch]
		outputPath
			The output path for log files.
			This defaults to a subdirectory called "outputLogs" within the Underwatch directory.

		outputMode
			screen
				No file output. Only displays changes on the screen.
			file
				All output is stored to a single file.
			sequence
				Default. Each output is stored in timestamped files.
		
		outputMultiple
			false
				Default. All recorded changes are stored in a single file.
			true
				Each file changed gets its own log.
		
		timestampFormat
			The timestamp format that all timestamps will be displayed in. See the guide below for making changes.
			This option is empty by default, but uses the default timestamp value of "%Y-%m-%d %H.%M.%S"
		
		quietMode
			true
				Underwatch will not report changes to the screen, but will save output logs normally if that option is enabled.
			
			false
				Default. Underwatch will report changes to the screen normally. 
		
		watchDescriptions
			true
				The _saveFile descriptions file will be monitored for changes.
			false
				Default.
		
		persistentMode
			true
				Underwatch will remain open after Undertale closes.
			false
				Underwatch closes when Undertale closes.
	

#Python datetime format codes

    %a  Locale’s abbreviated weekday name.
    %A  Locale’s full weekday name.      
    %b  Locale’s abbreviated month name.     
    %B  Locale’s full month name.
    %c  Locale’s appropriate date and time representation.   
    %d  Day of the month as a decimal number [01,31].    
    %f  Microsecond as a decimal number [0,999999], zero-padded on the left
    %H  Hour (24-hour clock) as a decimal number [00,23].    
    %I  Hour (12-hour clock) as a decimal number [01,12].    
    %j  Day of the year as a decimal number [001,366].   
    %m  Month as a decimal number [01,12].   
    %M  Minute as a decimal number [00,59].      
    %p  Locale’s equivalent of either AM or PM.
    %S  Second as a decimal number [00,61].
    %U  Week number of the year (Sunday as the first day of the week)
    %w  Weekday as a decimal number [0(Sunday),6].   
    %W  Week number of the year (Monday as the first day of the week)
    %x  Locale’s appropriate date representation.    
    %X  Locale’s appropriate time representation.    
    %y  Year without century as a decimal number [00,99].    
    %Y  Year with century as a decimal number.   
    %z  UTC offset in the form +HHMM or -HHMM.
    %Z  Time zone name (empty string if the object is naive).    
    %%  A literal '%' character.
