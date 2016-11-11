PImage img;

void setup() {
  size(410, 400);
  fill(0);
  background (255, 255, 255);
  img = loadImage("/home/pi/toku/imageToSave1.png");
}

void draw() {
  int iStart = new Float(img.height/3).intValue();
  int iHeight = img.height-iStart;
  copy(img, 0, iStart,img.width,iHeight,90,0,img.width,iHeight);
  save("nunuimageToSave2.png");
}
