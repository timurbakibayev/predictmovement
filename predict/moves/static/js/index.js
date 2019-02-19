let mousePressed = false;
let lastX = null, lastY = null;
let ctx = null;
let moves = [];
let currentMove = [];

function InitThis() {
    ctx = document.getElementById('myCanvas').getContext("2d");
    let canvas = $('#myCanvas');

    canvas.mousedown(function (e) {
        mousePressed = true;
        Draw(e.pageX - $(this).offset().left, e.pageY - $(this).offset().top, false);
    });

    canvas.mousemove(function (e) {
        if (mousePressed) {
            Draw(e.pageX - $(this).offset().left, e.pageY - $(this).offset().top, true);
        }
    });

    canvas.mouseup(function (e) {
        mousePressed = false;
        moves.push(currentMove);
        console.log(JSON.stringify(moves));
        console.log(JSON.stringify(moves).length);
    });
    canvas.mouseleave(function (e) {
        mousePressed = false;
    });
}

function Draw(x, y, isDown) {
    if (isDown) {
        ctx.beginPath();
        ctx.strokeStyle = "green";
        ctx.lineWidth = "2";
        ctx.lineJoin = "round";
        ctx.moveTo(lastX, lastY);
        ctx.lineTo(x, y);
        ctx.closePath();
        ctx.stroke();
        currentMove.push({x, y});
    }
    lastX = x;
    lastY = y;
}

function clearArea() {
    // Use the identity matrix while clearing the canvas
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
}

function tryPost() {
    fetch("/",
        {
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            method: "POST",
            body: JSON.stringify(moves),
        })
        .then(res => {
            console.log(res);
        })
}