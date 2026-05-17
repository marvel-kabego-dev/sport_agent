import json
import logging
from openai import AsyncOpenAI

from models.schemas import MatchEvent, ActionType

client = AsyncOpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",
)
logger = logging.getLogger(__name__)


async def extract_event(comment: str, sequence: int) -> MatchEvent | None:
    # 1. Format propre des actions pour le LLM
    actions = ", ".join(action.value for action in ActionType)

    format_json = """{
    "player": null,
    "team": null,
    "action": null,
    "minute": null,
    "home_score": null,
    "away_score": null
}"""
    
    system_prompt = """Tu es un extracteur d'événements de football.

    Règles absolues :
    - Réponds uniquement en JSON valide, sans texte avant ou après
    - Aucun Markdown, aucun échappement d'underscore
    - "team" ne peut valoir que "home", "away", ou null — jamais un nom d'équipe
    - "player" est toujours un nom complet en string, ou null — jamais un objet, jamais un numéro
    - Les valeurs de "action" doivent être exactement celles listées, sans modification
    - Un commentaire = exactement un seul objet JSON
    - Pour une substitution, "player" est le joueur qui sort uniquement
    - Le JSON se formate comme suit:
      "player": "Nom Prénom ou null si absent",
      "team": "home ou away ou null",
      "action": "une des actions autorisées",
      "minute": "entier ou null",
      "home_score": "entier ou null",
      "away_score": "entier ou null"
    - N'extrais "home_score" et "away_score" que si le score est explicitement 
    mentionné dans le commentaire sous forme numérique"""

    prompt = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": f"Actions autorisées : {actions}\n\nCommentaire :\n\"{comment}\"\n\nFormat attendu :\n{format_json}"}
]

    try:
        response = await client.chat.completions.create(
            model="mistral",
            messages=prompt
        )

        content = response.choices[0].message.content

        if not content:
            logger.error("[NER] Réponse vide du LLM")
            return None

        # 3. Parse JSON
        start = content.index("{")
        end = content.rindex("}") + 1
        data = json.loads(content[start:end])

        # 4. Ajout du champ système (PAS du LLM)
        data["sequence"] = sequence

        # 5. Validation Pydantic
        return MatchEvent(**data)

    except json.JSONDecodeError as e:
        logger.error(f"[NER] JSON invalide: {e} | content={content}")
        return None

    except Exception as e:
        logger.error(f"[NER] Erreur inattendue: {e}")
        return None