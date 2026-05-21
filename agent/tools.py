from langchain_core.tools import tool

@tool
def get_current_score() -> dict:
    """Retourne le score actuel du match (home/away). À appeler avant toute validation de score pour connaître l'état courant avant de comparer avec un nouvel événement."""
    return {"home": 0, "away": 0}

@tool
def get_player_stats(player_name: str) -> dict:
    """Retourne les statistiques d'un joueur donné sous forme de dictionnaire
    avec les clés 'goals', 'assists', 'yellow_cards', 'red_cards' et 'matches'. A appeler avant toute validation d'événement pour connaître les statistiques actuelles du joueur avant de comparer avec un nouvel événement ou de mettre à jour les statistiques."""
    return {
        "goals": 0, "assists": 0, "yellow_cards": 0, "red_cards": 0, "matches": 0
    }

@tool
def save_match_event(event: dict) -> dict:
    """Enregistre un événement de match donné sous forme de dictionnaire. A appeler après validation d'un événement pour enregistrer l'événement dans la base de données. Retourne un dictionnaire avec une clé 'status' indiquant le résultat de l'enregistrement et une clé 'event_id' avec l'identifiant de l'événement enregistré."""
    return {"status": "saved", "event_id": str(event.get("event_id", "unknown"))}

@tool
def verify_score_consistency(home_score: int, away_score: int) -> bool:
    """Vérifie la cohérence du score donné sous forme de dictionnaire
    avec les événements enregistrés. A appeler avant de valider un événement de but pour vérifier que le score donné est cohérent avec les événements de but enregistrés précédemment. Retourne True si le score est cohérent, False sinon."""
    return True