# Importar librerías para manipulación de los datos
import pandas as pd
import numpy as np
import EDAMAM_


# Importar librerías para el manejo de dash
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import dash_table
import plotly.graph_objs as go
from dash import Input, Output, dcc, html


# Claves / ID's de las aplicaciones asignadas
nutrition_appid= '5f1e7888'
nutrition_appkey= '5576413f5acb38f5259a58dad888d1b9'
recipes_appid = 'dcda2d5e'
recipes_appkey= '87ae2d34cdde47026fc341c8fbd7957f'
food_appid= '6b69c52c'
food_appkey= 'd5a448b534a0c358dfb47fa7a6548724'

# Se crea el objeto EDAMAM_consulta
EDAMAM_consulta = EDAMAM_.Edamam_mcd(id_nutrition=nutrition_appid, 
                                     key_nutrition= nutrition_appkey,
                                     id_recipes=recipes_appid,
                                     key_recipes=recipes_appkey,
                                     id_food=food_appid,
                                     key_food=food_appkey)

# Ejercución el método de la API de Recipe Search para realizar consultas de alimentos
Response_Recipe = EDAMAM_consulta.Search_recipe(query= 'salad')

# Ejecución del metodo que retorna los dataframes ya procesados de la consulta a la API Recipe Search 
EDAMAM_consulta.ingredients_table()


"""
Código para generar un Dashboard sobre información nutricional realizando consultas a las API's de EDAMAM

"""
# # Creación de figuras, y layouts en plotly - Dash

app = dash.Dash(
    __name__, meta_tags=[{"name":"viewport", "content":"width = device-width"}],
    external_stylesheets=[dbc.themes.BOOTSTRAP])

app.title = "Análisis Nutricional"
# Se define el server de la aplicación
server = app.server


# Se define diccionario con los colores del texto y background
colors = {
    'background': '#C6D500',
    'text':'#111111',
}

fig  = go.Figure()
fig.update_layout(
    plot_bgcolor = colors['background'],
    paper_bgcolor = colors['background'],
    font_color = colors['text']
)

# Se inicializan los ingredientes
ingredients = [{'label': 'Zuni-Inspired Grilled Chicken Salad','value': 'Zuni-Inspired Grilled Chicken Salad'},
               {'label': 'Steak & Chips Salad', 'value': 'Steak & Chips Salad'},
               {'label': 'Shrimp Salad', 'value': 'Shrimp Salad'},
               {'label': 'Strawberry Hazelnut Salad', 'value': 'Strawberry Hazelnut Salad'},
               {'label': 'Grilled Tofu Salad With Miso Dressing','value': 'Grilled Tofu Salad With Miso Dressing'},
               {'label': 'Chicken Salad-Stuffed Tomatoes','value': 'Chicken Salad-Stuffed Tomatoes'},
               {'label': 'Buffalo Chicken Salad', 'value': 'Buffalo Chicken Salad'},
               {'label': 'Buffalo Chicken Salad recipes','value': 'Buffalo Chicken Salad recipes'},
               {'label': 'Washing up free salad', 'value': 'Washing up free salad'},
               {'label': 'Quinoa Salad', 'value': 'Quinoa Salad'}]


# Estilo para cada uno de las hojas de los tabs creados
tab_selected_style = {
    "background": "gray",
    'text-transform': 'uppercase',
    'color' : '#BCBD22',
    'font-size': '15px',
    'font-weight': 'bold',
    'align-items': 'center',
    'justify-content': 'center',
    'border-radius': '8px',
    'padding':'6px',
    'border-style':'solid',
    'border-color':'gray',
    'background-color':'#384160',

}

# Estilo general del tab
tab_style = {
    'color': 'rgb(136,136,136)',
    'font-size': '15px',
    'font-weight': 'bold',
    'align-items': 'center',
    'justify-content': 'center',
    'border-radius': '8px',
    'padding':'6px',
    'border-style':'solid',
    'border-color':'gray',
}


# Se crea el diseño de la plantilla en general del dashboard
app.layout= html.Div(
    children=[
        dbc.Container([
        dcc.Store(id="store"),
        dcc.Store(id ="store2"),
        dbc.Navbar(
            children=[
                html.A(
                    dbc.Row(
                        [
                            dbc.Col(html.Img(src ="https://images.plot.ly/logo/new-branding/plotly-logomark.png", height = "40px")),
                            dbc.Col([
                              dbc.NavbarBrand("Análisis Nutricional", class_name="ml_2",style={'font-size':38, 
                                                                                               'font-weight':'bold',
                                                                                               'textAlign':'center',
                                                                                               'color':'#384160'})], 
                            width="auto",align="center"),
                        ], 
                        align = "center",
                    ),
                ),
            ],
            color = "#c6d500",
            #align = "center",
            sticky = "center",
            ),

        html.H5(
            children = ["Analiza la información nutricional de recetas realizando consultas a la API Food Recipe de ",
                        html.A('EDAMAM', href = 'https://developer.edamam.com/edamam-docs-nutrition-api',target = '_blank')],
            style = {'font-weight':'bold','color':'#384160','textAlign':'left', 'fontsize':'56px'}
        ),
        html.Hr(style={'color':'black'}),
        html.H2('Búsqueda de alimento:', style = {'font-weight':'bold', 'color':'#384160'}),
        html.Hr(style={'color':'black'}),
        dcc.Input(
            placeholder = 'Enter a value...',
            id = "string_contr",
            type = 'text',
            value = 'Salad',
            style = {'display':'inline-block', 'font-weight':'bold', 'width':300,'height':40, 'font-size':25}
            ),
        html.Hr(style={'color':'black'}),
        dbc.Button(
            "Search",
            color = "primary",
            id = "button",
            className = "mb-3",
        ),
        dbc.Tabs(id="tabs",active_tab="ingredients",style=tab_selected_style,
            children = [
                dbc.Tab(label="Ingredientes", 
                        tab_id="ingredients",
                        label_style = {'color':'#29A3A8'},
                        children = [
                            dcc.Dropdown(
                                id ="Dropdown",
                                options = [{'label':k, 'value':k} for k in ingredients],
                                style = {'font-weight':'bold','font-size':20,'padding':2, 'color':'black'},
                                value = 'Strawberry Hazelnut Salad',
                                ),
                            ], 
                        ),

                dbc.Tab(label = "Valor Nutricional", 
                        tab_id="comparison",
                        label_style = {'color':'#29A3A8'},
                        ),
                dbc.Tab(label="Acerca de:", 
                        tab_id="Acerca",
                        label_style = {'color':'#29A3A8'},
                        ),
            ],
        ),
        html.Div(id="tab-content", className="p-4", style = {'color' :'black',
                                                             'border-color':'black',
                                                             'backgroundColor': 'white',
                                                             'border-style':'solid',
                                                             'border-color':'gray',
                                                            }),
    ], ),],style = {'color' :'black','backgroundColor':colors['background']})

@app.callback(
    Output("tab-content", "children"),
    [Input("tabs", "active_tab"), 
    Input("store", "data")])
def render_tab_content(active_tab, data):
    """
    Esta función call back toma las propiedades de las pestañas como entradas, y toma la data de 
    cada gráfica almacenada enviada por la función callback anterior " generate graph", 
    dependiendo de la pestaña seleccionada despliega sus valores.
    
    """
    if active_tab and data is not None:
        if active_tab == "ingredients":
            return (html.Div([dbc.Row([html.H3(str(data["label_food"]))]),
                             dbc.Row([dbc.Col(html.Img(src = data["image"]), style = {'textAlign':'left'},),
                                      dbc.Col(children = data["card_cont1"] , style = {'textAlign':'center','padding':15}),
                                      dbc.Col(children = data["card_cont2"], style = {'textAlign':'center','padding': 15}),
                                      ],justify="left"),],
                            style = {'padding':10, 'flex':1, 'color':'#29A3A8', 'fontWeight':'bold'}), 
                    html.Div([html.H3(style={'color':"#29A3A8",'padding':25},children='Análisis por ingredientes'),
                              dbc.Col(dcc.Graph(figure=data["bar_1"])), 
                              dbc.Col(dcc.Graph(figure=data["bar_3"]))]))

        elif active_tab == "Acerca":
            return html.Div([
                dbc.Row([
                    dbc.Col(children=[
                        html.H3('Tabla - Guía de Nutrición'),
                        html.Hr(style={'color':'black'}),
                        dash_table.DataTable(
                            style_data={'whiteSpace': 'normal','height': 'auto'},
                            fill_width = False,
                            id = 'table_nut',
                            columns = [{"name":i, "id":i} for i in pd.DataFrame(data["Nut_guid"]).columns],
                            style_header={
                                'backgroundColor': 'gray',
                                'fontWeight': 'bold',
                                'border':'1px solid black'
                                },
                            style_cell = {'padding':'10px'},
                            style_as_list_view = True,
                            style_data_conditional=[
                                {
                                    'if': {'row_index': 'odd'},
                                    'backgroundColor': 'rgb(220, 220, 220)',
                                    }
                                ],
                            data = pd.DataFrame(data["Nut_guid"]).to_dict('records'),
                            ),
                        ],width="auto", align="center"),
                    ],justify = "center"),
                ],) 
                
        elif active_tab == "comparison":
            return html.Div([
                html.H3(style={'color':"#29A3A8",'padding':25},children='Valor Nutricional entre Alimentos'),
                dcc.Graph(figure = data["comparison"]),
                dcc.Graph(figure = data["scatter_1"])
                ])
    return "No tab selected"
 
 
@app.callback(Output("store", "data"),
              [Input("Dropdown", "value"),
              Input("store2","data")])

def generate_graphs(value, data_dict):
    """
    Esta función call back toma los datos de la función callback anterior y crea los objetos gráficos 
    de los datos recibidos 
    """
    
    if not data_dict:
        # generate empty graphs when app loads
        return {k: go.Figure(data=[]) if k not in 
                ["image","label_food","card_cont1","card_cont2"] else "" 
                for k in [
                    "bar_1",
                    "scatter_1", 
                    "comparison",
                    "bar_3", 
                    "image", 
                    "label_food", 
                    "card_cont1",
                    "card_cont2",]}
    else:
        
        # Se importa tabla guída de nutrientes
        data_Nut = pd.read_csv('Nutrient_Guide.csv', index_col = None, sep = ',', encoding='utf-8')

        df_food_nut = pd.DataFrame(data_dict['df_food_nut'])
        df_food_scatter = pd.DataFrame(data_dict['df_food_scatter'])
        food = pd.DataFrame(data_dict['food'])
        df_image = pd.DataFrame(data_dict['df_image'])
        df_summary = pd.DataFrame(data_dict['df_summ'])
        df_TNut = pd.DataFrame(data_dict['df_TNutr'])
        
        ################################################################################
        # Scatter Protein vs Energy
        fig_scatter = px.scatter_matrix(df_food_scatter, 
                                        dimensions=['Carbs', 'Protein', 'Fat','Fiber'], 
                                        color = "Food",height= 800)
        # Manipular el color del gráfico
        fig_scatter.update_layout(
            legend_title = 'Alimentos',
            paper_bgcolor="LightSteelBlue",
            font = dict(size = 16),
            title = '<b>Relación nutricional entre alimentos</b>',
            )
        fig_scatter.update_traces(diagonal_visible=False)
        ################################################################################

        # Se grafican las caracteristicas por ingredientes
        food_sorted = food.loc[lambda df: df['Types'] == value, ['ingredient name','weight','food']].sort_values(by = 'weight',ascending = True)

        
        ################################################################################
        # Objeto bar_1 -> Gráfico de barras se asignan los valores para la "porción por ingrediente" de la receta
        fig_bar1 =  px.bar(food_sorted, x = 'weight', y = 'ingredient name', orientation='h', color = 'food')
        # Manipular el color del gráfico
        fig_bar1.update_layout(
             legend_title = "Ingredientes",
             paper_bgcolor="LightSteelBlue",
            )
        # Se actualizan las propiedades y etiquetas del eje x 
        fig_bar1.update_xaxes(title='<b>Peso, g</b>', visible=True, showticklabels=False)
        fig_bar1.update_layout(uniformtext_minsize=8, 
                               uniformtext_mode='hide', 
                               title = '<b>Porción por ingrediente</b>',
                               font = dict(size = 14))
        # Se activa la visibilidad en las etiquetas de los ejes y se define la etiqueta del eje y
        fig_bar1.update_yaxes(title='<b>Ingredientes</b>', visible=True, showticklabels=False)
    
        ################################################################################
        # Objeto bar_2 -> Gráfico de barras en donde se asignan como valores 
        fig_bar2 = px.bar(df_food_nut, x = "Food", y = ['Carbs', 'Protein', 'Fat','Fiber'])
        fig_bar2.update_layout(
            legend_title = "Nutrientes",
            paper_bgcolor="LightSteelBlue")
        
        fig_bar2.update_layout(uniformtext_minsize=8, uniformtext_mode='hide', font = dict(size = 14))
        # Se activa la visibilidad en las etiquetas de los ejes
        fig_bar2.update_xaxes(title='<b>Alimentos</b>', visible=True, showticklabels=False)
        fig_bar2.update_yaxes(title='<b>Valor, g</b>', visible=True, showticklabels=True)
        
        ################################################################################
        # Objeto bar_3 -> Gráfico de barras de los nutrientes por alimento
        fig_bar3 = px.bar(df_TNut,x= 'label', y = value, color ='label')
        fig_bar3.update_traces(texttemplate='%{text:.2s}', textposition='outside')
        fig_bar3.update_layout(title= "<b>Total Diario</b>" ,
                               uniformtext_minsize=8, 
                               uniformtext_mode='hide', 
                               legend_title = 'Nutrientes',
                               paper_bgcolor="LightSteelBlue",
                               font = dict(size = 14))
        # Se activa la visibilidad en las etiquetas de los ejes
        fig_bar3.update_xaxes(title='<b>Nutrientes</b>', visible=True, showticklabels=False)

        ################################################################################
        # Se define el path de la imagen del alimento seleccionado
        image_url = df_image.loc[value,"image"]
        
        # Resumen Receta calories
        calories = df_summary.loc[value,'calories']
        totalWeight = df_summary.loc[value,'totalWeight']
        totalTime = df_summary.loc[value, 'totalTime']
        
        # Se asigan los valores de calorías y peso total por ingrediente en las tarjetas
        card_content_cal = dbc.Card([dbc.CardHeader("CALORÍAS, cal"), 
                                 dbc.CardBody(
                                     [
                                         html.H5(str(round(calories,2)), className="card-title"),
                                         ]),
                                 ], color ="primary", outline = True, )#style = {"width":"18rem"})
        
        card_content_weight = dbc.Card([dbc.CardHeader("PESO TOTAL, g"), 
                                 dbc.CardBody(
                                     [
                                         html.H5(str(round(totalWeight,2)), className="card-title"),
                                         ]),
                                 ],color ="primary", outline = True, )#style = {"width":"18rem"})
        
        
        # se crean variable diccionario con los valores de los objeetos gráficos y tarjetas.
        graph_dicts = {"bar_1": fig_bar1, 
                       "scatter_1": fig_scatter, 
                       "comparison": fig_bar2, 
                       "bar_3": fig_bar3,
                       "image": image_url, 
                       "label_food": value,
                       "card_cont1": card_content_cal,
                       "card_cont2": card_content_weight,
                       "Nut_guid":data_Nut.to_dict()
                       }

        # Se guardan los objettos graficos en un diccionario y se envían a dcc.store 
        return graph_dicts


@app.callback(Output("store2", "data"),
               Output("Dropdown", "options"),
              [Input("button", "n_clicks"), 
              Input("string_contr", "value")]) 
def query_Edamam(n, value):
    """
    Esta función realiza las consultas a la API de Recipe Search de EDAMAM y obtiene los dataframes
    procesados, el retorno de la función es una variable de tipo diccionario que se almacenda en dcc.store2
    """
    
    ctx = dash.callback_context
    print(value, "Si funciona")
    
    if ctx.triggered:
        #time.sleep(3)
        # Ejercución de los métodos de cada una de las API's para realizar consultas
        EDAMAM_consulta.Search_recipe(query= value)

        # Ejecución del metodo para genrar las tablas (dataframe) con la información requerida por los gráficos 
        EDAMAM_consulta.ingredients_table()
        
        # Se asignan los valores regresados por las instancias de la clase EDMAM_mcd
        food = EDAMAM_consulta.df_Recipe.reset_index()
        list_ingredients = EDAMAM_consulta.ingredients
        df_food_nut = EDAMAM_consulta.df_food_nut
        df_food_scatter = EDAMAM_consulta.df_food_scatter
        df_image = EDAMAM_consulta.image_recipe
        df_total_Nut = EDAMAM_consulta.df_totalNutrient
        
        # Recipe summary
        df_summary = EDAMAM_consulta.summary_r
        
        # Se define variable de tipo diccionario con los valores de los dataframes convertidos a tipo de dato dict
        df_dicts ={"food":food.to_dict() ,
                   "df_food_nut":df_food_nut.to_dict(), 
                   "df_food_scatter":df_food_scatter.to_dict(),
                   "df_image":df_image.to_dict(),
                   "df_summ": df_summary.to_dict(),
                   "df_TNutr":df_total_Nut.to_dict()
                   }
       
        options_list = [{"label": element, "value":element} for element in list_ingredients]
  
        return df_dicts, options_list
        
    else:
        print("NO EJECUTO API EDAMAM")
        #df_dicts ={"ingre":[], "df_food_nut":[], "df_food_scatter":[]}
        df_dicts = None
        ingred_non = [{'label': 'Zuni-Inspired Grilled Chicken Salad','value': 'Zuni-Inspired Grilled Chicken Salad'},
                      {'label': 'Steak & Chips Salad', 'value': 'Steak & Chips Salad'},
                      {'label': 'Shrimp Salad', 'value': 'Shrimp Salad'},
                      {'label': 'Strawberry Hazelnut Salad', 'value': 'Strawberry Hazelnut Salad'},
                      {'label': 'Grilled Tofu Salad With Miso Dressing','value': 'Grilled Tofu Salad With Miso Dressing'},
                      {'label': 'Chicken Salad-Stuffed Tomatoes','value': 'Chicken Salad-Stuffed Tomatoes'},
                      {'label': 'Buffalo Chicken Salad', 'value': 'Buffalo Chicken Salad'},
                      {'label': 'Buffalo Chicken Salad recipes','value': 'Buffalo Chicken Salad recipes'},
                      {'label': 'Washing up free salad', 'value': 'Washing up free salad'},
                      {'label': 'Quinoa Salad', 'value': 'Quinoa Salad'}]

        return df_dicts, ingred_non
        

if __name__ == "__main__":
    #from waitress import serve
    #serve(app, host = "0.0.0.0", port = 8080)
    app.run_server(debug=False)