from dash import Dash, html, dcc, Input, Output, MATCH, State

# Initialize Dash
app = Dash(__name__)

# Example data structure: 4 levels of nested values
data = {
    "Task 1": {
        "Subtask 1.1": {
            "Sub-Subtask 1.1.1": ["Item 1.1.1.1", "Item 1.1.1.2"],
            "Sub-Subtask 1.1.2": ["Item 1.1.2.1"],
        },
        "Subtask 1.2": ["Item 1.2.1", "Item 1.2.2"],
    },
    "Task 2": {
        "Subtask 2.1": ["Item 2.1.1"],
        "Subtask 2.2": {
            "Sub-Subtask 2.2.1": ["Item 2.2.1.1", "Item 2.2.1.2"]
        },
    },
}


# Function to generate nested checklists
def generate_checklist(data, level=0):
    """
    Recursively generates a nested checklist from the data structure.
    """
    checklists = []
    for key, value in data.items():
        if isinstance(value, dict):  # Nested tasks
            checklists.append(
                html.Div([
                    dcc.Checklist(
                        id={"type": "checklist", "level": level, "key": key},
                        options=[{"label": key, "value": key}],
                        value=[],
                        labelStyle={"display": "block"},
                    ),
                    html.Div(
                        generate_checklist(value, level=level + 1),
                        style={"margin-left": "20px"}
                    ),
                    html.Div(id={"type": "output", "level": level, "key": key}, style={"margin-left": "20px"}),
                ])
            )
        elif isinstance(value, list):  # Leaf level of the checklist
            checklists.append(
                html.Div([
                    dcc.Checklist(
                        id={"type": "checklist", "level": level, "key": key},
                        options=[{"label": item, "value": item} for item in value],
                        value=[],
                        labelStyle={"display": "block"},
                    ),
                    html.Div(id={"type": "output", "level": level, "key": key}, style={"margin-left": "20px"}),
                ])
            )
    return checklists


# Layout with nested checklist
app.layout = html.Div([
    html.H1("Nested Checklist"),
    html.Div(generate_checklist(data)),
])


# Dynamic callback for all checklists
@app.callback(
    Output({"type": "output", "level": MATCH, "key": MATCH}, "children"),
    Input({"type": "checklist", "level": MATCH, "key": MATCH}, "value"),
    State({"type": "checklist", "level": MATCH, "key": MATCH}, "id"),
)
def update_checked_values(checked_values, checklist_id):
    """
    Updates the output based on the selected values from each checklist.
    """
    return f"Selected in {checklist_id['key']} (Level {checklist_id['level']}): {checked_values}"


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
