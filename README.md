# fa_to_nc
1/ Récupérer les scripts :
- script_traitement_SR_light.py : ne récupère que les champs 2D
        Script principal
        En argument : date de début, date de fin au format YYYMMDD
        Ex pour récupérer le mois de janvier 2023 : script_traitement_SR_light.py 20230101 20230131

  - script_traitement_SR.py : récupère les champs 3D et les champs 2D.
        Script principal
        En argument : date de début, date de fin au format YYYMMDD

- num_jour_between.py (dans le dossier ../tools)
- fonction_recup.py
- fonction_recup_analyse.py
- prestaging.py
- prestaging_analyse.py
- script_recup.py
- Pour récupérer les champs 3D de contenu et les convertir en champs 2D (ex : LWP/IWP) : ../tools/masse_lwp_iwp.py et calcul_pression.py
Ainsi que le fichier /d0/Users/magnaldom/STOCKAGE_AROME_UP/A_B_AROME.nc.
Actuellement, calcul mis en place uniquement dans script_traitement_SR.py, mais tu peux copier cette partie dans script_recup_light.py.

Pour récupérer une expérience AROME :
- script_traitement_expe_SR(_light).py : récupère les champs 3D (2D) pour des expériences AROME
        Script principal
        En argument : date de début, date de fin au format YYYMMDD, nom de l'expérience ZZZZ.
        Ex : script_traitement_expe_SR_light.py 20230101 20230131 G017
- fonction_recup_expe.py
- prestaging_expe.py
- script_recup_expe.py

2/ Créer l'arborescence :
Il faut une aborescence pour les .nc (DATA/) mais aussi pour les .fa temporaire (temp/).
Ex : mkdir DATA/2023MM, mkdir temp/20023MM
De cette façon, en créant un dossier par mois, tu peux convertir plusieurs mois en même temps, sans que les fichiers impiètent l'un sur l'autre.

3/ Modifier dans le script principal (les lignes indiquées sont les lignes du script script_traitement_SR.py, mais ces lignes sont présentes dans les autres script_traitement*.py) :
- Les variables que tu veux récupérer (séparer 2D et 3D)
- Si tu veux récupérer les analyses :
        import fonction_recup_analyse (L28)
        python3 prestaging_analyse.py (L66)
        python3 script_recup_analyse.py (L68)
- Si tu veux récupérer les prévisions :
        import fonction_recup (L28)
        prestaging.py (L66)
        script_recup.py (L68)
- Les dossiers d'accueil : je passe par /d0, je te conseille de faire pareil. Modifie selon ton arborescence (L64, L107, L130, L186)
- Adapter les variables lues dans les boucles (L206, L223, L244), toutes les variables ne sont pas cherchées dans les .fa (pas le cas des LWP etc.)

4/ Egalement modifier les chemins dans les autres scripts :
- fonction_recup.py (L53, L80)
- script_recup.py (L52)

5/ Vider les dossiers /DATA/YYYYMM et temp/YYYYMM.

6/ Lancer ;)

Notes : 
Les scripts de récupération et de traitement sont lancés en parallèle, ce qui signifie que si l'un ne fonctionne pas, l'autre continuera de tourner dans tous les cas. Ce n'est pas un problème quand c'est script_recup.py qui ne fonctionne pas (car script_traitement.py ne peut pas fonctionner sans lui), mais script_recup peut continuer de télécharger les .fa même si script_traitement n'arrive pas à les traiter. Dans ce cas là, il faut kill le process manuellement (top, kill XXXX).
