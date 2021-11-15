# Solicitudes de recetas a la API de EDAMAM
# Se define clase Edamam_mcd
import pandas as pd
import requests     
import logging
import numpy as np




class Edamam_mcd:
    "API que regresa datos de tipo json"
    def __init__(self, 
                id_nutrition, 
                key_nutrition, 
                id_recipes,
                key_recipes,
                id_food,
                key_food):
        
        # Asignación de claves / ID de las API's
        self.id_nut = id_nutrition
        self.key_nut = key_nutrition
        self.id_rec = id_recipes
        self.key_rec = key_recipes
        self.id_food = id_food
        self.key_food = key_food
    
    def Nut_Analysis(self, query):
        self.Nut_ingredients = query
        # Se define url (Access Point) para realizar consulta a la API Nutrition Analysis
        url_req_nutr = 'https://api.edamam.com/api/nutrition-data'
        # Se definen los parametros a pasar por la función get para realizar consulta
        params_nutr= {
            'app_id':self.id_nut,
            'app_key':self.key_nut,
            'ingr':self.Nut_ingredients
            }
        # Envío de solicitud para realizar consulta de análisis nutricional
        Response = requests.get(url_req_nutr, params = params_nutr)

        # Imprimir el código del estatus
        print("Status Code (Nutrition Analysis API):", Response.status_code)
        
        if Response.status_code == 401:
            logging.error('{key} - Clave inválida (Nutrition Analysis API)'.format(key=self.key_nut))

        # Valor de retorno de tipo diccionario, Response tiene contenido JSON serializado
        self.r_Nut = Response.json()
        return self.r_Nut

    def Search_recipe(self, query):
        self.query_recipe = query

        # Se construye url con los parámetros para realizar consulta para busqueda de recetas de un platillo
        url_recipe = 'https://api.edamam.com/search?q={query}&app_id={id}&app_key={key}'.format(id=self.id_rec, key=self.key_rec,query=self.query_recipe)    

        Response = requests.get(url_recipe)
        #print('Response Recipe', Response)

        # Imprimir el código de estatus
        print("Status Code (Recipe Search API) :", Response.status_code)
        
        if Response.status_code == 401:
            logging.error('{key} - Clave inválida (Recipe Search API)'.format(key=self.key_rec))

        # Valor de retorno de tipo diccionario, Response tiene contenido JSON serializado 
        self.r_Recipe = Response.json()
        #print(self.r_Recipe)
        return self.r_Recipe

    def Search_food(self, query):
        self.query_food = query
        # Se define url (Access Point) para realizar consulta de análisis de comida
        url_food = 'https://api.edamam.com/api/food-database/parser?'
        # Se definen los parametros a pasar por la función get para realizar consulta
        params_food = {
            'app_id':self.id_food,
            'app_key':self.key_food,
            'ingr':self.query_food
            }
        # Se realiza una consulta dando la url
        Response = requests.get(url_food, params= params_food)
        
        # Imprimir el código de estatus
        print("Status Code (Food Database API):", Response.status_code)

        if Response.status_code == 401:
            logging.error('{key} - Clave inválida (Food Database API)'.format(key=self.key_rec))

        # Valor de retorno de tipo diccionario, Response tiene contenido JSON serializado
        self.r_Food = Response.json()
        return self.r_Food
    
    # Conjunto de funciones para generar dataframes con los datos principales de las consultas

    def Nutrient_Guide(self):
        # Manejo de excepciones
        try:
            # Se crean DataFrames de las variables totalNutrients, totalDaily y totalNutrientsKCal 
            self.df_Nutrition= pd.DataFrame(self.r_Nut.get('totalNutrients')).T.rename_axis(str(self.Nut_ingredients))
            self.df_totalDaily = pd.DataFrame(self.r_Nut.get('totalDaily')).T.rename_axis(str(self.Nut_ingredients))
            self.df_total_Nut =  pd.DataFrame(Response_Nut.get('totalNutrientsKCal')).T.rename_axis(str(self.Nut_ingredients))
            # Se obtiene las calorías del alimento
            self.Nutrient_Cal = self.r_Nut.get('calories')
            # Se obtiene el peso total del alimento
            self.totalWeight = self.r_Nut.get('totalWeight')
            
        except Exception as e:
            print(e)
        
    def ingredients_table(self):
        # Manejo de excepciones
        try:
            # Comprensión de listas: se crean nuevas listas con las etiquetas de la receta y con los ingredientes
            list_label = [element_hits.get('recipe').get('label') for element_hits in self.r_Recipe.get('hits')]
            #list_label = [element_hits.get('recipe').get('label') for element_hits in self.r_Recipe.get('hits')]
            list_ingredientes = [element_ingre.get('recipe').get('ingredients') for element_ingre in self.r_Recipe.get('hits')]
            # Se construye DataFrame 
            df_ = pd.DataFrame(list_ingredientes, index=list_label).stack().apply(pd.Series).drop(columns=['foodId'])
            
            # Se consutryen los DataFrames para desplegar en gráficos en el Dashboard
            # Se crean listas vacías
            food_list = []
            nutrient_list = []
            nutrient_label_list = []
            totalNut_list = []
            summary_r_list = []
            i = 0
            
            for element in self.r_Recipe['hits']:
                i+=1
                food_list.append(element.get('recipe').get('label'))
                nutrient_list.append([element.get('recipe').get('totalDaily').get(nutr_element).get('quantity') for nutr_element in element.get('recipe').get('totalDaily')])#[:6])
                totalNut_list.append([element.get('recipe').get('totalNutrients').get(nutr_element).get('quantity') 
                                      for nutr_element in element.get('recipe').get('totalNutrients') 
                                      if nutr_element != 'SUGAR.added'])
                # Calories
                summary_r_list.append([element.get('recipe').get('calories'), element.get('recipe').get('totalWeight'), element.get('recipe').get('totalTime')])
             
            # Indicadores Principales de la receta
            self.summary_r = pd.DataFrame(summary_r_list, columns = ['calories','totalWeight', 'totalTime'], index = food_list)
             
            nutrient_label_list = [element.get('recipe').get('totalDaily').get(nutr_element).get('label') for nutr_element in self.r_Recipe['hits'][0].get('recipe').get('totalDaily')]
            
            # Total Nutrient
            dict_totalNut = self.r_Recipe.get('hits')[0].get('recipe').get('totalNutrients')
            totalNut_label_list = [dict_totalNut.get(element).get('label') for element in dict_totalNut]
            totalNut_label_unit = [dict_totalNut.get(element).get('unit') for element in dict_totalNut]
            df_totalNut = pd.DataFrame(totalNut_list, columns = totalNut_label_list, index = food_list).fillna(0).T.reset_index(drop = False).rename(columns = {'index':'label'})
            self.df_totalNutrient = df_totalNut
            
            self.df_Recipe = df_.rename_axis(["Types", "Items"], axis = "rows").rename(columns = {"foodCategory": "food category", "text":"ingredient name"})
            # Tratamiento de datos para generar gráficos
            self.ingredients = pd.DataFrame([element[0] for element in self.df_Recipe.index.values.tolist()]).loc[:,0].unique().tolist()
            self.df_food = pd.DataFrame(nutrient_list, columns = nutrient_label_list, index =food_list) #[:6]
            #self.df_food_nut = self.df_food[['Carbs', 'Protein', 'Fat']].reset_index(drop = False).rename(columns={'index':'Food'})
            self.df_food_nut = self.df_food.reset_index(drop = False).rename(columns={'index':'Food'})
            self.df_food_scatter = self.df_food.reset_index(drop = False).rename(columns ={'index':'Food'})
            # Lista de comprensión imagenes
            self.image_recipe = pd.DataFrame([image.get('recipe').get('image') for image in self.r_Recipe.get('hits')], columns = ['image'], index = food_list)
            
        except Exception as e:
            print(e)

    def food_table(self):
        # Se generar listas vacias
        list_foods = []
        list_nutrients = []
        rename_nutrients = ['ENERGY (kcal)', 'PROTEIN (g)', 'FAT (g)', 'CARBS (g)', 'FIBER (g)']
        # Manejo de excepciones
        try:
            # Comprensión de listas: se crean nuevas listas con las etiquetas de los alimentos y con los nutrientes  
            list_foods = [element.get('food').get('label') for  element in self.r_Food['hints']]
            #print(list_foods)
            list_nutrients = [element.get('food').get('nutrients') for element in self.r_Food['hints']]
            # Se construye DataFrame
            self.df_food_table = pd.DataFrame(list_nutrients, index = list_foods).round(2).fillna('Unknown')
            self.df_food_table.columns = rename_nutrients
            
        except Exception as e:
            print(e) 
    
    def write_files(self):
        #  Exportar archivos .CSV/.xlsx
        path_Nutrition = '{Nut}_Nutritional_Analysis.xlsx'.format(Nut=self.Nut_ingredients)
        path_Recipe = '{Recipe}_Recipe.csv'.format(Recipe = self.query_recipe)
        path_food = '{food}_food.csv'.format(food = self.query_food)

        # Se exporta a excel el análisis nutricional 
        with pd.ExcelWriter(path_Nutrition) as writer:
            self.df_Nutrition.to_excel(writer, sheet_name= 'Nutritional_Analysis')
            self.df_totalDaily.to_excel(writer, sheet_name='Total_Daily')
            self.df_total_Nut.to_excel(writer, sheet_name='totalNutrientsKCal')
        # Se exporta en formato CSV los ingredientes de las recetas
        self.df_Recipe.to_csv(path_Recipe)
        # Se exporta en CSV el dataframe con el análisis de los alimentos
        self.df_food_table.to_csv(path_food)
