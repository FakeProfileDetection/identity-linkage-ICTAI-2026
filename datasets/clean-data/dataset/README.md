# Dataset

# Dataset info
Plaforms:
- 1 = Facebook clone
- 2 = Instagram clone
- 3 = Twitter clone

Videos:
- 1 = Coach Carter
- 2 = Oscar Slap
- 3 = Trump/Zelensky

Session:
- 1 = First session
- 2 = Second session

# Organization
The subdirectories contain the processed datasets.

## keypairs
Two files, containing the same dataset.  keypairs.csv and a parquet version. These are the processed keystroke features:
- user_id
- platform_id
- video_id
- session_id
- sequence_id
- key1
- key2
- key1_press
- key1_release
- key2_press
- key2_release
- HL
- IL
- PL
- RL
- valid
- error_description
- key1_timestamp
- outlier
- device_type

## keystroke-timeing-csv
These are the raw csv files.  Each file contains:
- Press or Release
- Key
- Time

The directory is organized by user_id.  Each user_id has 18 files.  The filename patters are <platform_id>_<video-id>_<session-id>_<user_id>.csv

## text
Raw text responses per user.

The directory is organized by user_id.  Each user_id has 18 files.  The filename patters are <platform_id>_<video-id>_<session-id>_<user_id>.txt


## top-10-aggregated-IL-features
Statistical features (mean, median, q1, q3, std) for top 10 most frequent digrams.  features_summary.json files contain the features and other metadata.

### stastical_IL_top_10_platform
Aggregated over each platform for all videos and session. 3 platforms = 3 samples per user. Features are:
- user_id
- platform_id
- 5 * 10 aggregated IL features

### stastical_IL_top_10_session
Aggregated over each session for all videos. 3 platforms + 2 sessions = 6 samples per user. Features are:
- user_id
- platform_id
- session_id
- 5 * 10 aggregated IL features

### stastical_IL_top_10_video
Aggregated over each videos. 3 platforms + 2 sessions + 6 videos = 18 samples per user. Features are:
- user_id
- platform_id
- session_id
- video_id
- 5 * 10 aggregated IL features
