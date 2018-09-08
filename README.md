# De Correspondent YouTube Extremism project
Exploring extremism on YouTube collaboration methods to ensure open and reproducible data research.

## For each working group please create your own folder on the master branch where to place your scripts
- Please use a descriptive folder name e.g. data gathering, topic modeling, etc.
- Please add a readme to the folder where you describe:
  - Your team members and contact information
  - Your approach; specifying which data you used as input, how you processed it (with link to script adn what frameworks are used), what your output data is and a link to where it is saved in the GDrive.
- You may create a branch for your subfolder to work on, so you do not have to synchornize all folders and scripts.

## Proposed high folder overview

- Data gathering
  - Video data (metadata, transcript, comments)
  - Channel data (videos with their data)
  - User data (subscriptions, videos likes)
  
- Topic mapping (can we identify what topics are prevalent in entities?)
  - Channel topic mapping
  - User topic mapping
  - Video topic mapping
  
- Clustering (can we identify entities that cluster around certain features?)
  - Channel clustering
  - User clustering
  - Video clustering
  
- Classification (can we classify entities to show similarities with certain topics?)
  - Channel classification
  - User classification
  - Video classification
  
- Network analysis (can we identify cliques of channels or users isolated around certain topics?)
  - Channel network
  - User network

- Temporal change (do we see differences November 2017 and August 2018?
  - Topic prevalence
  - Cluster membership
  - Classification
  - 
  
## Data storage standardisation
- Let's standardise how and where we save data. To ensure plaftorm and technology interoperability the proposal is to save all results as CSV files with the first row having column IDs.
- In your readme you can add additional information describing the columns.
- Temporary solutions is to dave your results as CSV on GDrive. Please create direct links from GitHub readme and scripts to the file to save browsing time.
- We are exploring http://data.world as next solution; it allows you to connect through API to read and write results there.

# Project discussion on Slack channel
[https://correspondentex.slack.com](https://correspondentex.slack.com)
