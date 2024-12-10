// Obtiene una referencia al elemento HTML canvas y su contexto de dibujo 2D
// El contexto (ctx) es el objeto que proporciona los métodos para dibujar
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');

// Variables de estado para el dibujo
let drawing = false;  // Indica si se está dibujando actualmente
let color = 'black';  // Color actual del pincel

// Coordenadas del último punto dibujado
let lastX = 0;
let lastY = 0;

// Configuración de los event listeners del canvas
// Similar a addActionListener en Java o connect en Qt
canvas.addEventListener('mousedown', startDrawing);  // Al presionar el botón del mouse
canvas.addEventListener('mouseup', stopDrawing);     // Al soltar el botón del mouse
canvas.addEventListener('mousemove', draw);          // Al mover el mouse
canvas.addEventListener('mouseout', stopDrawing);    // Cuando el mouse sale del canvas

// Se ejecuta cuando el usuario presiona el botón del mouse
// 'e' es el evento que contiene información como las coordenadas del mouse
function startDrawing(e) {
    drawing = true;
    // Destructuring assignment en ES6 - asigna las coordenadas actuales del mouse
    [lastX, lastY] = [e.offsetX, e.offsetY];
}

// Se ejecuta cuando el usuario suelta el botón del mouse
function stopDrawing(){
    drawing = false;
    // Reinicia las coordenadas del último punto
    [lastX, lastY] = [0, 0];
}

// Función principal de dibujo - se ejecuta cada vez que el mouse se mueve
function draw(e) {
    // Patrón guard clause: si no estamos dibujando, salir inmediatamente
    if (!drawing) return;

    // Configura los atributos del "pincel"
    ctx.strokeStyle = color;     // Color de la línea
    ctx.lineWidth = 10;         // Grosor de la línea en píxeles
    ctx.lineCap = 'round';      // Extremos redondeados en la línea
    ctx.lineJoin = 'round';     // Uniones redondeadas entre segmentos

    // Comienza un nuevo trazo
    ctx.beginPath();
    // Mueve el "pincel" al último punto registrado
    ctx.moveTo(lastX, lastY);
    // Dibuja una línea hasta la posición actual del mouse
    ctx.lineTo(e.offsetX, e.offsetY);
    // Renderiza la línea en el canvas
    ctx.stroke();

    // Actualiza las coordenadas del último punto
    [lastX, lastY] = [e.offsetX, e.offsetY];
}

// Event listeners para los botones de colores
// Funciones flecha (=>) son similares a lambdas en otros lenguajes
document.getElementById('color-black').addEventListener('click', () => color = 'black');
document.getElementById('color-red').addEventListener('click', () => color = 'red');
document.getElementById('color-blue').addEventListener('click', () => color = 'blue');

// Event listener para el botón de limpiar
document.getElementById('clear').addEventListener('click', () => {
    // clearRect borra un rectángulo en el canvas - en este caso, todo el canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);
})

// Event listener para guardar el dibujo
document.getElementById('guardar').addEventListener('click', (e) => {
    // Convierte el contenido del canvas a una URL de datos en formato PNG
    const imageData = canvas.toDataURL('image/png');
    // Almacena la URL de datos en un input hidden del formulario
    document.getElementById('canvasData').value = imageData;
});