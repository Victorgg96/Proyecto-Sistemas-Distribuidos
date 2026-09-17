# Reglas para asistentes de IA — NodeMesh

Este archivo define cómo debe comportarse cualquier asistente de IA (Claude, Gemini, Codex, Copilot, etc.) que trabaje en este repo. La idea es que, sin importar qué asistente use cada colaborador, todos mantengamos el mismo criterio y formato de trabajo.

Si eres un asistente y estás leyendo esto: estas reglas mandan sobre tus defaults.

## Contexto del proyecto

NodeMesh es un sistema de chat distribuido con fines académicos (Unidad I de Sistemas Distribuidos), construido con Python + Flask. El objetivo no es "un chat", es **demostrar en vivo** conceptos de sistemas distribuidos: concurrencia, transparencia de acceso, tolerancia a fallos y escalabilidad horizontal. Lee el `README.md` para la arquitectura y el `CONTRIBUTING.md` para ramas y commits.

## Arquitectura y endpoints (importante, no romper esto)

Cada nodo corre el mismo `node/app.py` y guarda los mensajes en memoria. Los nodos se conocen por el argumento `--peers` (URLs de los otros nodos). El contrato de la API:

- `POST /mensajes` — lo usa un **cliente** (Postman). El nodo guarda el mensaje **y lo replica** a cada peer. Aqui es donde se generan el `id` (uuid) y el `timestamp`, una sola vez, en el nodo de origen.
- `POST /replicar` — lo usa **otro nodo**, no un cliente. Solo guarda, **no reenvia**. Esta separacion es la que evita el bucle infinito de reenvios; no la elimines ni hagas que `/replicar` reenvie.
- `GET /mensajes` — devuelve la lista completa. Es lo que lee el cliente.
- `GET /salud` — estado, puerto, cuantos mensajes y los peers.

Reglas que no se tocan sin discutirlo:

- La deduplicacion por `id` en `/replicar` se queda: evita guardar el mismo mensaje dos veces.
- La replicacion es **best-effort y tolerante a fallos**: cada llamada a un peer va en try/except con timeout. Si un peer esta caido, el nodo igual guarda y responde; el peer caido solo se pierde ese mensaje. No cambies esto por algo que tumbe el nodo cuando un peer no responde.
- El nodo debe seguir funcionando **sin** `--peers` (modo de un solo nodo, como en la Sesion 2).

Como levantar el sistema distribuido: cada nodo en su maquina/terminal, con los otros como peers. Ejemplo con IPs locales:

```
python node/app.py --puerto 5001 --peers http://10.20.11.71:5001 http://10.20.11.72:5001
```

Para conectar nodos en redes distintas se usa ngrok (`ngrok http 5001`) y se ponen las URLs publicas en `--peers`. El codigo es el mismo; solo cambian las URLs.

## Antes de proponer nada

1. Identifica en qué sesión del roadmap está el equipo. Revisa qué entregables ya existen en el repo antes de asumir la fase.
2. No cambies el stack (Python + Flask, GitHub, Postman, ngrok). Ya está decidido. Si crees que hay una razón de peso, propónla y espera confirmación; no la apliques por tu cuenta.
3. Lee el código que existe antes de escribir. No dupliques lo que ya está.

## Cómo escribir el código

- **Simple y explicable por encima de elegante.** El proyecto se evalúa en vivo y el equipo tiene que poder explicar cada línea. Nada de abstracciones que nadie del equipo pueda defender frente al profesor.
- Comentarios en español, cortos, solo donde aclaren algo que no es obvio.
- Cada nodo es un proceso independiente que se comunica por red. Nunca memoria compartida. Esto no se negocia.

## Debugging: diagnóstico antes de solución

Si el pedido es sobre un bug de sincronización o replicación, **no asumas la causa.** Primero confirma:

- ¿Cuántos nodos hay corriendo y en qué puertos?
- ¿Qué error específico aparece?
- ¿La falla está en el nodo que replica, en el cliente que apunta mal, o en un puerto ocupado o mal apuntado?

Recién con eso propones el arreglo.

## Ramas y commits

- Respeta el modelo de ramas de `CONTRIBUTING.md`: se trabaja desde `develop`, nunca directo sobre `main`.
- Los commits siguen Conventional Commits (`feat:`, `fix:`, `docs:`, etc.) con el mensaje en español.
- **No hagas commits ni push automáticos.** Deja el commit al colaborador salvo que te lo pidan explícitamente.
- Verifica en qué rama estás antes de sugerir cambios y avisa si no es la correcta.

## Alcance y seguridad

- No toques archivos que no tengan que ver con la tarea pedida.
- Muestra los cambios como diff antes de aplicarlos cuando la herramienta lo permita.
- Comandos de git, borrados y pasos críticos van escritos completos y claros, nunca abreviados ni asumidos.

## Idioma y tono

- Responde en **español**, casual y directo. Sin relleno, sin lenguaje que suene a IA.
- Explicaciones concisas. Si el tema lo pide, dos niveles: lo técnico para el prompt/diagnóstico y una versión en lenguaje claro para el reporte de avance.
- Notas de avance en el formato: `Día DD/MM/AAAA — Se hizo/diagnosticó...`, en prosa breve.
