# Documentación de APIs - Proyecto Backend Parcial 2

Este documento contiene la documentación detallada y ejemplos de uso de las APIs actualmente implementadas en el proyecto, basándose en las definiciones en [main.py](file:///c:/Users/Horizonte/Desktop/Proyecto%20Backend%20Parcial%202/main.py) y los esquemas en [schemas.py](file:///c:/Users/Horizonte/Desktop/Proyecto%20Backend%20Parcial%202/schemas.py).

---

## Resumen de Endpoints Disponibles

| Categoría | Método | Endpoint | Descripción | Estado/Código |
| :--- | :--- | :--- | :--- | :--- |
| **General** | `GET` | `/` | Comprobación de estado inicial (Root) | `200 OK` |
| **Vehículos** | `POST` | `/vehiculos` | Crear un nuevo vehículo | `201 Created` |
| | `GET` | `/vehiculos` | Obtener lista de todos los vehículos | `200 OK` |
| | `GET` | `/vehiculos/{id}` | Obtener detalles de un vehículo por ID | `200 OK` / `404 Not Found` |
| | `PUT` | `/vehiculos/{id}` | Actualizar parcialmente un vehículo | `200 OK` / `404 Not Found` |
| | `DELETE`| `/vehiculos/{id}` | Eliminar un vehículo por ID | `200 OK` / `404 Not Found` |
| **Calles** | `POST` | `/calles` | Crear una nueva calle | `201 Created` |
| | `GET` | `/calles` | Obtener lista de todas las calles | `200 OK` |
| | `GET` | `/calles/{id}` | Obtener detalles de una calle por ID | `200 OK` / `404 Not Found` |
| | `PUT` | `/calles/{id}` | Actualizar parcialmente una calle | `200 OK` / `404 Not Found` |
| | `DELETE`| `/calles/{id}` | Eliminar una calle por ID | `200 OK` / `404 Not Found` |

> [!NOTE]
> Los modelos de datos y esquemas para **Estacionamientos** y **Registros** están definidos en [models.py](file:///c:/Users/Horizonte/Desktop/Proyecto%20Backend%20Parcial%202/models.py) y [schemas.py](file:///c:/Users/Horizonte/Desktop/Proyecto%20Backend%20Parcial%202/schemas.py), pero actualmente **no** cuentan con endpoints implementados en [main.py](file:///c:/Users/Horizonte/Desktop/Proyecto%20Backend%20Parcial%202/main.py).

---

## 1. Endpoints de Vehículos

### Crear Vehículo
Crea un nuevo registro de vehículo en la base de datos.
- **URL:** `/vehiculos`
- **Método:** `POST`
- **Cuerpo de la Petición (JSON):**
  ```json
  {
    "vehiculoDescripcion": "Toyota Hilux Blanca"
  }
  ```

#### Ejemplo de Petición (cURL):
```bash
curl -X POST "http://localhost:8000/vehiculos" \
     -H "Content-Type: application/json" \
     -d '{"vehiculoDescripcion": "Toyota Hilux Blanca"}'
```

#### Respuesta de Éxito (`201 Created`):
```json
{
  "idVehiculo": 1,
  "vehiculoDescripcion": "Toyota Hilux Blanca"
}
```

---

### Obtener Todos los Vehículos
Retorna la lista de todos los vehículos registrados.
- **URL:** `/vehiculos`
- **Método:** `GET`

#### Ejemplo de Petición (cURL):
```bash
curl -X GET "http://localhost:8000/vehiculos"
```

#### Respuesta de Éxito (`200 OK`):
```json
[
  {
    "idVehiculo": 1,
    "vehiculoDescripcion": "Toyota Hilux Blanca"
  },
  {
    "idVehiculo": 2,
    "vehiculoDescripcion": "Ford Fiesta Azul"
  }
]
```

---

### Obtener Vehículo por ID
Obtiene la información de un vehículo específico usando su ID.
- **URL:** `/vehiculos/{id}`
- **Método:** `GET`

#### Ejemplo de Petición (cURL):
```bash
curl -X GET "http://localhost:8000/vehiculos/1"
```

#### Respuesta de Éxito (`200 OK`):
```json
{
  "idVehiculo": 1,
  "vehiculoDescripcion": "Toyota Hilux Blanca"
}
```

#### Respuesta de Error (`404 Not Found`):
```json
{
  "detail": "Vehiculo no encontrado"
}
```

---

### Actualizar Vehículo
Actualiza la descripción de un vehículo existente por su ID. Permite actualizaciones parciales.
- **URL:** `/vehiculos/{id}`
- **Método:** `PUT`
- **Cuerpo de la Petición (JSON):**
  ```json
  {
    "vehiculoDescripcion": "Toyota Hilux Gris Plata"
  }
  ```

#### Ejemplo de Petición (cURL):
```bash
curl -X PUT "http://localhost:8000/vehiculos/1" \
     -H "Content-Type: application/json" \
     -d '{"vehiculoDescripcion": "Toyota Hilux Gris Plata"}'
```

#### Respuesta de Éxito (`200 OK`):
```json
{
  "idVehiculo": 1,
  "vehiculoDescripcion": "Toyota Hilux Gris Plata"
}
```

#### Respuesta de Error (`404 Not Found`):
```json
{
  "detail": "Vehiculo no encontrado"
}
```

---

### Eliminar Vehículo
Elimina un vehículo de la base de datos utilizando su ID.
- **URL:** `/vehiculos/{id}`
- **Método:** `DELETE`

#### Ejemplo de Petición (cURL):
```bash
curl -X DELETE "http://localhost:8000/vehiculos/1"
```

#### Respuesta de Éxito (`200 OK`):
Retorna el objeto que ha sido eliminado.
```json
{
  "idVehiculo": 1,
  "vehiculoDescripcion": "Toyota Hilux Gris Plata"
}
```

#### Respuesta de Error (`404 Not Found`):
```json
{
  "detail": "Vehiculo no encontrado"
}
```

---

## 2. Endpoints de Calles

### Crear Calle
Crea una nueva calle en la base de datos.
- **URL:** `/calles`
- **Método:** `POST`
- **Cuerpo de la Petición (JSON):**
  ```json
  {
    "nombreCalle": "Av. Siempreviva"
  }
  ```

#### Ejemplo de Petición (cURL):
```bash
curl -X POST "http://localhost:8000/calles" \
     -H "Content-Type: application/json" \
     -d '{"nombreCalle": "Av. Siempreviva"}'
```

#### Respuesta de Éxito (`201 Created`):
```json
{
  "idCalle": 1,
  "nombreCalle": "Av. Siempreviva"
}
```

---

### Obtener Todas las Calles
Retorna la lista de todas las calles registradas.
- **URL:** `/calles`
- **Método:** `GET`

#### Ejemplo de Petición (cURL):
```bash
curl -X GET "http://localhost:8000/calles"
```

#### Respuesta de Éxito (`200 OK`):
```json
[
  {
    "idCalle": 1,
    "nombreCalle": "Av. Siempreviva"
  },
  {
    "idCalle": 2,
    "nombreCalle": "Calle Falsa 123"
  }
]
```

---

### Obtener Calle por ID
Obtiene la información de una calle específica usando su ID.
- **URL:** `/calles/{id}`
- **Método:** `GET`

#### Ejemplo de Petición (cURL):
```bash
curl -X GET "http://localhost:8000/calles/1"
```

#### Respuesta de Éxito (`200 OK`):
```json
{
  "idCalle": 1,
  "nombreCalle": "Av. Siempreviva"
}
```

#### Respuesta de Error (`404 Not Found`):
```json
{
  "detail": "Calle no encontrada"
}
```

---

### Actualizar Calle
Actualiza el nombre de una calle existente. Permite actualizaciones parciales.
- **URL:** `/calles/{id}`
- **Método:** `PUT`
- **Cuerpo de la Petición (JSON):**
  ```json
  {
    "nombreCalle": "Av. Siempre Viva (Modificada)"
  }
  ```

#### Ejemplo de Petición (cURL):
```bash
curl -X PUT "http://localhost:8000/calles/1" \
     -H "Content-Type: application/json" \
     -d '{"nombreCalle": "Av. Siempre Viva (Modificada)"}'
```

#### Respuesta de Éxito (`200 OK`):
```json
{
  "idCalle": 1,
  "nombreCalle": "Av. Siempre Viva (Modificada)"
}
```

#### Respuesta de Error (`404 Not Found`):
```json
{
  "detail": "Calle no encontrada"
}
```

---

### Eliminar Calle
Elimina una calle específica por su ID.
- **URL:** `/calles/{id}`
- **Método:** `DELETE`

#### Ejemplo de Petición (cURL):
```bash
curl -X DELETE "http://localhost:8000/calles/1"
```

#### Respuesta de Éxito (`200 OK`):
Retorna el objeto de la calle que ha sido eliminada.
```json
{
  "idCalle": 1,
  "nombreCalle": "Av. Siempre Viva (Modificada)"
}
```

#### Respuesta de Error (`404 Not Found`):
```json
{
  "detail": "Calle no encontrada"
}
```

---

## 3. Endpoint de Estado (Root)

### Comprobación de Servidor
- **URL:** `/`
- **Método:** `GET`

#### Ejemplo de Petición (cURL):
```bash
curl -X GET "http://localhost:8000/"
```

#### Respuesta de Éxito (`200 OK`):
```json
{
  "Hello": "World"
}
```
