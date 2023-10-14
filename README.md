# MoviePy-2.0
Skripta "posnetek.py" je glavno orodje za avtomatsko urejanje video posnetkov. Glavna knjižnica, ki se uporablja za to, je MoviePy. Trenutno je njena glavna funkcija dodajanje besedila. To pomeni, da lahko vstavite besedilo določene barve (glej "config.json"), velikosti, v časovnem obdobju od ... do ... ter na določeni poziciji v videu (x, y).

## Navodila
### Windows
Za tiste, ki uporabljate Windows, je uporaba te skripte precej enostavna. V izdaji (release) najdete datoteko ZIP, ki vsebuje že pripravljeno prenosno različico Pythona(Portable Pzthon). To datoteko ZIP prenesite, razpakirajte in takoj začnite uporabljati.
1. Razpakirajte datoteko kamor želite.
2. Zaženite "DevelopmentEnvironment.bat".
3. Sledite temu ukazu za zagon skripte: python.exe posnetek.py -c config.json -i files/input.mp4 -o files/out.mp4
### Linux/MacOS
Če uporabljate Linux ali MacOS, boste morali MoviePy namestiti ročno. Navodila za namestitev najdete tukaj:
https://zulko.github.io/moviepy/install.html 
