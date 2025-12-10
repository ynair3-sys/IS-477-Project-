<h1>Yamuna and Monisha's Final Project</h1>	

<h2>Are Student's Sleeping on Success?
Modeling The Relationship Between Sleep Patterns and Academic Performance Among College Students</h2>	

<h2>Contributors</h2>	
  <li>Monisha Mudunuri (monisha5)</li>
  <li>Yamuna Nair (ynair3)</li>

<h2>Summary</h2>	

Sleep deprivation is extremely common among college students. Many students stay awake for days and run on only 3-4 hours of sleep at a time, yet somehow still manage to get good grades. This raises an important question: does sleep really matter for academic success, or can students perform well despite getting very little rest?

Our project examines how sleep patterns affect academic performance among college students by analyzing two different datasets. The first dataset is the CMU Sleep and GPA Dataset, which contains objective measurements from 634 first-year students at three universities (Carnegie Mellon, University of Washington, and Notre Dame). These students wore Fitbit devices for one month during their spring semester to track their sleep. The dataset includes metrics like total sleep time, bedtime variability, sleep midpoint, and daytime sleep, along with GPA data and demographic information. The second dataset comes from Kaggle and contains survey responses from 1,000 students about their sleep habits, study behaviors, social media usage, exercise, diet, mental health, and exam scores.
Our main research question is: How do sleep patterns influence GPA and study productivity among college students? We also want to know if factors like sleep timing and bedtime consistency matter for academic performance beyond just total hours of sleep. In other words, does how you sleep matter as much as how long you sleep?

Our workflow started with automated data acquisition. We wrote Python scripts that downloaded the CMU dataset from its public URL and verified both datasets using SHA-256 checksums saved in CHECKSUMS.txt. Since the Kaggle dataset cannot be redistributed, our script checked that the manually downloaded file was correct. We used the OpenRefine techniques that we learn in class to manually check the data, remove duplicates, fix missing values, standardize column names, convert units, and flag outliers. We also ensured to trim whitespace, verifying categories, and ensuring correct data types. We saved all cleaned versions of datasets in the  data/processed/ Cleaned CSV Datasets directory (the cleaned datasets are called cleaned_cmu-sleep and cleaned_student_habits). 
Combining the two datasets was our biggest challenge because they have different structures. One uses objective Fitbit measurements while the other uses self-reported survey data. We matched up overlapping variables like sleep duration and academic performance to create a unified dataset that let us compare both sources. After integration, we performed exploratory data analysis and created visualizations to find patterns in sleep behavior and academic outcomes.

We used correlation analysis and regression modeling to look at how sleep duration affects GPA and exam scores directly, and how it affects study habits and productivity indirectly. We checked whether bedtime consistency and sleep timing predict academic success separately from total sleep hours. We created scatter plots, correlation heatmaps, and distribution charts to show the relationships between sleep variability, study hours, lifestyle factors, and performance.

We faced several challenges. The two datasets represent different student groups from different time periods, making direct comparisons difficult. The Kaggle data relies on self-reports, which can be biased, while the CMU data only includes students who consistently wore their Fitbit devices. Time constraints forced us to adjust our timeline and delay data integration while we improved our data cleaning. Both Yamuna and I equally contributed to all aspects of this project. Our findings and results helped answer whether college students can truly succeed without adequate sleep, and what the costs might be for their well-being and long-term success.











<h2>Data profile</h2>	

Data Profile

**Dataset 1: CMU Sleep and GPA Dataset with Fitbit Data**

The first dataset comes from a research project at three colleges: Carnegie Mellon, the University of Washington, and Notre Dame. Students in the study wore Fitbit watches for about a month during their spring semester. Because of that, the dataset has very detailed information about how the students slept and how active they were every day. It includes variables such how long they slept, how much time they spent in REM sleep, deep sleep, and light sleep, and how many times they woke up during the night. It also shows step count, minutes spent being active, minutes spent sitting, and calories burned. Their school information is there too, like their semester GPA and how they were doing in their classes which we found really nice for the long run. Each row in the dataset represents one day for one student, which adds up to around nineteen thousand days of data. All the measurements use clear units like minutes or percentages. Everything is organized so you can follow each student over time.There is no personal information that could identify any student. Everyone is assigned an ID number instead of a name, and the data does not include anything specific like exact addresses or the exact time someone fell asleep. The original researchers got approval from their universities and the students agreed to be part of the study.

In our project, this dataset helps us because it gives real measured sleep data instead of guesses. Before we used the dataset, we cleaned it via OpenRefine checking for missing values, removing strange outliers, editing cells to be numeric, and more. The cleaned files are saved in a processed folder for reference. 

**Dataset 2: Kaggle Student Habits and Academic Performance Dataset**

The second dataset is from Kaggle and is based on a survey that one thousand students filled out. Unlike the Fitbit data, this one is all self reported, meaning students answered questions about their own habits.It includes their usual sleep hours, what time they go to bed, how good they think their sleep is, how much they study, how much time they spend on social media, how often they exercise, and how stressed they feel. It also has information about their GPA, their course load, their age, gender, and whether they live on campus or off campus.In this dataset, each student is one row. Most answers are either numbers or short text responses. Since it is a survey, all the data comes from one moment in time and does not track students across multiple days.

Important to note there is no personal information like names or emails. Still, because it was collected by someone in the Kaggle community and not through an official research study, the consent process is not very clear. That means we treat this dataset as helpful and interesting, but not as strong as the Fitbit dataset when making big claims. Even though we couldn’t find where this dataset was originally collected or confirm any official IRB approval, we still decided to use it because it had a lot of signs that it was reliable and useful. Kaggle gave it a perfect 10.0 usability score, which basically means it’s complete, clear, and easy to work with. The dataset comes with really good descriptions that explain what every column means, and the Kaggle page says it’s a simulated but realistic dataset with 1,000 student records. It includes things like study hours, sleep, social media time, diet quality, and mental health, all connected to final exam scores. The creator made it for machine learning, regression, classification, and visualizations, so it fits exactly what we needed for our project. It’s already clean, organized, and ready to explore without a lot of extra work. Kaggle also expects it to be updated every year, which shows that it’s being maintained. Plus, the topics it covers—like stress, sleep, and social media—are super real for students today. Even though the data is simulated, it still feels realistic and helps us study patterns about how habits might affect school performance. Because of the high usability score, clear documentation, and how well it matched our goals, we felt okay using it along with the CMU dataset, even if we couldn’t track down where it originally came from.

We clean this dataset too by handling missing answers, converting text answers into numbers when needed, and creating new scores like time management or wellness scores.

**Integration Strategy**

The two datasets cannot be directly combined because they come from different groups of students at different schools and times. But they work well together in a different way. The Fitbit dataset gives very accurate sleep information based on real measurements. The Kaggle dataset gives personal context that devices cannot measure, like stress levels, study habits, and how students feel about their sleep. To connect the two datasets, we use three approaches. The first approach is to analyze each dataset separately and see if similar patterns show up in both. The second approach is to match students from one dataset to students in the other who have similar characteristics, even though they are not the same people. The third approach is to compare the results from both datasets and combine the findings to get bigger conclusions.

All the processed files and results are kept in a folder for our integrated sleep study so everything stays organized and easy to follow.

<h2>Data Quality</h2>	

We assessed the quality of both datasets by checking for completeness, consistency, accuracy, and any issues that might affect our analysis. All cleaning and validation were done manually using OpenRefine to make sure every correction was intentional and documented.

**Completeness and Missing Data** 

The CMU Sleep Dataset included 634 students and 15 columns. While most fields were complete, the demo_firstgencolumn had unclear entries—some students were marked as “2,” and others had blank values. Since the meaning wasn’t clear, we recorded all uncertain entries as “Unknown” rather than guessing.

We also looked at frac_nights_with_data, which shows how consistently students wore their Fitbits. Some students wore their device every night, while others didn’t, so the reliability of sleep data varies from student to student.

The Kaggle Student Habits Dataset had 1,000 students and 16 columns with no missing values. However, because all the information was self-reported, we had to keep in mind the possibility of inaccurate recall or students reporting what sounds better than reality.

**Consistency and Format Issues**

Both datasets had major formatting problems. In the CMU dataset, many columns that should have been numeric were incorrectly stored as text. We manually converted 11 columns into the correct numeric format in OpenRefine, including sleep measures like TotalSleepTime, bedtime_mssd, and midpoint_sleep, along with academic variables such as term_gpa and cum_gpa. A few fields, like study and demo_race, were originally treated as numbers but were actually categorical labels, so we converted them back into text.

In the Student Habits dataset, several text fields had hidden spaces or inconsistent formatting. We removed whitespace across all text columns and changed 10 fields—such as age, sleep_hours, exercise_frequency, attendance_percentage, and exam_score—from text to numbers so they could be used in analysis.

**Accuracy Checks and Duplicates**

We checked all values to make sure they were reasonable. For example, no one should have negative sleep hours, more than 24 hours of sleep, a GPA above 4.0, or attendance outside the 0–100% range. When we found extreme values, we reviewed them manually in OpenRefine. Most of them reflected real edge cases rather than errors, so we kept them.

We also removed duplicate entries in the CMU dataset using subject_id, ensuring each student only appeared once. The Student Habits dataset had no duplicates.

**Tools and Workflow**

Since we did all data cleaning manually, our workflow was straightforward:

1. Load the datasets into OpenRefine
2. Fix formatting issues, convert data types, and clean categories
3. Review and correct inaccuracies
4. Document every change using OpenRefine’s built-in history
   
We exported the OpenRefine histories for both datasets so the entire cleaning process is fully reproducible (17 steps for CMU and 16 steps for the Student Habits dataset). Cleaned files were saved in data/processed/Cleaned CSV Datasets and raw files remained untouched in data/raw/.

**Changes and Standardization**

To make the two datasets comparable, we standardized measurements. For example, the CMU dataset reported sleep in minutes whereas the Kaggle dataset reported sleep in hours—so we converted everything to hours for consistency. We also created three sleep categories based on widely accepted sleep health guidelines:
- Low sleep: under 6 hours
- Moderate sleep: 6–8 hours
- High sleep: over 8 hours

**Limitations**

The CMU dataset only includes first-year students at three universities during one semester, so it doesn’t necessarily represent all college students. And because the study relied on volunteers who wore Fitbits regularly, the sample may differ from the general student population.

The Kaggle dataset is self-reported, which means students may have overestimated positive habits (like studying) and underestimated negative ones (like screen time). Since the two datasets come from different populations, we had to be cautious when comparing them.

**Impact on Analysis**

After cleaning, the CMU dataset retained all 634 students with complete sleep and GPA information, and the Student Habits dataset kept all 1,000 entries with no missing values. Because every cleaning step was done manually and documented, our analysis is fully transparent and reproducible. The resulting datasets are cleaner, more consistent, and more reliable, giving us a strong foundation for our findings.

<h2>Findings</h2>	

We looked at data from 1,547 college students and found some clear patterns about how sleep affects school performance. Sleep does matter for grades, but the effect is smaller than many people think.

**Sleep Patterns Among Students**

Most students in our study are not getting enough sleep. On average, students sleep only 6.52 hours per night, which is below the recommended 7–8 hours. When we looked at the sleep categories, the results were concerning. About 1,056 students, or 68 percent, fall into the Poor or Insufficient sleep groups.

Here’s the breakdown:
- 489 students sleep less than 6 hours
- 567 students sleep 6–7 hours
- 363 students sleep 7–8 hours
- 128 students sleep more than 8 hours
  
Most students sleep 6–7 hours, and the average is still below the recommended 7 hours.

**Sleep and Academic Performance: The Direct Effect**

Students who sleep more usually have better grades, but the effect is small. The correlation between sleep and academic scores is only 0.14, meaning sleep explains about 2 percent of why some students do better than others.

The scatter plot shows a line going upward, meaning more sleep is linked to higher scores, but the dots are very spread out. The equation y = 2.25x + 60.87 tells us that each extra hour of sleep raises a student’s score by about 2.25 points. So going from 6 to 8 hours would increase a score by about 4.5 points.

**Comparing sleep groups:**

- Poor sleep (<6 hours): 71.3 average score
- Insufficient sleep (6–7 hours): 77.3 average
- Adequate sleep (7–8 hours): 78.8 average
- Optimal sleep (>8 hours): 74.7 average

These results show that 7–8 hours is best. Students who slept more than 8 hours scored lower, which was surprising. An ANOVA test confirmed these differences are real (F = 16.49, p < 0.001).

**Comparing Fitbit Data and Self-Reports**

We compared two datasets. CMU students used Fitbits to track sleep automatically, while Kaggle students reported their own sleep.

Findings:

- CMU students slept 6.61 hours on average with less variation (SD = 0.85)
- Kaggle students reported 6.47 hours with more variation (SD = 1.23)

This shows self-reported sleep is less accurate. CMU students also had much higher academic scores (86.4 vs. 69.6), though the scores aren’t directly comparable because the systems were different.

The sleep–grade link was slightly different too:

- CMU (Fitbit): correlation 0.16, slope 2.30 points per hour
- Kaggle (self-report): correlation 0.12, slope 1.68 points per hour
  
Measured sleep shows a slightly stronger effect, but it is still small.

**How Sleep Affects Performance: The Productivity Question**

We wanted to see if getting more sleep makes students more productive. Surprisingly, it doesn’t. Sleep had almost no connection to productivity (correlation -0.015). Students who slept more didn’t study longer or attend class more often.

Productivity itself, though, really matters for grades (correlation 0.66). Across all sleep groups, students studied about the same which was around 3.3–3.6 hours per day and attendance was similar, around 84–85%. This shows that sleep doesn’t boost performance by making students more productive.

A mediation test confirmed that sleep does have a direct effect on scores, adding about 1.68 points for each extra hour of sleep. However, this effect is not due to changes in productivity. The proportion mediated was -0.08, which shows that productivity does not explain the link between sleep and grades.

**What the Numbers Really Mean**

Sleep does help grades, but the effect is small. Getting an extra hour of sleep might raise a score by 2 to 3 points, which is not enough to dramatically change grades. Sleep seems to help more directly, probably by improving focus or thinking, rather than by increasing study time or class attendance. With 68 percent of students not getting enough sleep, it is clear that many are trading sleep for other responsibilities or simply not prioritizing it, even though it offers clear benefits


<h2>Future work</h2>	

Our project gave us a good look at how sleep patterns might relate to academic performance, but it also exposed several limitations in the data, methods, and tools we used. These limitations shaped our findings and show where improvements could make the analysis stronger. Being aware of these gaps can help future research produce more reliable insights into how sleep affects academic outcomes.

**Limitations**

One big limitation was the quality of the data. The CMU Sleep Dataset had missing demographic informatio  n, inconsistent responses, and some entries that looked inaccurate. Since the data comes from students reporting their own habits, it’s vulnerable to errors like forgetting details, estimating incorrectly, or answering in ways they think are “better” than reality. This makes some of the variables less trustworthy.

The Kaggle Student Habits dataset is released under the Apache License 2.0, which means we can use, modify, and share it freely as long as we acknowledge the source, include the license, and document any changes. While the license allows this, the dataset itself comes from different student submissions that weren’t all verified, so errors could exist. In our project, we manually cleaned and standardized the data using OpenRefine and carefully documented every change.

Our methodology had its limits as well. Because the datasets had relatively few variables, we mainly relied on descriptive statistics, simple correlations, and basic visualizations. These approaches help spot general trends but can’t fully capture all the factors that influence academic performance. Students’ grades are affected by stress, workload, extracurricular activities, jobs, and mental health—most of which weren’t included in the datasets. This means our results show associations but can’t prove causation.

**What We Would Do With More Time or Better Data**

If we had more time or better data, the first step would be to get richer datasets. Ideally, these would include detailed sleep information, academic performance, demographics, stress and mental health measures, and information about jobs, study habits, and extracurriculars. Adding timestamps would let us track patterns over weeks or months instead of looking at a single snapshot.
Better data would also let us run more advanced analyses. Multivariate regressions could control for confounding factors, clustering could reveal distinct sleep behavior groups, and machine learning models like random forests or gradient boosting could detect more complex patterns. 

**Extending Workflow Automation**

There’s also room to make the workflow more automated. Python pipelines could handle data cleaning, analysis, modeling, and visualization in one system. Using Jupyter notebooks or a simple ETL setup would make updates faster, reduce mistakes, and make the process easier to reproduce. Automation could also allow the project to update results continuously instead of producing just one static analysis.

**Opportunities for Deeper Modeling and Better Visualizations**

Future studies could take a closer look using more advanced methods. Instead of looking at each factor on its own, predictive models like multiple regression or machine learning could help show how sleep, study habits, and lifestyle together affect academic performance. Clustering analysis could also group students in other ways for example, high achievers who sleep less, students who perform poorly despite enough sleep, or those who make up for poor sleep with strong study habits. This would help show whether different types of students might benefit from different strategies.

Visualizations could also be more interactive instead of just static charts. For example, dashboards built with tools like Tableau could let users filter by things like gender, major, or school to see how patterns change across groups. Interactive heatmaps could show correlations between all the variables at once, making it easier to spot surprising connections between mental health, exercise, and grades. Users could click on data points to see details about individual students or hover over charts to get exact numbers, making the data more engaging and easier to explore.

**Reflection**

Overall, Yamuna and I believe that this project provided us with a solid foundation for understanding the relationship between sleep and academic performance. Even with data and methodology limits, we were able to identify clear patterns, clean and standardize the datasets using the steps we learnt in class and labs, and create meaningful visualizations. Our findings highlight the value of healthy sleep habits and could serve as a starting point for future research or initiatives supporting student wellness.


<h2>Reproducing This Project</h2>







<h2>References</h2>
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
