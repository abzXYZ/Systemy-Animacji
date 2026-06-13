import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

const info = document.getElementById('info');
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer();

renderer.setSize(window.innerWidth, window.innerHeight);
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.0;
renderer.outputColorSpace = THREE.SRGBColorSpace;
document.body.appendChild(renderer.domElement);

const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.minDistance = 1;
controls.maxDistance = 50;

camera.position.z = 5;
controls.update();

const ROTATION_SPEED = 0.5; // rad/s

const ambientLight = new THREE.AmbientLight(0xffffff, 0.15);
scene.add(ambientLight);

const keyLight = new THREE.DirectionalLight(0xffe0b0, 3.0);
keyLight.position.set(-3, 4, 3);
scene.add(keyLight);

const fillLight = new THREE.DirectionalLight(0xa0c0ff, 1.0);
fillLight.position.set(4, 1, 2);
scene.add(fillLight);

const rimLight = new THREE.DirectionalLight(0x00ffcc, 1.8);
rimLight.position.set(0, -2, -5);
scene.add(rimLight);

addEventListener("resize", () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});

function fitCameraToModel(model) {
    const box = new THREE.Box3().setFromObject(model);
    const center = box.getCenter(new THREE.Vector3());
    const size = box.getSize(new THREE.Vector3());

    // Wybiera oś modelu, na której jest on największy
    const maxAxis = Math.max(size.x, size.y, size.z);

    // Dopasowuje odległość kamery od modelu
    const fovRad = THREE.MathUtils.degToRad(camera.fov);
    const distance = (maxAxis / 2) / Math.tan(fovRad / 2) * 1.25;
    camera.position.copy(center);
    camera.position.z += distance;

    // Dopasuj max i min distance kamery
    controls.target.copy(center);
    controls.minDistance = distance * 0.1;
    controls.maxDistance = distance * 5;
    controls.update();
}

function loadGLTF(url) {
    return new Promise((resolve, reject) => {
        new GLTFLoader().load(url, resolve, undefined, reject);
    });
}

let model = null;

async function loadModel() {
    try {
        const gltf = await loadGLTF('/biomech_13.glb');
        model = gltf.scene;
        scene.add(model);

        let meshCount = 0;
        model.traverse((node) => {
            if (node.isMesh) {
                console.log(`[${meshCount}] ${node.name}`);
                meshCount++;
            }
        });

        fitCameraToModel(model);

        info.textContent = `Wczytano ${meshCount} mesh-y`;
    } catch (error) {
        console.error(error);
        info.textContent = `BŁĄD WCZYTYWANIA: ${error.message ?? error}`;
    }
}

loadModel();

const clock = new THREE.Clock();

function animate() {
    requestAnimationFrame(animate);

    const delta = clock.getDelta();

    if (model) {
        model.rotation.y += ROTATION_SPEED * delta;
    }

    controls.update();
    renderer.render(scene, camera);
}

animate();