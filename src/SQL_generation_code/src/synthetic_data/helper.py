import re


def map_semql_actions_only(semql):
    intermediate = re.sub(r'C\([0-9]*\)', 'C(*)', semql)
    intermediate = re.sub(r'T\([0-9]*\)', 'T(*)', intermediate)
    intermediate = re.sub(r'V\([0-9]*\)', 'V(*)', intermediate)

    return intermediate

def get_ops(op) -> str:
    id_c = op.id_c
    return op.grammar_dict[id_c].split(' ')[1]