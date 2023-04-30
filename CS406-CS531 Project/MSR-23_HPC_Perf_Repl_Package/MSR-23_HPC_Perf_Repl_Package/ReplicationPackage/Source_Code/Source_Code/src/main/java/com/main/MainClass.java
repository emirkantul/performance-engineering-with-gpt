package com.main;


import java.util.Scanner;

import com.git.repodownloader.ProjectLoader;
import com.performance.commitanalyzer.CommitAnalysisMngr;



public class MainClass {

	public static void main(String[] args) {

		System.out.println("Enter your action:");

		System.out.println("1->Download Projects" + "\n2->Commit Change Analysis");

		Scanner cin = new Scanner(System.in);

		System.out.println("Enter an integer: ");
		int inputid = cin.nextInt();

		if (inputid == 1) {
			ProjectLoader projloader = new ProjectLoader();
			projloader.LoadDownloadProjects();
			System.out.println("Download Projects->Completed");

		} else if (inputid == 2) {
			CommitAnalysisMngr commitmngr = new CommitAnalysisMngr();
			commitmngr.PerformCommitAnalysis();
			System.out.println("Commit Change Analysis->Completed");
		}

	}
}