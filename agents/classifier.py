from state import IncidentState
import os
from dotenv import load_dotenv
import time
from models import ClassificationResult

load_dotenv()
groq_api_key = os.getenv("groq_api_key")

def classifier_node(state: IncidentState) -> dict:
    
    """
    Classifies the incident based on the raw input provided by the user.
    
    Args:
        state (IncidentState): The current state of the incident.
        
    Returns:
        IncidentState: Updated state with classification results.
    """
    start = time.time()
    try:
        from langchain_groq import ChatGroq
        from langchain_core.prompts import ChatPromptTemplate
        from langchain_core.output_parsers import JsonOutputParser
        llm = ChatGroq(
                    model="llama-3.1-8b-instant",
                    api_key=groq_api_key,
                )
        base_template = ChatPromptTemplate.from_template(
            """
            You are an incident classification agent. Classify the following incident based on the raw input provided by the user. 
            Provide the severity (P1, P2, or P3), affected_service, incident_type, structured_description, and search_queries.
            
            {format_instructions}
            
            Raw Input: {raw_input}
            """
        )
        output_parser = JsonOutputParser(pydantic_object=ClassificationResult)
        prompt = base_template.partial(format_instructions=output_parser.get_format_instructions())
        chain = prompt | llm | output_parser
        result = chain.invoke({"raw_input": state["raw_input"]})
    except Exception as e:
        print(f"Error in classifier_node: {e}")
        return {
            "severity": None,
            "affected_service": None,
            "incident_type": None,
            "structured_description": None,
            "search_queries": None,
            "start_time": start
        }

    return {
        "severity": result.get("severity"),
        "affected_service": result.get("affected_service"),
        "incident_type": result.get("incident_type"),
        "structured_description": result.get("structured_description"),
        "search_queries": result.get("search_queries"),
        "start_time": start
    }