class Particle {
    constructor(container) {
        this.container = container;
        this.element = document.createElement('div');
        this.element.className = 'particle';
        this.size = Math.random() * 15 + 5;
        this.opacity = Math.random() * 0.5 + 0.2;
        this.x = Math.random() * 100;
        this.y = Math.random() * 100;
        this.speedX = Math.random() * 0.5 - 0.25;
        this.speedY = Math.random() * 0.5 - 0.25;
        this.rotation = Math.random() * 360;
        this.rotationSpeed = Math.random() * 2 - 1;

        this.element.style.cssText = `
            position: absolute;
            width: ${this.size}px;
            height: ${this.size}px;
            background: rgba(255, 255, 255, ${this.opacity});
            border-radius: 50%;
            left: ${this.x}%;
            top: ${this.y}%;
            transform: rotate(${this.rotation}deg);
            pointer-events: none;
        `;

        this.container.appendChild(this.element);
    }

    update() {
        this.x += this.speedX;
        this.y += this.speedY;
        this.rotation += this.rotationSpeed;

        // Wrap around screen
        if (this.x > 100) this.x = 0;
        if (this.x < 0) this.x = 100;
        if (this.y > 100) this.y = 0;
        if (this.y < 0) this.y = 100;

        this.element.style.left = `${this.x}%`;
        this.element.style.top = `${this.y}%`;
        this.element.style.transform = `rotate(${this.rotation}deg)`;
    }
}

// Initialize particles
document.addEventListener('DOMContentLoaded', () => {
    const container = document.querySelector('.background-animation');
    const particles = [];
    const particleCount = 20;

    // Create particles
    for (let i = 0; i < particleCount; i++) {
        particles.push(new Particle(container));
    }

    // Animation loop
    function animate() {
        particles.forEach(particle => particle.update());
        requestAnimationFrame(animate);
    }

    animate();

    // Add mouse interaction
    document.addEventListener('mousemove', (e) => {
        const mouseX = e.clientX / window.innerWidth;
        const mouseY = e.clientY / window.innerHeight;

        particles.forEach(particle => {
            const distX = (mouseX * 100) - particle.x;
            const distY = (mouseY * 100) - particle.y;
            const distance = Math.sqrt(distX * distX + distY * distY);

            if (distance < 20) {
                particle.speedX += distX * 0.002;
                particle.speedY += distY * 0.002;
            }
        });
    });
});
