
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Load the data
daily_activity = pd.read_csv("../input/fitbit/Fitabase Data 4.12.16-5.12.16/dailyActivity_merged.csv")
daily_sleep = pd.read_csv("../input/fitbit/Fitabase Data 4.12.16-5.12.16/sleepDay_merged.csv")
weight_info = pd.read_csv("../input/fitbit/Fitabase Data 4.12.16-5.12.16/weightLogInfo_merged.csv")


daily_calories, daily_intensities, daily_steps = None, None, None

# Clean date columns
date_format = "%m/%d/%y"
daily_activity["Date"] = pd.to_datetime(daily_activity["ActivityDate"], format=date_format)
daily_sleep["Date"] = pd.to_datetime(daily_sleep["SleepDay"], format=date_format)
weight_info["Date"] = pd.to_datetime(weight_info["Date"], format=date_format)
weight_info["IsManualReport"] = weight_info["IsManualReport"].astype('category')

# Merge dataframes
final_df = pd.merge(pd.merge(daily_activity, daily_sleep, on=['Id', 'Date'], how='outer'),
                    weight_info, on=['Id', 'Date'], how='outer')


final_df = final_df.drop(columns=['TrackerDistance', 'LoggedActivitiesDistance',
                                  'TotalSleepRecords', 'WeightPounds', 'Fat', 'BMI', 'IsManualReport'])

# Check variables
final_df.info()
final_df.describe()

# Set up seaborn theme
sns.set_theme()

# Calories vs Total Steps
plt.figure(figsize=(10, 6))
sns.scatterplot(data=final_df, x='TotalSteps', y='Calories', hue='Calories', palette='viridis', alpha=0.7)
sns.regplot(data=final_df, x='TotalSteps', y='Calories', scatter=False)
plt.title('Calories burned by total steps taken')
plt.xlabel('Total Steps')
plt.ylabel('Calories')
plt.legend(title='Calories')
plt.show()

# Users' daily activity
plt.figure(figsize=(10, 6))
sns.boxplot(data=final_df.assign(weekdays=final_df['Date'].dt.day_name()), x='weekdays', y='TotalSteps')
plt.title("Users' activity by day")
plt.xlabel('Day of the week')
plt.ylabel('Steps')
plt.show()

# Intensity of exercise activity
plt.figure(figsize=(10, 6))
intensity_df = final_df[['VeryActiveDistance', 'ModeratelyActiveDistance', 'LightActiveDistance']]
intensity_df.sum().plot(kind='bar', color=['#66CC99', 'lightcoral', 'cornflowerblue'])
plt.title('Intensity of exercise activity')
plt.xlabel('Activity level')
plt.ylabel('Distance')
plt.show()

# Distribution of daily activity level
plt.figure(figsize=(8, 8))
activity_minutes_df = final_df[['VeryActiveMinutes', 'FairlyActiveMinutes', 'LightlyActiveMinutes', 'SedentaryMinutes']]
activity_minutes_df.sum().plot.pie(autopct='%1.2f%%', colors=['#66CC99', 'lightcoral', 'cornflowerblue', 'lightgrey'])
plt.title('Distribution of daily activity level in minutes')
plt.show()

# Sleep distribution
plt.figure(figsize=(10, 6))
sns.histplot(final_df['TotalMinutesAsleep'], bins=30, kde=True, hue_discrete=True, palette='Set2')
plt.title('Sleep distribution')
plt.xlabel('Time slept (minutes)')
plt.ylabel('Count')
plt.show()

# Sleep vs distance covered
fig = px.scatter(final_df, x='TotalSteps', y='TotalTimeInBed - TotalMinutesAsleep',
                 labels={'TotalSteps': 'Steps taken', 'TotalTimeInBed - TotalMinutesAsleep': 'Time in bed not asleep (minutes)'},
                 title="Users' difficulty to sleep vs steps taken")
fig.update_layout(xaxis_title="Steps taken", yaxis_title="Time in bed not asleep (minutes)")
fig.show()

# Weight vs distance covered
plt.figure(figsize=(10, 6))
sns.scatterplot(data=final_df.groupby('Id').mean(), x='WeightKg', y='TotalDistance', size='WeightKg', hue='Id', palette='viridis', alpha=0.7)
plt.title('Weight (kg) vs distance covered')
plt.xlabel('Kilograms')
plt.ylabel('Total Distance')
plt.show()
