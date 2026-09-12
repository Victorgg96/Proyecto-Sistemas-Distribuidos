# NodeMesh

Sistema de chat distribuido. Varios nodos independientes que replican los mensajes entre sí: te conectas a cualquiera y el sistema sigue funcionando aunque tumbes uno.

Proyecto integrador de la Unidad I de **Sistemas Distribuidos**. No es un producto real; es una demo funcional para mostrar en código y en vivo los conceptos del curso: concurrencia, transparencia de acceso, tolerancia a fallos y escalabilidad horizontal.

## Qué demuestra

- **Procesos independientes por red.** Cada nodo es su propio proceso y se comunica por HTTP, nunca por memoria compartida.
- **Transparencia de acceso.** El cliente se conecta a cualquier nodo sin saber a cuál. Da igual.
- **Replicación.** Un mensaje que entra por el Nodo A aparece en el B y en el C.
- **Tolerancia a fallos.** Apagas un nodo y el chat sigue vivo con los que quedan.
- **Escalabilidad horizontal.** Agregar un nodo reparte la carga; el sistema no se reescribe para crecer.

## Arquitectura

```
        Cliente (terminal o Postman)
                    |
        +-----------+-----------+
        |           |           |
     Nodo A       Nodo B      Nodo C
   (puerto 5001)(puerto 5002)(puerto 5003)
        |-------- replican mensajes entre sí --------|
```

Todos los nodos corren el mismo programa en puertos (o contenedores) distintos. Cuando uno recibe un mensaje nuevo, lo reenvía a los demás. El diagrama completo vive en `docs/arquitectura.drawio`.

## Stack

| Herramienta | Para qué |
|---|---|
| Python 3 + FastAPI | Cada nodo. Tipado, docs automáticas en `/docs` y cliente de prueba sin instalar nada. |
| Docker Desktop | Levantar 2-3 instancias del mismo nodo como si fueran máquinas distintas. |
| Postman / `/docs` de FastAPI | Probar endpoints antes de tener cliente. |
| ngrok (free) | Exponer un nodo a internet para simular distribución real. *(opcional)* |
| draw.io | Diagrama de arquitectura. |

El stack ya está decidido. No se cambia sin una razón puesta sobre la mesa. Lo único innegociable: **cada nodo es un proceso independiente que se comunica por red**.

## Estructura del repo

```
nodemesh/
├── node.py               # el nodo (mismo código para todas las instancias)
├── requirements.txt
├── Dockerfile
├── docker-compose.yml    # levanta los 2-3 nodos
├── docs/
│   └── arquitectura.drawio
├── AGENTS.md             # reglas para asistentes de IA
├── CONTRIBUTING.md       # ramas, commits, flujo de trabajo
└── README.md
```

## Cómo correrlo

Requisitos: Python 3.10+ y Docker Desktop.

**Un solo nodo (desarrollo):**

```bash
pip install -r requirements.txt
uvicorn node:app --port 5001
```

Abre `http://localhost:5001/docs` para probar los endpoints desde el navegador.

**El sistema completo (2-3 nodos):**

```bash
docker compose up --build
```

Cada nodo queda en su puerto (5001, 5002, 5003). Manda un mensaje a uno y consúltalo desde otro para verificar la replicación.

**Probar tolerancia a fallos:**

```bash
docker compose stop nodo-b
```

El chat sigue respondiendo en los nodos que quedan.

## Roadmap

El proyecto se construye en 4 sesiones. Cada una tiene un entregable concreto.

| Sesión | Objetivo | Entregable |
|---|---|---|
| 1 | Diseño y arranque | Diagrama de arquitectura + repo con README |
| 2 | Un nodo funcionando | Un nodo que recibe, guarda y entrega mensajes, probado |
| 3 | De un nodo a sistema distribuido | 2-3 nodos replicando mensajes entre sí |
| 4 | Tolerancia a fallos y cierre | Caída de un nodo en vivo + README final + demo |

## Equipo

| Persona | Rol |
|---|---|
| — | Arquitectura y replicación |
| — | Pruebas y tolerancia a fallos |
| — | Documentación y diagrama |

## Cómo colaborar

Lee `CONTRIBUTING.md` antes de tu primer commit. Resumen: se trabaja sobre `develop`, nunca directo en `main`, y los commits siguen el formato `feat:`, `fix:`, `docs:`, etc.
