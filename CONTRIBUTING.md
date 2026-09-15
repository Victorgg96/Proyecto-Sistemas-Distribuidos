# Guía de colaboración — NodeMesh

Reglas para que todos trabajemos igual y no rompamos el repo antes de la entrega. Léelas antes de tu primer push.

## Modelo de ramas

Usamos un flujo simplificado con dos ramas permanentes y ramas de trabajo desechables.

| Rama | Para qué | Reglas |
|---|---|---|
| `main` | Código estable y entregable. Es lo que se demuestra. | Protegida. Nadie hace push directo. Solo recibe merges desde `develop`. |
| `develop` | Integración. Aquí se junta el trabajo de todos antes de tocar `main`. | Base de todas las ramas de trabajo. Push directo solo para arreglos mínimos. |
| Ramas de trabajo | Una tarea concreta (un feature, un fix, docs). | Salen de `develop` y regresan a `develop` por Pull Request. Se borran al mergear. |

La regla de oro: **nunca trabajes directo sobre `main`.** Si algo llega mal a `develop`, se arregla ahí sin tumbar lo que ya funciona en `main`.

### Nombre de las ramas de trabajo

```
<tipo>/<autor>/sesion<N>-<descripcion-corta>
```

- `<tipo>`: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`
- `<autor>`: tu nombre corto (ej. `diego`)
- `sesion<N>`: la sesión del roadmap a la que pertenece
- `<descripcion-corta>`: en minúsculas y con guiones

Ejemplos:

```
feat/diego/sesion2-nodo-chat
feat/ana/sesion3-replicacion
fix/luis/sesion3-puerto-duplicado
docs/diego/sesion1-readme
```

## Formato de commits

Seguimos **Conventional Commits**. El mensaje va en español.

```
<tipo>(<alcance opcional>): <descripción en presente>
```

| Tipo | Cuándo se usa |
|---|---|
| `feat` | Una funcionalidad nueva |
| `fix` | Corregir un bug |
| `docs` | Solo documentación (README, comentarios, diagrama) |
| `refactor` | Reorganizar código sin cambiar comportamiento |
| `test` | Agregar o ajustar pruebas |
| `chore` | Configuración, dependencias, cosas de mantenimiento |
| `style` | Formato, indentación, nombres (sin lógica) |

Ejemplos:

```
feat(nodo): endpoint para recibir y guardar mensajes
feat(replicacion): reenvío de mensajes a los demás nodos
fix(nodo): puerto ocupado al levantar segunda instancia
docs(readme): instrucciones para levantar el sistema
chore(deps): agregar httpx a requirements
```

Reglas de commit:

- Uno por actividad relevante del roadmap, no uno al final del día.
- Descripción en presente y directa: "agrega", "corrige", no "agregué" ni "agregando".
- Si necesitas explicar el porqué, va en el cuerpo del commit, una línea en blanco después del título.

## Flujo de trabajo

1. Actualiza `develop`: `git checkout develop && git pull`
2. Crea tu rama: `git checkout -b feat/diego/sesion2-nodo-chat`
3. Trabaja y haz commits siguiendo el formato.
4. Sube tu rama: `git push -u origin feat/diego/sesion2-nodo-chat`
5. Abre un Pull Request hacia `develop`. Que otro del equipo lo revise.
6. Al mergear, borra la rama.
7. `main` solo se actualiza desde `develop` cuando lo que hay ahí ya está probado y listo para demo.

## Debugging: diagnóstico antes de solución

Antes de tocar código, confirma en qué capa está el problema. No asumas la causa. Pregúntate:

- ¿Es el nodo que no replica?
- ¿Es el cliente que apunta al nodo equivocado?
- ¿Es un puerto ocupado o mal apuntado?

Un mensaje de error concreto y saber cuántos nodos corren y en qué puertos ahorra la mitad del tiempo.
