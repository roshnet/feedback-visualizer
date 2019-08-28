# Define remark strings and logic to set remarks based on marks.

AO1_REMARKS = (
    """
    Needs to have more focus and should work upon understanding of the concepts,
    theories, scientific and technological applications. Should aim to increase
    confidence by making an effort to be more involved in class discussions.
    Need to revise more thoroughly.
    """,

    """
    Has demonstrated fair knowledge and understanding of scientific phenomena,
    facts, laws, definitions, concepts and theories.  Consistent practice will
    help improve for better performance.
    """,

    """
    Has demonstrated good knowledge and understanding of scientific phenomena,
    facts, laws, definitions, concepts and theories.  Showing great improvements.
    """,

    """
    There has been a strong knowledge and understanding of scientific phenomena,
    facts, laws, definitions, concepts and theories shown during assessments.
    Demonstrated good scientific and technological applications of the concepts
    to the problems.
    """
)


AO2_REMARKS = (
    """
    Needs to work on handling information and problem solving by doing more of
    written practice.    
    """,

    """
    Has Shown fair progress in this objective of physics. He/ she is an able
    learner who can present reasoned explanations for phenomena, patterns and
    relationships.
    A more organised written practice will help improve further to enhance
    grades.
    """,

    """
    Is able to present reasoned explanations for phenomena, patterns and
    relationships in a given problem very well. Shown a good progress in
    handling information and problem solving by transfer of information from
    one form to other form.
    """,

    """
    Has shown a strong capability to locate, select, organise and present
    information from a variety of sources and present reasoned explanations
    for phenomena, patterns and relationships. Keep progressing by putting
    consistent efforts.
    """
)


def set_remarks(**kwargs):
    remarks = {}

    # Cast list values to int
    for key in kwargs.keys():
        for i in range(len(kwargs[key])):
            kwargs[key][i] = int(kwargs[key][i])

    ao1_pc = (sum(kwargs['ao1']) * 4/3)
    ao2_pc = (sum(kwargs['ao2']) * 4/3)

    # Assign AO1 comments
    if ao1_pc >= 0 and ao1_pc < 45:
        remarks['ao1'] = AO1_REMARKS[0]
    elif ao1_pc >= 45 and ao1_pc < 60:
        remarks['ao1'] = AO1_REMARKS[1]
    elif ao1_pc >= 60 and ao1_pc < 80:
        remarks['ao1'] = AO1_REMARKS[2]
    elif ao1_pc >= 80:
        remarks['ao1'] = AO1_REMARKS[3]

    # Assign AO2 comments
    if ao2_pc >= 0 and ao2_pc < 45:
        remarks['ao2'] = AO2_REMARKS[0]
    elif ao2_pc >= 45 and ao2_pc < 60:
        remarks['ao2'] = AO2_REMARKS[1]
    elif ao2_pc >= 60 and ao2_pc < 80:
        remarks['ao2'] = AO2_REMARKS[2]
    elif ao2_pc >= 80:
        remarks['ao2'] = AO2_REMARKS[3]

    return remarks
