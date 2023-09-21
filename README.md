# Overview
`mkdocs-pre-gen` pre-processes specific Markdown files, converting them into plain HTML blocks inside a `.md` file. These processed files are treated as regular `.md` files and gets generated alongside the originals. This enables Markdown files that rely on a complex set of plugins to be pre-generated, making them easier to serve in environments where the those complex plugin configuration for rendering are unavailable.

## Why, it's a pretty niche use case?
This becomes necessary when using the [mkdocs-multirepo-plugin](https://github.com/jdoiro3/mkdocs-multirepo-plugin) and wanting to avoid the complexity of managing individual repository packages and dependencies to make tools like mkdocs-click function correctly.

## How?
This is achieved by pre-rendering selected `.md` files that can't easily be built in a streamlined environment, such as when using mkdocs-click with the multi-repo plugin. These pre-rendered files can be commited to the source code which will make it possible for the multirepo environment to render them without the need of the plugins used in the source repo. The pre-rendered files will look like standard `.md` pages, though they contain html, and will be treated just like any other docuement.

# Usage

Enable the plugin:
```yaml
plugins:
  - pre-gen
```

Create the file you want to be pre-rendered by adding `.template` as the extension.

Example before doc build or serve:
```
.
├── docs
│   ├── index.md
│   ├── my-pre-rendered-doc.template
│   └── test.template
└── mkdocs.yml
```

After the docs have been built or serve you should all `.template` files having a generated .md file alongside them:
```
.
├── docs
│   ├── index.md
│   ├── my-pre-rendered-doc.md
│   ├── my-pre-rendered-doc.template
│   ├── test.md
│   └── test.template
└── mkdocs.yml
```

Contents of `my-pre-rendered-docs.template`:
```
$ cat docs/my-pre-rendered-doc.template
# Hello world
I will render as html in docs/pre-rendered-doc.md
```

Contents of the generated `my-pre-rendered-doc.md`:
```
$ cat docs/my-pre-rendered-doc.md
<h1 id="hello-world">Hello world</h1>
<p>I will render as html in docs/pre-rendered-doc.md
```

Config Used in this example:
```
site_name: My Docs

nav:
  - index.md
  - my-pre-rendered-doc.md

plugins:
  - pre-gen
```

# Installation
```
pip install git+https://github.com/werner-smit/mkdocs-pre-gen.git
```



 




