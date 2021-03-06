import logging

from eusurvey.limesurvey import common

logger = logging.getLogger(__name__)


"""
'Q', ';', 'afAMF', '1', '[:] Multi-Flex 1-10', '', 'en', '', '', 'N', '', '1', '', '', '', 'afSrcFilter', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '1', '', '', '', '', '', '', '', '', '', '', 'maxSelect', '', '', '', '', '', 'minSelect', '', '', '', '', 'ceil(num2)', 'floor(num)', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''
"""

def get_question_row(formset, total):
    field_name = common.get_matrix_value(formset.matrix_id)
    partial_question = [
        'Q',
        ';',
        field_name,
        1,
        formset.question,
        formset.help_text,
        'en',
        '',
        common.get_mandatory(formset),
        '',
    ]
    full_question = partial_question + common.get_missing(partial_question, total)
    custom_fields = (
        ('same_default', 1),
    )
    full_question = common.update_row(full_question, custom_fields)
    return full_question

"""
'SQ', '0', 'sq1', '', 'First sub-question', '', 'en', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''
"""


def get_subquestion_id(question_list):
    question_ids = []
    for question in question_list:
        # question name: answer6251697|1|1
        q_id = 'sq%s' % question['input']['name'].split('|')[1]
        if q_id not in question_ids:
            question_ids.append(q_id)
    # Subquestion id should be consistent
    if len(question_ids) == 1:
        return question_ids[0]
    raise ValueError('Inconsistent subquestion naming: `%s`' % question_list)


def get_subquestion_rows(formset, total):
    subquestion_rows = []
    for name, question_list in formset.field_list:
        subquestion_id = get_subquestion_id(question_list)
        partial_row = [
            'SQ',
            0,
            subquestion_id,
            '',
            name,
            '',
            'en',
        ]
        full_row = partial_row + common.get_missing(partial_row, total)
        subquestion_rows.append(full_row)
    return subquestion_rows


def get_answers(raw_question_list):
    question_list = []
    for question in raw_question_list:
        # question name: answer6251697|1|1
        name = question['input']['name'].split('|')[2]
        value = (name, question['label'])
        if value not in question_list:
            question_list.append(value)
    return question_list


def get_answers_set(formset):
    answer_set = []
    total_answers = 0
    for name, question_list in formset.field_list:
        answers = get_answers(question_list)
        total_answers = len(answers)
        # The order of the fields is significant this is why a list is
        # being used instead of a set.
        [answer_set.append(a) for a in answers if a not in answer_set]
    assert len(answer_set) == total_answers, "Invalid answer count. `%s`" % formset
    return answer_set

"""
'SQ', '1', '1', '1', 'Never', '', 'en', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''
"""


def get_answer_rows(formset, total):
    answer_set = get_answers_set(formset)
    answer_rows = []
    for i, (name, label) in enumerate(answer_set, start=1):
        partial_row = [
            'SQ',
            1,
            name,
            i,
            label,
            '',
            'en',
            ''
        ]
        full_row = partial_row + common.get_missing(partial_row, total)
        answer_rows.append(full_row)
    return answer_rows


def prepare_tabletable_row(formset, total):
    tabletable_row = [get_question_row(formset, total)]
    tabletable_row += get_subquestion_rows(formset, total)
    tabletable_row += get_answer_rows(formset, total)
    return tabletable_row
