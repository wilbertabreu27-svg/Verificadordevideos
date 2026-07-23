from flask import Flask, request, jsonify, render_template_string
import os

app = Flask(__name__)

# Tu página web completa incrustada en Python para evitar problemas de conexión
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Analizador de Autenticidad de Medios</title>
    <style>
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            text-align: center; 
            padding: 40px 20px; 
            background-color: #f0f2f5; 
            margin: 0;
        }
        .upload-container { 
            background: white; 
            padding: 40px 30px; 
            border-radius: 16px; 
            box-shadow: 0 6px 20px rgba(0,0,0,0.1); 
            max-width: 450px; 
            margin: auto; 
        }
        h2 { color: #1c1e21; margin-top: 0; }
        p { color: #606770; font-size: 15px; margin-bottom: 25px; }
        input[type="file"] { display: none; }
        .custom-file-btn { 
            display: inline-block;
            background-color: #1877f2; 
            color: white; 
            padding: 14px 28px; 
            border-radius: 8px; 
            cursor: pointer; 
            font-size: 16px; 
            font-weight: bold;
            box-shadow: 0 4px 10px rgba(24, 119, 242, 0.3);
            transition: background-color 0.2s, transform 0.1s;
        }
        .custom-file-btn:hover { background-color: #166fe5; }
        .custom-file-btn:active { transform: scale(0.98); }
        #file-info { margin-top: 20px; font-size: 14px; color: #333; word-break: break-all; }
        #status { margin-top: 20px; font-weight: 600; color: #444; padding: 10px; border-radius: 6px; }
    </style>
</head>
<body>

<div class="upload-container">
    <h2>Verificador de Medios</h2>
    <p>Selecciona un video o un audio de tu dispositivo para verificar su autenticidad.</p>

    <input type="file" id="mediaInput" accept="video/*, audio/*">

    <label for="mediaInput" class="custom-file-btn">
        📁 Buscar Video o Audio
    </label>

    <div id="file-info"></div>
    <div id="status"></div>
</div>

<script>
    const fileInput = document.getElementById('mediaInput');
    const fileInfo = document.getElementById('file-info');
    const statusDisplay = document.getElementById('status');

    fileInput.addEventListener('change', function(event) {
        const file = event.target.files[0];
        
        if (file) {
            fileInfo.innerHTML = `<strong>Archivo seleccionado:</strong> ${file.name} (${(file.size / (1024*1024)).toFixed(2)} MB)`;
            
            statusDisplay.style.color = "#1877f2";
            statusDisplay.innerHTML = "🔄 Subiendo archivo al servidor de análisis...";

            const formData = new FormData();
            formData.append('mediaInput', file);

            // Se conecta a la misma dirección web automáticamente
            fetch('/upload', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                statusDisplay.style.color = "#2e7d32";
                statusDisplay.innerHTML = `✅ ${data.mensaje}`;
            })
            .catch(error => {
                statusDisplay.style.color = "red";
                statusDisplay.innerHTML = "❌ Error de conexión con el servidor.";
                console.error(error);
            });
        } else {
            fileInfo.innerHTML = "";
            statusDisplay.innerHTML = "";
        }
    });
</script>

</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'mediaInput' not in request.files:
        return jsonify({"mensaje": "No se encontró ningún archivo"}), 400
    
    file = request.files['mediaInput']
    
    if file.filename == '':
        return jsonify({"mensaje": "Ningún archivo seleccionado"}), 400
    
    if file:
        # Aquí puedes integrar tus funciones de Python/IA más adelante
        return jsonify({"mensaje": "¡Archivo recibido y procesado por el servidor con éxito!"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
