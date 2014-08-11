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
    path = os.path.join(backup_dir, note['id'] + '.txt')
    #print path
    f = open(path, "w")
    # print json.dumps(note, indent=2)
    f.write("id: %s\n" % note['id'])
    f.write("tags: %s\n" % ", ".join(note['d']['tags']).encode('utf8'))
    f.write("\n")
    f.write(note['d']['content'].encode('utf8'))
print "Done: %d files." % len(notes['index'])
