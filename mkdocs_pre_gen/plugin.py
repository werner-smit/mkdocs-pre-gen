"""
MkDocs Template Pre-Processor Plugin

This MkDocs plugin automates the generation of Markdown files from template files. It processes
template files with a '.template' extension and converts them to '.md' files using MkDocs' built-in
markdown extensions. The generated Markdown files can be included in your MkDocs documentation.

Usage:
1. Create template files with a '.template' extension in your 'docs' directory.
2. Configure the plugin in your 'mkdocs.yml' file.
3. Run 'mkdocs build' to pre-generate Markdown files

Configuration in 'mkdocs.yml':
plugins:
  - template-pre-processor

Author: [Werner Smit]
Version: 0.1.0
"""
import os

import mkdocs
from mkdocs.config.base import Config
from mkdocs.config import config_options
from mkdocs.structure.files import Files, File
from mkdocs.exceptions import PluginError
from mkdocs.plugins import BasePlugin
from markdown import Markdown
from mkdocs import utils
from mkdocs.plugins import get_plugin_logger

# TODO: Make a config var
GENERATE_PRE_PROCESS_ONLY = False

log = get_plugin_logger(__name__)

class PreGenPlugin(BasePlugin):
    config_scheme = (
        ('template_extension', config_options.Type(str, default='.template')),
    )

    def on_pre_build(self, config: Config):
        """Initialize the plugin with the MkDocs configuration."""
        self.global_config = config
        #self.config = config
        self.template_ext = self.config['template_extension']

    def _get_md_handler(self) -> Markdown:
        """Create and configure a Markdown handler with extensions."""
        md = Markdown(
            extensions=self.global_config.get('markdown_extensions', []),
            extension_configs=self.global_config['mdx_configs'] or {},
        )
        return md

    def _make_content(self, template_content: str) -> str:
        """Convert template content to Markdown."""
        md = self._get_md_handler()
        if GENERATE_PRE_PROCESS_ONLY:
            # Run line preprocessors if generating pre-processed content only
            lines = template_content.split("\n")
            for prep in md.preprocessors:
                lines = prep.run(lines)
            parsed_content = '\n'.join(lines)
        else:
            # Convert the template content to HTML
            parsed_content = md.convert(template_content)
        return parsed_content

    def on_files(self, files: Files, config: Config, **kwargs):
        """Process template files and generate Markdown files."""
        docs_dir = config['docs_dir']
        for file in files:
            # Skip files that are not template files
            if not file.src_path.endswith(self.template_ext):
                continue

            template_path = file.abs_src_path
            markdown_path = os.path.splitext(template_path)[0]  # Remove the .template extension
            markdown_rel_file = os.path.splitext(file.src_path)[0]
            # Ensure the resulting file is an .md file
            if not markdown_path.endswith('.md'):
                markdown_path += '.md'
                markdown_rel_file += '.md'

            with open(template_path, 'r', encoding='utf-8') as template_file:
                template_content = template_file.read()

            # Use MkDocs' built-in markdown extensions to pre-evaluate the template
            markdown_content = self._make_content(template_content)

            # The file doesn't exist yet, so we add it to the files list in order to be rendered once it has been
            # written.
            if not os.path.isfile(markdown_path):
                files.append(File(
                    markdown_rel_file,
                    config['docs_dir'],
                    config['site_dir'],
                    config['use_directory_urls'],
                ))

            # Write the generated Markdown content to the .md file
            with open(markdown_path, 'w', encoding='utf-8') as markdown_file:
                if is_data_different(markdown_path, markdown_content):
                    markdown_file.writelines(markdown_content)
            log.info(f'Converted {file.src_path} -> {markdown_rel_file}')
        return files

def is_data_different(filename, new_data):
    try:
        with open(filename, 'r') as file:
            existing_data = file.read()
            return existing_data != new_data
    except FileNotFoundError:
        # If the file doesn't exist, consider the data as different.
        return True
