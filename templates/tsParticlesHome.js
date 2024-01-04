tsParticles.load("tsparticles", {
    fpsLimit: 30,
    interactivity: {
        detect_on: "canvas",
        events: {
            onclick: { enable: true, mode: "push" },
            onhover: {
                enable: true,
                mode: "repulse",
                parallax: { enable: false, force: 60, smooth: 10 }
            },
            resize: true
        },
        modes: {
            bubble: { distance: 400, duration: 2, opacity: 1, size: 40, speed: 3 },
            grab: { distance: 400, links: { opacity: 1 } },
            push: { quantity: 1 },
            remove: { quantity: 2 },
            repulse: { distance: 320, duration: 0.4 }
        }
    },
    particles: {
        color: { value: "random" },
        links: {
            color: "random",
            distance: 500,
            enable: false,
            opacity: 1,
            width: 1
        },
        move: {
            attract: { enable: false, rotateX: 600, rotateY: 1200 },
            bounce: true,
            direction: "none",
            enable: true,
            out_mode: "out",
            random: false,
            speed: 1,
            straight: false
        },
        rotate: {
            animation: {
                enable: true,
                speed: .5,
                sync: false
            }
        },
        number: { density: { enable: true, area: 800 }, value: 8 },
        opacity: {
            animation: { enable: true, minimumValue: 0.9, speed: .1, sync: false },
            random: false,
            value: 1
        },
        shape: {
            character: [
                {
                    fill: true,
                    font: 'Helvetica Neue',
                    style: "",
                    value: ['Python', 'AQI', 'ML', 'AI', 'Plotly', 'Flask', 'SARIMAX', 'Seaborn'],
                    weight: "200"
                }
            ],
            image: {
                height: 100,
                replace_color: true,
                // src: "images/github.svg",
                width: 100
            },
            polygon: { nb_sides: 5 },
            stroke: { color: "random", width: 1 },
            type: "char"
        },
        size: {
            anim: { enable: true, minimumValue: 2, speed: 1, sync: false },
            random: { minimumValue: 2, enable: true },
            value: 20
        }
    },
    detectRetina: true
});
