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

dump = api.note.index(data=True)
index = dump['index']
# the dump might be paged; go through all the pages
while 'mark' in dump:
    dump = api.note.index(data=True, mark=dump['mark'])
    index = index + dump['index']

trashed = 0
for note in index:
    dir_path = backup_dir
    #if the note was trashed, put it into a 'TRASH' subdirectory
    if note['d']['deleted']== True:
        dir_path = os.path.join(dir_path, 'TRASH')
        trashed = trashed + 1

    #if the note has a single tag, put it into a subdirectory named as the tag
    if len(note['d']['tags'])==1:
        dir_path = os.path.join(dir_path, note['d']['tags'][0])

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
        # record pinned notes and whatever else
        if len(note['d']['systemTags'])>0:
            f.write("System tags: %s\n" % ", ".join(note['d']['systemTags']).encode('utf8'))
    os.utime(path,(note['d']['modificationDate'],note['d']['modificationDate']))

print "Done: %d files (%d in TRASH)." % (len(index), trashed)
