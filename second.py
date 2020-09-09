"""
Flask
Django
Dash - Plotly  ( Flask + ReactJS ) - Web Application ( Web Site )
Web Page  ( Rectangle Page  - HTML )
"""
import pandas as pd
import dash   # !pip install dash
import dash_html_components as html
import webbrowser
# Global Variables
app = dash.Dash()  # Creating your object

def load_data():
    dataset_name = 'India_terror1.csv'
    global df
    df = pd.read_csv(dataset_name)
    print(df.sample(5))
def open_browser():
    # Opening the Browser
    webbrowser.open_new('http://127.0.0.1:8050/')
def create_app_ui():
    # Heading and a Button
    main_layout = html.Div(
    [
    html.H1(id='Main_title', children='Terrorism Analysis with Insights'),
    html.Button(id='button_close', children = 'Click to Test'),
    html.Button(id='button_open',children='press'),
    html.
    # goto w3schools  learn HTML
    ]
    )
    return main_layout
def main():
    print("Welcome to the Project Season 3 ")
    load_data()
    open_browser()
    global app
    app.layout = create_app_ui()  # blank Container Page
    # change the title
    app.title = "Terrorism Analysis with python"
    # Change the favicon
    # https://www.favicon.cc/  upload your icon for your project  download your favicon
    # create a directory assests  and copy your favicon.ico there
    app.run_server()
    print("Thanks for using my Project ")
    # Industry Best Practices
    app = None
    df = None
# pl do  not type your code here
if __name__ == '__main__' :
    main()