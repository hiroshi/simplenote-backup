simplenote-backup
=================

- It backups your notes as separated files named with note-id (like 68b329da9893e34099c7d8ad5cb9c940.txt)
- Backup files contains tags.
- It stores files in `~/Dropbox/SimplenoteBackups` by default.

## Sample of the content of a backup file of a note.

    id: 68b329da9893e34099c7d8ad5cb9c940
    tags: foo, bar

    Content of the note start here after the blank line after headers like email.
    ....

## Why

I know https://app.simplenote.com has "Download .zip", but it doesn't include tags.
I know https://app.simplenote.com has "Export notes", but it seems to exclude notes in trash.
Neither of both provide us automation or periodical task (like cron).
I tired of searching around other options...

## Technical notes

- It uses simperium-python sdk.
- I don't trust 3rd party tool which handle password, so you should not trust me. And simperium API didn't provide us a way like OAuth. So I let you get a token from http://app.simplenote.com/ by yourself.


## Installation (OS X)

Sorry, if your desktop OS is not an OS X.
Sorry, if you are not familiar with command line.
I hope you figure out how to deal with it.

### 1. Create a working directory

If you don't have no idea where to place the directory, home directory is an option.

    mkdir ~/SimplenoteBackup
    cd ~/SimplenoteBackup

### 2. Get what needed

    git clone https://github.com/Simperium/simperium-python.git
    git clone https://github.com/hiroshi/simplenote-backup.git

### 3. Get your token

  1. Open https://app.simplenote.com and login.
  2. Open the inspector in your browser (A shortcut may be Command + Alt + i).
  3. Type `simperium_opts.token` in the console of the inspector.
  4. You will see a token, like "a543b9622f7bf1a340a8a6682d09ad17".

### 4. Run the script

    cd ~/SimplenoteBackup/simplenote-backup
    make TOKEN=YOUR_TOKEN_HERE
    
If succeed you will see like this:

    Starting backup your simplenote to: /Users/hiroshi/Dropbox/SimplenoteBackups
    Done: 100 files.


If you'd like to choose another destination directory, add BACKUP_DIR option.

    make TOKEN=YOUR_TOKEN_HERE BACKUP_DIR=~/my-simplenote-backup


### 5. Add cron task if you wish

    crontab -e

If you wish to execute a backup job once an hour, add following line:

    0 * * * * cd $HOME/SimplenoteBackup/simplenote-backup && make TOKEN=YOU_TOKEN_HERE > cron.log 2>&1


## TODO
- Provide an archive file packed with simperium sdk.
- Run the script as a service somewhere so that you don't need to open desktop machine for backing up notes entered in your mobile deices.
- Provide a bookmarklet to grab token in https://app.simplenote.com to ease setup.
