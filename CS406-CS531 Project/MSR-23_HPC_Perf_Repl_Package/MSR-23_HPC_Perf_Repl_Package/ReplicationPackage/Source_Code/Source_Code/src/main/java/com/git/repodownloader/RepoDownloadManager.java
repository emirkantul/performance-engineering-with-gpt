package com.git.repodownloader;

import java.io.File;
import java.util.List;

import com.config.Config;
import com.utility.ProjectPropertyAnalyzer;


public class RepoDownloadManager {
	
	public static final String GIT_BASE_PATH="https://github.com/";
	

	
	public void downloadProjects(List<String> gitpaths)
	{
		CloneRemoteRepository cloner=new CloneRemoteRepository();
		
		for(int index=0;index<gitpaths.size();index++)
		{			
			String remoterepo=gitpaths.get(index);
			String localfolder=ProjectPropertyAnalyzer.getProjName(remoterepo);			
			
			String localrepo=Config.repoDir+localfolder;
			
			File f = new File(localrepo);
			
			if (f.exists() && f.isDirectory()) {
				System.out.println("Repo Already downloaded:"+remoterepo);
			} else {
				cloner.DownloadRemoteRepository(localrepo, remoterepo);
				
			}	
			
		}
	}	
	
}
