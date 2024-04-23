fileName = "border2mod3.py"

clone:
  # Clone the repo
  git clone https://github.com/killswwitch1011/SALLY-volume-detection/
  cp Makefile ~

# Cleans everything except Makefile
clean:
  rm *.jpg
  rm *.tif
  rm *.py
run:
  python ${fileName}
check:
  rpicam-hello
  
