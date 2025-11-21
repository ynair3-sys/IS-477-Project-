<h1>Yamuna & Monisha's Interim Status Report</h1>	

<h2>Overview</h2>	


Sleep is very important right? Despite this, college students choose to stay awake days on end willingly to run on only 3-4 hours of sleep at a time. Is this healthy, we know not. Yet, many of our peers still continue this routine, and somehow manage to attain good grades. So really is sleep all thaty important? We hope to uncover how sleep patterns influence academic performance and study productivity aong college students by integrating two distinct datasets. We want to undertsnad the direct effects of sleep on GPA, exam scores, and the indirect effects sleep has on study habits as well as productivity. We hope to uncover this answer through data analysis, incorporating ethical data handling, ensuring quality, integration, and automated reproducibility.  


<h2>Progress Update</h2>
<h5>Data Aquisition</h5>

Yamuna and I handled data acquisition by creating a Python script that fully automates downloading and validating our datasets. For the CMU Sleep & GPA dataset, the script pulls the CSV directly from the public URL using requests, saves it into our project’s data/raw directory, and immediately generates a SHA-256 checksum to confirm file integrity. 

For the Kaggle dataset, since redistribution isn’t allowed, the script checks for a manually downloaded file in the correct folder and verifies its checksum the same way. Both datasets are then summarized with basic row, column, and size information. All computed checksums are stored in a CHECKSUMS.txt file so anyone can reproduce the acquisition process and verify that the data they’re using matches the original source.


<h5>Github Organization</h5>

<img width="521" height="367" alt="Screenshot 2025-11-20 at 5 11 36 PM" src="https://github.com/user-attachments/assets/561a6810-ea31-4f2e-a271-15bc1ad0e4b3" />


<h5>Data Cleaning</h5>

For data cleaning, Monisha first ran the Python script to handle the major preprocessing steps—removing duplicates, fixing missing values, standardizing column names, converting units, flagging outliers, and validating numerical ranges. After running the script, we noticed that the parental_education column had its “None” values stripped to blanks, so Yamuna used OpenRefine for manual validation and correction of the datasets. In OpenRefine, Yamuna trimmed whitespace across all text fields to remove hidden characters, used text and categorical facets to confirm that category labels were consistent, and applied numeric facets to check that all numeric columns were correctly typed and fell within expected ranges. She also scanned for duplicate student IDs and duplicate rows to ensure no repeated entries remained. Together, the script and OpenRefine steps gave us a fully standardized, validated dataset ready for analysis.

<h5>Data Integration</h5>
-what we did, what artifacts were created, what decisisons were made

<h2>Artifacts</h2>
<h5>Raw Data: these files represent the original datsets exactly as downloaded. They are used as the source files for all cleaning and integration steps.</h5>
  <li><strong>data/raw/stduent_habits.csv</li></strong>
  <li><strong>data/raw/cmu_sleep.csv</li></strong>
  <li><strong>data/raw/CHECKSUMS.txt</li></strong>

<h5>Processed (Cleaned) Data Files: Outputs from the data-cleaning workflow.</h5>
  <li><strong>data/processed/cleaned_student_habits.csv</li></strong>
  <li><strong>data/processed/student_habits_cleaned.csv</li></strong>
  <li><strong>data/processed/cmu_sleep_cleaned.csv</li></strong>
  <li><strong>data/processed/cleaning_report.txt</li></strong>

<h5>Scripts:</h5>
  <li><strong>scripts/01_data_acquisition.py: Downloads or copies raw       data into the project structure.</li></strong>
  <li><strong>scripts/02_data_cleaning.py: Standardizes types, validates    ranges, trims whitespace, and writes cleaned outputs.</li></strong>
  <li><strong>data/processed/cmu_sleep_cleaned.csv</li></strong>
  <li><strong>data/processed/cleaning_report.txt</li></strong>





  

<h2>Changes to the Project Plan</h2>	
<h5>Summary of Changes</h5>
Yamuna and I made a few changes to our original project plan to reflect our actual workflow and the tools we adopted along the way. We pushed data iIntegration to next week because we chose to spend additional time strengthening our data cleaning phase. After learning how to use OpenRefine, we incorporated it into our workflow to perform more precise cleaning than initially planned. We also shifted the timelines for Workflow Automation and Reproducibility to earlier dates to accommodate the updated final project deadline (December 7th). No changes were needed based on Milestone 2 feedback, as our work aligned with project requirements, but we did clarify several questions with the TAs to ensure we remained on track.

<h5>Reason for Changes</h5>
These changes were necessary to make sure our cleaned datasets were thorough, consistent, and ready for smooth integration. Taking extra time to learn and use OpenRefine improved the overall quality of our preprocessing, even though it slightly delayed our other tasks. We adjusted the deadlines for Workflow Automation and Reproducibility to ensure we have enough time to complete all deliverables ahead of the final submission date. Overall, the changes to the timeline improve our workflow without compromising quality, and the guidance we received from 

<h2>Issues, Blockers, Risks</h2>	
We didn’t encounter major blockers, but there were a few risks. All datasets can be redistributed, so there are no restrictions on sharing files within our project. Time constraints were a factor since data cleaning took longer than expected, but we adjusted the timeline to stay on track. A minor tool limitation exists because OpenRefine requires manual interaction, but we mitigated this by documenting our cleaning steps to ensure reproducibility.

<h2>Next Steps</h2>

* Integrate the two cleaned datasets and store the output in data/integrated/.
  
* Finalize column alignment and document integration rules.
* Begin exploratory data analysis and produce initial visualizations.
* Build the automated “Run All” workflow for acquisition → cleaning → integration → EDA.
* Prepare for correlation and regression analysis on sleep vs. performance.
* Resolve any blockers related to join keys, mismatched columns, or missing values.

<h2>Updated Timeline</h2>

<ul>
 <li><strong>Project Setup (by Oct 6)</strong> – Finalize topic, form team, create GitHub repo, and identify two datasets. (Both)</li>
 <li><strong>Data Collection (by Oct 13)</strong> – Acquire datasets, verify integrity, and document sources. (Yamuna)</li>
 <li><strong>PStorage & Organization (by Oct 27)</strong> – Structure files, load data into clean format. (Monisha)</li>
 <li><strong>Data Cleaning (by Nov 3)</strong> – Handle missing values, duplicates, and inconsistencies. (Both))</li>
 <li><strong>Data Integration (by Nov 25)</strong> – Merge datasets, align schemas, and document process. (Both)</li>
 <li><strong>Interim Status Report (Due Nov 20)</strong> – Submit progress summary and contributions. (Both)</li>
 <li><strong>Analysis & Visualization (by Nov 28)</strong> – Analyze correlations and create visualizations. (Monisha lead, Yamuna support)</li>
 <li><strong>Workflow Automation (by Nov 30)</strong> – Develop “Run All” workflow. (Yamuna lead, Monisha support)</li>
 <li><strong>Reproducibility (by Dec 2</strong>) – Upload output to Box, finalize documentation. (Both)</li>
 <li><strong>Final Submission (Due Dec 7)</strong> – Submit final report, scripts, and artifacts. (Both)</li>

<h2>Contributions By each Team Memember</h2>	
<h5>Yamuna's Contributions</h5>
For this milestone, my partner and I worked collaboratively on all components of the project. We jointly did all the data acquisition, dataset inspection, cleaning, and documentation. Together, we executed the scripts, reviewed cleaning decisions, created the processing report, and organized the repository structure. We also co-wrote this StatusReport.md and revised our project timeline. While specific tasks were individually assigned, I actively participated in both the technical and documentation stages through pair programming and joint decision-making. We did completed everything so far with each other in person. 

<h5>Monisha's Contributions</h5>

For this milestone, I worked closely with Yamuna on all parts of the project. We sat together and collaborated on data acquisition, cleaning, and documentation, running scripts and validating decisions as a team. I actively participated in both technical tasks and report writing, ensuring the datasets were clean and reproducible. Overall, our contributions were joint, and all work was completed through in-person collaboration.





