"""Arquitecto: diagnóstico y plan del repositorio, en una sola llamada."""

from graph.state import WorkflowState
from graph.context import _ctx, _const_block


INSTRUCTIONS = (
    "Eres el arquitecto de software del equipo. Analiza el Issue, sus criterios "
    "de aceptación y las interfaces del producto disponibles en el contexto y "
    "el snapshot. Si falta el Issue o algún criterio, indícalo como pendiente; "
    "no lo inventes.\n"
    "Define componentes, responsabilidades y límites del cambio. Especifica "
    "entradas, respuestas y errores de la API, con ejemplos coherentes con las "
    "interfaces existentes. Relaciona cada criterio con el componente que lo "
    "resuelve y declara supuestos y preguntas pendientes.\n"
    "Distingue hechos observados de propuestas y sustenta el diagnóstico con "
    "rutas o interfaces disponibles. No afirmes verificaciones o resultados que "
    "no hayas obtenido."
)

def architect_node(state: WorkflowState, invoke) -> dict:
    prompt = (INSTRUCTIONS + _const_block(state, "Respeta el alcance del issue y la constitución.") + "\nRepositorio: " + state['repo_name']
            + "\nTipo: " + state.get('project_type','ambos')
            + "\nCódigo original:\n" + _ctx(state['snapshot'],10000)
            + "\nEn ## Analysis incluye el diagnóstico, las interfaces relevantes, "
            "el contrato de API con ejemplos y la relación entre criterios de "
            "aceptación y componentes. Señala evidencia, supuestos y preguntas "
            "pendientes. En ## Plan incluye los archivos afectados y el orden "
            "de los cambios. Devuelve exactamente ## Analysis y ## Plan, cada "
            "una en su propia línea.")
    report = invoke(prompt)
    analysis, separator, plan = report.partition("\n## Plan\n")
    if not analysis.startswith("## Analysis\n") or not separator or not plan.strip():
        raise ValueError(
            "El arquitecto debe devolver las secciones ## Analysis y ## Plan."
        )
    return {
        "out_architect": report,
        "out_analysis": analysis.removeprefix("## Analysis\n").strip(),
        "out_plan": plan.strip(),
    }
