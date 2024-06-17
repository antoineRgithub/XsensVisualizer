from shiny import reactive, App, Inputs, Outputs, Session, render, ui, run_app
from shinyswatch import theme
import matplotlib.pyplot as plt
from faicons import icon_svg
import prgmFinale1_4 as prog
from pathlib import Path



app_ui = ui.page_sidebar(

    ui.sidebar(
        
        ui.input_text_area(
            "noms_csv", "Entrer les noms de vos fichiers 📁 (sans le '.csv', du plus fixe au plus mobile)", placeholder="ex : humerus avant_bras main"
            ),

        ui.input_radio_buttons(
            "sep",
            "Selectionner le separateur pour les csv :",
            (';',',')

        ),
        ui.input_numeric(
            "nbre_de_lignes", "Selectionner le nombre de lignes des csv", 1, min=1
        ),
        
        ui.input_text_area(
            "longueurs_moins", "Entrer les distances entre les capteurs et les articulations 📏 (vers le point fixe) [mm]", placeholder="ex : 115 100 30"
            )
        ,
        ui.input_text_area(
            "longueurs_plus", "Entrer les distances entre les capteurs et les articulations 📏 (vers le point le plus mobile) [mm]", placeholder="ex : 115 100 30"
            )
        ,
        ui.input_action_button(
            "run", "Run simulation", icon=icon_svg("play"), class_="btn-primary"
        ),
        title="Paramètres à insérer :"
    ),
    ui.panel_title(title = "Outil de simulation pour la création d'un avatar statique 🚀"),
    ui.output_plot("plot"),
    ui.output_plot("animation"),
    )



def server(input: Inputs, output: Outputs, session: Session):
    @render.plot
    @reactive.event(input.run)
    def plot():
        liste_noms_csv = input.noms_csv().split()
        trajectoires = prog.Trajectory(liste_noms_csv)
        liste_longueurs_m = input.longueurs_moins().split()
        liste_longueurs_moins = [int(l) for l in liste_longueurs_m]
        liste_longueurs_p = input.longueurs_plus().split()
        liste_longueurs_plus = [int(l) for l in liste_longueurs_p]
        
        if liste_noms_csv[0] == "ex":
            pass
        
        else :
            trajectoires.convertFiles(input.sep())

            for i in range(len(liste_noms_csv)) :
                trajectoires.calculateTrajectory(liste_noms_csv[i], liste_longueurs_plus[i], liste_longueurs_moins[i])
                trajectoires.calculateExtremitiesTrajectories(liste_noms_csv[i], liste_longueurs_plus[i], liste_longueurs_moins[i])

            for i in range(len(liste_noms_csv) - 1):
                trajectoires.defineJoint(liste_noms_csv[i], liste_noms_csv[i+1])
            
            trajectoires.exportCSV()

            fig = trajectoires.displayTrajectory()[1]
            ax = trajectoires.displayTrajectory()[0]
        
        return fig
    
    @render.plot
    @reactive.event(input.run)
    def animation():
        plt.close()
        liste_noms_csv = input.noms_csv().split()
        trajectoires = prog.Trajectory(liste_noms_csv)
        liste_longueurs_m = input.longueurs_moins().split()
        liste_longueurs_moins = [int(l) for l in liste_longueurs_m]
        liste_longueurs_p = input.longueurs_plus().split()
        liste_longueurs_plus = [int(l) for l in liste_longueurs_p]
        
        trajectoires.convertFiles(input.sep())

        for i in range(len(liste_noms_csv)) :
            trajectoires.calculateTrajectory(liste_noms_csv[i], liste_longueurs_plus[i], liste_longueurs_moins[i])
            trajectoires.calculateExtremitiesTrajectories(liste_noms_csv[i], liste_longueurs_plus[i], liste_longueurs_moins[i])

        for i in range(len(liste_noms_csv) - 1):
            trajectoires.defineJoint(liste_noms_csv[i], liste_noms_csv[i+1])
        
        trajectoires.exportCSV()

        trajectoires.displayAnimation()
        plt.close()
        return
    
www_dir = Path(__file__).parent / "www"
        
    


app = App(app_ui, server,static_assets=www_dir)

run_app(app, launch_browser= True)

