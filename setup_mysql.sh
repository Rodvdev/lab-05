#!/bin/bash

# Script de configuración para MySQL
echo "🚀 Configurando aplicación Flask con MySQL..."

# Verificar si MySQL está instalado
if ! command -v mysql &> /dev/null; then
    echo "❌ MySQL no está instalado. Por favor instala MySQL primero."
    echo "   En Ubuntu/Debian: sudo apt-get install mysql-server"
    echo "   En macOS: brew install mysql"
    echo "   En Windows: descarga desde https://dev.mysql.com/downloads/mysql/"
    exit 1
fi

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 no está instalado. Por favor instala Python 3 primero."
    exit 1
fi

# Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv venv
fi

# Activar entorno virtual
echo "🔧 Activando entorno virtual..."
source venv/bin/activate

# Instalar dependencias
echo "📥 Instalando dependencias..."
pip install -r requirements.txt

# Crear archivo .env si no existe
if [ ! -f ".env" ]; then
    echo "⚙️  Creando archivo de configuración .env..."
    cat > .env << EOF
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/lab_05
DB_USER=root
DB_PASSWORD=password
DB_PORT=3306
SECRET_KEY=dev-secret-key-change-in-production
FLASK_ENV=development
FLASK_DEBUG=True
EOF
    echo "✅ Archivo .env creado. Por favor edita las credenciales de MySQL según tu configuración."
fi

# Solicitar credenciales de MySQL
echo ""
echo "🔐 Configuración de MySQL:"
read -p "Usuario de MySQL [root]: " mysql_user
mysql_user=${mysql_user:-root}

read -s -p "Contraseña de MySQL: " mysql_password
echo ""

read -p "Puerto de MySQL [3306]: " mysql_port
mysql_port=${mysql_port:-3306}

# Crear base de datos
echo "🗄️  Creando base de datos..."
    mysql -u "$mysql_user" -p"$mysql_password" -P "$mysql_port" -e "CREATE DATABASE IF NOT EXISTS lab_05;"

if [ $? -eq 0 ]; then
    echo "✅ Base de datos creada correctamente"
    
    # Ejecutar script SQL
    echo "📊 Ejecutando script SQL..."
    mysql -u "$mysql_user" -p"$mysql_password" -P "$mysql_port" lab_05 < database.sql
    
    if [ $? -eq 0 ]; then
        echo "✅ Tablas creadas correctamente"
        
        # Actualizar archivo .env con las credenciales reales
        sed -i "s/DB_USER=root/DB_USER=$mysql_user/" .env
        sed -i "s/DB_PASSWORD=password/DB_PASSWORD=$mysql_password/" .env
        sed -i "s/:3306/:$mysql_port/" .env
        sed -i "s/mysql+pymysql:\/\/root:password@localhost:3306/mysql+pymysql:\/\/$mysql_user:$mysql_password@localhost:$mysql_port/" .env
        
        echo "✅ Configuración completada"
        echo ""
        echo "🎉 ¡Todo listo! Para ejecutar la aplicación:"
        echo "   1. Activa el entorno virtual: source venv/bin/activate"
        echo "   2. Ejecuta la aplicación: python run.py"
        echo "   3. Abre tu navegador en: http://localhost:5000"
        
    else
        echo "❌ Error al ejecutar el script SQL"
        exit 1
    fi
else
    echo "❌ Error al crear la base de datos"
    exit 1
fi
