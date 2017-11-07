# audioReactive

This repo contains the modules needed to make LEDs audio-reactive.  Intended to just be the core audio-reactive elements, not full code for visualizations.  This should plug into those.

To set up audio/sound stuff:

sudo apt-get install python-numpy python-scipy python-pyaudio
sudo nano /etc/asound.conf

enter this text in the file and save it:
"pcm.!default {
    type hw
    card 1
}
ctl.!default {
    type hw
    card 1
}"

sudo nano /usr/share/alsa/alsa.conf
change the following lines:
defaults.ctl.card 0 to defaults.ctl.card 1
defaults.pcm.card 0 to defaults.pcm.card 1
