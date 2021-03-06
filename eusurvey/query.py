import os
import requests
import logging

from eusurvey import settings
from eusurvey.fields.common import get, get_inner_html
from eusurvey.models import FormTree
from slugify import slugify
from lxml import html

logger = logging.getLogger(__name__)


def get_form_tree(url):
    """Reads the form URL."""
    response = requests.get(url, headers=settings.HEADERS)
    tree = html.fromstring(response.content)
    return FormTree(tree=tree, response=response, stream=response.content)


def get_form_title(tree):
    """Gets the title of the form."""
    title = get(tree.xpath('//div[@class="surveytitle"]'))
    remove_elements = (
        '<div class="surveytitle">',
        '</div>',
    )
    title_text = get_inner_html(title, remove_elements)
    return title_text


def get_survey_dict(url):
    """Extracts the survey information."""
    form_tree = get_form_tree(url)
    name = slugify(url, only_ascii=True)
    title = get_form_title(form_tree.tree)
    return {
        'url': url,
        'name': name,
        'title': title,
        'form_tree': form_tree,
        'id': None, # TODO: get form ID
        'survey_path': os.path.join(settings.DB_ROOT, name),
    }
