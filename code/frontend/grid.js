document.addEventListener('DOMContentLoaded', function() {
    const canvas = document.getElementById("canvas");
    const ctx = canvas.getContext("2d");
    const p = 10;
    const cw = 20;
    const bw = 500;
    const bh = 500;

    const cols = bw / cw;
    const rows = bh / cw;

    canvas.width = bw + 2*p;
    canvas.height = bh + 2*p;
    // drawGrid(ctx);

    function drawGrid(ctx) {
        ctx.strokeStyle = '#ccc';
        for (let x = 0; x <= bw; x+= cw) {
            ctx.beginPath();
            ctx.moveTo(p + x, p);
            ctx.lineTo(p + x, p + bh);
            ctx.stroke();
        }
        for (let y = 0; y <= bh; y+= cw) {
            ctx.beginPath();
            ctx.moveTo(p, y + p);
            ctx.lineTo(p + bw, y + p);
            ctx.stroke();
        }
    }

    function drawImage() {
        fetch(`http://localhost:9099/coords/${cols}/${rows}/`)
        .then(response => response.json())
        .then(data => {
            ctx.fillStyle = "lightgreen";
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            data.coords.forEach(item => {
                ctx.fillStyle = item.color;
                // console.table(item);

                const x = item.x * cw + p;
                const y = item.y * cw + p;

                if (item.draw) {
                    ctx.fillRect(x, y, cw, cw);
                }
            });
        })
        .catch(err => console.error('Error fetching image data:', err));
    }

    setInterval(drawImage, 1000);
});



