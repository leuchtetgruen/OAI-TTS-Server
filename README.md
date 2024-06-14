# OAI-TTS-Server
A simple OpenAI TTS compatible voice server based on Pico2Wave. Can easily be adjusted to use other TTS backends.

This server aims to solve the problem, that in Open Web UI when using the local TTS system the language of the text is not taken into consideration. As Open Web UI allows to use an OpenAI TTS compatible TTS system, I created this wrapper around pico2wave for creating audio responses that are not in the wrong language.


## Requirements

- Pico2Wave
- Sox

Installable via `apt-get install libttspico-utils sox` on Ubuntu
