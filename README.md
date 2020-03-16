# betatorrentseries

This is a tool to download torrents from 1337x.to based on your unseen episodes on BetaSeries.

## How to set up

### Ouside of Docker

- Install Python 3.6 or later and transmission-daemon
- Copy `.env.example ` to `.env` and change values as you wanted
- Run `run.sh`

### Docker

#### Standalone

- Copy `src/.env.example` to `.env` and change values for BetaSeries
- Run ./test_image.sh, it should create a `downloads` folder that will be set as an alias of `/root/downloads` on the Docker container

#### Custom

- Copy `src/.env.example` to `.env` and change values for BetaSeries
- Just build the image and bind `/root/downloads` to whatever is your wanted destination folder

## How it works

When you start betatorrent.py, the following things happens:
- It gets your unseen shows from BetaSeries
- For each unseen episode, it spawns a new thread that will do the following thing:
    - Mark episode as downloaded
    - Go on 1337x and search for "%Show name% SxxExx", for example "Doctor Who S20E01"
    - Sort by desc size and take the first torrent (should be the best quality)
    - Add that torrent to Transmission and wait for it to be done downloading
    - Copy the biggest file of the torrent to the final destination and rename it
    - Delete the torrent and data from Transmission

## Is it legal?

Most likely a no, as it uses 1337x to download copyrighted content.

Might be legal for some webseries hosted on torrent sites. Don't quote me on that.

Built for educational purpose.
