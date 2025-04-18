from tasks.scraper_task import scrapear_y_guardar

# Define el cliente y las URLs a scrapear
cliente = "recetron"
urls = [
    "https://solitemp.com/",
    "https://www.albapesa.com/",
    "https://vexia.com.co/"
]

# Lanza la tarea
scrapear_y_guardar.delay(cliente, urls)
