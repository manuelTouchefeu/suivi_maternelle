"use strict";

function getRandomInt(min, max) {
    return min + Math.floor(Math.random() * (max - min));
}

window.addEventListener('load' , function() {
    var canvas = document.getElementById('canvas');
    var ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    function Blade(x, y, pt1X, pt1Y, pt2X, pt2Y, endX, endY, angle, color) {
        this.color =  "rgb(" + color + ", " + color + ", " + color + ")";
        this.x = x;
        this.y = y;
        this.pt1X = pt1X;
        this.pt1Y = pt1Y;
        this.pt2X = pt2X;
        this.pt2Y = pt2Y;
        this.endX = endX;
        this.endY = endY;
        this.angle = angle;
        this.state = [true, false][getRandomInt(0,1)];     
        //console.log(green);
        this.draw = function(angle) {
            ctx.save();
            ctx.beginPath();
            ctx.strokeStyle = this.color;
            ctx.translate(this.x, this.y);
            if (this.endX == 10 || this.endX == -10) {
                this.state = !this.state;
            }
            ctx.rotate(this.angle*Math.PI/180);
            this.endX = (this.state ? this.endX-1 : this.endX+1);
            ctx.bezierCurveTo(this.pt1X, this.pt1Y, this.pt2X, this.pt2Y ,this.endX, this.endY);
            ctx.stroke();
            ctx.restore();
        }
    }

    var blades = [];
    for(var i=0; i<1500; i++) {
        blades.push(new Blade(getRandomInt(0, canvas.width), getRandomInt(0, canvas.height),
                              0, 0,
                              getRandomInt(0, -50), getRandomInt(0, -150),
                              getRandomInt(0, 10), getRandomInt(-150, -200),
                              getRandomInt(0, 10),
                              getRandomInt(0, 200)));
    }

    function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height)
        ctx.lineWidth = 1;
        for(var i=0; i<blades.length; i++) {
            blades[i].draw();
        }
    }
    var myInterval = setInterval(animate, 30);

}, false);
