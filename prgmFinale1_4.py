from calculatePandas import *

if __name__ == '__main__':

    filesNb = input("\nNombre de fichiers à traiter : ")
    rowsNb = input("Nombre de lignes dans les fichiers .csv (doivent être harmonisés si besoin) \nAttention : c'est la valeur dans la dernière ligne de PacketCounter du fichier csv: ")
    
    while True:

        try:
            fileNameList = []
            plusList = []
            minusList = []

            for i in range(int(filesNb)):
                fileName = input("\nNom du fichier n°" + str(i+1) + " (NE PAS rajouter l'extension du fichier .csv) : ")
                fileNameList.append(fileName)
                plus = input("Taille de l'extrémité + (en mm) : ")
                moins = input("Taille de l'extrémité - (en mm) : ")
                plusList.append(int(plus))
                minusList.append(int(moins))

            trajectories = Trajectory(fileNameList)
            trajectories.convertFiles(";")
            if not trajectories.testAll(rowsNb):
                raise KeyError
            break

        except KeyError:
            print("\nErreur: L'index spécifié n'est pas trouvé dans le DataFrame. Veuillez redonner le nombre de lignes.")
            rowsNb = input("Rappel : c'est la valeur dans la dernière ligne de PacketCounter du fichier csv: ")

    for i in range(int(filesNb)):
        trajectories.calculateTrajectory(fileNameList[i], plusList[i], minusList[i])
        trajectories.calculateExtremitiesTrajectories(fileNameList[i], plusList[i], minusList[i])

    for i in range(int(filesNb)-1):
        trajectories.defineJoint(fileNameList[i], fileNameList[i+1])
        
    bool1 = input("\nVoulez-vous avoir un aperçu des trajectories ? Oui ou Non    :    ")
    if bool1 == "Oui":
        trajectories.displayTrajectory()

    bool2 = input("Voulez-vous avoir un aperçu en animation ? Oui ou Non    :    ")
    if bool2 == "Oui":
        trajectories.displayAnimation()

    bool3 = input("Voulez-vous exporter les différentes trajectories et angles dans un nouveau fichier csv ? Oui ou Non    :    ")
    if bool3 == "Oui":
        trajectories.exportCSV()
        print("Les valeurs ont été exportés dans un fichier dont le nom est res_fileName.csv")