from dash import Dash, html, dcc, Input, Output, State, ALL, ctx

# Initialize Dash
app = Dash(__name__)

# Example data structure
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
                ], style={"margin-left": "20px"})
            )
    return checklists


# Layout with nested checklist
app.layout = html.Div([
    html.H1("Nested Checklist"),
    html.Div(generate_checklist(data)),
    html.Div(id="output", style={"margin-top": "20px", "border": "1px solid black", "padding": "10px"}),
])


# Callback to handle all checklist inputs with a static output
@app.callback(
    Output("output", "children"),
    Input({"type": "checklist", "level": ALL, "key": ALL}, "value"),
)

def update_static_output(all_checked_values):
    print('------')
    checked_values = []
    for checklist in all_checked_values:
        if checklist:
            for value in checklist:
                checked_values.append(value)
    print(checked_values)


    # Display selected values in output
    return [
        html.Div(f"{key}: {', '.join(values)}" if values else f"{key}: None")
        for key, values in selected_values.items()
    ]


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
