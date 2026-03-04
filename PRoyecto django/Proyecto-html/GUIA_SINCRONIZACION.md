# 🔧 Guía de Sincronización - Solucionar Errores de Base de Datos

## 🎯 Problema

Al hacer `git pull` de los cambios, obtienes errores como:
- ❌ "Table does not exist"
- ❌ "Migration conflicts"
- ❌ "Database connection failed"
- ❌ "Schema mismatch"

## ✅ Solución Rápida

### **Para Windows (PowerShell)**

1. **Abre PowerShell** en la carpeta del proyecto
   ```powershell
   # Ve a la carpeta del proyecto
   cd "c:\...\Proyecto-html\PRoyecto django\Proyecto-html"
   ```

2. **Ejecuta el script de sincronización**
   ```powershell
   .\sync.ps1
   ```
   
   *Este script automáticamente*:
   - Aplica todas las migraciones ✓
   - Limpia la caché de Python ✓
   - Recolecta archivos estáticos ✓
   - Verifica la integridad del proyecto ✓

3. **Listo!** Ahora puedes iniciar el servidor
   ```powershell
   python manage.py runserver
   ```

### **Para macOS/Linux** (o Terminal)

1. **Abre Terminal** en la carpeta del proyecto

2. **Ejecuta el script de sincronización**
   ```bash
   python sync_database.py
   ```

3. **Listo!** Ahora puedes iniciar el servidor
   ```bash
   python manage.py runserver
   ```

---

## 📋 Pasos Manuales (Si el script no funciona)

Si el script automático no resuelve el problema, sigue estos pasos manualmente:

### 1️⃣ Verifica las migraciones pendientes
```bash
python manage.py migrate --plan
```

### 2️⃣ Aplica las migraciones
```bash
python manage.py migrate --verbosity=2
```

### 3️⃣ Limpia la caché
```bash
python manage.py clear_cache
```

### 4️⃣ Recolecta archivos estáticos (IMPORTANTE)
```bash
python manage.py collectstatic --noinput
```

### 5️⃣ Verifica la integridad
```bash
python manage.py check
```

### 6️⃣ Inicia el servidor
```bash
python manage.py runserver
```

---

## 🆘 Si Aún No Funciona

### Opción A: Restaurar Base de Datos (Desarrollo Solamente)

**⚠️ ADVERTENCIA: Esto borrará TODOS los datos locales**

```bash
# 1. Elimina la base de datos actual
del db.sqlite3

# 2. Crea una nueva base de datos
python manage.py migrate

# 3. Crea un nuevo superusuario
python manage.py createsuperuser
```

### Opción B: Verificar Instalación de Dependencias

```bash
# Reinstala todas las dependencias
pip install -r requirements.txt

# Luego ejecuta la sincronización
python sync_database.py
```

### Opción C: Verificar Python y Virtualenv

```bash
# Verifica tu versión de Python
python --version
# Debe ser 3.8 o superior

# Activa el virtualenv
source venv/bin/activate  # macOS/Linux
venv\Scripts\Activate.ps1  # Windows PowerShell
```

---

## 🔍 Diagnóstico

Para diagnosticar el problema específico:

```bash
# Ver todas las migraciones
python manage.py showmigrations

# Ver migraciones de una app específica
python manage.py showmigrations Gesicom

# Ver plan de migraciones pendientes
python manage.py migrate --plan

# Ver logs detallados
python manage.py migrate --verbosity=3
```

---

## 📞 Contacto

Si después de seguir esta guía sigues teniendo problemas:

1. **Captura el error exacto**: Copia todo el mensaje de error
2. **Intenta los pasos manuales**: Anota dónde falla exactamente
3. **Contacta a Santiago**: Envía el error exacto y el paso donde falló

---

## ✅ Checklist de Verificación

Después de sincronizar, verifica que:

- [ ] El servidor inicia sin errores: `python manage.py runserver`
- [ ] Puedes acceder a http://localhost:8000/login
- [ ] Puedes acceder a http://localhost:8000/administrador (requiere login)
- [ ] La base de datos tiene tus datos
- [ ] Las migraciones están todas aplicadas: `python manage.py showmigrations`

---

**Última actualización**: 4 de marzo de 2026  
**Estado**: ✅ Funcional
