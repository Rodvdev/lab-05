from flask import Blueprint, request, render_template, redirect, url_for, flash, jsonify
from services.profesor_service import ProfesorService

profesor_bp = Blueprint('profesor', __name__)

@profesor_bp.route('/')
def index():
    """Lista todos los profesores"""
    result = ProfesorService.get_active_profesores()
    if result['status'] != 200:
        flash('Error al cargar los profesores', 'error')
        return render_template('profesores/index.html', profesores=[])
    
    profesores = result['data']
    return render_template('profesores/index.html', profesores=profesores)

@profesor_bp.route('/create', methods=['GET', 'POST'])
def create():
    """Crear un nuevo profesor"""
    if request.method == 'POST':
        data = {
            'nombre': request.form['nombre'],
            'apellido': request.form['apellido'],
            'email': request.form['email'],
            'telefono': request.form.get('telefono'),
            'especialidad': request.form['especialidad'],
            'salario': request.form['salario'],
            'fecha_contratacion': request.form['fecha_contratacion']
        }
        
        result = ProfesorService.create_profesor(data)
        if result['status'] == 201:
            flash('Profesor creado exitosamente', 'success')
            return redirect(url_for('profesor.index'))
        else:
            flash(result['error'], 'error')
    
    return render_template('profesores/create.html')

@profesor_bp.route('/<int:id>')
def show(id):
    """Mostrar detalles de un profesor"""
    result = ProfesorService.get_profesor(id)
    if result['status'] != 200:
        flash(result['error'], 'error')
        return redirect(url_for('profesor.index'))
    
    profesor = result['data']
    return render_template('profesores/show.html', profesor=profesor)

@profesor_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):
    """Editar un profesor"""
    if request.method == 'POST':
        data = {
            'nombre': request.form['nombre'],
            'apellido': request.form['apellido'],
            'email': request.form['email'],
            'telefono': request.form.get('telefono'),
            'especialidad': request.form['especialidad'],
            'salario': request.form['salario'],
            'fecha_contratacion': request.form['fecha_contratacion']
        }
        
        result = ProfesorService.update_profesor(id, data)
        if result['status'] == 200:
            flash('Profesor actualizado exitosamente', 'success')
            return redirect(url_for('profesor.show', id=id))
        else:
            flash(result['error'], 'error')
    
    # GET request - mostrar formulario de edición
    result = ProfesorService.get_profesor(id)
    if result['status'] != 200:
        flash(result['error'], 'error')
        return redirect(url_for('profesor.index'))
    
    profesor = result['data']
    return render_template('profesores/edit.html', profesor=profesor)

@profesor_bp.route('/<int:id>/delete', methods=['POST'])
def delete(id):
    """Eliminar un profesor"""
    result = ProfesorService.delete_profesor(id)
    if result['status'] == 200:
        flash('Profesor eliminado exitosamente', 'success')
    else:
        flash(result['error'], 'error')
    
    return redirect(url_for('profesor.index'))

# API Routes (opcional - para uso con AJAX)
@profesor_bp.route('/api', methods=['GET'])
def api_list():
    """API endpoint para listar profesores"""
    result = ProfesorService.get_active_profesores()
    return jsonify(result), result['status']

@profesor_bp.route('/api/<int:id>', methods=['GET'])
def api_show(id):
    """API endpoint para mostrar un profesor"""
    result = ProfesorService.get_profesor(id)
    return jsonify(result), result['status']

@profesor_bp.route('/api', methods=['POST'])
def api_create():
    """API endpoint para crear profesor"""
    data = request.get_json()
    result = ProfesorService.create_profesor(data)
    return jsonify(result), result['status']

@profesor_bp.route('/api/<int:id>', methods=['PUT'])
def api_update(id):
    """API endpoint para actualizar profesor"""
    data = request.get_json()
    result = ProfesorService.update_profesor(id, data)
    return jsonify(result), result['status']

@profesor_bp.route('/api/<int:id>', methods=['DELETE'])
def api_delete(id):
    """API endpoint para eliminar profesor"""
    result = ProfesorService.delete_profesor(id)
    return jsonify(result), result['status']
