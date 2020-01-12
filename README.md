# *drafter*: Smart draft management

This is a tool designed to help with a particular workflow:

- In a work directory (e.g., a git repo), you have some active (likely version-controlled) "source" files.
- You have a `drafts/` subdirectory, where you copy the source files with a date, to make them distinguishable for colleagues.

`drafter` will help in copying files to the drafts folder.

For example, say you are preparing a paper. You have a manuscript file and a cover letter:

```
project_dir
├── drafts
├── cover-letter.docx
└── manuscript.docx
```

The manuscript and cover letter are version controlled, but when you want to
send a version to a colleague, you want some kind of human-readable version
control. To initiate a draft:

```
> drafter manuscript.docx
Drafts to initiate:
  manuscript.docx -> drafts/2020-01-12_manuscript.docx
```

And then you have file structure:

```
project_dir
├── drafts
│   └── 2020-01-12_manuscript.docx
├── cover-letter.docx
└── manuscript.docx
```

If you change the manuscript file and call `drafter` again (with no arguments),
you'll get a new draft, either with a new date (I wrote this on 12 Jan 2020),
or with the same date and a version number:

```
> drafter
Drafts to update:
  manuscript.docx -> drafts/2020-01-12_manuscript-v2.docx
```

`drafter` checks if the source and the latest draft are different, so if you
call `drafter` again without changing the source file, it won't make a new
version:

```
> drafter
Up to date drafts:
  manuscript.docx == drafts/2020-01-12_manuscript-v2.docx
All source files up to date
```

If you want to put the cover letter under "drafts control", then you specify it
on the command line: `drafter cover-letter.docx`.

## To do

- Maybe rename it "dit", because it's "draft control"? I thought it also might make sense to keep some log that matches git commits with draft versions, so you can know that `commit 3f1c01940bd0c1388e8e9d78d6babaefb509e757` is the same as 3 Jan 2019 version 2, or something.

## Author

Scott Olesen <swo@alum.mit.edu>
