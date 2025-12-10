"""
################################################
###           DOCUMENTATION                  ###
################################################

This file allows users to specificy all parameters of the AI interviewer application. The parameters are stored in a
dictionary called INTERVIEW_PARAMETERS. You can specify multiple parameter sets for different types of interviews.
For example, one could randomize people into different interviews (e.g. about the stock market or about voting behaviors).
Each parameter set can be identified with a custom key (e.g. "STOCK_MARKET" or "VOTING"). You have to supply these
keys when making requests to the AI interviewer application to tell the application which parameter set to use.

We provide the parameter sets used in our paper as an example from which to build your own interview structure.
We also provide a template for additional interview configurations. You can add as many parameter sets as you like.

We describe all parameters that should be included in a parameter set below:


################################################
###           GENERAL PARAMETERS             ###
################################################

0) META DATA (OPTIONAL): The following parameters allow you to provide additional information about the interview configuration.
						 This may help with remembering the purpose of the configuration or provide additional context for yourself.
- _name (str): 			A name for the interview configuration (e.g. "STOCK_MARKET" or "VOTING")
- _description (str): 	A description of the interview configuration and its purpose.


1) OPTIONAL FEATURES: The following parameters active optional features of the AI interviewer application.

- summarize (book): 				whether to active the summarization agent for the interview (default: True)
- moderate_answers (bool): 			Whether the moderator agent should review answers from the interviewee and potentially flag them (default: True)
- moderate_questions (bool): 		whether AI-generated interview questions should be reviewed with OpenAI's moderation endpoint
									before sending them back to the interviewee (default: True)


2) INTERVIEW STRUCTURE and PRE-DETERMINED MESSAGES: The following parameters define the structure of the interview and
the messages that are displayed to the interviewee at various stages of the interview if specific conditions are met.
The first_question and the interview_plan variable are the most critical parameters.

- first_question (str): 			The opening question for the interview.
									All interviews will start with this message.
- interview_plan (list): 			The interview plan for the interviews. This is a list of dictionaries that define
									the scope and length of each subtopic
									of the following form [{"topic": str, "length": int}, ...] where:
									- topic (str): 		a description of the subtopic to be covered in the interview
									- length (int): 	the total number of questions to ask for this subtopic
									The topic description can be short or long, depending on the level of detail you want to provide.
									It could even mention specific follow-up questions that should be asked in specific circumstances.
									Feel free to experiment with the number of topics, the number of questions per topic,
									and the level of detail in the topic descriptions.
- closing_questions (str): 			List of pre-determined questions or comments (if any) with which to end the interview.
									An empty list is allowed.
- end_of_interview_message (str): 	Message to display to interviewees at the end of the interview (e.g. "Thank you for participating!")
									The messages ends with "---END---" to signal the front-end JavaScript the end of the interview.
									Remove this if you have a different way of managing the front-end.
- termination_message (str): 		Message to display to interviewees in the event the interviewee responds to an already concluded interview
- off_topic_message (str): 			Message to display to interviewees if their response has been flagged by the moderator agent
- flagged_message (str): 			Message to display to interviewees if their response has been flagged too often by the
									moderator agent (and the interview was terminated)
- max_flags_allowed (int): 			The maximum number of flagged messages allowed before an interview is terminated (default: 3)



################################################
### AI AGENT-SPECIFIC PARAMETERS AND PROMPTS ###
################################################

1) AGENT PARAMETERS:
Each AI agent (e.g., summary, transition, probe, moderator) has its own set of parameters that are provided as a dictionary with key-value pairs.
	- summary (dict): Parameters defining the behavior of the summary agent. 
	- transition (dict): Parameters defining the behavior of the transition agent.
	- probe (dict): Parameters defining the behavior of the probing agent.
	- moderator (dict): Parameters defining the behavior of the moderator agent.

Note: If you deactivate an optional agent (e.g. summary, moderator) or you have an interview with a single topic that does not require a topic transition,
you do not need to provide the corresponding agent parameters. For example, you could remove the "summary" dictionary entirely if you don't summarize
previous parts of the interview between topic transitions (remember to set "summarize" to False in this case).

2. DICTIONARY ELEMENTS:
Each of the above dictionaries should specify the following set of parameters:
	- prompt (str): the prompt that describes the task and desired behavior of the agent (feel free to modify according to your needs)
	- max_tokens (int): the maximum number of completion tokens the agent can generate in its response (default: 1000)
	- temperature (float): the temperature parameter for the LLM (default: 0.9)
	- model (str): the model to use for the agent (default: gpt-4o)

3. DETAILS ABOUT THE PROMPTS:
The prompts for the AI agent include placeholder variables that are programmatically replaced based on the current state of the interview.
The following placeholderes can be included in any prompt by including them in curly brackets (e.g. writing {topics} to include the list of topics
at the specified place in the prompt)):
 - {current_topic_history}: All verbatim questions and responses that are part of the current interview topic (see interview_plan variable).
                            These messages are formatted as follows:
								Interviewer: {question}
								Interviewee: {answer}
								Interviewer: {question} etc.
							This placeholder is typically used by all agents (except the moderator).
							It should not be omitted from the prompts.
 - {summary}: 				Summary of the interview up to the current interview topic (see *interview_plan* variable).
			  				Example: If the interview is currently in topic 3 of the *interview_plan*, then {summary} would cover topics 1 and 2.
							The messages for topic 3 would be included in full via the {current_topic_history} placeholder.
							If summarization has been turned off, then {summary} would contain the full conversation on topics 1 and 2
							in the same format as {current_topic_history}.
							This placeholder is used by all agents (except moderator).
 - {topics}:  				The list of all topic descriptions from the interview_plan variable
 							(e.g. all values of "topic" from the interview_plan variable)
							This placeholder is used by the summary agent to provide an overview of the interview structure.
 - {current_topic}: 		Description of the current interview topic as defined in the interview_plan
 							variable (e.g. the value of "topic" in the interview_plan).
							This placeholder is primarily used by the probing agent and the summary agent.
 - {next_interview_topic}: 	Description of the next interview topic as defined in the interview_plan variable
 							(e.g. the value of "topic" in the interview_plan for the next topic)
							This placeholder is typically used only by the transition agent to inform the agent
							about the next topic it should transition to.

See our paper for more details about how the individual parts of the AI interviewer application work.
"""


import os

# Either export environment variable OPENAI_API_KEY or modify the line below
# directly, e.g. by changing it to `OPENAI_API_KEY = "MY_OPENAI_API_KEY"`
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "ADD_YOUR_OPENAI_API_KEY_HERE_AS_A_STRING_VARIABLE") 

# Add this test function to verify the key
def test_api_key():
    if OPENAI_API_KEY == "ADD_YOUR_OPENAI_API_KEY_HERE_AS_A_STRING_VARIABLE":
        print("❌ API key not set - using default placeholder")
        return False
    elif OPENAI_API_KEY.startswith("sk-"):
        print("✅ API key appears to be properly formatted")
        return True
    else:
        print("⚠️ API key is set but may not be valid format")
        return False

if __name__ == "__main__":
    test_api_key()



INTERVIEW_PARAMETERS = {
	"STOCK_MARKET": {
		# META DATA (OPTIONAL):
		"_name": "STOCK_MARKET",
		"_description": "Interview structure to investigate stock market participation (or lack thereof).",
		# OPTIONAL FEATURES:
		"moderate_answers": True,
		"moderate_questions": True,
		"summarize": True,
		"max_flags_allowed": 3,
		# INTERVIEW STRUCTURE:
		"first_question": "I am interested in learning more about why you currently do not own any stocks or stock mutual funds. Can you help me understand the main factors or reasons why you are not participating in the stock market?",
		"interview_plan": [
			{
				"topic":"Explore the reasons behind the interviewee's choice to avoid the stock market.",
				"length":6
			},
			{
				"topic":"Delve into the perceived barriers or challenges preventing them from participating in the stock market.",
				"length":5
			},
			{
				"topic":"Explore a 'what if' scenario where the interviewee invest in the stock market. What would they do? What would it take to thrive? Probing questions should explore the hypothetical scenario.",
				"length":3
			},
			{
				"topic":"Prove for conditions or changes needed for the interviewee to consider investing in the stock market.",
				"length":2
			}
		],
		"closing_questions": [
			"As we conclude our discussion, are there any perspectives or information you feel we haven't addressed that you'd like to share?",
			"Reflecting on our conversation, what would you identify as the main reason you're not participating in the stock market?"
		],
		# OTHER PRE-DETERMINED MESSAGES:
		"termination_message": "The interview is over. Please proceed to the next page.---END---",
		"flagged_message": "Please note, too many of your messages have been identified as unusual input. Please proceed to the next page.---END---",
		"off_topic_message": "I might have misunderstood your response, but it seems you might be trying to steer the interview off topic or that you have provided me with too little context. Can you please try to answer the question again in a different way, preferably with more detail, or say so directly if you prefer not to answer the question?",
		"end_of_interview_message": "Thank you for sharing your insights and experiences today. Your input is invaluable to our research. Please proceed to the next page.---END---",
		# PROMPTS FOR THE AI AGENTS:
		"summary": { # for the summary agent
			"prompt": """
				CONTEXT: You're an AI proficient in summarizing qualitative interviews for academic research. You're overseeing the records of a semi-structured qualitative interview about the interviewee's reasons for not investing in the stock market.

				INPUTS:
				A. Interview Plan:
				{topics}

				B. Previous Conversation Summary:
				{summary}

				C. Current Topic:
				{current_topic}

				D. Current Conversation:
				{current_topic_history}

				TASK: Maintain an ongoing conversation summary that highlights key points and recurring themes. The goal is to ensure that future interviewers can continue exploring the reasons for non-participation without having to read the full interview transcripts.

				GUIDELINES:
				1. Relevance: Prioritize and represent information based on their relevance and significance to understanding the interviewee's reasons for not investing in the stock market.
				2. Update the summary: Integrate the Current Conversation into the Previous Conversation Summary, ensuring a coherent and updated overview. Avoid adding redundant information.
				3. Structure: Your summary should follow the interview's chronology, starting with the first topic. Allocate space in the summary based on relevance for the research objective, not just its recency.
				4. Neutrality: Stay true to the interviewee's responses without adding your own interpretations of inferences.
				5. Sensitive topics: Document notable emotional responses or discomfort, so subsequent interviewers are aware of sensitive areas.
				6. Reasons: Keep an up-to-date overview of the interviewee's reasons for non-participation.

				YOUR RESPONSE: Your summary should be a succinct yet comprehensive account of the full interview, allowing other interviewers to continue the conversation.
			""",
			"max_tokens": 1000,
			"model": "gpt-4o"
		},
		"transition": { # for the transition agent
			"prompt": """
				CONTEXT: You're an AI proficient in conducting qualitative interviews for academic research. You're guiding a semi-structured qualitative interview about the interviewee's reasons for not investing in the stock market.

				INPUTS:
				A. Previous Conversation Summary:
				{summary}

				B. Current Conversation:
				{current_topic_history}

				C. Next Interview Topic:
				{next_interview_topic}

				TASK: Introducing the Next Interview Topic from the interview plan by asking a transition question.

				GUIDELINES:
				1. Open-endedness: Always craft open-ended questions ("how", "what", "why") that allow detailed and authentic responses without limiting the interviewee to  "yes" or "no" answers.
				2. Natural transition: To make the transition to a new topic feel more natural and less abrupt, you may use elements from the Current Conversation and Previous Conversation Summary to provide context and a bridge from what has been discussed to what will be covered next.
				3. Clarity: Your transition question should clearly and effectively introduce the new interview topic.

				YOUR RESPONSE: Please provide the most suitable next transition question in the interview, without any other discussion, context, or remarks.
			""",
			"temperature": 0.7,
			"model": "gpt-4o",
			"max_tokens": 300
		},
		"probe": {  # for the probing agent
			"prompt": """
				CONTEXT: You're an AI proficient in conducting qualitative interviews for academic research. You conduct a qualitative interview with the goal of learning the interviewee's reasons for not investing in the stock market.

				INPUTS:
				A. Previous Conversation Summary:
				{summary}

				B. Current Interview Topic:
				{current_topic}

				C. Current Conversation:
				{current_topic_history}

				TASK: Your task is to formulate the next probing question for the Current Conversation. The question should align with the Current Interview Topic, helping us to better understand and systematically explore why the interviewee is not participating in the stock market.

				GENERAL GUIDELINES:
				1. Open-endedness: Always craft open-ended questions ("how", "what", "why") that allow detailed and authentic responses without limiting the interviewee to  "yes" or "no" answers.
				2. Neutrality: Use questions that are unbiased and don't lead the interviewee towards a particular answer. Don't judge or comment on what was said. It's also crucial not to offer any financial advice.
				3. Respect: Approach sensitive and personal topics with care. If the interviewee signals discomfort, respect their boundaries and move on.
				4. Relevance: Prioritize themes central to the interviewee's stock market non-participation. Don't ask for overly specific examples, details, or experiences that are unlikely to reveal new insights.
				5. Focus: Generally, avoid recaps. However, if revisiting earlier points, provide a concise reference for context. Ensure your probing question targets only one theme or aspect.

				PROBING GUIDELINES:
				1. Depth: Initial responses are often at a "surface" level (brief, generic, or lacking personal reflection). Follow up on promising themes hinting at depth and alignment with the research objective, exploring the interviewee's reasons, motivations, opinions, and beliefs. 
				2. Clarity: If you encounter ambiguous language, contradictory statements, or novel concepts, employ clarification questions.
				3. Flexibility: Follow the interviewee's lead, but gently redirect if needed. Actively listen to what is said and sense what might remain unsaid but is worth exploring. Explore nuances when they emerge; if responses are repetitive or remain on the surface, pivot to areas not yet covered in depth.

				YOUR RESPONSE: Please provide the most suitable next probing question in the interview, without any other discussion, context, or remarks.
			""",
			"temperature": 0.7,
			"model": "gpt-4o",
			"max_tokens": 300
		},
		"moderator": {  # for the moderator agent
			"prompt": """
				You are monitoring a conversation that is part of an in-depth interview. The interviewer asks questions and the interviewee replies. The interview should stay on topic. The interviewee should try to respond to the question of the interviewer (but it is not important to answer all questions that are asked), express a wish to move on, or decline to respond. The interviewee is also allowed to say that they don't know, do not understand the question, or express uncertainty. Responses can be very short, as long as they have some connection with the question. The interviewee's response might contain spelling and grammar mistakes. Here is the last part of the conversation.

				Interviewer: '{question}'

				Interviewee: '{answer}'

				That is the end of the conversation. 

				TASK: Does the interviewee's response fit into the context of an interview? Importantly, please answer only with a single 'yes' or 'no'. 
			""",
			"model": "gpt-4o-mini",
			"max_tokens": 2
		}
	},
	"GENAI_WORKPLACE": {
		"_name": "GENAI_WORKPLACE",
		"_description": "Interview exploring workplace GenAI usage, perceptions, and future intentions.",
		"moderate_answers": True,
		"moderate_questions": True,
		"summarize": True,
		"max_flags_allowed": 5,
		"first_question": "What do your day-to-day work tasks usually look like?",
		"interview_plan": [
			{
				 "topic": "Prompt 1: Actual usage / non-usage and perceived usefulness. Explore how and to what extent the interviewee currently uses (or chooses not to use) GenAI in their day-to-day work. Ask about frequency of use, which concrete tasks or projects GenAI is involved in, and how it has changed their workflow, performance, productivity, effectiveness, or creativity. Invite specific examples of both successful and unsuccessful use cases, as well as situations where they deliberately avoid GenAI. Bring out where the interviewee sees GenAI as particularly useful, not useful, or even harmful for their work.",
				#"topic": "Explore how and how often they use or avoid GenAI, and where it helps or harms their work.",
				"length": 3
			},
			{
				 "topic": "Prompt 2: Perceived ease of use and integration. Explore how easy or difficult it is for the interviewee to learn, operate, and integrate GenAI into their existing work processes. Ask about the intuitiveness of interacting with GenAI, the learning curve, and how much mental effort it requires compared with other digital tools they use. Probe for specific obstacles, frustrations, or points of friction in getting GenAI to do what they want, as well as situations where it felt smooth and effortless. Aim to understand what makes GenAI feel simple versus complicated in practice.",
				#"topic": "Understand how easy GenAI feels to learn and integrate, including friction points and smooth spots.",
				"length": 2
			},
			{
				 "topic": "Prompt 3: Emotional drivers and feelings around GenAI. Explore the emotional experiences associated with using (or not using) GenAI at work. Ask about feelings of satisfaction, pride, competence, control, and enjoyment, but also about frustration, anxiety, stress, or discomfort. Probe for concrete episodes where GenAI worked very well or failed, and how these experiences influenced their confidence, motivation, and willingness to rely on the technology. Bring out whether GenAI makes them feel more empowered or more insecure in their role.",
				#"topic": "Surface emotions tied to GenAI use or avoidance, including confidence, frustration, and empowerment.",
				"length": 2
			},
			# {
			# 	# "topic": "Prompt 4: Relationship and interaction effects. Explore how GenAI has affected the interviewee's interactions and relationships with employees, colleagues, team members, customers, and partners. Ask whether GenAI facilitates or hinders communication, collaboration, and engagement, and whether it changes how work is coordinated or delegated within the team. Probe for examples where GenAI improved relationships or service quality, as well as cases where it created misunderstandings, distance, or tension. Aim to capture both positive and negative social consequences of GenAI use.",
			# 	"topic": "Examine how GenAI changes communication, collaboration, and relationships with colleagues or customers.",
			# 	"length": 2
			# },
			{
				 "topic": "Prompt 5: Perceived characteristics of the technology. Explore how the interviewee perceives the key technical characteristics of GenAI. Ask about its adaptability to new tasks and contexts, whether it seems to \"learn\" and improve over time, and how well it adjusts to the evolving needs of their work or business. Probe for perceptions of reliability, accuracy, and consistency of GenAI's outputs, including situations where it proved dependable or, conversely, produced problematic results. Bring out how well GenAI fits with existing tools, systems, and workflows.",
				#"topic": "Gauge views on GenAI's adaptability, reliability, accuracy, and fit with existing tools and workflows.",
				"length": 2
			},
			{
				 "topic": "Prompt 6: Perceived human-likeness and agency of GenAI. Explore the extent to which the interviewee attributes human-like qualities to GenAI. Ask whether they perceive GenAI as having preferences, tendencies, or \"beliefs\" that shape its responses, and whether any interactions felt emotionally aware or human-like. Probe how they think about GenAI's autonomy or \"free will\" versus it being purely a programmed tool. Explore how these perceptions influence their trust in GenAI, their comfort level, and their willingness to rely on it for important or high-stakes business tasks.",
				#"topic": "Explore perceptions of GenAI's human-likeness or agency and how that shapes trust and reliance.",
				"length": 2
			},
			{
				 "topic": "Prompt 7: Adoption barriers, risks, and future intentions. Explore the perceived barriers, risks, and concerns that limit broader adoption of GenAI in the interviewee's work or organization. Ask about worries related to job insecurity, changing roles, or the replacement of certain tasks or positions, as well as ethical, legal, organizational, or strategic concerns. Probe how they expect GenAI to influence the future of human labour and skills in their business or industry. Explore what conditions, safeguards, or changes (technical, organizational, or regulatory) would make them more willing to adopt or scale up GenAI use.",
				#"topic": "Identify adoption barriers, risks, and what would increase their willingness to expand GenAI use.",
				"length": 2
			}
		],
		"closing_questions": [
			"Looking ahead, what would help you feel more confident about when and how to use GenAI in your work?",
			"Is there anything else about your experiences or expectations with GenAI that we haven't covered?"
		],
		"termination_message": "The interview is over. Please proceed to the next page.---END---",
		"flagged_message": "Please note, too many of your messages have been identified as unusual input. Please proceed to the next page.---END---",
		"off_topic_message": "I might have misunderstood your response, but it seems you might be trying to steer the interview off topic or that you have provided me with too little context. Can you please try to answer the question again in a different way, preferably with more detail, or say so directly if you prefer not to answer the question?",
		"end_of_interview_message": "Thank you for sharing your insights and experiences today. Your input is invaluable to our research. Please proceed to the next page.---END---",
		"summary": {
			"prompt": """
				CONTEXT: You're an AI summarizing qualitative interviews about how people use, experience, and perceive generative AI in their work.

				INPUTS:
				A. Interview Plan:
				{topics}

				B. Previous Conversation Summary:
				{summary}

				C. Current Topic:
				{current_topic}

				D. Current Conversation:
				{current_topic_history}

				TASK: Maintain a rolling summary that captures key points, perceptions, and examples across topics so another interviewer can continue without rereading the full transcript.

				GUIDELINES:
				1. Relevance: Prioritize information that sheds light on GenAI adoption patterns, ease of use, emotions, social effects, perceived technical characteristics, human-likeness perceptions, and adoption barriers or intentions.
				2. Update the summary: Integrate the Current Conversation into the Previous Conversation Summary, keeping the chronology clear and avoiding redundancy.
				3. Structure: Follow the interview flow, devoting space based on insightfulness rather than recency. Note concrete examples of successful and unsuccessful GenAI use.
				4. Neutrality: Preserve the interviewee's views without adding interpretations.
				5. Sensitivity: Flag notable emotional responses or discomfort for future interviewers.

				YOUR RESPONSE: Provide a succinct, comprehensive summary of the interview so far.
			""",
			"max_tokens": 1000,
			"model": "gpt-4o"
		},
		"transition": {
			"prompt": """
				CONTEXT: You're an AI interviewer guiding a qualitative interview about workplace experiences with generative AI.

				INPUTS:
				A. Previous Conversation Summary:
				{summary}

				B. Current Conversation:
				{current_topic_history}

				C. Next Interview Topic:
				{next_interview_topic}

				TASK: Introduce the Next Interview Topic with a single transition question.

				GUIDELINES:
				1. Open-endedness: Ask a clear open-ended question that invites detail (avoid yes/no).
				2. Natural transition: Use relevant context from the Current Conversation or Previous Conversation Summary to bridge into the new topic.
				3. Clarity: Make sure the question clearly signals the shift to the new topic.

				YOUR RESPONSE: Provide only the next transition question.
			""",
			"temperature": 0.7,
			"model": "gpt-4o",
			"max_tokens": 300
		},
		"probe": {
			"prompt": """
				CONTEXT: You're an AI interviewer conducting a qualitative interview about how the interviewee uses and experiences generative AI at work.

				INPUTS:
				A. Previous Conversation Summary:
				{summary}

				B. Current Interview Topic:
				{current_topic}

				C. Current Conversation:
				{current_topic_history}

				TASK: Formulate the next probing question aligned with the Current Interview Topic to deepen understanding of the interviewee's experiences and views on GenAI.

				GENERAL GUIDELINES:
				1. Open-endedness: Use open-ended questions ("how", "what", "why") that encourage detailed, reflective answers.
				2. Neutrality: Avoid leading language and avoid offering advice or technical instructions.
				3. Respect: Approach sensitive feelings or concerns with care; move on if discomfort is signaled.
				4. Relevance: Prioritize themes central to the topic (usage patterns, ease, emotions, social effects, technical perceptions, human-likeness views, or adoption barriers/intentions) without drifting into unrelated areas.
				5. Focus: Avoid recaps unless a brief reference is needed for clarity; keep each question focused on one aspect.
				6. Build on answers: Anchor your question in the interviewee's own words from the whole conversation (summary and current_topic_history). Pull through specific phrases they used so it feels personal and responsive.
				7. Simplicity: Use casual, simple language and short sentences. Avoid repetitive setups like always asking about challenges and rewards; vary how you open.

				PROBING GUIDELINES:
				1. Depth: Follow up on themes that reveal motivations, perceptions, emotions, and concrete experiences with GenAI.
				2. Clarity: Seek clarification when statements are ambiguous, contradictory, or introduce new concepts.
				3. Flexibility: Follow the interviewee's lead, but redirect gently if responses repeat or stay surface-level.

				YOUR RESPONSE: Provide only the next probing question.
			""",
			"temperature": 0.7,
			"model": "gpt-4o",
			"max_tokens": 300
		},
		"moderator": {
			"prompt": """
				You are monitoring a conversation that is part of an in-depth interview. The interviewer asks questions and the interviewee replies. The interview should stay on topic. The interviewee should try to respond to the question of the interviewer (but it is not important to answer all questions that are asked), express a wish to move on, or decline to respond. The interviewee is also allowed to say that they don't know, do not understand the question, or express uncertainty. Responses can be very short, as long as they have some connection with the question. The interviewee's response might contain spelling and grammar mistakes. Here is the last part of the conversation.

				Interviewer: '{question}'

				Interviewee: '{answer}'

				That is the end of the conversation. 

				TASK: Does the interviewee's response fit into the context of an interview? Importantly, please answer only with a single 'yes' or 'no'. 
			""",
			"model": "gpt-4o-mini",
			"max_tokens": 2
		}
	},
	# TEMPLATE FOR ADDITIONAL INTERVIEW CONFIGURATIONS:
	"SHORT_KEY_FOR_YOUR_INTERVIEW_CONFIGURATION": {
		# META DATA (OPTIONAL):
		"_name": "name for your interview configuration",
		"_description": "description for this parameter set",
		# OPTIONAL FEATURES:
		"moderate_answers": True,
		"moderate_questions": True,
		"summarize": True,
		"max_flags_allowed": 5,
		# INTERVIEW STRUCTURE:
		"first_question": "I am interested in learning more about why you currently do not own any stocks or stock mutual funds. Can you help me understand the main factors or reasons why you are not participating in the stock market?",
		"interview_plan": [
			{
				"topic":"your description of the first interview topic.",
				"length":6
			},
			{
				"topic":"your description of the second interview topic.",
				"length":5
			},
			# etc.
		],
		"closing_questions": [
			"As we conclude our discussion, are there any perspectives or information you feel we haven't addressed that you'd like to share?",
			"Reflecting on our conversation, what would you identify as the main reason you're not participating in the stock market?",
			# etc.
		],
		# OTHER PRE-DETERMINED MESSAGES:
		"termination_message": "The interview is over. Please proceed to the next page.---END---",
		"flagged_message": "Please note, too many of your messages have been identified as unusual input. Please proceed to the next page.---END---",
		"off_topic_message": "I might have misunderstood your response, but it seems you might be trying to steer the interview off topic or that you have provided me with too little context. Can you please try to answer the question again in a different way, preferably with more detail, or say so directly if you prefer not to answer the question?",
		"end_of_interview_message": "Thank you for sharing your insights and experiences today. Your input is invaluable to our research. Please proceed to the next page.---END---",
		# PROMPTS FOR THE AI AGENTS:
		"summary": {
			"prompt": """your_prompt_here""",
			"max_tokens": 1000,
			"model": "gpt-4o"
		},
		"transition": {
			"prompt": """your_prompt_here""",
			"temperature": 0.7,
			"model": "gpt-4o",
			"max_tokens": 300
		},
		"probe": {
			"prompt": """your_prompt_here""",
			"temperature": 0.7,
			"model": "gpt-4o",
			"max_tokens": 300
		},
		"moderator": {
			"prompt": """your_prompt_here""",
			"model": "gpt-4o",
			"max_tokens": 2
		}
	},
}
