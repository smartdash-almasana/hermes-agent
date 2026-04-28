# SmartPyme Factory Agents

## Roles

- Hermes: orquestador. Define ciclo, tarea, estado y coordinación.
- Codex: worker. Recibe tarea, modifica código, reporta DONE/ERROR.
- Gemini 2.5 Pro: auditor. Revisa evidencia, tests y consistencia.
- Aliesi: aprobación humana por Telegram. Autoriza ciclos críticos.

## Regla central

El worker no decide arquitectura, no coordina, no crea runners.
Ejecuta una tarea puntual y reporta resultado.
