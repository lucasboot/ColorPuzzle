// FUNÇÇOE DO MHA: VELOCIDADE, ACELERAÇÃO E POSIÇÃO, RESPECTIVAMENTE :P
//modification


// ---------------------------------------------

function setup() {
  w = 480
  h = 480
  canvas = createCanvas(w, h)
  canvas.position (245,0)
  char = w/20
  rad = char*2 - 4
}

function draw() {
  background(51)
  fill(255)
  ellipse( mouseX, char, rad, rad)
  for(let i = 1; i <= 10; i++){
    for(let j = 1; j <= 10; j++){
      fill(0)
      ellipse(-char + i*2*char, char + j*2*char, rad, rad)
    }
  }
}
