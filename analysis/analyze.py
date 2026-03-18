"""
Analysis script for scraped jobs.
Usage: python analysis/analyze.py
Generates console summary + charts in plots/
"""

import pandas as pd
import matplotlib.pyplot as plt
import re
import os

PLOTS_DIR = 'plots'
os.makedirs(PLOTS_DIR, exist_ok=True)

df = pd.read_csv('../data/final/jobs.csv')

print("Dataset shape:", df.shape)
print("\nSample:")
print(df.head())

# Clean data
df = df.fillna('')
df['required_skills'] = df['required_skills'].str.lower()

# Top companies
top_comp = df['company_name'].value_counts().head(10)
print("\nTop companies:\n", top_comp)

# Top locations
top_loc = df['location'].value_counts().head(10)
print("\nTop locations:\n", top_loc)

# Top titles
top_title = df['job_title'].value_counts().head(10)
print("\nTop job titles:\n", top_title)

# Entry-level/intern/junior count
entry_keywords = ['intern', 'junior', 'entry', 'new grad']
df['entry_level'] = df['job_title'].str.lower().str.contains('|'.join(entry_keywords), na=False)
entry_count = df['entry_level'].sum()
print(f"\nEntry-level positions: {entry_count} ({entry_count/len(df)*100:.1f}%)")

# Top skills (simple word count)
all_skills = ' '.join(df['required_skills'])
words = re.findall(r'\b\w+\b', all_skills.lower())
skill_count = pd.Series(words).value_counts().head(15)
print("\nTop skills:\n", skill_count)

# Charts
fig, axs = plt.subplots(2, 2, figsize=(15, 10))

top_comp.plot(kind='bar', ax=axs[0,0])
axs[0,0].set_title('Top Companies')
axs[0,0].tick_params(axis='x', rotation=45)

top_loc.plot(kind='bar', ax=axs[0,1])
axs[0,1].set_title('Top Locations')
axs[0,1].tick_params(axis='x', rotation=45)

top_title.plot(kind='bar', ax=axs[1,0])
axs[1,0].set_title('Top Job Titles')
axs[1,0].tick_params(axis='x', rotation=45)

skill_count.plot(kind='bar', ax=axs[1,1])
axs[1,1].set_title('Top Skills')
axs[1,1].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig(f'{PLOTS_DIR}/summary_charts.png')
plt.show()

print("\nCharts saved to plots/summary_charts.png")
