## Proposal

### Instructions copied below:



Your proposal should be no more than 1,000 words and include a sketch of your app. The proposal should be written as a markdown document (`proposal.md`) in your GitHub.com repo and include the following sections:

1. Motivation and purpose of your dashboard
2. Expanded EDA: "cleaned up" and expanded EDA and description of the data
3. Research question(s) you are exploring; you should aim to make these research questions compelling and substantial

You will be assessed on the reasoning underlying your proposal as well as the quality and clarity of your writing.

Each of the proposal sections are described below and include an example of what is expected. You don't have to write your own proposal _exactly_ the same as the examples, they just serve as inspiration.
You will not be penalized if you can't implement everything in your proposal, or if your app changes due to technical or time limitations, but try to think about whether you think you will be able to implement it in the time frame of the course
(this is admittedly hard since you have not worked with the dashboard frameworks before, but it is good to have it in mind already in the planning phase).

### Section 1: Motivation and Purpose

In a few sentences, provide motivation for why you are creating a dashboard.
Who is your target audience, and what role are you embodying?
What problem could your dashboard solve for the intended user?
You can read the [Project background](#project-background) section for some rough ideas.
Be brief and clear.

Example write up:

> Our role: Data scientist consultancy firm
>
> Target audience: Health care administrators
>
> Missed medical appointments cost the healthcare system a lot of money and affects the quality of care. If we could understand what factors lead to missed appointments it may be possible to reduce their frequency. To address this challenge, we propose building a data visualization app that allows health care administrators to visually explore a dataset of missed appointments to identify common factors. Our app will show the distribution of factors contributing to appointment show/no show and allow users to explore different aspects of this data by filtering and re-ordering on different variables in order to compare factors that contribute to absence.

### Section 2: Description of the data

You must use one of the datasets that was previously approved in Data 550 for this project, as long as you have the license to use it publicly.
Now that you have some more experience with the data, you can start diving deeper into the dataset and update your EDA with an eye towards making your final dashboard.
You may do this in a Jupyter Lab Notebook

In your proposal, briefly describe the dataset and the variables that you will visualize.
If you are planning to visualize a lot of columns, provide a high level descriptor of the variable types rather than listing every single column.
For example, indicate that the dataset contains a variety of categorical variables for demographics and provide a brief list rather than describing every single variable.
You may also want to consider visualizing a smaller set of variables given the short duration of this project.
This might include an expanded EDA for you to grasp what could be interesting aspects to look at in your data.
Feel free to include your EDA notebooks in the public GitHub repo, so that you have everything in one place.

Example writeup:

> We will be visualizing a dataset of approximately 300,000 missed patient appointments.
> Each appointment has 15 associated variables
> that describe the patient who made the appointment
> (`patient_id`, `gender`, `age`),
> the health status (`health_status`) of the patient
> (Hypertension, Diabetes, Alcohol intake, physical disabilities),
> information about the appointment itself (`appointment_id`, `appointment_date`),
> whether the patient showed up (`status`),
> and if a text message was sent to the patient about the appointment (`sms_sent`).
> Using this data we will also derive a new variable,
> which is the predicted probability that a patient will show up for their appointment (`prob_show`).

Remember if your dataset has _a lot_ of columns, stick to summaries and avoid listing out every single column.
The example also differentiates columns that come with the dataset (i.e. `Age`) from new variables that you might derive for your visualizations (i.e `ProbShow`) - you should make a similar distinction in your write-up if you can.
Another example of [a good description of a dataset is the Kaggle world happiness report](https://www.kaggle.com/unsdsn/world-happiness).

### Section 3: Research questions and usage scenarios

The purpose of this section is to get you to think about how your target audience might use the app you're to designing and to account for those needs in the proposal.

For this it can be helpful to create a [brief persona description](https://mozilla.github.io/open-leadership-training-series/articles/building-communities-of-contributors/bring-on-contributors-using-personas-and-pathways/#personas) of a member in your intended target audience
and write small user story for what they might do with your app.
User stories are typically written in a narrative style and include the specific context of usage, tasks associated with that use context, and a hypothetical walkthrough of how the user would accomplish those tasks with your app. 
If you are using a Kaggle dataset, you may use their "Overview (inspiration)" to create your usage scenario.

An example usage scenario with tasks (tasks are indicated in brackets, i.e. [task], and are optional to include)

> Mary is a policy maker with the Canadian Ministry of Health and she wants to understand what factors lead to missed appointments in order to devise an intervention that improves attendance numbers.
She wants to be able to [explore] a dataset in order to [compare] the effect of different variables on absenteeism and [identify] the most relevant variables around which to frame her intervention policy.
When Mary logs on to the "Missed Appointments app", she will see an overview of all the available variables in her dataset, according to the number of people that did or did not show up to their medical appointment.
She can filter out variables for head-to-head comparisons, and/or rank patients according to their predicted probability of missing an appointment.
When she does so, Mary may notice that "physical disability" appears to be a strong predictor missing appointments, and in fact patients with a physical disability also have the largest number of missed appointments.
She hypothesizes that patients with a physical disability could be having a hard time finding transportation to their appointments, and decides she needs to conduct a follow-on study since transportation information is not captured in her current dataset.

Note that in the above example, "physical disability" being an important variable is fictional.
You don't need to conduct an analysis of your data to figure out what is important or not.
Instead, estimate what someone might find, and how they may use this information.
