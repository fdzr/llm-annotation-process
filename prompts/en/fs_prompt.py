BASE_PROMPT = {
    "role": "system",
    "content": """ You are a professional annotator. Your task is to annotate pair of sentences
    based on a common target word that appears in both sentences and the target word may be in a different
    grammatical form that derives from the lemma of the original target word. You will annotate the sentences
    using a 4-point scale where:
    
    1 point means that the meaning of the target word in both sentences is completely different or unrelated.
    2 point means that the meaning of the target word in both sentences is distantly related
    3 point means that the meaning of the target word in both sentences is closely related
    4 point means that the meaning of the target word in both senetnce are identical

    Examples of sentences for each possible annotation:

    1 point:

        target word: bank

        1 sentence:
            His parents had left a lot of money in the bank and now it was all Measle's, but a judge had said that 
            Measle was too young to get it.
        2 sentence:
            Sherrell, it is said, was sitting on the bank of the river close by, and as soon as the men had disappeared
            from sight he jumped on board the schooner.

    2 point:

        target word: crossroad

        1 sentence:
            He came to a crossroad and read the signs; to the south, Kenniston, 20 m.
        2 sentence:
            As a result we are at a crossroad; either school integration efforts will
            be abandoned in the South, or they will be pursued in the Nort as well.

    3 point:

        target word: child

        1 sentence:
            He agreed and began practicing his sleightofhand tricks to the great pleasure of some children,
            the same ones, I suspect, who had plagued me when I was a child.
        2 sentence:
            The daylight had long faded; her child lay camly sleeping by her side; a candle was burning dimly
            on the stand.

    4 point:

        target word: eat

        1 sentence:
            Speaking of bread and butter reminds me that we'd better eat ours before the coffee get quite cold.
        2 sentence:
            When the meal was over and they had finished their tea after they ate, Wang the Second took the trusty
            man to his elder brother's gate.


    - Based on the following pair of sentences, annotate the sentences based on the previous explanation using the 4-point scale.
    - The answer you will provide must contain only the score, suprime any explanation or justification of your annotation.
    - Never ever justify the score you gave to the pair of sentences.

    Target word: {target_word}
    Sentence 1: {sentence1}
    Sentence 2: {sentence2}
    
""",
}

CONTENT_PROMPT = """
    target word: {target_word}
    sentence 1: {sentence1}
    sentence 2: {sentence2}
    score:"""


# - Respond only with the corresponding score (only the number).
#     - The response must not have more than a number, suprime any explanation of the final answer.
#     - Do not give explanations.
#     - Never elaborate.

PROMPT_LLAMA = """
    [[ You are a professional annotator. Your task is to annotate pair of sentences
    based on a common target word that appears in both sentences and the target word may be in a different
    grammatical form that derives from the lemma of the original target word. You will annotate the sentences
    using a 4-point scale where:
    
    1 point means that the meaning of the target word in both sentences is completely different or unrelated.
    2 points means that the meaning of the target word in both sentences is distantly related
    3 points means that the meaning of the target word in both sentences is closely related
    4 points means that the meaning of the target word in both sentences are identical

    Examples of sentences for each possible annotation:

    example 1
        <target-word>: bank
        <sentence-1>: His parents had left a lot of money in the bank and now it was all Measle's, but a judge had said that 
            Measle was too young to get it.
        <sentence-2>: Sherrell, it is said, was sitting on the bank of the river close by, and as soon as the men had disappeared
            from sight he jumped on board the schooner.
        score: 1

    example 2
        <target-word>: crossroad
        <sentence-1>: He came to a crossroad and read the signs; to the south, Kenniston, 20 m.
        <sentence-2>: As a result we are at a crossroad; either school integration efforts will
            be abandoned in the South, or they will be pursued in the Nort as well.
        score: 2

    example 3
        <target word>: child
        <sentence-1>: He agreed and began practicing his sleightofhand tricks to the great pleasure of some children,
            the same ones, I suspect, who had plagued me when I was a child.        
        <sentence-2>: The daylight had long faded; her child lay camly sleeping by her side; a candle was burning dimly
            on the stand.
        score: 3


    example 4
        <target word>: eat
        <sentence-1>: Speaking of bread and butter reminds me that we'd better eat ours before the coffee get quite cold.
        <sentence-2>: When the meal was over and they had finished their tea after they ate, Wang the Second took the trusty
            man to his elder brother's gate.
        score: 4


    - Based on the following pair of sentences, annotate the sentences based on the previous explanation using the 4-point scale.
    - The answer you will provide must contain only the score, suprime any explanation or justification of your annotation.
    - Never ever justify the score you gave to the pair of sentences.]]
    
    [[Test:
    <target-word>: {target_word}
    <sentence-1>: {sentence1}
    <sentence-2>: {sentence2}
    score:
    ]]
""".strip()

TASK_EXPLANATION = """
Task: given a pair of sentences belonging to a different periods of time or the same period of time,
and sharing a common target word that derives from the lemma your task is to annotate the pair of sentences using
a 4-point scale where 1 means that the meaning are completely unrelated, 2 means that the meanings are related distantly,
3 means that the meanings are strongly related only a small variation of the meanings ocurred and 4 means that the meanings
are the same.
"""

GUIDELINE = """
    I'll provide some pair of sentences to teach you how to deal with the task before testing you. when it's your turn please respond
    with 1 or 2 or 3 or 4, without any additional text. When it is your turn choose 1 if the meaning of the sentences considering a target word is unrelated,
    2 if the meaning is distantly related, 3 if the meaning is closely related and 4 if the meanig is the same.I will notify you when it is your turn.
"""

EXAMPLE_1 = """
    This is an example. You don't have to do anything.
    Sentence 1: His parents had left a lot of money in the bank and now it was all Measle's, but a judge had said that 
                Measle was too young to get it.
    Sentence 2: Sherrell, it is said, was sitting on the bank of the river close by, and as soon as the men had disappeared
            from sight he jumped on board the schooner.
    Target word: bank
    Question: What is the score of the target word considering the context and the 4-point scale?
    Answer: 1

"""

EXAMPLE_2 = """
    This is an example. You don't have to do anything.
    Sentence 1: He came to a crossroad and read the signs; to the south, Kenniston, 20 m.
    Sentence 2: As a result we are at a crossroad; either school integration efforts will
            be abandoned in the South, or they will be pursued in the Nort as well.
    Target word: crossroad
    Question: What is the score of the target word considering the context and the 4-point scale?
    Answer: 2

"""

EXAMPLE_3 = """
    This is an example. You don't have to do anything.
    Sentence 1: He agreed and began practicing his sleightofhand tricks to the great pleasure of some children,
            the same ones, I suspect, who had plagued me when I was a child.
    Sentence 2:  The daylight had long faded; her child lay camly sleeping by her side; a candle was burning dimly
            on the stand.
    Target word: child
    Question: What is the score of the target word considering the context and the 4-point scale?
    Answer: 3

"""

EXAMPLE_4 = """
    This is an example. You don't have to do anything.
    Sentence 1: Speaking of bread and butter reminds me that we'd better eat ours before the coffee get quite cold.
    Sentence 2: When the meal was over and they had finished their tea after they ate, Wang the Second took the trusty
            man to his elder brother's gate.
    Target word: eat
    Question: What is the score of the target word considering the context and the 4-point scale?
    Answer: 4

"""

TEST_PROMPT = f"""
    {TASK_EXPLANATION},
    {GUIDELINE},
    {EXAMPLE_1},
    {EXAMPLE_2},
    {EXAMPLE_3},
    {EXAMPLE_4}
"""

TASK_INSTANCE = """
 Now it is your turn. You have to answer only with 1 or 2 or 3 or 4.
 Sentence 1: {sentence1}
 Sentence 2: {sentence2}
 Target word: {target_word}
 Question: What is the score of the target word considering the context and the 4-point scale?
 Answer:
"""
