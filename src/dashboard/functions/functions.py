import os

def handle_uploaded_file(f):  
    with open('./static/upload/'+f.name, 'wb+') as destination:  
        for chunk in f.chunks():  
            destination.write(chunk)
    
    # Modifier le nom du fichier csv importé
    directory = "./static/upload/"
    files = os.listdir(directory)

    if "data.csv" in files:
        old_file = os.path.join(directory, "data.csv")
        os.unlink(old_file)

    for file in files:
        if file.endswith(".csv"):
            os.rename(os.path.join(directory, file), os.path.join(directory, "data.csv"))
            break