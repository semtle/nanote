import curses
import re
import settings
from editor import Editor


def main():
    running = True

    default_note = settings.args['default_note']
    editor = Editor(default_note)

    end_state = None

    while running:
        try:
            editor.draw_screen()
            cy, cx = editor.cursor

            c = editor.screen.getch()
            handled_key = False
            for key, shortcut in settings.shortcuts:
                if c == ord(key)-64:
                    if shortcut == 'quit':
                        running = False
                        
                    elif shortcut == 'save':
                        editor.save_note(editor.current_note)
                        
                    elif shortcut == 'goto note':
                        result = editor.dialog('Enter the name of the note to load (^C to cancel):')
                        if result:
                            editor.load_note(result)
                            
                    elif shortcut == 'forward':
                        editor.forward()
                        
                    elif shortcut == 'back':
                        editor.back()
                        
                    elif shortcut == 'new note':
                        editor.load_note(None)
                        
                    elif shortcut == 'settings':
                        editor.load_note('**settings**')
                        
                    elif shortcut == 'paste':
                        if editor.cuts:
                            editor.buffer = editor.buffer[:cy] + editor.cuts + editor.buffer[cy:]
                            editor.correct_cursor(cy+len(editor.cuts), cx)
                    
                    elif shortcut == 'cut':
                        if editor.cutting:
                            editor.cuts += editor.buffer[cy]
                        else:
                            editor.cuts = [editor.buffer[cy]]
                            
                        editor.buffer = editor.buffer[:cy] + editor.buffer[cy+1:]
                        
                    handled_key = True
            if not handled_key:
                if c == curses.KEY_UP:
                    editor.correct_cursor(cy-1, min(cx, len(editor.buffer[cy-1]) if 0 <= cy-1 < len(editor.buffer) else 0))
                    editor.cutting = False
                elif c == curses.KEY_DOWN:
                    editor.correct_cursor(cy+1, cx)
                    editor.cutting = False
                elif c == curses.KEY_LEFT:
                    editor.correct_cursor(cy, cx-1)
                elif c == curses.KEY_RIGHT:
                    editor.correct_cursor(cy, cx+1)
                elif c == curses.KEY_LEFT + 279:
                    # ctrl left
                    first = True
                    while first or not (cx==0 or (cy < len(editor.buffer) and len(editor.buffer[cy])>0 and editor.buffer[cy][cx-1] == ' ')):
                        first = False
                        editor.correct_cursor(cy, cx-1)
                        cy, cx = editor.cursor
                elif c == curses.KEY_RIGHT + 293:
                    # ctrl right
                    first = True
                    while first or not (cx==0 or (cy < len(editor.buffer) and len(editor.buffer[cy])>0 and editor.buffer[cy][cx-1] == ' ')):
                        first = False
                        editor.correct_cursor(cy, cx+1)
                        cy, cx = editor.cursor
                elif c == ord('\n'):
                    follow_link = False
                    for pos, text in editor.links:
                        if pos < cx < pos+len(text):
                            follow_link = text[1:-1]
                            current_note = follow_link
                            editor.load_note(current_note)
                    if not follow_link:
                        editor.altered = True
                        if cy == len(editor.buffer):
                            editor.buffer.append('')
                        else:
                            editor.buffer = editor.buffer[:cy] + [editor.buffer[cy][:cx]] + [editor.buffer[cy][cx:]] + editor.buffer[cy+1:]
                        editor.correct_cursor(cy+1, 0)
                elif c == curses.KEY_BACKSPACE:
                    editor.altered = True
                    if cy < len(editor.buffer[cy]):
                        if cx > 0:
                            editor.buffer[cy] = editor.buffer[cy][:cx-1] + editor.buffer[cy][cx:]
                            editor.status = 'backspace'
                        else:
                            editor.buffer = editor.buffer[:cy-1] + [editor.buffer[cy-1] + editor.buffer[cy]] + editor.buffer[cy+1:]
                    editor.correct_cursor(cy, cx-1)
                elif c == ord('\t'):
                    # tab
                    tab = ' '*settings.args['tab_width']
                    if cy == len(editor.buffer): 
                        editor.buffer.append(tab)
                    else:
                        editor.buffer[cy] = tab + editor.buffer[cy]
                    editor.correct_cursor(cy, cx+len(tab))
                elif c == 353:
                    # shift+tab
                    tab = ' '*settings.args['tab_width']
                    if cy < len(editor.buffer) and editor.buffer[cy].startswith(tab):
                        editor.buffer[cy] = editor.buffer[cy][len(tab):]
                    editor.correct_cursor(cy, cx-len(tab))
                elif c == curses.KEY_DC:
                    editor.altered = True
                    if cy < len(editor.buffer[cy]):
                        if editor.buffer[cy]:
                            editor.buffer[cy] = editor.buffer[cy][:cx] + editor.buffer[cy][cx+1:]
                        else:
                            editor.buffer = editor.buffer[:cy] + editor.buffer[cy+1:]
                elif c == curses.KEY_HOME:
                    if cx == 0 and cy < len(editor.buffer) and editor.buffer[cy]:
                        stripped = editor.buffer[cy].lstrip(' ')
                        cx = len(editor.buffer[cy]) - len(stripped)
                        editor.correct_cursor(cy, cx)
                    else:
                        editor.correct_cursor(cy, 0)
                elif c == curses.KEY_END:
                    if cy < len(buffer):
                        editor.correct_cursor(cy, len(editor.buffer[cy]))
                # TODO: c<255? not all of those are good characters
                elif 0 < c < 255:
                    editor.altered = True
                    if cy > len(editor.buffer)-1: editor.buffer += ['']
                    editor.buffer[cy] = editor.buffer[cy][:cx] + chr(c) + editor.buffer[cy][cx:]
                    editor.correct_cursor(cy, cx+1)
                    
                #editor.status = str(c)

        except KeyboardInterrupt:
            running = False
            
        except Exception as e:
            editor.status = 'exception: %s' % e
            end_state = editor.status
            running = False
        
    editor.end_app()
    if end_state: print end_state

if __name__ == '__main__':
    main()
