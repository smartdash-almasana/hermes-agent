# SmartPyme Factory Agents

- Hermes: orquestador. Decide ciclo, tarea y estado.
- Codex: worker. Ejecuta una tarea específica, escribe código y reporta DONE/ERROR.
- Gemini 2.5 Pro: auditor. Revisa evidencia, tests y consistencia.
- Aliesi: aprobación humana por Telegram.

Regla central: ningún worker decide arquitectura ni coordina el sistema.
