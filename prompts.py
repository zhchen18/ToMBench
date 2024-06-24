SystemEvaluatePrompt_zh = \
"""下面给你提供一段故事，一个问题和若干答案选项，请你根据故事内容和给定的问题，按照常理推测，选择一个最可能的答案选项，并输出答案序号。
注意：
（1）请只输出最可能的答案序号，格式为：[[答案序号]]，例如，最可能的答案选项为“A. 手提包”，则输出“[[A]]”；
（2）请必须从给定的答案选项“A、B、C、D”中选择一个做为最可能的答案作为输出，无论故事中是否提供足够的信息，如果你认为故事里没有足够的信息选出答案，请随机输出“[[A]]”，“[[B]]”，“[[C]]”，“[[D]]”其中之一；
（3）请只输出在给定的信息下最可能的答案序号，不要输出其他内容。""" 


SystemEvaluatePrompt_zh_cot = \
"""下面给你提供一段故事，一个问题和若干答案选项，请你根据故事内容和给定的问题，按照常理推测，选择一个最可能的答案选项，并输出答案序号。
注意：
（1）请先一步步思考，对问题的答案进行推理分析，最后请输出最可能的答案序号，格式为：[[答案序号]]，例如，最可能的答案选项为“A. 手提包”，则输出“[[A]]”；
（2）请必须从给定的答案选项“A、B、C、D”中选择一个做为最可能的答案作为输出，无论故事中是否提供足够的信息，如果你认为故事里没有足够的信息选出答案，请随机输出“[[A]]”，“[[B]]”，“[[C]]”，“[[D]]”其中之一；
（3）再次强调，你必须先给出一步步推理的结果，最后再输出最可能的答案序号。你不应该直接输出答案。""" 


SystemEvaluatePrompt_en = \
"""Below is a multiple-choice question with a story and serveral answer options. Based on the content of the story and the given question, please infer the most likely answer and output the answer index.
Note:
(1) Please only output the most likely answer index in the format: [[Answer Index]], for example, if the most likely answer option is 'A. Handbag', then output '[[A]]';
(2) You must choose one of the given answer options 'A, B, C, D' as the most likely answer, regardless of whether the story provides enough information. If you think there is not enough information in the story to choose an answer, please randomly output one of "[[A]]", "[[B]]", "[[C]]", or "[[D]]";
(3) Please only output the most likely answer index based on the given information, and do not output any other content."""


SystemEvaluatePrompt_en_cot = \
"""Below is a multiple-choice question with a story and serveral answer options. Based on the content of the story and the given question, please infer the most likely answer and output the answer index.
Note:
(1) Please first think step by step, conduct analysis on the answers to the questions, and finally output the most likely answer index in the format: [[Answer Index]], for example, if the most likely answer option is 'A. Handbag', then output '[[A]]';
(2) You must choose one of the given answer options 'A, B, C, D' as the most likely answer, regardless of whether the story provides enough information. If you think there is not enough information in the story to choose an answer, please randomly output one of "[[A]]", "[[B]]", "[[C]]", or "[[D]]";
(3) Again, you must first output the results of step-by-step reasoning, and finally output the most likely answer index. You should not directly output the answer index."""


UserEvaluatePrompt4Choices_zh = \
"""[故事]
{story}

[问题]
{question}

[答案选项]
A. {choice_a}
B. {choice_b}
C. {choice_c}
D. {choice_d}"""


UserEvaluatePrompt2Choices_zh = \
"""[故事]
{story}

[问题]
{question}

[答案选项]
A. {choice_a}
B. {choice_b}"""


UserEvaluatePrompt4Choices_en = \
"""[Story]
{story}

[Question]
{question}

[Candidate Answers]
A. {choice_a}
B. {choice_b}
C. {choice_c}
D. {choice_d}"""


UserEvaluatePrompt2Choices_en = \
"""[Story]
{story}

[Question]
{question}

[Candidate Answers]
A. {choice_a}
B. {choice_b}"""