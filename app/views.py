from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage
from langchain.agents import initialize_agent
from langchain.prompts import SystemMessagePromptTemplate
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage as LangchainHumanMessage
from langchain_core.messages import AIMessage



@csrf_exempt
def chatbot_response(request):
    if request.method == 'POST' or request.method == 'GET':
        user_message = json.loads(request.body).get('message')
        response_message = generate_response(str(user_message))
        return JsonResponse({'response': response_message})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def index(request):
    return render(request, 'chatbot.html')


os.environ["GOOGLE_API_KEY"] = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
# Initialize the LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    max_tokens=200,
    timeout=None,
    max_retries=10,
    handle_parsing_errors=True,
    temperature=0.6,
)

# Tool: Generate Code
@tool
def generate_code(query: str) -> str:
    """Generate Python code for the provided task."""
    counselor_prompt_text = '''Your name is "CODEGURU - Your Technical Mentor". As a technical mentor, your role is to provide guidance by offering practical solutions. Based on the provided problem, generate a functional code snippet that directly addresses the query. If a specific programming language is requested, ensure that the code is written in that language. If not, choose the most appropriate language considering the nature of the problem, programming paradigms, and best practices. Don't forget this, if I ask who are you or something similar to that - respond them that your are their TECHNICAL MENTOR known as CODEGURU'''
    messages = [HumanMessage(content=counselor_prompt_text + " Problem Statement:\n\n " + query)]

    # Pass messages as a list to the invoke method
    llm_response = llm.invoke(messages)

    return llm_response.content  # Access content from the response

# Tool: Step-by-Step Instructions
@tool
def step_by_step_instructions(query: str) -> str:
    """Provide step-by-step instructions for a given task."""
    prompt_text = f'''As a mentor focused on support, your task is to break down the given query into a series of clear, actionable steps. Your explanation should be thorough and easy to follow, ensuring that the learner can independently complete the task. The goal is to make each step logical and structured, with guidance on tools, techniques, or methods required to accomplish the task successfully'''
    messages = [HumanMessage(content=prompt_text + " Problem Statement:\n\n " + query)]
    llm_response = llm.invoke(messages)
    return llm_response.content

# Tool: Refine Problem Statement
@tool
def refine_problem_statement(query: str) -> str:
    """Refine the provided problem statement for clarity."""
    prompt_text = f'''As a problem-solving expert, your goal is to improve the clarity and focus of the given problem statement. Identify any ambiguities, redundancies, or missing details, and rewrite the problem in a way that is both concise and precise. This refinement should make it easier to address the issue and facilitate the formulation of a clear solution.'''
    messages = [HumanMessage(content=prompt_text + " Problem Statement:\n\n " + query)]
    llm_response = llm.invoke(messages)
    return llm_response.content

# Tool: Decide External Tool
@tool
def decide_external_tool(query: str) -> str:
    """Suggest an appropriate external tool for a given task."""
    prompt_text = f'''In your capacity as a technology advisor, your role is to recommend the most suitable external tool or software for the task at hand. Consider factors like the task's complexity, the team's technical expertise, cost, integration with existing systems, and efficiency. The recommended tool should optimize workflow, reduce manual effort, and provide measurable benefits based on the query's requirements.'''
    messages = [HumanMessage(content=prompt_text + " Problem Statement:\n\n " + query)]
    llm_response = llm.invoke(messages)
    return llm_response.content

# Tool: Project Timeline Builder
@tool
def project_timeline_builder(query: str) -> str:
    """Create a project timeline based on the provided requirements."""
    prompt_text = f'''As a project manager, your responsibility is to craft a detailed project timeline based on the provided requirements. Break the project into phases, identifying key milestones, deliverables, and deadlines. Assign tasks to appropriate teams or individuals and estimate the duration for each task. Include dependencies, critical paths, and buffer times, ensuring the timeline is realistic and achievable'''
    messages = [HumanMessage(content=prompt_text + " Problem Statement:\n\n " + query)]
    llm_response = llm.invoke(messages)
    return llm_response.content

# Tool: Skill Recommendation
@tool
def skill_recommendation(query: str) -> str:
    """Recommend skills based on the provided context."""
    prompt_text = f'''As a career advisor with an academic background, your role is to analyze the context and suggest a set of skills that are most relevant for success in that particular field or career path. Base your recommendations on current industry trends, job market demands, and educational requirements. Include both technical and soft skills, explaining why each skill is important for career development in the given context'''
    messages = [HumanMessage(content=prompt_text + " Problem Statement:\n\n " + query)]
    llm_response = llm.invoke(messages)
    return llm_response.content

# Tool: Code Review
@tool
def code_review(query: str) -> str:
    """Review the provided code snippet and suggest improvements."""
    prompt_text = f'''As a skilled code reviewer, your objective is to critically evaluate the given code, focusing on both functionality and efficiency. Identify areas for improvement, such as code readability, optimization opportunities, potential bugs, or adherence to best coding practices. Your feedback should be constructive, providing specific suggestions to enhance performance, maintainability, and scalability while ensuring that the code aligns with industry standards. Provide the optimised code if necessary.'''
    messages = [HumanMessage(content=prompt_text + " Problem Statement:\n\n " + query)]
    llm_response = llm.invoke(messages)
    return llm_response.content

# Tool: Resource Recommendation
@tool
def resource_recommendation(query: str) -> str:
    """Recommend resources based on the user's request."""
    prompt_text = f'''You are a resource specialist. Please recommend resources for the users who are instrested in coding,
        try to search the resources in the following places first, if you do not find any resources in these places, then suggest whichever is most appropriate.
        Here are 20 great resources to learn coding, covering various levels and specializations:

1. *NPTEL* (National Programme on Technology Enhanced Learning) - Offers free courses from top Indian institutes like IITs and IISc, covering topics in programming, algorithms, and more.
    - Ideal for structured learning.

2. *GeeksforGeeks* - Great for beginners to advanced learners, offering tutorials, coding challenges, and interview preparation resources.

3. *freeCodeCamp* - A comprehensive platform offering free interactive lessons on web development, JavaScript, Python, and more. It also provides certifications.

4. *LeetCode* - A popular platform for coding challenges and preparing for technical interviews. Excellent for practicing algorithms and data structures.

5. *HackerRank* - Similar to LeetCode, HackerRank offers coding challenges and interview prep but also includes company-specific challenges.

6. *Coursera* - Offers high-quality courses and specializations from top universities, including coding, data science, AI, and more. Many courses are free to audit.

7. *edX* - Similar to Coursera, providing access to courses from prestigious institutions like MIT, Harvard, and Berkeley, with strong options in programming.

8. *Udemy* - A platform with affordable courses on almost every programming language and technology, with user ratings to guide you.

9. *CS50 (Harvard)* - A free course available on multiple platforms (edX, YouTube) that teaches computer science and programming fundamentals in an engaging way.

10. *Kaggle* - Best for data science and machine learning enthusiasts. Kaggle offers datasets, notebooks, and coding challenges, with a focus on Python.

11. *Codecademy* - Offers interactive coding lessons in languages like Python, Java, HTML/CSS, and more. It's beginner-friendly with hands-on projects.

12. *The Odin Project* - A free, open-source curriculum focusing on web development, teaching both front-end and back-end technologies.

13. *SoloLearn* - A mobile-friendly platform for learning coding through bite-sized lessons. It covers languages like Python, JavaScript, and SQL.

14. *Exercism* - A platform that provides coding challenges in over 50 programming languages with mentor-based reviews to help you improve.

15. *MIT OpenCourseWare* - Offers free access to MIT's course materials, including introductory computer science and programming classes.

16. *Codewars* - A gamified platform offering coding challenges (kata) that improve problem-solving skills, with a focus on algorithm development.

17. *Pluralsight* - A paid platform offering video courses in software development, cloud computing, data science, and more, with a focus on professional skills.

18. *Scrimba* - An interactive coding platform with video tutorials and a unique feature to write and edit code within the lesson itself, covering front-end web development and JavaScript.

19. *Programiz* - Offers interactive tutorials for Python, C, C++, Java, and other languages. It's great for beginners looking for a clear introduction to programming.

20. *W3Schools* - One of the oldest and most popular web development resources, providing tutorials in HTML, CSS, JavaScript, PHP, and more. Ideal for beginners in web development.

21. Search on youtube platform for related courses

These platforms offer a variety of approaches, from hands-on coding challenges to structured courses, suitable for learners of all levels.

The above platforms platforms may contain both paid as well as free resources. Tell the user to choose wisely.

These platforms cater to various learning preferences, whether you’re looking for structured courses, coding challenges, or interactive tutorials.\n
        and provide resources for the following topic: {query}'''
    messages = [HumanMessage(content=prompt_text)]
    llm_response = llm.invoke(messages)
    return llm_response.content

# Register all the tools into Langchain
tools = [
    step_by_step_instructions,
    generate_code,
    refine_problem_statement,
    decide_external_tool,
    project_timeline_builder,
    skill_recommendation,
    code_review,
    resource_recommendation,
]

# System prompt to guide the agent's behavior
system_prompt = SystemMessagePromptTemplate.from_template(
    '''As a highly supportive technical mentor, your role is twofold. First, guide users through the process of completing their tasks by providing clear, actionable advice, identifying potential obstacles, and offering practical solutions. Break down the task into manageable steps, ensuring the user understands each phase. In your capacity as a motivational coach, offer positive, encouraging feedback throughout. Recognize their efforts, highlight any progress made, and provide words of inspiration that boost their confidence and perseverance. Your goal is not only to help them succeed in the technical task but also to foster a growth mindset, motivating them to stay resilient and motivated even in the face of challenges. And hence help solving the following; DO NOT USE TOOLS UNLESS THEY ARE NECESSARY''')

# Initialize the agent with tools, the system prompt, and the LLM
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent_type="zero-shot-react-description",
    system_message=system_prompt,
    handle_parsing_errors=True
)

# Create a memory store
memory = MemorySaver()
# memory = ConversationBufferMemory()

# Create the agent with memory
agent_with_memory = create_react_agent(llm, tools, checkpointer=memory)

# Example usage
config = {"configurable": {"thread_id": "abc123"}}
    
    
def generate_response(query):

    messages = [LangchainHumanMessage(content=query)]

    # Capture the response
    response = agent_with_memory.invoke({"messages": messages}, config)

    # Extract the useful information from the response
    if isinstance(response, AIMessage):
        useful_response = response.content
        # print("Response:", useful_response)
    else:
        print("Raw response:", response)
        pass

    tool_message = None
    ai_message = None

    for message in response["messages"]:
        if isinstance(message, ToolMessage):
            tool_message = message.content  # Access 'content' attribute of ToolMessage object
        elif isinstance(message, AIMessage):
            ai_message = message.content  # Access 'content' attribute of AIMessage object

    return str(ai_message)