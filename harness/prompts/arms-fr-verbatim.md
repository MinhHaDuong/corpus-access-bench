> Redacted under the naming policy (PROTOCOL.md): the two reference
> works are described by role, never named. The unredacted original is
> sealed with the instrument and recorded in `instrument/MANIFEST.sha256`.

# Prompts verbatim des quatre bras (campagnes v2, août 2026)

Servir tel quel à chaque bras (agent frais, un tirage). Remplacer les chemins
par l'emplacement réel des artefacts. Le modèle candidat se règle au
lancement ; les prompts ne changent pas.

## Bras A — carte

Réponds à un questionnaire d'histoire de la pensée économique.
Lis d'abord et uniquement ce fichier de questions : <feuille-de-reponse.md>

RESSOURCES : une carte du champ extraite du reference work on the History of
Economic Analysis (the reference work's editors, the publisher, 2016) — 196 notices, folios,
1613 renvois : <conception/reference work-canon.md> (liste), <conception/reference work-map.md>
(notices + renvois). Les trois volumes du reference work en PDF + extraits texte.
Page précise : pdftotext -f N -l N -layout <pdf> -. La carte donne des folios
imprimés ; décalage PDF : +27 au a volume ; caler II/III sur l'en-tête courant.
La carte ne dit pas le contenu : elle route vers des pages. Pour répondre au
fond, ouvre les pages.

INTERDICTIONS STRICTES — leur violation invalide la mesure :
aucun accès web ; ne lis AUCUN fichier sous article-het/, aucun *.tex, ni
refs.bib, ni STATE.md, ni tickets/, ni conception/ autre que les deux
fichiers nommés, ni aucun répertoire eval* autre que la feuille.
Plafond : 200 appels d'outil.

CONSIGNE : réponds aux 60 questions, 150 mots max chacune, numérotées 1-60,
en français. Si tu ne sais pas, dis-le : une abstention honnête est notée
séparément d'une erreur affirmée, et vaut mieux qu'elle. N'invente aucune
référence. Termine par exactement deux lignes :
TOOL CALLS: <nombre>
SOURCES USED: <ce que tu as réellement ouvert — notices et folios consultés>
Ton texte final EST le livrable ; il sera corrigé en aveugle. Pas de
préambule, pas de commentaire de méthode hors des deux lignes finales.

## Bras B — PDF sans carte

Identique au bras A, en remplaçant le bloc RESSOURCES par : les trois volumes
du reference work en PDF + extraits texte complets (grep dedans pour localiser) ;
et en ajoutant aux interdictions : pas de conception/ du tout (notamment PAS
reference work-canon.md ni reference work-map.md), pas de .knowledge.toml.

## Bras C — à froid

Réponds à un questionnaire d'histoire de la pensée économique.
Lis ce fichier de questions, et lui seul : <feuille-de-reponse.md>
Après cette lecture, n'utilise PLUS AUCUN outil : ni fichier, ni web, ni
shell. Tu réponds uniquement depuis ce que tu sais déjà.
[Même CONSIGNE que le bras A.]

## Bras D — web seul

Réponds à un questionnaire d'histoire de la pensée économique.
Lis d'abord ce fichier de questions, et lui seul : <feuille-de-reponse.md>
RESSOURCES : WebSearch et WebFetch, exclusivement.
INTERDICTIONS : ne lis AUCUN fichier local autre que la feuille. Plafond 200
appels. Cite tes sources web.
[Même CONSIGNE que le bras A.]

## Juges (3 par campagne, modèle ≠ candidats, accès web)

Lire dans l'ordre : feuille-de-reponse.md, rubric-v2.md (la suivre
exactement, aveuglement partiel et corrigé indicatif compris), corrige.md,
puis les cinq copies blind-<campagne>/copie-1..5.md. Vérifier au web ; les
vérifications du juge priment le corrigé. Ne lire ni answers-*, ni KEY-*,
ni SCELLE-*. Sortie au format strict de rubric-v2.md (60 lignes notées par
copie, TOTAL /60, FABRICATIONS, PLUS FAIBLES, ## classement).
Angles : J1 grille nue ; J2 fabrication et assurance rhétorique ; J3
substance historiographique (l'articulation demandée, pas deux notices
juxtaposées).
