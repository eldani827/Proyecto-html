# 📦 INSTRUCCIONES PARA TUS COMPAÑEROS - Sincronización de Cambios

## 🎯 ¿Qué hacer cuando haces `git pull`?

Después de descargar los cambios, **SIEMPRE** ejecuta el script de sincronización:

---

### **OPCIÓN 1: Script Automático (RECOMENDADO) ⭐**

#### Para Windows (PowerShell):
```powershell
# 1. Abre PowerShell en la carpeta del proyecto

# 2. Ejecuta:
.\sync.ps1

# 3. ¡Listo! El script lo hace todo automáticamente
```

#### Para macOS/Linux (Terminal):
```bash
# 1. Abre Terminal en la carpeta del proyecto

# 2. Ejecuta:
python sync_database.py

# 3. ¡Listo!
```

---

### **OPCIÓN 2: Comandos Manuales**

Si el script no funciona, ejecuta esto en orden:

```bash
# 1. Aplicar migraciones
python manage.py migrate --verbosity=2

# 2. Limpiar caché
python manage.py clear_cache

# 3. Recolectar estáticos
python manage.py collectstatic --noinput

# 4. Verificar integridad
python manage.py check

# 5. Iniciar el servidor
python manage.py runserver
```

---

## 🚀 Después de Sincronizar

Una vez sincronizado, puedes:

1. **Iniciar el servidor**:
   ```bash
   python manage.py runserver
   ```

2. **Acceder a la aplicación**:
   - http://localhost:8000/login

3. **Acceder al panel de administración**:
   - http://localhost:8000/administrador/
   - (Requiere estar logueado con una cuenta de administrador)

---

## ⚠️ Problemas Comunes

### Error: "Table doesn't exist"
```bash
python manage.py migrate
```

### Error: "AttributeError: module has no attribute"
```bash
# Limpiar caché de Python
python manage.py clear_cache
# Si no funciona, elimina carpetas __pycache__
```

### Error: "ModuleNotFoundError"
```bash
# Reinstalar dependencias
pip install -r requirements.txt
```

### Base de datos corrupta (Solo desarrollo)
```bash
# ⚠️ ESTO BORRA TODOS LOS DATOS LOCALES
del db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

---

## 📋 Orden de Sincronización Recomendado

Cada vez que hagas `git pull`:

```
┌─────────────────────────────────────┐
│ 1. git pull origin main             │
├─────────────────────────────────────┤
│ 2. (Sistema) Ejecutar sync.ps1 o    │
│            python sync_database.py  │
├─────────────────────────────────────┤
│ 3. python manage.py runserver       │
├─────────────────────────────────────┤
│ 4. Abrir http://localhost:8000      │
└─────────────────────────────────────┘
```

---

## ✅ Checklist de Verificación

Después de sincronizar, verifica que:

- [ ] **El servidor inicia sin errores**
  - `python manage.py runserver`
  - Deberías ver "Starting development server at http://127.0.0.1:8000/"

- [ ] **Puedes acceder al login**
  - Abre http://localhost:8000/login
  - Deberías ver el formulario de login

- [ ] **Puedes ver el panel de administración**
  - Inicia sesión
  - Ve a http://localhost:8000/administrador/
  - Deberías ver el dashboard

- [ ] **Las migraciones están aplicadas**
  ```bash
  python manage.py showmigrations
  ```
  - Todas las migraciones deben tener [X] (aplicadas)

---

## 🆘 Si Aún Tienes Problemas

1. **Captura la **salida exacta** del error:**
   - Copia TODO el mensaje de error que ves en la terminal
   - No solo la última línea

2. **Intenta sincronizar nuevamente:**
   ```bash
   python sync_database.py  # o .\sync.ps1
   ```

3. **Contacta a Santiago** con:
   - El paso exacto donde falla (ej: "en migrate")
   - El mensaje de error completo
   - Tu sistema operativo (Windows/Mac/Linux)

---

## 💡 Consejos Importantes

- ✅ **Siempre sincroniza después de hacer `git pull`**
- ✅ **Usa el script automático, es más seguro**
- ✅ **Si cambias manualmente la BD, sincroniza nuevamente**
- ✅ **En Windows, puede que necesites ejecutar como Administrador**

---

## 📞 Sistema de Creación de Usuarios

**IMPORTANTE**: A partir de ahora, para crear cuentas de usuario:

1. Ve a http://localhost:8000/administrador/
2. Haz click en "Gestión de Usuarios"
3. Haz click en "➕ Crear Nuevo Usuario"
4. Completa el formulario:
   - **Usuario**: El nombre de usuario
   - **Email**: El correo
   - **Contraseña**: Mínimo 8 caracteres, 1 mayúscula, 1 número o símbolo
   - **Roles**: Selecciona qué tipo de acceso tiene

**El usuario estará ACTIVO inmediatamente y puede acceder de una vez.**

---

**Última actualización**: 4 de marzo de 2026  
**Versión**: 2.0 (Con sistema de usuarios funcional)
