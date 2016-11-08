PImage img;

void setup() {
  size(410, 400);
  fill(0);
  background (255, 255, 255);
  img = loadImage("/home/pi/imageToSave1.png");
}

void draw() {
  //imageMode(CENTER);
  //image(img, 300, 330, 210, 700);  // Draw image using CENTER mode
  int iStart = new Float(img.height/3).intValue();
  int iHeight = img.height-2*iStart;
  copy(img, 0, 0,img.width,iHeight,90,0,img.width,iHeight);
  save("nunuimageToSave1.png");
  exit();
}
