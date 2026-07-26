from llm.groq_client import ask_groq



def router_agent(question: str) -> str:
    """
    Routes user request to correct AI Agent.

    Returns:

    coding
    documentation
    rag
    testing
    architecture
    code_review

    """

    question_lower = question.lower()



    testing_keywords = [

        "unit test",
        "pytest",
        "test case",
        "testing",
        "test code",
        "generate test",
        "automation test",
        "tdd"

    ]



    architecture_keywords = [

        "architecture",
        "system design",
        "system architecture",
        "design system",
        "folder structure",
        "software architecture",
        "database design",
        "scalable system",
        "microservices"

    ]


    review_keywords = [

        "review code",
        "code review",
        "review my code",
        "improve code",
        "code quality",
        "clean code",
        "solid violation",
        "security issue",
        "performance issue"

    ]


    coding_keywords = [

        "code",
        "python",
        "java",
        "c#",
        "bug",
        "debug",
        "error",
        "exception",
        "fix",
        "algorithm",
        "optimize",
        "function",
        "class",
        "loop",
        "array",
        "string"

    ]

    documentation_keywords = [

        "readme",
        "documentation",
        "api docs",
        "api documentation",
        "comment",
        "docstring",
        "project document"

    ]


    rag_keywords = [

        "solid",
        "oop",
        "design pattern",
        "git",
        "github",
        "sql",
        "docker",
        "kubernetes",
        "rest api",
        "agile",
        "scrum",
        "refactoring",
        "dependency injection"

    ]


    upload_keywords = [

    "uploaded",

    "uploaded pdf",

    "my pdf",

    "this document",

    "this pdf",

    "uploaded document"

   ]


    for keyword in testing_keywords:

        if keyword in question_lower:

            return "testing"



    for keyword in architecture_keywords:

        if keyword in question_lower:

            return "architecture"



    for keyword in review_keywords:

        if keyword in question_lower:

            return "code_review"



    for keyword in documentation_keywords:

        if keyword in question_lower:

            return "documentation"



    for keyword in coding_keywords:

        if keyword in question_lower:

            return "coding"



    for keyword in rag_keywords:

        if keyword in question_lower:

            return "rag"

    for keyword in upload_keywords:

        if keyword in question_lower:

            return "upload_rag"





    prompt = f"""

You are an AI Router Agent.

Classify user request into ONE category.

Categories:

coding
documentation
rag
testing
architecture
code_review


Rules:

coding:
- code explanation
- debugging
- programming problems


documentation:
- README
- API documentation
- comments


testing:
- unit tests
- pytest
- test cases


architecture:
- system design
- architecture
- folder structure


code_review:
- review code
- security
- performance
- quality


rag:
- software engineering concepts
- documentation search


Return ONLY category name.


User Question:

{question}

"""


    try:

        response = ask_groq(prompt).strip().lower()


        valid_agents = [

            "coding",
            "documentation",
            "rag",
            "testing",
            "architecture",
            "code_review"

        ]


        if response in valid_agents:

            return response



    except Exception:

        pass



    return "rag"