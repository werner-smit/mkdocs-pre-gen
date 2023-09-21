import os
import tempfile
import shutil

import pytest

from mkdocs.config.base import load_config
from mkdocs.structure.files import Files, get_files
from mkdocs.structure.toc import TableOfContents
from mkdocs_pre_gen.plugin import PreGenPlugin


@pytest.fixture
def make_docs_dir():
    tmpdir = tempfile.mkdtemp()
    # Create a "docs" directory within the temporary directory
    docs_dir = os.path.join(tmpdir, 'docs')
    os.mkdir(docs_dir)
    yield docs_dir
    shutil.rmtree(tmpdir)

# Currently hardcoded in the test_mkdocs_conf.yml
template_extension = '.template'

def test_plugin(make_docs_dir):

    docs_dir = make_docs_dir

    # Create a test .template file in the "templates" directory
    template_file_path = os.path.join(docs_dir, f'test_template.{template_extension}') # TODO: Test multiple extensions.
    with open(template_file_path, 'w', encoding='utf-8') as template_file:
        template_file.write("# This is a {{ variable }} template.\n !!! danger highlight blink \"Don't try this at home\"\n ...")

    # Configure the plugin
    plugin = PreGenPlugin()

    # Simulate MkDocs configuration
    mkdocs_config = load_config('tests/fixtures/test_mkdocs_conf.yml')
    mkdocs_config['docs_dir'] = docs_dir
    plugin.load_config(mkdocs_config.data)

    # Simulate the MkDocs files collection and table of contents
    files = get_files(mkdocs_config)
    toc = TableOfContents([])
    #import pdb; pdb.set_trace()

    print(files._files)
    plugin.on_pre_build(mkdocs_config)
    # Call the plugin's on_files method to process the template
    plugin.on_files(files, mkdocs_config)

    processed_file_path = template_file_path.replace(template_extension, '.md')
    # Verify that the .template file was processed and a corresponding .md file was created
    assert os.path.isfile(processed_file_path)
    print(open(processed_file_path).read())

