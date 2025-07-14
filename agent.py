{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 17,
   "id": "8be97d08-f1d2-41cc-b933-5b350f959ffc",
   "metadata": {},
   "outputs": [],
   "source": [
    "from langgraph.graph import StateGraph, END\n",
    "from typing import TypedDict, Dict, Any\n",
    "import json"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 18,
   "id": "f36adcd6-c318-4280-bf3d-90086320cbe6",
   "metadata": {},
   "outputs": [],
   "source": [
    "#Define the Input\n",
    "class BusinessData(TypedDict):\n",
    "    current_day: Dict[str, Any]\n",
    "    previous_day: Dict[str, Any]\n",
    "    metrics: Dict[str, Any]\n",
    "    recommendations: Dict[str, Any]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 19,
   "id": "0a3914e3-b2f8-46f9-9534-4d5502c7a7a3",
   "metadata": {},
   "outputs": [],
   "source": [
    "#Input Node\n",
    "def input_node(state: BusinessData) -> BusinessData:\n",
    "    return state"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 20,
   "id": "8f0e331b-3e8d-4b14-b37f-c15f7eda4e52",
   "metadata": {},
   "outputs": [],
   "source": [
    "#Processing Nodes\n",
    "def processing_node(state: BusinessData) -> BusinessData:\n",
    "    current = state['current_day']\n",
    "    previous = state['previous_day']\n",
    "\n",
    "    revenue_today = current['revenue']\n",
    "    cost_today = current['cost']\n",
    "    customers_today = current['customers']\n",
    "\n",
    "    revenue_yesterday = previous['revenue']\n",
    "    cost_yesterday = previous['cost']\n",
    "    customers_yesterday = previous['customers']\n",
    "\n",
    "    profit = revenue_today - cost_today\n",
    "\n",
    "    # Percentage changes\n",
    "    revenue_change = ((revenue_today - revenue_yesterday) / revenue_yesterday) * 100\n",
    "    cost_change = ((cost_today - cost_yesterday) / cost_yesterday) * 100\n",
    "\n",
    "    # CAC: Cost / Customers\n",
    "    cac_today = cost_today / customers_today\n",
    "    cac_yesterday = cost_yesterday / customers_yesterday\n",
    "    cac_change = ((cac_today - cac_yesterday) / cac_yesterday) * 100\n",
    "\n",
    "    state['metrics'] = {\n",
    "        'profit': profit,\n",
    "        'revenue_change_percent': revenue_change,\n",
    "        'cost_change_percent': cost_change,\n",
    "        'cac_today': cac_today,\n",
    "        'cac_change_percent': cac_change,\n",
    "    }\n",
    "    return state"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 21,
   "id": "921614ae-069a-444a-bb54-77016e09a902",
   "metadata": {},
   "outputs": [],
   "source": [
    "#Recommendation Nodes\n",
    "def recommendation_node(state: BusinessData) -> BusinessData:\n",
    "    metrics = state['metrics']\n",
    "    recommendations = []\n",
    "\n",
    "    if metrics['profit'] < 0:\n",
    "        recommendations.append(\"Reduce costs.\")\n",
    "\n",
    "    if metrics['cac_change_percent'] > 20:\n",
    "        recommendations.append(\"Review marketing campaigns.\")\n",
    "\n",
    "    if metrics['revenue_change_percent'] > 5:\n",
    "        recommendations.append(\"Consider increasing advertising budget.\")\n",
    "\n",
    "    alerts = []\n",
    "    if metrics['cac_change_percent'] > 20:\n",
    "        alerts.append(\"⚠️ CAC has increased by more than 20%!\")\n",
    "\n",
    "    state['recommendations'] = {\n",
    "        'profit_status': \"Profit\" if metrics['profit'] >= 0 else \"Loss\",\n",
    "        'alerts': alerts,\n",
    "        'decisions': recommendations\n",
    "    }\n",
    "    return state"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 22,
   "id": "20320ceb-eece-46aa-b3b7-e8ea22c3d99d",
   "metadata": {},
   "outputs": [],
   "source": [
    "#Build the Graph\n",
    "builder = StateGraph(BusinessData)\n",
    "builder.add_node(\"input\", input_node)\n",
    "builder.add_node(\"process\", processing_node)\n",
    "builder.add_node(\"recommend\", recommendation_node)\n",
    "\n",
    "builder.set_entry_point(\"input\")\n",
    "builder.add_edge(\"input\", \"process\")\n",
    "builder.add_edge(\"process\", \"recommend\")\n",
    "builder.add_edge(\"recommend\", END)\n",
    "\n",
    "graph = builder.compile()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 23,
   "id": "cf0e944b-c539-41d6-88ae-7f522251391d",
   "metadata": {},
   "outputs": [],
   "source": [
    "#User Input Execution\n",
    "def main():\n",
    "    print(\"\\nEnter business data as JSON (e.g., from file or manual paste):\")\n",
    "    try:\n",
    "        user_input = input()\n",
    "        business_data = json.loads(user_input)\n",
    "        result = graph.invoke(business_data)\n",
    "        print(\"\\n Recommendation Output \")\n",
    "        print(json.dumps(result[\"recommendations\"], indent=4))\n",
    "    except Exception as e:\n",
    "        print(\"\\n❌ Error:\", e)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 24,
   "id": "d6c87ee6-6a19-4f51-acfc-c62fc93bd67b",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "\n",
      "Enter business data as JSON (e.g., from file or manual paste):\n"
     ]
    },
    {
     "name": "stdin",
     "output_type": "stream",
     "text": [
      " m\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "\n",
      "❌ Error: Expecting value: line 1 column 1 (char 0)\n"
     ]
    }
   ],
   "source": [
    "def test_agent():\n",
    "    test_data = {\n",
    "        \"current_day\": {\"revenue\": 1200, \"cost\": 1300, \"customers\": 40},\n",
    "        \"previous_day\": {\"revenue\": 1500, \"cost\": 1000, \"customers\": 50},\n",
    "        \"metrics\": {},\n",
    "        \"recommendations\": {}\n",
    "    }\n",
    "    output = graph.invoke(test_data)\n",
    "    assert output['recommendations']['profit_status'] == \"Loss\"\n",
    "    assert \"Reduce costs.\" in output['recommendations']['decisions']\n",
    "    print(\"Test passed.\")\n",
    "\n",
    "if __name__ == \"__main__\":\n",
    "    main()\n",
    "    # Uncomment to run test: test_agent()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "82d14b1b-ee8d-46fa-91f2-2f649ae8d78f",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.13.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
