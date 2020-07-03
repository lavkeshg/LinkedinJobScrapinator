# Overview

The project is a simple tool that scrapes search results from linkedin and refine them to fit entry-level candidate profiles. Even though linkedin search filter offers an option of refining jobs with entry-level requirements, it is often observed that the results generated require work experience for a significant number of years. Until linkedin figures that out you can run the tool using the `run.sh` file and a csv file is generated with links to jobs which will re-direct you to their linkedin application pages.

# Brownie features

Additionally, the tool scores each result on the basis of the skills that matches with your resume. These skills are currently hard-coded into a regex in the main file. However future releases will accept input of user-defined skills. The score is negatively impacted by the number of years experience which is required for the job. Most importantly, an added feature discards results that require 'security clearance', international students applying in the US can benefit from this feature.

# Requirements
Selenium, Beautifulsoup and Chrome
