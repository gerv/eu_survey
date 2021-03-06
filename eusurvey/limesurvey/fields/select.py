import logging

from eusurvey.limesurvey import common

logger = logging.getLogger(__name__)

"""Example
'Q', '!', 'weight_units', '1', 'Which units are you using for weight?', '', 'en', '', 'Y', 'N', '', '1', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '1', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''
'A', '0', 'kg', 'kg', 'kilograms', '', 'en', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''
'A', '0', 'lb', 'lb', 'pounds', '', 'en', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''
"""


def get_question_row(formset, total):
    field_name = common.get_name(formset.field['name'])
    partial_question = [
        'Q',
        '!',
        field_name,
        1,
        formset.question,
        formset.help_text,
        'en',
        '',
        common.get_mandatory(formset),
        '',
    ]
    full_row = partial_question + common.get_missing(partial_question, total)
    full_row.append(formset.get_dependencies())
    return full_row


def get_answer_row(field, total):
    value = field['input']['value']
    if not value:
        return None
    row_value = common.get_value(value)
    partial_row = [
        'A',
        0,
        row_value,
        '',
        field['label'],
        '',
        'en',
        '',
        '',
        '',
    ]
    full_row = partial_row + common.get_missing(partial_row, total)
    # Add row metadata:
    field_id = field['input'].get('id').replace('trigger', '')
    metadata = {
        'field_id': field_id,
    }
    full_row.append(metadata)
    return full_row


def prepare_select_row(formset, total):
    select_row = [get_question_row(formset, total)]
    for field in formset.option_list:
        answer_row = get_answer_row(field, total)
        if not answer_row:
            continue
        select_row.append(answer_row)
    return select_row
