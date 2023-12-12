import os
import openai
import csv
openai.api_key = os.getenv("OPENAI_API_KEY")


# Open the input and output files
with open('sample_30.csv', 'r') as csvfile, open('result.csv', 'w', newline='') as output_csv:
    reader = csv.DictReader(csvfile)
    writer = csv.writer(output_csv)

    # Write the header row for the output CSV
    writer.writerow(["Title", "Description", "Goal Amount", "Output", "Ground Truth"])

    # Loop through the input CSV rows and process them
    for row in reader:
        # print(row)
        m = [{"role": "system", "content": """ The characteristics of a successful campaign's description can be identified as follows:
1. Clear and Compelling Title: Each campaign has a concise and descriptive title, such as "Mike Coddington Kidney Transplant" or "Support Drew's New Jaw". These titles immediately convey the purpose of the campaign and whom it is intended to help.
2. Detailed Description: The descriptions should be detailed, providing context and background information about the situation. They often include personal stories or specific reasons for the fundraising, which can create an emotional connection with potential donors.
3. Length of Description: A balanced amount of information (neither too brief nor excessively long) contributes to a successful campaign.
4. Goal amount: Setting a too high amount for the goal can lead to unsuccessful campaign.

Common characteristics of an unsuccessful campaign descriptions:
1.Vague or Unclear Descriptions: Descriptions that lack clear information about the purpose of the campaign, the beneficiaries, or how the funds will be used can lead to a lack of trust or interest from potential donors.
2.Lack of Personal Touch or Story: Campaigns that fail to make a personal connection with the audience or don’t provide a compelling story may struggle to evoke empathy or interest.
Overly Ambitious or Unspecified Goals: Goals that seem overly ambitious or are not clearly justified can deter potential donors. Similarly, a lack of specific goals can make a campaign appear less credible.
3.Poor Presentation: Errors in spelling, grammar, or formatting, as well as a lack of engaging media (like images or videos), can negatively impact the perception of the campaign.
4.Lack of Urgency: If the campaign doesn’t convey a sense of urgency or immediate need, potential donors might be less compelled to act quickly.
Limited Engagement or Updates: Campaigns that do not update their supporters or engage with their audience may lose momentum and fail to build a community around their cause.
4.Inadequate Promotion: Insufficient promotion and visibility can lead to unsuccessful campaigns. If a campaign is not effectively shared or marketed, it may not reach enough potential donors.
5.Lack of Transparency: If donors feel that there is a lack of transparency in where the funds are going or how they will be used, they may be reluctant to contribute.
6.Negativity or Pessimism: Overly negative tones or a lack of optimism in the campaign description can be off-putting to potential donors.

Now given the title, description and the goal amount of a campaign, your job is to decide whether it can be successful. If it can be successful, output '1', otherwise output '0'. """}]
        title = row['Title']
        description = row['Description']
        goal_amount = row['Goal Amount']
        success = row['success']

        input_statement = f"Title: {title}\nDescription: {description}\nGoal Amount: {goal_amount}\n"
        # input_statement = row[0]
        dic = {}
        dic["role"] = "user"
        dic["content"] = input_statement
        m.append(dic)

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=m
        )

        output = completion.choices[0].message['content']
        writer.writerow([title, description, goal_amount, output, success])
