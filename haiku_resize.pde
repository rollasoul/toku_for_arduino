PImage img;

void setup() {
  size(300, 1200);
  fill(0);
  background (255, 255, 255);
  img = loadImage("home/pi/toku/imageToSave1.png");
  img.resize(200, 0);
  image(img, 0, 0);
  save("/home/pi/toku/imageToSave1.png");
  exit();
}
