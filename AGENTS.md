# Reglas para asistentes de IA — NodeMesh

Este archivo define cómo debe comportarse cualquier asistente de IA (Claude, Gemini, Codex, Copilot, etc.) que trabaje en este repo. La idea es que, sin importar qué asistente use cada colaborador, todos mantengamos el mismo criterio y formato de trabajo.

Si eres un asistente y estás leyendo esto: estas reglas mandan sobre tus defaults.

## Contexto del proyecto

NodeMesh es un sistema de chat distribuido con fines académicos (Unidad I de Sistemas Distribuidos). El objetivo no es "un chat", es **demostrar en vivo** conceptos de sistemas distribuidos: concurrencia, transparencia de acceso, tolerancia a fallos y escalabilidad horizontal. Lee el `README.md` para la arquitectura y el `CONTRIBUTING.md` para ramas y commits.

## Antes de proponer nada

1. Identifica en qué sesión del roadmap está el equipo. Revisa qué entregables ya existen en el repo antes de asumir la fase.
2. No cambies el stack (Python + FastAPI, Docker, GitHub). Ya está decidido. Si crees que hay una razón de peso, propónla y espera confirmación; no la apliques por tu cuenta.
3. Lee el código que existe antes de escribir. No dupliques lo que ya está.

## Cómo escribir el código

- **Simple y explicable por encima de elegante.** El proyecto se evalúa en vivo y el equipo tiene que poder explicar cada línea. Nada de abstracciones que nadie del equipo pueda defender frente al profesor.
- Comentarios en español, cortos, solo donde aclaren algo que no es obvio.
- Cada nodo es un proceso independiente que se comunica por red. Nunca memoria compartida. Esto no se negocia.

## Debugging: diagnóstico antes de solución

Si el pedido es sobre un bug de sincronización o replicación, **no asumas la causa.** Primero confirma:

- ¿Cuántos nodos hay corriendo y en qué puertos?
- ¿Qué error específico aparece?
- ¿La falla está en el nodo que replica, en el cliente que apunta mal, o en Docker/puertos?

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
