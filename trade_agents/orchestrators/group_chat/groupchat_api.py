# groupchat_api.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
import uvicorn
import random
import logging

app = FastAPI()
logger = logging.getLogger("groupchat_api")
logging.basicConfig(level=logging.INFO)

# In-memory storage (can be replaced with a database)
cohorts: Dict[str, List[str]] = {}
topics: Dict[str, str] = {}
messages: Dict[str, List[Dict]] = {}
agents: Dict[str, Dict] = {}
proposers: Dict[str, str] = {} 

# Pydantic models
class Agent(BaseModel):
    id: str
    index: int

class Message(BaseModel):
    agent_id: str
    content: str
    cohort_id: str
    round_num: Optional[int] = 1
    sub_round_num: Optional[int] = 1

class TopicProposal(BaseModel):
    agent_id: str
    topic: str
    cohort_id: str
    round_num: Optional[int] = 1

class CohortFormationRequest(BaseModel):
    agent_ids: List[str]
    cohort_size: int

class CohortResponse(BaseModel):
    cohort_id: str
    agent_ids: List[str]

class ProposerSelectionRequest(BaseModel):
    cohort_id: str
    agent_ids: List[str]

class ProposerResponse(BaseModel):
    cohort_id: str
    proposer_id: str

class GetMessagesResponse(BaseModel):
    cohort_id: str
    messages: List[Dict]

class GetTopicResponse(BaseModel):
    cohort_id: str
    topic: str

# Endpoint to register agents (optional)
@app.post("/register_agent")
def register_agent(agent: Agent):
    agents[agent.id] = agent.dict()
    logger.info(f"Agent registered: {agent.id}")
    return {"message": "Agent registered"}

# Endpoint to form cohorts
@app.post("/form_cohorts", response_model=List[CohortResponse])
def form_cohorts(request: CohortFormationRequest):
    global cohorts
    agent_ids = request.agent_ids
    cohort_size = request.cohort_size
    random.shuffle(agent_ids)
    cohorts = {}
    cohort_responses = []
    for i in range(0, len(agent_ids), cohort_size):
        cohort_agent_ids = agent_ids[i:i + cohort_size]
        cohort_id = f"cohort_{i // cohort_size}"
        cohorts[cohort_id] = cohort_agent_ids
        cohort_responses.append(CohortResponse(cohort_id=cohort_id, agent_ids=cohort_agent_ids))
        # Initialize messages and topics for the cohort
        messages[cohort_id] = []
        topics[cohort_id] = ""
        proposers[cohort_id] = ""  # Initialize proposer
        logger.info(f"Cohort formed: {cohort_id} with agents {cohort_agent_ids}")
    return cohort_responses

# Endpoint to select a topic proposer for a cohort
@app.post("/select_proposer", response_model=ProposerResponse)
def select_proposer(request: ProposerSelectionRequest):
    cohort_id = request.cohort_id
    agent_ids = request.agent_ids
    if cohort_id not in cohorts:
        raise HTTPException(status_code=404, detail="Cohort not found")
    # Rotate proposers within the cohort
    current_proposer = proposers.get(cohort_id)
    if current_proposer in agent_ids:
        current_index = agent_ids.index(current_proposer)
        next_index = (current_index + 1) % len(agent_ids)
        proposer_id = agent_ids[next_index]
    else:
        proposer_id = random.choice(agent_ids)
    proposers[cohort_id] = proposer_id
    logger.info(f"Proposer selected for {cohort_id}: {proposer_id}")
    return ProposerResponse(cohort_id=cohort_id, proposer_id=proposer_id)

# Endpoint for agents to propose topics
@app.post("/propose_topic")
def propose_topic(proposal: TopicProposal):
    cohort_id = proposal.cohort_id
    if cohort_id not in cohorts:
        raise HTTPException(status_code=404, detail="Cohort not found")
    if proposal.agent_id != proposers.get(cohort_id):
        raise HTTPException(status_code=403, detail="Agent is not the proposer for this cohort")
    topics[cohort_id] = proposal.topic
    logger.debug(f"Topic proposed for {cohort_id} by {proposal.agent_id}: {proposal.topic}")
    return {"message": "Topic accepted"}

# Endpoint to get the topic for a cohort
@app.get("/get_topic/{cohort_id}", response_model=GetTopicResponse)
def get_topic(cohort_id: str):
    topic = topics.get(cohort_id)
    if topic == "":
        raise HTTPException(status_code=404, detail="Topic not set for this cohort")
    return GetTopicResponse(cohort_id=cohort_id, topic=topic)

# Endpoint for agents to post messages
@app.post("/post_message")
def post_message(message: Message):
    cohort_id = message.cohort_id
    if cohort_id not in cohorts:
        raise HTTPException(status_code=404, detail="Cohort not found")
    if message.agent_id not in cohorts[cohort_id]:
        raise HTTPException(status_code=403, detail="Agent not part of this cohort")
    message_entry = {
        "agent_id": message.agent_id,
        "content": message.content,
        "round_num": message.round_num,
        "sub_round_num": message.sub_round_num,
    }
    messages[cohort_id].append(message_entry)
    logger.debug(f"Message from {message.agent_id} in {cohort_id}: {message.content}")
    return {"message": "Message posted"}

# Endpoint to get messages for a cohort
@app.get("/get_messages/{cohort_id}", response_model=GetMessagesResponse)
def get_messages(cohort_id: str):
    if cohort_id not in messages:
        raise HTTPException(status_code=404, detail="No messages for this cohort")
    return GetMessagesResponse(cohort_id=cohort_id, messages=messages[cohort_id])

# Endpoint to get agents in a cohort
@app.get("/get_cohort_agents/{cohort_id}")
def get_cohort_agents(cohort_id: str):
    if cohort_id not in cohorts:
        raise HTTPException(status_code=404, detail="Cohort not found")
    return {"cohort_id": cohort_id, "agent_ids": cohorts[cohort_id]}

# Endpoint to get the current proposer for a cohort
@app.get("/get_proposer/{cohort_id}")
def get_proposer(cohort_id: str):
    proposer_id = proposers.get(cohort_id)
    if not proposer_id:
        raise HTTPException(status_code=404, detail="Proposer not set for this cohort")
    return {"cohort_id": cohort_id, "proposer_id": proposer_id}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Run the FastAPI application
if __name__ == "__main__":
    uvicorn.run("groupchat_api:app", host="0.0.0.0", port=8001, reload=True)
