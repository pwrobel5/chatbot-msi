import requests
import csv

BEGIN_FROM = 50
NUM_OF_SENTENCES_TAKEN = 1000

response = requests.get("https://wolnelektury.pl/media/book/txt/ogniem-i-mieczem-tom-pierwszy.txt")
first_text = response.text.replace("\t", " ").replace("\n", " ").split(".")[BEGIN_FROM:(BEGIN_FROM + NUM_OF_SENTENCES_TAKEN)]

response = requests.get("https://wolnelektury.pl/media/book/txt/homer-odyseja.txt")
second_text = response.text.replace("\t", " ").replace("\n", " ").split(".")[BEGIN_FROM:(BEGIN_FROM + NUM_OF_SENTENCES_TAKEN)]

with open("text_set.csv", "w", newline="") as csvfile:
    csv_writer = csv.writer(csvfile, delimiter=";")
    csv_writer.writerow(["label", "text"])
    for sentence in first_text:
        csv_writer.writerow(["Ogniem i mieczem", sentence])
    for sentence in second_text:
        csv_writer.writerow(["Odyseja", sentence])