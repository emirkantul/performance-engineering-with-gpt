package com.git.repodownloader;

import java.util.List;

import com.config.Config;
import com.utility.fileprocess.TextFileReaderWriter;

public class ProjectLoader {

	public ProjectLoader() {

	}

	public void LoadDownloadProjects() {
		String filepath = Config.gitProjList;

		List<String> projlist = TextFileReaderWriter.GetFileContentByLine(filepath);

		RepoDownloadManager repomngr = new RepoDownloadManager();
		repomngr.downloadProjects(projlist);

	}

}
