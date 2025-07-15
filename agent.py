from langgraph.graph import StateGraph, END
from typing import TypedDict, Dict, Any
import json

#Define the Input
class BusinessData(TypedDict):
    current_day: Dict[str, Any]
    previous_day: Dict[str, Any]
    metrics: Dict[str, Any]
    recommendations: Dict[str, Any]

#Input Node
def input_node(state: BusinessData) -> BusinessData:
    return state

#Processing Nodes
def processing_node(state: BusinessData) -> BusinessData:
    current = state['current_day']
    previous = state['previous_day']

    revenue_today = current['revenue']
    cost_today = current['cost']
    customers_today = current['customers']

    revenue_yesterday = previous['revenue']
    cost_yesterday = previous['cost']
    customers_yesterday = previous['customers']

    profit = revenue_today - cost_today

    # Percentage changes
    revenue_change = ((revenue_today - revenue_yesterday) / revenue_yesterday) * 100
    cost_change = ((cost_today - cost_yesterday) / cost_yesterday) * 100

    # CAC: Cost / Customers
    cac_today = cost_today / customers_today
    cac_yesterday = cost_yesterday / customers_yesterday
    cac_change = ((cac_today - cac_yesterday) / cac_yesterday) * 100

    state['metrics'] = {
        'profit': profit,
        'revenue_change_percent': revenue_change,
        'cost_change_percent': cost_change,
        'cac_today': cac_today,
        'cac_change_percent': cac_change,
    }
    return state

#Recommendation Nodes
def recommendation_node(state: BusinessData) -> BusinessData:
    metrics = state['metrics']
    recommendations = []

    if metrics['profit'] < 0:
        recommendations.append("Reduce costs.")

    if metrics['cac_change_percent'] > 20:
        recommendations.append("Review marketing campaigns.")

    if metrics['revenue_change_percent'] > 5:
        recommendations.append("Consider increasing advertising budget.")

    alerts = []
    if metrics['cac_change_percent'] > 20:
        alerts.append("⚠️ CAC has increased by more than 20%!")

    state['recommendations'] = {
        'profit_status': "Profit" if metrics['profit'] >= 0 else "Loss",
        'alerts': alerts,
        'decisions': recommendations
    }
    return state

#Build the Graph
builder = StateGraph(BusinessData)
builder.add_node("input", input_node)
builder.add_node("process", processing_node)
builder.add_node("recommend", recommendation_node)

builder.set_entry_point("input")
builder.add_edge("input", "process")
builder.add_edge("process", "recommend")
builder.add_edge("recommend", END)

graph = builder.compile()

#User Input Execution
def main():
    print("\nEnter business data as JSON (e.g., from file or manual paste):")
    try:
        user_input = input()
        business_data = json.loads(user_input)
        result = graph.invoke(business_data)
        print("\n Recommendation Output ")
        print(json.dumps(result["recommendations"], indent=4))
    except Exception as e:
        print("\n❌ Error:", e)

def test_agent():
    test_data = {
        "current_day": {"revenue": 1200, "cost": 1300, "customers": 40},
        "previous_day": {"revenue": 1500, "cost": 1000, "customers": 50},
        "metrics": {},
        "recommendations": {}
    }
    output = graph.invoke(test_data)
    assert output['recommendations']['profit_status'] == "Loss"
    assert "Reduce costs." in output['recommendations']['decisions']
    print("Test passed.")

if __name__ == "__main__":
    main()
    # Uncomment to run test: test_agent()

