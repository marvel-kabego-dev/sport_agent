from langgraph.graph import StateGraph
from agent.agent import AgentState
from langgraph.graph import START, END
from typing import Dict, Literal
from agent.tools import get_current_score, get_player_stats, verify_score_consistency, save_match_event
from extraction.ner import extract_event

graph = StateGraph(AgentState)

async def extract_node(state: dict) -> Dict:
    print(f"\n--- [Nœud] 1. Extract ---")
    comment = state["comment"]
    print(f"Commentaire reçu : '{comment}'")
    event = await extract_event(comment, state.get("sequence", 0))
    return {"event": event}

async def read_state_node(state: dict) -> Dict:
    print("\n--- [Nœud] 2. Read State ---")

    event = state["event"]

    if event is None:
        return {
            "current_score": None,
            "player_stats": None
        }
    current_score = get_current_score.invoke({})
    player_stats = get_player_stats.invoke({"player_name": event.player or ""})
    return {"current_score": current_score, "player_stats": player_stats}


async def validate_node(state: dict) -> Dict:
    print("\n--- [Nœud] 3. Validate ---")
    event = state["event"]
    current_score = state.get("current_score")

    if event is None:
        return {"validation_passed": False, "error": "Extraction échouée — aucun événement."}

    score_ok = verify_score_consistency.invoke({
        "home_score": event.home_score or 0,
        "away_score": event.away_score or 0
    })

    if score_ok:
        return {"validation_passed": True, "error": ""}
    else:
        return {"validation_passed": False, "error": "Score incohérent avec l'historique."}


async def save_node(state: dict) -> Dict:
    print("\n--- [Nœud] 4. Save ---")
    # Lit : state["event"]
    event = state["event"]

    save_match_event.invoke({"event": event.model_dump() if event is not None else None})
    
    return {"error": None}


async def reject_node(state: dict) -> Dict:
    print("\n--- [Nœud] 5. Reject ---")
    error_msg = state.get("error", "Aucune erreur spécifiée")
    print(f"Événement rejeté. Cause : {error_msg}")
    
    return {}


def routing_function(state: dict) -> Literal["save", "reject"]:
    if state.get("validation_passed") is True:
        return "save"
    return "reject"

graph.add_node("extract", extract_node)
graph.add_node("read_state", read_state_node)
graph.add_node("validate", validate_node)
graph.add_node("save", save_node)
graph.add_node("reject", reject_node)

graph.set_entry_point("extract")
graph.add_edge("extract", "read_state")
graph.add_edge("read_state", "validate")
graph.add_edge("save", END)
graph.add_edge("reject", END)
graph.add_conditional_edges(
    "validate",
    routing_function,
    {"save": "save", "reject": "reject"}
)

app = graph.compile()