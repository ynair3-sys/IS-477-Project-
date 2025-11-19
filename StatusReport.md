<h1>Yamuna & Monisha's Interim Status Report</h1>	

<h2>Overview</h2>	


Sleep is very important right? Despite this, college students choose to stay awake days on end willingly to run on only 3-4 hours of sleep at a time. Is this healthy, we know not. Yet, many of our peers still continue this routine, and somehow manage to attain good grades. So really is sleep all thaty important? We hope to uncover how sleep patterns influence academic performance and study productivity aong college students by integrating two distinct datasets. We want to undertsnad the direct effects of sleep on GPA, exam scores, and the indirect effects sleep has on study habits as well as productivity. We hope to uncover this answer through data analysis, incorporating ethical data handling, ensuring quality, integration, and automated reproducibility.  


<h2>DataSets</h2>
<h5>DataSet #1: CMU Sleep and GPA Dataset</h5>
Our first dataset that we have chosen is regarding CMU sleep and GPA. It was sourceed from Carnegie Mellon Univeristy Statistics and Data Science Repository. Its format is CSV. This dataset contains sleep and academic data from 634 first year college students across three universities being Carnegie Mellon, Univeristy of Washington, and Notre Dame. The study was about students wearing fitbit devices for one month during their spring semster to track sleep patterns. 

<h6>Key Variables:</h6>
-Sleep metrics: TotalSleepTime (minutes), bedtime_mssd (variablity), midpoint_sleep, and daytime_sleep

-Academic: term_gpa(0-4scale), cum_gpa, term_units

-Demographics: demo_gender, demo_race, demo_firstgen

-Data quallity: frac_nights_with_data

<h6>Source:</h6>
URL: https://cmustatistics.github.io/data-repository/data/cmu-sleep.csv

<h5>DataSet #2: Student Habits vs Academic Performance</h5>
This datset includes durvey data from 1,000 students captruing sleep habits, study behaviors, lifestyle factors, and academic performance. It is in CSV format. 

<h6>Key Variables:</h6>
Sleep: sleep_hours

Study Habits: study_hours_per_day, attendance_percentage

Distractions: social_media_hours, netflix_hours 

Lifestyle: diet_quality, excercise_frequency, mental_health_rating

Academic: exam_score

Demographics: age, gender, parental_education_level

<h6>Source:</h6>
URL: https://www.kaggle.com/datasets/jayaantanaath/student-habits-vs-academic-performance

<h2>Timeline</h2>	

Our project will progress in clearly defined phases, with equal contributions from both team members. We will meet weekly and track all updates in GitHub.

<ul>
 <li><strong>Project Setup (by Oct 6)</strong> – Finalize topic, form team, create GitHub repo, and identify two datasets. (Both)</li>
 <li><strong>Data Collection (by Oct 13)</strong> – Acquire datasets, verify integrity, and document sources. (Yamuna)</li>
 <li><strong>PStorage & Organization (by Oct 27)</strong> – Structure files, load data into clean format. (Monisha)</li>
 <li><strong>Data Cleaning (by Nov 3)</strong> – Handle missing values, duplicates, and inconsistencies. (Both))</li>
 <li><strong>Data Integration (by Nov 10)</strong> – Merge datasets, align schemas, and document process. (Both)</li>
 <li><strong>Interim Status Report (Due Nov 11)</strong> – Submit progress summary and contributions. (Both)</li>
 <li><strong>Analysis & Visualization (by Nov 24)</strong> – Analyze correlations and create visualizations. (Monisha lead, Yamuna support)</li>
 <li><strong>Workflow Automation (by Dec 5)</strong> – Develop “Run All” workflow. (Yamuna lead, Monisha support)</li>
 <li><strong>Reproducibility (by Dec 8</strong>) – Upload output to Box, finalize documentation. (Both)</li>
 <li><strong>Final Submission (Due Dec 10)</strong> – Submit final report, scripts, and artifacts. (Both)</li>

<h2>Constraints</h2>	
Our project faces a couple constraints that we believe may mpact our interpretation if not addressed. First, the two datasets represent different student populations sampled at different time periods, which limits our ability to directly compare findings any may affect any generalizations. The metadata in the Kaggle dataset informas us that it relies on self-reported survey data, introducing potential response bias. Meanwhile the CMU dataset's objective Fitbit measurements are limited to students who consistently wore their devices. It is also a known constraint that since we are expected to finish the project within 10 weeks time, we are forced to using personal computing resources rather than high-performance computing, and must manage data dtorage carefully gicen Github's file size limitations. We also acknowledge that missing data in both datasets may reduce our effective sample sizes for certain analyses. 

