import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# file_path = 'train.csv'
df = pd.read_csv(file_path)
# df.head()

# Define keywords to search for in the 'source_text' column
keywords = ['surgery', 'cancer']
campaigns_over_100k = df[df['goal'] > 100000]

# Check for the presence of keywords in the 'source_text' of these campaigns
campaigns_with_keywords = campaigns_over_100k['source_text'].apply(
    lambda text: any(keyword in text.lower() for keyword in keywords)
)


def calculate_success_rate(df):
    return (df['target_text'] == 'positive').mean() * 100


def calculate_average_goal(df):
    return df['goal'].mean()


def calculate_average_goal_by_success(df):
    successful_goals = df[df['target_text'] == 'positive']['goal'].mean()
    unsuccessful_goals = df[df['target_text'] == 'negative']['goal'].mean()
    return successful_goals, unsuccessful_goals


def calculate_success_rate_by_keyword(df, keyword):
    keyword_filter = df['source_text'].str.contains(keyword, case=False, na=False)
    success_rate = (df[keyword_filter]['target_text'] == 'positive').mean() * 100
    return success_rate


def plot_keyword_distribution(campaigns_with_keywords, campaigns_over_100k):
    labels = 'Contains Keywords', 'Does Not Contain Keywords'
    sizes = [campaigns_with_keywords.sum(), len(campaigns_over_100k) - campaigns_with_keywords.sum()]
    colors = ['#ff9999','#66b3ff']
    explode = (0.1, 0)

    plt.figure(figsize=(7, 7))
    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
    plt.axis('equal')
    plt.title('Percentage of Campaigns Over $100k with Keywords "Surgery" or "Cancer"')
    plt.show()


def plot_goals_statistics(df):
    successful_goals = df[df['target_text'] == 'positive']['goal']
    unsuccessful_goals = df[df['target_text'] == 'negative']['goal']

    average_successful_goals = successful_goals.mean()
    average_unsuccessful_goals = unsuccessful_goals.mean()

    median_successful_goals = successful_goals.median()
    median_unsuccessful_goals = unsuccessful_goals.median()

    # Prepare the bar plot for averages and medians
    labels = ['Successful', 'Unsuccessful']
    average_goals = [average_successful_goals, average_unsuccessful_goals]
    median_goals = [median_successful_goals, median_unsuccessful_goals]

    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width/2, average_goals, width, label='Average')
    rects2 = ax.bar(x + width/2, median_goals, width, label='Median')

    ax.set_ylabel('Goal Amount ($)')
    ax.set_title('Average vs Median Goal Amounts by Campaign Outcome')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    plt.show()


percentage_with_keywords = (campaigns_with_keywords.sum() / len(campaigns_over_100k)) * 100
print(f"Percentage of Campaigns Over $100k with Keywords 'Surgery' or 'Cancer': {percentage_with_keywords:.2f}%")

overall_success_rate = calculate_success_rate(df)
print(f"Overall Success Rate: {overall_success_rate:.2f}%")

average_goal = calculate_average_goal(df)
print(f"Average Goal Amount: ${average_goal:.2f}")

median_goal = df['goal'].median()
print(f"Median Goal Amount: ${median_goal:.2f}")

average_goal_success, average_goal_failure = calculate_average_goal_by_success(df)
print(f"Average Goal Amount for Successful Campaigns: ${average_goal_success:.2f}")
print(f"Average Goal Amount for Unsuccessful Campaigns: ${average_goal_failure:.2f}")

median_goal_success = df[df['target_text'] == 'positive']['goal'].median()
median_goal_failure = df[df['target_text'] == 'negative']['goal'].median()
print(f"Median Goal Amount for Successful Campaigns: ${median_goal_success:.2f}")
print(f"Median Goal Amount for Unsuccessful Campaigns: ${median_goal_failure:.2f}")

success_rate_surgery = calculate_success_rate_by_keyword(df, 'surgery')
success_rate_cancer = calculate_success_rate_by_keyword(df, 'cancer')
print(f"Success Rate for Campaigns with Keyword 'Surgery': {success_rate_surgery:.2f}%")
print(f"Success Rate for Campaigns with Keyword 'Cancer': {success_rate_cancer:.2f}%")

# Plot the graphs
plot_keyword_distribution(campaigns_with_keywords, campaigns_over_100k)
plot_goals_statistics(df)
