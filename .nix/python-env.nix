{ pkgs }:

# Non-hardware runtime deps needed to import shelfslide/src modules and run the
# test suite. RPi.GPIO/epaper/spidev/gpiozero are intentionally excluded: they
# are only imported lazily inside WaveshareDisplay and are not needed off-Pi.
pkgs.python312.withPackages (ps: with ps; [
  pyyaml
  requests
  pillow
  pytest
  pytest-mock
])
