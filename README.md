# Audio Visualizer

A webapp that allows you to visualize Audio with graphs or cool-looking videos.
Available [online at https://audiovisual-twt.herokuapp.com/](https://audiovisual-twt.herokuapp.com/) or locally.

## Description

This project was created for the [Timathon](https://twtcodejam.net/) with the theme "Visualization".
This is a Flask webapp that gets information from the audio file the user provides. It is able to generate graphs or let the user place "widgets" on a whiteboard to organize the creation of a video (those widgets can be beat visualizers, frequencies volume visualizers...).

## How to use
- [Online at https://audiovisual-twt.herokuapp.com/](https://audiovisual-twt.herokuapp.com/)

- Locally by cloning the repo:

  First, clone the repo and open a commandline in the cloned folder. You must have Python installed (tested with 3.8.7).

  Install pip requirements : `pip install -r requirements.txt`

  Run Flask: `flask run`

  And finally, open the address Flask will give you. It should be something like `http://127.0.0.1:5000/`

## Credits

This project uses the [librosa](https://github.com/librosa/librosa) library, version 0.8.0 : Brian McFee; Vincent Lostanlen
Cornell Lab of Ornithology / New York University; Alexandros Metsai; Matt McVicar; Stefan Balke; Carl Thomé; Colin Raffel; Frank Zalkow; Ayoub Malek; Dana; Kyungyun Lee; Oriol Nieto; Jack Mason; Dan Ellis; Eric Battenberg; Scott Seyfarth; Ryuichi Yamamoto; Keunwoo Choi; viktorandreevichmorozov; Josh Moore; Rachel Bittner; Shunsuke Hidaka; Ziyao Wei; nullmightybofo; Darío Hereñú; Fabian-Robert Stöter; Pius Friesch; Adam Weiss; Matt Vollrath; Taewoon Kim (from [zenodo](https://zenodo.org/record/3955228)).

It uses Matplotlib : [J. D. Hunter, "Matplotlib: A 2D Graphics Environment", Computing in Science & Engineering, vol. 9, no. 3, pp. 90-95, 2007](https://doi.org/10.1109/MCSE.2007.55)

It uses IPython [Fernando Pérez, Brian E. Granger, IPython: A System for Interactive Scientific Computing, Computing in Science and Engineering, vol. 9, no. 3, pp. 21-29, May/June 2007, doi:10.1109/MCSE.2007.53. URL: https://ipython.org](https://ipython.org)

It uses [Pillow](https://github.com/python-pillow/Pillow), [opencv-python](https://github.com/opencv/opencv-python), the [moviepy library](https://github.com/Zulko/moviepy), [Flask](https://flask.palletsprojects.com/en/1.1.x/).

Frontend's noise texture generated with [Noise texture generator](https://github.com/andrewckor/Noise-texture-generator)

## License

This project is under the MIT Licence. Learn more [here](LICENSE)

## About openh264
This repository incldues openh264 binaries: `openh264-1.8.0-win64.dll`, `openh264-1.8.0-win32.dll`

Copyright from [cisco](https://github.com/cisco/openh264)
```
Copyright (c) 2013, Cisco Systems
All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice, this
  list of conditions and the following disclaimer in the documentation and/or
  other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
```
cisco/openh264 is licensed under the BSD 2-Clause "Simplified" License
A permissive license that comes in two variants, the BSD 2-Clause and BSD 3-Clause. Both have very minute differences to the MIT license.
```
Permissions: Commercial use, Modification, Distribution, Private use.
Limitations: Liability, Warranty.
Conditions: License and copyright notice.
```
