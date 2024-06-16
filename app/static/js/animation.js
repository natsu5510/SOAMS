// Get the container
const container = document.getElementById('animation-container');

// Check if the container is correctly referenced
if (container) {
    // Set up the scene, camera, and renderer
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, container.clientWidth / container.clientHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(container.clientWidth, container.clientHeight);

    // Set the background color of the renderer to match your interface background color
    renderer.setClearColor(0xf8f9fc); // Replace with your interface background color
    container.appendChild(renderer.domElement);

    // Add lighting to the scene
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
    scene.add(ambientLight);

    const pointLight = new THREE.PointLight(0xffffff, 0.5);
    pointLight.position.set(10, 10, 10);
    scene.add(pointLight);

    // Load font and create 3D text
    const loader = new THREE.FontLoader();
    loader.load('https://threejs.org/examples/fonts/helvetiker_regular.typeface.json', function (font) {
        const textGeometry = new THREE.TextGeometry('Welcome!', {
            font: font,
            size: 2,
            height: 0.5,
            curveSegments: 12,
            bevelEnabled: true,
            bevelThickness: 0.1,
            bevelSize: 0.1,
            bevelOffset: 0,
            bevelSegments: 5
        });

        // Create a material with Phong shading for more realistic lighting
        const textMaterial = new THREE.MeshPhongMaterial({ color: 0xff0000, shininess: 100 });
        const textMesh = new THREE.Mesh(textGeometry, textMaterial);

        // Position the text
        textMesh.position.set(-5, 0, 0);

        // Add text to the scene
        scene.add(textMesh);

        // Set initial scale for animation
        textMesh.scale.set(0.1, 0.1, 0.1);

        // Animation loop
        function animate() {
            requestAnimationFrame(animate);

            // Rotate the text for some animation effect
            textMesh.rotation.y += 0.03; // Increase rotation speed

            // Gradually scale up the text
            if (textMesh.scale.x < 1) {
                textMesh.scale.multiplyScalar(1.02); // Gradual scale increase factor
            }

            renderer.render(scene, camera);
        }

        // Start the animation
        animate();
    });

    // Set the camera position
    camera.position.z = 10;
} else {
    console.error('Cannot find animation container');
}
