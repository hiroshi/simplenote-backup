import os, sys, json
from simperium.core import Api as SimperiumApi

appname = 'chalk-bump-f49' # Simplenote
token = os.environ['TOKEN']
backup_dir = sys.argv[1] if len(sys.argv) > 1 else (os.path.join(os.environ['HOME'], "Dropbox/SimplenoteBackups"))
print "Starting backup your simplenote to: %s" % backup_dir
if not os.path.exists(backup_dir):
    print "Creating directory: %s" % backup_dir
    os.makedirs(backup_dir)

api = SimperiumApi(appname, token)
#print token
notes = api.note.index(data=True)
for note in notes['index']:
    #if the note has a single tag, put it into a subdirectory named as the tag
    if len(note['d']['tags'])==1:
        tag = note['d']['tags'][0]
    else:
        tag = ''
    dir_path = os.path.join(backup_dir, tag)
    try:
        os.makedirs(dir_path)
    except OSError as e:
        if e.errno == 17:
            # the subdir already exists
            pass

    path = os.path.join(dir_path, note['id'] + '.txt')
    #print path
    with open(path, "w") as f:
        # print json.dumps(note, indent=2)
        #f.write("id: %s\n" % note['id'])
        f.write(note['d']['content'].encode('utf8'))
        f.write("\n")
        f.write("Tags: %s\n" % ", ".join(note['d']['tags']).encode('utf8'))
    os.utime(path,(note['d']['modificationDate'],note['d']['modificationDate']))

print "Done: %d files." % len(notes['index'])
