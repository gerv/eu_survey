import logging

from eusurvey.fields.extractors import base
from eusurvey.fields.common import get_label

logger = logging.getLogger(__name__)

def get_input(element):
    _a = lambda x: element.attrib.get(x)
    attrs = ['id', 'name', 'data-id', 'value']
    field = dict([(k, _a(k)) for k in attrs])
    if 'data-dependencies' in element.attrib:
        dependencies = _a('data-dependencies').split(';')
    else:
        dependencies = None
    field['data-dependencies'] = dependencies
    field['type'] = 'checkbox'
    return field


def get_input_list(section):
    input_list = []
    for element in section.xpath('.//table[@class="answers-table"]//input'):
        input_list.append({
            'input': get_input(element),
            'label': get_label(element, section),
        })
    return input_list


class CheckboxFieldExtractor(base.Extractor):
    field_type = 'checkbox'
    pattern = './/table[@class="answers-table"]//input[@type="checkbox"]'

    def extract_field(self, section):
        self.field_list = get_input_list(section)
