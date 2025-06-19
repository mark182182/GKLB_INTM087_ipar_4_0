# GKLB_INTM087_ipar_4_0

Motorsebesség szabályozás hőérzékelő segítségével.

# A projekt céljának ismertetése

Olyan beágyazott rendszer létrehozása, amivel képesek vagyunk egy kapcsoló segítségével egy egyenáramú motor vezérlését be- és kikapcsolni, illetve a motor sebességét szabályozni egy hőérzékelő által mért adatok alapján segítségével.

# Hardveres követelmények

- Raspberry Pi 4 Model B
- Breadboard BB-102 (630/200)
- KC-1602-BB-I2C LCD kijelző
- RC522-MFRC RFID író/olvasó (és hozzátartozó RFID kulcsok)
- STUP-SX1308 DC-DC konverter modul 2.5...28V step-up, 2A
- MAB400 Nagy teljesítményű motor 12V DC, 6.8W
- L298N-MOD Kettős teljes H-híd, motor meghajtó modul
- DS18B20+ Hőmérő IC, digitális
- Fémréteg ellenállás 4,7 K 1% 0,6W
- TACT-64N-F mikrokapcsoló, SPST-NO, THT, 6 x 6mm, 4.3mm, fekete
- Szalagkábelek csatlakozóval RC-40-20/MF és RC-40-20/MM

# Futtatás

- `start.sh` szkript indításával x86 és ARM alatt
