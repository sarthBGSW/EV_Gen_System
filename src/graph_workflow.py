from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
from src.search_tools import ResearchEngine
from src.llm_engine import ModelFactory
import operator

# Define the State Schema
class GraphState(TypedDict):
    scope: str
    draft: str
    critique: str
    iteration_count: int
    max_iterations: int
    search_data: str
    drafter_model: str
    critic_model: str

class EVGraph:
    def __init__(self):
        self.researcher = ResearchEngine()
        self.engine = ModelFactory()
    
    # --- NODE 1: Research ---
    def research_node(self, state: GraphState) -> GraphState:
        """
        Gathers web data based on the scope.
        """
        print("🔍 Running Research Node...")
        query = state["scope"]
        search_results = self.researcher.search_web(query)
        
        state["search_data"] = search_results
        return state
    
    # --- NODE 2: Draft Generation ---
    def drafter_node(self, state: GraphState) -> GraphState:
        """
        Generates or refines the draft using the search data and any previous critique.
        """
        print(f"✍️ Running Drafter Node (Iteration {state['iteration_count'] + 1})...")
        
        # Build prompt with context
        prompt = f"""
You are an expert business analyst writing a comprehensive report section.

**Scope:** {state['scope']}

**Research Data:**
{state['search_data']}

**Current Draft (if any):**
{state['draft'] if state['draft'] else 'This is the first draft.'}

**Previous Critique (if any):**
{state['critique'] if state['critique'] else 'No critique yet.'}

**Instructions:**
- Write a detailed, data-driven analysis
- Include specific figures, trends, and insights from the research data
- Use professional business language
- Structure with clear headings and bullet points where appropriate
- Cite data sources when possible
- Address any critique points if provided

Write the improved draft now:
"""
        
        # Generate draft
        draft = self.engine.generate(
            model_name=state["drafter_model"],
            prompt=prompt,
            system_role="You are an expert EV industry analyst and report writer."
        )
        
        # Update state
        state["draft"] = draft
        state["iteration_count"] += 1
        
        return state
    
    # --- NODE 3: Critique ---
    def critic_node(self, state: GraphState) -> GraphState:
        """
        Reviews the draft and provides constructive critique.
        """
        print("🤔 Running Critic Node...")
        
        critique_prompt = f"""
You are a harsh but constructive editor reviewing a business report draft.

**Draft to Review:**
{state['draft']}

**Evaluation Criteria:**
1. Data accuracy and credibility
2. Logical flow and structure
3. Completeness of analysis
4. Professional tone
5. Missing key insights or data points

Provide specific, actionable critique focusing on improvements needed:
"""
        
        critique = self.engine.generate(
            model_name=state["critic_model"],
            prompt=critique_prompt,
            system_role="You are a critical editor focused on quality and accuracy."
        )
        
        state["critique"] = critique
        return state
    
    # --- ROUTING LOGIC ---
    def should_continue(self, state: GraphState) -> str:
        """
        Decides whether to continue iterating or end.
        """
        if state["iteration_count"] >= state["max_iterations"]:
            print("✅ Max iterations reached. Ending workflow.")
            return "end"
        else:
            print(f"🔄 Continue to next iteration ({state['iteration_count']}/{state['max_iterations']})")
            return "continue"
    
    # --- BUILD THE GRAPH ---
    def build_graph(self):
        """
        Constructs the LangGraph workflow.
        """
        workflow = StateGraph(GraphState)
        
        # Add nodes
        workflow.add_node("research", self.research_node)
        workflow.add_node("drafter", self.drafter_node)
        workflow.add_node("critic", self.critic_node)
        
        # Define edges
        workflow.set_entry_point("research")
        workflow.add_edge("research", "drafter")
        
        # Conditional edge: continue or end
        workflow.add_conditional_edges(
            "drafter",
            self.should_continue,
            {
                "continue": "critic",
                "end": END
            }
        )
        
        # After critique, go back to drafter
        workflow.add_edge("critic", "drafter")
        
        # Compile
        app = workflow.compile()
        return app
