# MoviePy-2.0
Skripta "posnetek.py" je glavno orodje za avtomatsko urejanje video posnetkov. Glavna knjižnica, ki se uporablja za to, je MoviePy. Trenutno je njena glavna funkcija dodajanje besedila. To pomeni, da lahko vstavite besedilo določene barve (glej "config.json"), velikosti, v časovnem obdobju od ... do ... ter na določeni poziciji v videu (x, y).

## Navodila
### Windows
Za tiste, ki uporabljate Windows, je uporaba te skripte precej enostavna. V izdaji (release) najdete datoteko ZIP, ki vsebuje že pripravljeno prenosno različico Pythona(Portable Pzthon). To datoteko ZIP prenesite, razpakirajte in takoj začnite uporabljati.
1. Razpakirajte datoteko kamor želite.
2. Potrebno je naložiti najnovejšo skripto iz githuba-a in vse ostale folderje in fajlove, ki so v repositorju
3. Izvananje skripte
### Linux/MacOS
Če uporabljate Linux ali MacOS, boste morali MoviePy namestiti ročno. Navodila za namestitev najdete tukaj:
https://zulko.github.io/moviepy/install.html 

### Izvananje skripte
```
python posnetek.py -c pot/do/konfiguracija.json -i pot/do/vhoda -o pot/do/izhoda
```
- Zamenjajte pot/do/konfiguracija.json z dejansko potjo do vaše JSON konfiguracijske datoteke.
- Zamenjajte pot/do/vhoda s potjo do mape, ki vsebuje vhodne videoposnetke.
- Zamenjajte pot/do/izhoda s potjo, kjer želite shraniti urejene videoposnetke.

## Začetna in končna špica

### Funkcija "add_title_and_end_screen":

Ta funkcija je odgovorna za izboljšanje posameznega video posnetka. Prejme več parametrov, vključno s potjo do video posnetka, naslovi, podnaslovi in potjo za izhodno datoteko urejenega video posnetka.

#### Predpogoji:

- Da bi ta skript deloval pravilno, morate imeti ustrezno urejen imenik s predhodno določeno strukturo:
  - Folder "input": V tem imeniku morajo biti shranjeni vsi videoposnetki, ki jih želite izboljšati.
  - Folder "output": V tem imeniku bodo shranjeni urejeni videoposnetki.
  - Folder "fonts": Ta imenik naj vsebuje prilagojeno pisavo za besedilne elemente.
  - Folder "photos": Ta imenik naj vsebuje slike ali logotipe, ki se bodo uporabili v videoposnetkih.

1. **`title_duration`**:
   - Začne z določitvijo trajanja za začetno in končno platno, ki je nastavljeno na 5 sekund. To trajanje se lahko prilagodi po potrebi.

2. **Naloži video**:
   - Vhodni video se naloži s pomočjo funkcije `VideoFileClip` iz knjižnice MoviePy. S tem je video pripravljen za nadaljnje urejanje.

3. **Text Elements**:
   - Ustvarjeni so različni besedilni elementi, ki se prekrijejo na videu:
     - `theme`: Naslov videoposnetka, prikazan na začetku.
     - `duration_txt`: Besedilo, ki označuje trajanje videoposnetka.
     - `duration_str`: Izračunano trajanje videoposnetka z dodanim časom za naslov in zaključek.
     - `subtitle`: Podnaslov videoposnetka.
     - `lea`: Besedilni element, povezan z "LAPSy Embedded Academy."
     - `next_video`: Naslov naslednjega videoposnetka, ki se prikaže na koncu.
     - `end_title`: Sporočilo, prikazano ob zaključku, npr. "Hvala za ogled!"

4. **Font in style**:
   - Koda določi prilagojeno pisavo (`custom_font`), trenutno **garamond.ttf** in določi velikost pisave, barvo in položaj za vsak besedilni element. Te lastnosti se lahko prilagodijo glede na slog vašega videoposnetka.

5. **Text Clips**:
   - Besedilni posnetki se ustvarijo za vsak besedilni element s pomočjo funkcije `TextClip` iz MoviePy. Vsak besedilni posnetek je nastavljen na določeno trajanje in postavljen na želeno mesto v videu.

6. **Color Clips**:
   - Ustvarita se dva barvna posnetka: `color_clip` z belo podlago za naslovna platna in `red_lane` z rdečo podlago. Oba imata enako trajanje kot naslovna platna.

7. **Image Clip**:
   - Dva slikovna posnetka (`fri_logo_clip` in `lea_logo_clip`) se ustvarita iz slikovnih datotek. V zagotovljenem primeru gre za logotipa. Slike se prilagodijo in postavijo znotraj videa. Slikovne datoteke logotipov se lahko prilagodijo glede na vaše potrebe.

8. **Prekrivanje besedila, barv in slik**:
   - Besedilni posnetki, barvni posnetki in slike se združijo v dva sestavljena videoposnetka: `start_text_overlay_clip` za začetek in `end_text_overlay_clip` za konec videa. Ti sestavljeni posnetki se združijo z besedilnimi in vizualnimi elementi za ustvarjanje profesionalnega prekrivanja.

9. **Povezava videoposnetkov**:
   - Končni videoposnetek se ustvari s povezovanjem `start_text_overlay_clip`, izvirnega videoposnetka (`video_clip`) in `end_text_overlay_clip`.

10. **Shranjevanje videoposnetka**:
    - Izboljšan videoposnetek se shrani v določeno izhodno pot s pomočjo metode `write_videofile` s kodekom, nastavljenim na 'libx264'.

### Funkcija "edit_all_videos":

Ta funkcija avtomatizira postopek izboljšave videoposnetkov za več videoposnetkov na podlagi JSON konfiguracijske datoteke.

1. **Nalaganje konfiguracije**:
   - Začne z branjem JSON konfiguracijske datoteke, odstrani morebitne komentarje in jo analizira s pomočjo vgrajene knjižnice json v Pythonu. Konfiguracija mora vsebovati podrobnosti za vsak videoposnetek, ki ga želite izboljšati. Pogledaj spica.json!

2. **Zanka za videoposnetke**:
   - Funkcija zanka preide skozi vsak videoposnetek v določeni mapi. Za vsak videoposnetek preveri, ali ima povezan konfiguracijski element v JSON datoteki.

3. **Obravnavanje videoposnetkov**:
   - Če najde konfiguracijski element, skript kliče `add_title_and_end_screen`, da izboljša videoposnetek z navedenimi podrobnostmi, vključno z naslovom videoposnetka, podnaslovom in drugimi informacijami.

4. **Skrivanje udeležencev**
   - Če v spica.json je postavljen element `place` na bottom ali right, to pomeni da v posnetku so vidni udeleženci in jih mora skriti. Skripa kliče `hide_people`.
   - V funkciji hide_people se prav tako nahaja parameter "cut". Ta parameter običajno prevzame vrednost 0 v .json datoteki, razen če so udeleženci vidni na celotnem zaslonu že na začetku posnetka. V takem primeru se ta parameter uporablja za odložitev začetka videoposnetka, kar omogoča, da se udeleženci odstranijo od začetka.

5. **Videoposnetek ni najden**:
   - Če videoposnetek nima povezanega konfiguracijskega elementa, skript izpiše sporočilo, ki označuje, da videoposnetka ni

### Funkcija "hide_people":

Funkcija hide_people skrije ljudi v videoposnetku na podlagi navedene pozicije.

## Funkcija `edit_all_videos`

Ta funkcija avtomatizira postopek izboljšave videoposnetkov za več videoposnetkov na podlagi JSON konfiguracijske datoteke.

1. **Nalaganje konfiguracije**:
   - Začne z branjem JSON konfiguracijske datoteke, odstrani morebitne komentarje in jo analizira s pomočjo vgrajene knjižnice json v Pythonu. Konfiguracija mora vsebovati podrobnosti za vsak videoposnetek, ki ga želite izboljšati. Pogledaj `spica.json`!

2. **Zanka za videoposnetke**:
   - Funkcija zanka preide skozi vsak videoposnetek v določeni mapi. Za vsak videoposnetek preveri, ali ima povezan konfiguracijski element v JSON datoteki.

3. **Obravnavanje videoposnetkov**:
   - Če najde konfiguracijski element, skript kliče `add_title_and_end_screen`, da izboljša videoposnetek z navedenimi podrobnostmi, vključno z naslovom videoposnetka, podnaslovom in drugimi informacijami.

4. **Videoposnetek ni najden**:
   - Če videoposnetek nima povezanega konfiguracijskega elementa, skript izpiše sporočilo, ki označuje, da videoposnetka ni.

## Funkcija `hide_people`

1. **Parametri:**
   - `video_path` (str): Pot do vhodne videodatoteke.
   - `output_path` (str): Pot do izhodne videodatoteke.
   - `position` (str): Pozicija, kjer se postavi skrivalni trak. Če je "None", skrivanje ni izvedeno.
   - `start_time` (int): Parameter se uporablja za odložitev začetka videoposnetka, kar omogoča, da se udeleženci odstranijo že od začetka.

2. **Delovanje:**
   - Naloži vhodni videoposnetek in skrije ljudi s prekrivanjem z zastavo.
   - Če je `start_time` večji od 0, se začetek posnetka odloži za določen čas.
   - Shrani spremenjeni videoposnetek na navedeno izhodno pot.

## Glavna funkcija `main`

Ta funkcija je odgovorna za zagon skripte z ukazi iz ukazne vrstice. Sprejema argumente, ki določajo pot do konfiguracijske datoteke (`-c`), vhodnega videa (`-i`) in izhodnega videa (`-o`).


 
