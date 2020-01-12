# drafter

It tries to be smart about saving drafts

1. Look in "this" folder for all candidate "source" files
    - This will happen in drafter.py
1. Look in "drafts" folder for all candidate draft files
    - Happen in drafter.py
1. Match source files and drafts by their filenames
    - Function **to be written** in draft_group.py
1. For each possible match, order the draft files by date and version number
    - In draft_group.py
1. Check if source file is identical to most recent draft file
    - In draft_group.py
1. If not, suggest copying the source file to an increment draft file name (by date or version number)
    - In draft_group.py
