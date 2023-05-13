simplenote-backup
=================

- It backups your notes as separate files named by note ids (like 68b329da9893e34099c7d8ad5cb9c940.txt)
- Backup files contain tags.
- It stores files in `~/Dropbox/SimplenoteBackups` by default.
  - If a note has only one tag, put it into a directory named by the tag. This lets you keep the structure when you import notes into the Notes.app.


## Sample of the content of a backup file of a note.

    Content of the note.
    After the content and a blank line, tags follow.
    
    tags: foo, bar


## Why

I know https://app.simplenote.com has a "Download .zip" feature, but it doesn't include tags.
I know https://app.simplenote.com has an "Export notes" feature, but it seems to exclude notes in trash.
Neither of these lets us automate backing up (for instance periodically using cron).
I am tired of searching around for other options...

## Technical notes

- It uses the simperium-python sdk.
- I don't trust 3rd party tools that handle my password, so I don't require you to trust me either. The simperium API didn't provide us with a way like OAuth. So you need to retrieve a token from http://app.simplenote.com/ by yourself.


## Installation (OS X)

Sorry if your desktop OS is not an OS X.
Sorry if you are not familiar with the command line.
I hope you can figure out how to deal with this nontheless.

### 1. Create a working directory

If you don't have any idea where to place the directory, your home directory is an option. I.e.

    mkdir ~/SimplenoteBackup
    cd ~/SimplenoteBackup

### 2. Get what's needed

    git clone https://github.com/Simperium/simperium-python.git
    git clone https://github.com/hiroshi/simplenote-backup.git

### 3. Get your token

  1. Open https://app.simplenote.com and log in.
  2. Open the inspector in your browser (A shortcut may be Command + Alt + j).
  3. Type `simperium_opts.token` in the console of the inspector, and press enter.
  4. You will see your token; it looks like "a543b9622f7bf1a340a8a6682d09ad17".

### 4. Run my script

    cd ~/SimplenoteBackup/simplenote-backup
    make TOKEN=YOUR_TOKEN_HERE

If it succeeds you will see something like this:

    Starting backup your simplenote to: /Users/hiroshi/Dropbox/SimplenoteBackups
    Done: 3156 files (1605 in TRASH).


If you'd like to choose another destination directory, add BACKUP_DIR option to the `make` command.

    make TOKEN=YOUR_TOKEN_HERE BACKUP_DIR=~/my-simplenote-backup


### 5. Add a cron task if you wish

    crontab -e

If you wish to execute a backup job once an hour, add the following line to your crontab:

    0 * * * * cd $HOME/SimplenoteBackup/simplenote-backup && make TOKEN=YOU_TOKEN_HERE > cron.log 2>&1

## Build and run without Python using Docker

    # Build a local Docker image straight from sources on Github.
    docker build --pull -t simplenote-backup github.com/hiroshi/simplenote-backup
    
    # Create host's backup dir. Otherwise, Docker will create it, but with wrong ownership (root:root).
    mkdir -vp /path/to/backups/
    
    # Launch a one-off container which will dump files in your specified path, mounted at container's /data/ directory.
    docker run --rm -it --user $(id -u):$(id -g) -e BACKUP_DIR=/data/ -e TOKEN=your_token -v /path/to/backups/:/data/ simplenote-backup

## TODO
- Provide an archive file packed with simperium sdk.
- Run the script as a service somewhere so that you don't need to keep open a desktop machine for backing up notes entered eg. on your mobile device.
- Provide a bookmarklet to the grab token from https://app.simplenote.com, to ease setup.
