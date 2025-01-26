document.addEventListener("DOMContentLoaded", () => {
    const canvas = document.getElementById("canvas");
    const ctx = canvas.getContext("2d");

    // Set canvas size
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    // Track mouse position
    let mousePos = { x: canvas.width / 2, y: canvas.height / 2 };

    class Circle {
        constructor(radius, x, y, mass = 1) {
            this.radius = radius;
            this.pos = { x, y };
            this.vel = { x: 0, y: 0 };
            this.acc = { x: 0, y: 0 };
            this.mass = mass;
            this.friction = 0.998;
        }

        // Update position
        update() {
            this.vel.x *= this.friction;
            this.vel.y *= this.friction;
            this.vel.x += this.acc.x;
            this.vel.y += this.acc.y;
            this.pos.x += this.vel.x;
            this.pos.y += this.vel.y;
            this.acc.x = 0;
            this.acc.y = 0;
        }

        // Apply a force
        applyForce(force) {
            this.acc.x += force.x / this.mass;
            this.acc.y += force.y / this.mass;
        }

        // Move circle toward target
        moveTowards(target, speed) {
            const dx = target.x - this.pos.x;
            const dy = target.y - this.pos.y;
            const distance = Math.sqrt(dx ** 2 + dy ** 2);

            // Prevent over-adjustment near the target
            if (distance > 1) {
                const force = { x: (dx / distance) * speed, y: (dy / distance) * speed };
                this.applyForce(force);
            }
        }

        // Draw the circle
        draw() {
            ctx.beginPath();
            ctx.arc(this.pos.x, this.pos.y, this.radius, 0, 2 * Math.PI);
            ctx.fillStyle = "#FF0000";
            ctx.fill();
        }
    }

    // Create an array of circles
    const circles = Array.from({ length: 100 }, (_, i) => new Circle(5, 100 + i * 20, 100));

    // Update mouse position on canvas
    canvas.addEventListener("mousemove", (event) => {
        mousePos = { x: event.clientX, y: event.clientY };
    });

    // Resize canvas when window size changes
    window.addEventListener("resize", () => {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    });

    // Animation loop
    function animate() {
        ctx.fillStyle = "rgba(0, 0, 0, 0.1)"; // Fading trail effect
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        circles.forEach(circle => {
            circle.moveTowards(mousePos, 0.5); // Move toward the mouse
            circle.update(); // Update position and velocity
            circle.draw(); // Draw the circle
        });

        requestAnimationFrame(animate); // Repeat the loop
    }

    animate(); // Start the animation
});
