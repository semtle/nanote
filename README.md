nanote is a terminal note-taking application.

nanote is written in pure Python and relies only on the Python standard library. To get started, run "python setup.py install".

Usage: nanote [note name]

Nanote supports linking to notes by surrounding the note name in [square_brackets]. It also supports limited markdown formatting, including:

    *bold text*, 

    _underlining_, and

        * bulleted

        * lists

![nanote](http://4.bp.blogspot.com/-OwfTCgWkffQ/ULo4I2WZWQI/AAAAAAAAAEw/LW8Nx79znL8/s1600/Screenshot+from+2012-12-01+12:01:45.png)

Press CTRL+T from nanote to edit the settings file. From here, you can change the path that nanote searches for notes. Multiple paths are separated by colons and searched in order; the final path is the one where new notes are written to.