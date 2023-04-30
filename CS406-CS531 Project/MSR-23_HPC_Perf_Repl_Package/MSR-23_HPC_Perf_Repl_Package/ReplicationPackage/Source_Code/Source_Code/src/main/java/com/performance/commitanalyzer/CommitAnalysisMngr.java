package com.performance.commitanalyzer;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import com.config.Config;
import com.git.commitanalyzer.CommitAnalyzer;
import com.opencsv.exceptions.CsvDataTypeMismatchException;
import com.opencsv.exceptions.CsvRequiredFieldEmptyException;
import com.performancefix.entity.PerfFixData;
import com.utility.ProjectPropertyAnalyzer;
import com.utility.fileprocess.ApacheCSVReaderWriter;
import com.utility.fileprocess.CSVReaderWriter;
import com.utility.fileprocess.TextFileReaderWriter;

public class CommitAnalysisMngr {

	public CommitAnalysisMngr() {

	}

	public void PerformCommitAnalysis() {
		String filepath = Config.gitProjList;

		List<String> projlist = TextFileReaderWriter.GetFileContentByLine(filepath);
		List<PerfFixData> fixdata = new ArrayList<>();

		for (String proj : projlist) {
			String projname = ProjectPropertyAnalyzer.getProjName(proj);

			CommitAnalyzer cmtanalyzer = null;

			try {
				cmtanalyzer = new CommitAnalyzer("test", projname, proj);
				List<PerfFixData> projfixdata = cmtanalyzer.getAllPerformanceCommits();

				if (projfixdata.size() > 0) {
					fixdata.addAll(projfixdata);
				}

			} catch (Exception e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}

		if (fixdata.size() > 0) {
			ApacheCSVReaderWriter writer = new ApacheCSVReaderWriter();

			try {
				writer.WritePerfFixCommitData(fixdata, Config.csvFile);
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}

		}

	}

}
