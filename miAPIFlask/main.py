from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

# URL de la API FastAPI
# Lo declaro a una variable para no tener que escribir todo el URL y evitar errores
API_URL = 'http://localhost:5000'

@app.route('/')
def index():
    # Consultar usuarios desde la API
    response = requests.get(f'{API_URL}/v1/usuarios/')
    
    if response.status_code == 200:
        data = response.json()
        usuarios = data.get('Usuarios', [])
    else:
        usuarios = []
    
    return render_template('index.html', usuarios=usuarios)

@app.route('/Agregar', methods=['POST'])
def agregar_usuario():
    # Obtenemos el usuario del formulario
    nuevo_usuario = {
        'id': request.form.get('id'),
        'nombre': request.form.get('nombre'),
        'edad': request.form.get('edad')
    }
    
    # Hacer POST a la API
    response = requests.post(f'{API_URL}/v1/usuarios/', json=nuevo_usuario)
    
    return redirect(url_for('index'))

@app.route('/eliminar', methods=['POST'])
def eliminar_usuario():
    id = request.form.get('id')
    
    # Hacer DELETE a la API
    response = requests.delete(f'{API_URL}/v1/usuarios/{id}')
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5010, debug=True)


