<h1>Yamuna and Monisha's Final Project</h1>	

<h2>Are Student's Sleeping on Success?
Modeling The Relationship Between Sleep Patterns and Academic Performance Among College Students</h2>	

<h2>Contributors</h2>	
  <li>Monisha Mudunuri </li>
  <li>Yamuna Nair</li>

<h2>Summary</h2>	

Sleep deprivation is extremely common among college students. Many students stay awake for days and run on only 3-4 hours of sleep at a time, yet somehow still manage to get good grades. This raises an important question: does sleep really matter for academic success, or can students perform well despite getting very little rest?

Our project examines how sleep patterns affect academic performance among college students by analyzing two different datasets. The first dataset is the CMU Sleep and GPA Dataset, which contains objective measurements from 634 first-year students at three universities (Carnegie Mellon, University of Washington, and Notre Dame). These students wore Fitbit devices for one month during their spring semester to track their sleep. The dataset includes metrics like total sleep time, bedtime variability, sleep midpoint, and daytime sleep, along with GPA data and demographic information. The second dataset comes from Kaggle and contains survey responses from 1,000 students about their sleep habits, study behaviors, social media usage, exercise, diet, mental health, and exam scores.
Our main research question is: How do sleep patterns influence GPA and study productivity among college students? We also want to know if factors like sleep timing and bedtime consistency matter for academic performance beyond just total hours of sleep. In other words, does how you sleep matter as much as how long you sleep?

Our workflow started with automated data acquisition. We wrote Python scripts that downloaded the CMU dataset from its public URL and verified both datasets using SHA-256 checksums saved in CHECKSUMS.txt. Since the Kaggle dataset cannot be redistributed, our script checked that the manually downloaded file was correct. We used the OpenRefine techniques that we learn in class to manually check the data, remove duplicates, fix missing values, standardize column names, convert units, and flag outliers. We also ensured to trim whitespace, verifying categories, and ensuring correct data types. We saved all cleaned versions of datasets in the  data/processed/ Cleaned CSV Datasets directory (the cleaned datasets are called cleaned_cmu-sleep and cleaned_student_habits). 
Combining the two datasets was our biggest challenge because they have different structures. One uses objective Fitbit measurements while the other uses self-reported survey data. We matched up overlapping variables like sleep duration and academic performance to create a unified dataset that let us compare both sources. After integration, we performed exploratory data analysis and created visualizations to find patterns in sleep behavior and academic outcomes.

We used correlation analysis and regression modeling to look at how sleep duration affects GPA and exam scores directly, and how it affects study habits and productivity indirectly. We checked whether bedtime consistency and sleep timing predict academic success separately from total sleep hours. We created scatter plots, correlation heatmaps, and distribution charts to show the relationships between sleep variability, study hours, lifestyle factors, and performance.

We faced several challenges. The two datasets represent different student groups from different time periods, making direct comparisons difficult. The Kaggle data relies on self-reports, which can be biased, while the CMU data only includes students who consistently wore their Fitbit devices. Time constraints forced us to adjust our timeline and delay data integration while we improved our data cleaning. Both Yamuna and I equally contributed to all aspects of this project. Our findings and results helped answer whether college students can truly succeed without adequate sleep, and what the costs might be for their well-being and long-term success.











<h2>Data profile</h2>	
(500–1000 words)
For each dataset, include:
Name of dataset
Source (API, website, generated internally, etc.)
Description (variables, schema, shape, time span, units)
How it was obtained (script, manual download, programmatic retrieval)
Ethical or legal considerations
Licensing restrictions
Terms of Use requirements
Personally identifiable information (PII) handling
Any de-identification steps
How the data fits into your analysis pipeline
Where it is stored in your repo, and where the output data from Box should be placed

<h2>Data quality</h2>	
(500–1000 words)
Summarize quality assessment:
Completeness (missingness patterns)
Consistency (format issues, schema mismatches)
Accuracy (validation checks, outliers)
Timeliness
Duplicates
Biases or sampling limitations
Tools used (profiling scripts, pandas checks, visualizations)
Actions you took to address issues
Cleaning steps
Transformations
Derived variables added
Conclude with the net impact on your analysis.

<h2>Findings</h2>	
(Up to ~500 words)
Describe final analytical results, including:
Key numerical results
Patterns/trends discovered
Visualizations (insert ![](path/to/figure.png) if including inline)
Interpretation—what the numbers actually mean
Any hypotheses supported or contradicted
Be direct and evidence-based.

<h2>Future work</h2>	
(500–1000 words)
Discuss:
Limitations (data, methodology, tooling)
What you would do with more time or better data
How workflow automation could be extended
Opportunities for deeper modeling or improved visualizations
Practical next steps for anyone continuing this project

<h2>Reproducing This Project<h2></h2>
A strict step-by-step workflow someone can follow start to finish.

<h2>References</h2>	
Provide formatted citations for:
Datasets
Dataset name. URL. Accessed on <date>. License: <license>.
Software
Python packages or libraries used.
Example:
Pedregosa et al., Scikit-learn: Machine Learning in Python (2011).
Papers / background sources
Author(s). Year. Title. Journal/Conference. DOI/URL.
Use consistent citation style (APA, Chicago, IEEE, etc.).


CMU Sleep Dataset
Carnegie Mellon University, Department of Statistics & Data Science. (n.d.). CMU Sleep Study Dataset [Data set]. CMU Statistics Data Repository. Retrieved December 9, 2025, from https://cmustatistics.github.io/data-repository/data/cmu-sleep.csv.
License: Not specified; use permitted for educational and research purposes only, but redistribution or commercial use is not explicitly allowed


### Software/Code
This project's code is licensed under the MIT License. See [LICENSE](LICENSE) file.

### Data Sources

**CMU Sleep Dataset:**
- Source: Carnegie Mellon University Statistics & Data Science Repository
- Citation: Creswell, J. D., et al. (2023). Nightly sleep duration predicts grade point average in the first year of college. PNAS, 120(8), e2209123120.
- License: Open for academic use with attribution
- URL: https://cmustatistics.github.io/data-repository/psychology/cmu-sleep.html

**Kaggle Student Habits Dataset:**
- Source: Kaggle (jayaantanaath)
- Citation: Jayaantanaath. (2025). Student Habits vs Academic Performance [Dataset]. Kaggle.
- License: Public dataset on Kaggle
- URL: https://www.kaggle.com/datasets/jayaantanaath/student-habits-vs-academic-performance
