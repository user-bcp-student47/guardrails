"""Ingeniero de pruebas: edita aquí las instrucciones de revisión."""

from graph.state import WorkflowState
from graph.context import _ctx, _const_block, _feedback_block


INSTRUCTIONS = (
    'Eres el Ingeniero de pruebas del equipo. Relaciona cada criterio de aceptación '
    'del plan con una prueba y su resultado esperado. Incluye casos positivos, '
    'negativos, de borde e integración. Detalla preparación, datos de prueba, '
    'comandos reproducibles y limpieza. Comprueba los contratos de API y '
    'persistencia, además de las correcciones propuestas. No inventes ejecuciones: '
    'marca NO EJECUTADO cuando no tengas una salida real.\n'
)


def testing_node(state: WorkflowState, invoke) -> dict:
    prompt = (INSTRUCTIONS + _const_block(state, "Respeta las restricciones del proyecto y la constitución.") + "\nRepositorio: " + state["repo_name"] + "\nPlan:\n" + _ctx(state.get("out_plan", ""),2500) + "\nCódigo original:\n" + _ctx(state.get("snapshot", ""),4000) + "\nBackend:\n" + _ctx(state.get("out_backend", ""),6000) + "\nFrontend:\n" + _ctx(state.get("out_frontend", ""),6000) + _feedback_block(state) + '\nDevuelve un informe con cobertura por criterio, pruebas propuestas, comandos y resultados reales o NO EJECUTADO. Si propones cambios en archivos, usa exactamente el formato ### ruta/archivo seguido de un bloque de código markdown.')
    if state.get("include_data"):
        prompt += "\nContrato aprobado de Datos y persistencia:\n" + _ctx(state.get("out_data", ""), 6000)
    return {"out_testing": invoke(prompt)}
