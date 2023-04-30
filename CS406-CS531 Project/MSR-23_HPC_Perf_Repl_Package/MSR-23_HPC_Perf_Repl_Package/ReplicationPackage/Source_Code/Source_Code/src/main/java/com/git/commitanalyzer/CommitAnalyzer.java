package com.git.commitanalyzer;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.Reader;
import java.io.StringWriter;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.Collections;
import java.util.Date;
import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.Queue;
import java.util.StringTokenizer;

import org.eclipse.jgit.api.Git;
//import org.apache.commons.compress.utils.IOUtils;
import org.eclipse.jgit.errors.IncorrectObjectTypeException;
import org.eclipse.jgit.errors.MissingObjectException;
import org.eclipse.jgit.lib.FileMode;
import org.eclipse.jgit.lib.ObjectId;
import org.eclipse.jgit.lib.ObjectLoader;
import org.eclipse.jgit.lib.Ref;
import org.eclipse.jgit.lib.Repository;
import org.eclipse.jgit.revwalk.RevCommit;
import org.eclipse.jgit.revwalk.RevTree;
import org.eclipse.jgit.revwalk.RevWalk;
import org.eclipse.jgit.treewalk.TreeWalk;
import org.eclipse.jgit.treewalk.filter.PathFilter;
import com.config.Config;
import com.performancefix.entity.PerfFixData;

/**
 * 
 * @author Foyzul Hassan
 *
 * 
 */

public class CommitAnalyzer {

	/** Various methods encapsulating methods to treats Git and commits datas */
	private CommitAnalyzingUtils commitAnalyzingUtils;

	/** Name of the project */
	private String project;

	/** Owner of the project (necessary for Markdown parsing) */
	private String projectOwner;

	/** Path to the directory */
	private String directoryPath;

	/** Repository object, representing the directory */
	private Repository repository;

	/** Git entity to treat with the Repository data */
	private Git git;

	/** Revision walker from JGit */
	private RevWalk rw;

	private String gradleChanges;

	private String gitUrl;

	/** Classic constructor */
	public CommitAnalyzer(String projectOwner, String project) throws Exception {
		this.projectOwner = projectOwner;
		this.project = project;

		directoryPath = Config.repoDir + project + "/.git";

		commitAnalyzingUtils = new CommitAnalyzingUtils();

		repository = commitAnalyzingUtils.setRepository(directoryPath);
		git = new Git(repository);
		rw = new RevWalk(repository);

		this.gradleChanges = "";
	}

	/** Classic constructor */
	public CommitAnalyzer(String projectOwner, String project, String giturl) throws Exception {
		this.projectOwner = projectOwner;
		this.project = project;

		directoryPath = Config.repoDir + project + "/.git";

		commitAnalyzingUtils = new CommitAnalyzingUtils();

		repository = commitAnalyzingUtils.setRepository(directoryPath);
		git = new Git(repository);
		rw = new RevWalk(repository);

		this.gradleChanges = "";
		this.gitUrl = giturl;
	}

	public List<PerfFixData> getAllPerformanceCommits()
			throws MissingObjectException, IncorrectObjectTypeException, IOException {
		List<PerfFixData> perffixdata = new ArrayList<>();

		Collection<Ref> allRefs = repository.getAllRefs().values();

		// a RevWalk allows to walk over commits based on some filtering that is defined
		try (RevWalk revWalk = new RevWalk(repository)) {
			for (Ref ref : allRefs) {
				revWalk.markStart(revWalk.parseCommit(ref.getObjectId()));
			}
			// System.out.println("Walking all commits starting with " + allRefs.size() + "
			// refs: " + allRefs);
			int count = 0;
			for (RevCommit commit : revWalk) {
				System.out.println("Commit: " + commit);
				count++;

				String commitmsg = commit.getFullMessage().toLowerCase();
				commitmsg = commitmsg.replaceAll(",", " cma ");
				commitmsg = commitmsg.replaceAll("\"", " quote ");

				if (isPerformanceCommit(commitmsg) && !commitmsg.contains("merge")) {
					String commitid = commit.getName();
					PerfFixData fixdata = new PerfFixData(this.project, this.getGitUrl(), commitid);
					fixdata.setFixCommitMsg(commitmsg);
					fixdata.setPatchPath("");
					fixdata.setAssetChangeCount(0);
					fixdata.setSrcFileChangeCount(0);
					perffixdata.add(fixdata);
				}

			}
			// System.out.println("Had " + count + " commits");
			// System.out.println(this.project);
		}

		return perffixdata;
	}

	private boolean isPerformanceCommit(String commitmsg) {
//		for (String token : Config.perfCommitToken) {
//			if (commitmsg.contains(token)) {
//				return true;
//			}
//		}

		boolean flag = false;

		List<String> perftokens = Arrays.asList(Config.perfCommitToken);
		StringTokenizer st = new StringTokenizer(commitmsg);

		while (st.hasMoreTokens()) {
			String token = st.nextToken();
			if (perftokens.contains(token)) {
				flag = true;
				break;
			}

		}

		return flag;
	}

	public String getGitUrl() {
		return gitUrl;
	}

	public void setGitUrl(String gitUrl) {
		this.gitUrl = gitUrl;
	}

	public RevTree getTree(String cmtid) throws IOException {
		ObjectId lastCommitId = repository.resolve(cmtid);

		// a RevWalk allows to walk over commits based on some filtering
		try (RevWalk revWalk = new RevWalk(repository)) {
			RevCommit commit = revWalk.parseCommit(lastCommitId);

			// System.out.println("Time of commit (seconds since epoch): " +
			// commit.getCommitTime());

			// and using commit's tree find the path
			RevTree tree = commit.getTree();
			// System.out.println("Having tree: " + tree);
			return tree;
		}
	}

	public String getStringFile(RevTree tree, String filter) throws IOException {
		// now try to find a specific file
		try (TreeWalk treeWalk = new TreeWalk(repository)) {

			treeWalk.addTree(tree);
			treeWalk.setRecursive(true);

			treeWalk.setFilter(PathFilter.create(filter));
			if (!treeWalk.next()) {
				throw new IllegalStateException("Did not find expected file:" + filter);
			}

			// FileMode specifies the type of file, FileMode.REGULAR_FILE for
			// normal file, FileMode.EXECUTABLE_FILE for executable bit
			// set
			FileMode fileMode = treeWalk.getFileMode(0);
			ObjectLoader loader = repository.open(treeWalk.getObjectId(0));

			// loader.copyTo(System.out);
			byte[] butestr = loader.getBytes();

			String str = new String(butestr);

			return str;

		}
	}

}
