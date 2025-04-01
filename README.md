# fa_to_nc
1/ Récupérer les scripts :
- script_traitement_SR_light.py :
        Script principale
        En argument : date de début, date de fin au format YYYMMDD
        Ex pour récupérer le mois de janvier 2023 : script_traitement_SR_light.py 20230101 20230131

- num_jour_between.py
- fonction_recup.py
- fonction_recup_analyse.py
- prestaging.py
- prestaging_abalyse.py
- script_recup.py

2/ Créer l'arborescence :
Il faut une aborescence pour les .nc (DATA/) mais aussi pour les .fa temporaire (temp/).
Ex : mkdir DATA/2023MM, mkdir temp/20023XX
De cette façon, tu peux convertir plusieurs mois en même temps, sans que les fichiers impiètent l'un sur l'autre.

3/ Modifier dans le script principal :
- Si tu veux récupérer les analyses :
        import fonction_recup_analyse (L30)
        prestaging_analyse.py (L57)
- Si tu veux récupérer les prévisions :
        import fonction_recup (L30)
        prestaging.py (L57)
- Les dossiers d'accueil : je passe par /d0, je te conseille de faire pareil. Modifie selon ton arborescence (L55, L97, L120, L176)

4/ Lancer ;)
