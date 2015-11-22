## Ablauf
- Laden von python3.3.3
```sh
$ module load python/3.3.3
```

- Erzeugen von dummyFiles für Test

```sh
$ python3.3.3 CreateDummyFiles.py 
```

1. Kopieren von '/home/b/beesbook' nach Ziel-Ordner
2. Halli 

    ```
      $ python3.3.3 sortByDayNCam.py 
    ```
    1. Log auf mgl. Fehler checken
    - falseChecksum.csv auf Dateien mit fehlerhafter Checksum prüfen.
    - falsch kopierte Dateien manuell kopieren oder über extra Skript.

2. Checken ob alle Dateien kopiert wurden.
    ```
       $ python3.3.3 final_verification.py
    ```
    1. Status-Files löschen und folgenden Befehl nochmal ausführen um zu überprüfen, bei welchen Dateien die Prüfsummen nicht übereinstimmen
    
        ```
        $ python3.3.3 sortByDayNCam.py 
        ```
3. Ab Punkt 1. wiederholen mit '/gfs1/work/bebesook/beesbook_data_2015'
