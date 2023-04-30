package com.config;

public class Config {

	public static String rootDir = "H:\\Research\\HPC_Performance\\Project_Repo\\";
	//
	// text file that contains list of projects to analyze
	public static String gitProjList = rootDir + "Project_Source.txt";
	// reporDir used for storing Unity Projects
	public static String repoDir = rootDir + "GitRepo/";

	public static String csvFile = rootDir + "perf_commit_data_Updated.csv";

	public static String[] perfCommitToken = { "performance", "speed up", "accelerate", "fast", "slow", "latenc",
			"contention", "optimize", "efficient" };

	public static int commitid = 1;
	public static int stmtUniqueId = 1;

}