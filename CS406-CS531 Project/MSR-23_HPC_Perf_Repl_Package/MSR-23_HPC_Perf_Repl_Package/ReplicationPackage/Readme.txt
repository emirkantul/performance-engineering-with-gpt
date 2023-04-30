1.Dataset 
The list of 23 projects we used is in the file “HPC_Project_List.txt”, which contains the git URLs for the projects we downloaded and analyzed. The files for RQ1, RQ2, RQ3, and RQ4 are included in separate spreadsheets under the RQ folder. Summary_Results_of_Labelled_Data contains the intermediate data which we used for calculating Fleiss' Kappa.

***NOTE*** While opening the RQ spreadsheets, If you see a prompt like “Current window is too small to display” or you can't see the whole spreadsheet, then to view the whole spreadsheet, you need to use an external monitor to view the large file.

2.Source Code 
The source code of the tool we used to generate the data we used for our analysis is available under the Source Code folder. This project is compatible with IntelliJ and Eclipse IDEs. It needs Java 8 or newer to be executed and it comes with all the libraries needed for its execution. The MainClass.java file can be executed directly from respective folders. Additionally, the Config.java allows several configurations, most importantly of which are the *rootDir” and gitProjList which provides the list of the projects being analyzed.

