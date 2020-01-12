# drafter

This is a tool designed to help with a particular workflow:

- In a work directory (e.g., a git repo), you has some active (likely version-controlled) "source" files.
- You have a `drafts/` subdirectory, where you copy the source files with a date, to make them distinguishable for colleagues.

`drafter.py` will help in copying files to the drafts folder.

For example, say you are preparing a paper. You have a manuscript file and a cover letter:

```
project_dir
├── drafts
├── project-cover-letter.docx
└── project-manuscript.docx
```

The manuscript and cover letter are version controlled, but when you want to
send a version to a colleague, you want some kind of human-readable version
control. To initiate a draft:

```
> drafter.py project-manuscript.py
Drafts to initiate:
  project-manuscript.docx -> drafts/2020-01-12_project-manuscript.docx
```

And then you have file structure:

```
project_dir
├── drafts
│   └── 2020-01-12_project-manuscript.docx
├── project-cover-letter.docx
└── project-manuscript.docx
```

If you change the manuscript file and call `drafter.py` again (with no
arguments), you'll get a new draft, either with a new date, or with the same
date and a version number:

```
> drafter.py
Drafts to update:
  project-manuscript.docx -> drafts/2020-01-12_project-manuscript-v2.docx
```

`drafter.py` checks if the source and the latest draft are different, so if you
call `drafter.py` again without changing the source file, it won't make a new
version.

## Author

Scott Olesen <swo@alum.mit.edu>
