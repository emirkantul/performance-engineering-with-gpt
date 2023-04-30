package com.utility.fileprocess;

import java.io.FileWriter;
import java.io.IOException;
import java.io.Reader;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.apache.commons.csv.CSVFormat;
import org.apache.commons.csv.CSVParser;
import org.apache.commons.csv.CSVPrinter;
import org.apache.commons.csv.CSVRecord;

import com.performancefix.entity.PerfFixData;



public class ApacheCSVReaderWriter {

	
	public void WritePerfFixCommitData(List<PerfFixData> fixdata, String csvfilepath) throws IOException {
	FileWriter out = new FileWriter(csvfilepath);
	String[] HEADERS = { "Id", "ProjName", "ProjGitUrl","fixCommitId","fixCommitMsg" };

	try (CSVPrinter printer = new CSVPrinter(out, CSVFormat.DEFAULT.withHeader(HEADERS))) {

		for (PerfFixData item : fixdata) {
			printer.printRecord(item.getId(),item.getProjName(),item.getProjGitUrl(),item.getFixCommitID(),item.getFixCommitMsg());
		}

	}
}
	
	

}
