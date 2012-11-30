import argparse
import ConfigParser
import os
import sys



shortcuts = [
             ('O', 'save'),
             ('X', 'quit'),
             ('N', 'new note'),
             ('G', 'goto note'),
             ('K', 'cut'),
             ('U', 'paste'),
             ('B', 'back'),
             ('F', 'forward'),
             ('T', 'settings'),
             ]

def make_dir_if_not_exists(path):
    if not os.path.exists(path): os.makedirs(path)

home_dir = os.path.expanduser('~/.nanote/')
make_dir_if_not_exists(home_dir)
config_file_path = os.path.join(home_dir, 'settings')

defaults = {
            'path': os.path.join(home_dir, 'notes'),
            'default_note': sys.argv[1] if len(sys.argv) > 1 else '',
            'tab_width': '4',
}

config = ConfigParser.SafeConfigParser(defaults)
config.read(config_file_path)

# get note search paths
# TODO: parse sys.argv arguments
args = {}
for arg in ('path', 'default_note', 'tab_width'):
    if config.has_section('nanote'):
        args[arg] = config.get('nanote', arg)
    else:
        args[arg] = config.defaults()[arg]
        
args['tab_width'] = int(args['tab_width'])

NOTE_SEARCH_PATHS = '.:' + args['path']

NOTE_SEARCH_PATHS = [os.path.expanduser(p) for p in NOTE_SEARCH_PATHS.split(':')]


for path in NOTE_SEARCH_PATHS:
    make_dir_if_not_exists(path)

def find_note(note_name):
    # given a note name (i.e. school:homework), search {path}/school/homework for all 
    # paths on the note search path
    if note_name == '**settings**': return config_file_path
    note_name = note_name.replace(':', '/')
    note_paths = [os.path.join(path, note_name) for path in NOTE_SEARCH_PATHS]
    for path in note_paths:
        if os.path.exists(path): return path
    return None
    
def default_note_path(note_name):
    note_name = note_name.replace(':', '/')
    return os.path.join(NOTE_SEARCH_PATHS[-1], note_name)
