from state import IncidentState

def orchestrate_incident(state: IncidentState) -> dict:
    """
    Orchestrates the incident management process based on the current state.
    takes in severity, incident_type, affected_service, search_queries and decides which
    searches are relevant and what category the incident falls into.
    Also return any additional context or refined search queries for the downstream nodes
    """
    # Further processing based on category
    severity, incident_type, affected_service, search_queries = state["severity"], state["incident_type"], state["affected_service"], state["search_queries"]
    try:
        if severity == "P1":
            category = "Critical"
        elif severity == "P2":
            category = "High"
        elif severity == "P3":
            category = "Medium"
        else:
            category = "Unknown"
    except Exception as e:
        print(f"Error in orchestrate_incident: {e}")
        category = "Unknown"

    return {
        "category": category
    }