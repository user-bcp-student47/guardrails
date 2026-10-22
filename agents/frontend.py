"""Rol frontend: edita aquí sus instrucciones y entregables."""

from graph.state import WorkflowState
from graph.context import _ctx, _runs, _const_block, _ronda, _feedback_block


INSTRUCTIONS = """Eres un desarrollador frontend/API que implementa el recorrido del usuario según el contrato de API aprobado.
Define campos, validaciones, acciones y mensajes.
Cubre estados de carga, vacío, éxito y error, y evita envíos duplicados.
Conserva etiquetas accesibles, navegación por teclado y foco visible.
Incluye cómo comprobar el recorrido y sus errores.
Devuelve los cambios con ### ruta/archivo.ext seguido de su bloque de código. Incorpora las observaciones del Chapter en las siguientes rondas."""


def frontend_node(state: WorkflowState, invoke) -> dict:
    """
    Implementa los cambios de frontend/API del plan.
    Mismo tratamiento del feedback que el backend.
    Se salta si project_type no incluye frontend.
    Escribe en: out_frontend
    """
    if not _runs(state, "frontend"):
        print("[frontend_node] project_type no incluye frontend — saltando.")
        return {}

    print(f"[frontend_node] Refactorizando frontend/API (ronda {_ronda(state)})...")

    prompt = (INSTRUCTIONS + _const_block(state, "Respeta las restricciones del proyecto y la constitución.") + "\nRepositorio: " + state["repo_name"] + "\nPlan:\n" + _ctx(state.get("out_plan", ""),2500) + "\nCódigo original:\n" + _ctx(state.get("snapshot", ""),4000) + _feedback_block(state) + '\nPara código usa ### ruta/archivo.ext seguida de un bloque markdown.')
    return {"out_frontend": invoke(prompt)}
