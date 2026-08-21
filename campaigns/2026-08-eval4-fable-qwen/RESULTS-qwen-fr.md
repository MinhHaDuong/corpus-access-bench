> Redacted under the naming policy (PROTOCOL.md): the two reference
> works are described by role, never named. The unredacted original is
> sealed with the instrument and recorded in `instrument/MANIFEST.sha256`.

# Tour Qwen (eval4) — résultats et verdict, 2026-08-21

Pré-enregistrement : addendum « enjeu 27B », MR #195, committé avant tout run.
Effort : juges Claude à l'effort de session ; Qwen 27B Q4_K_M sans réglage.

## Notes (moyenne de 3 juges : J1 grille/Opus, J2 fabrication/Opus, J3 substance/Sonnet)

| Copie | J1 | J2 | J3 | moy/60 | Canon | Périph | Adjac | P+A/40 |
|---|---|---|---|---|---|---|---|---|
| ancre Opus-C v2 | 51,50 | 55,75 | 58,75 | 55,33 | 18,7 | 18,4 | 18,2 | 36,67 |
| copie salée | 53,00 | 54,00 | 55,75 | 54,25 | 18,5 | 17,6 | 18,2 | 35,75 |
| **Qwen B′ (MD)** | 42,25 | 43,00 | 49,50 | **44,92** | 15,3 | 15,2 | 14,3 | **29,58** |
| Qwen A (carte) | 37,25 | 38,50 | 43,50 | 39,75 | 14,2 | 12,2 | 13,3 | 25,50 |
| Qwen B (PDF) | 34,50 | 36,25 | 42,00 | 37,58 | 14,1 | 11,6 | 11,9 | 23,50 |
| Qwen D (web) | 27,50 | 25,50 | 37,00 | 30,00 | 11,7 | 8,7 | 9,7 | 18,33 |
| Qwen C (froid) | 26,00 | 21,25 | 26,75 | 24,67 | 8,8 | 7,8 | 8,1 | 15,83 |

## Verdicts contre les prédictions gelées

1. **ΔQwen(B′−C) ≥ +2 sur périphérie+adjacence : TIENT, +13,75.** Le corpus
   outillé fait passer Qwen de 24,67 à 44,92/60 (+20,25 au total). Le
   répertoire MD domine les deux autres accès : +4,08 sur la carte, +6,08
   sur les PDF/extraits. Même le bras web (+5,33 vs froid) aide.
2. **Zéro faux « pas de notice » : TIENT.** Les quatre revendications
   d'absence de Qwen B′ (Richard Jones, W. F. Lloyd, John Rae, Mangoldt)
   sont exactes, vérifiées par `ls` du répertoire ; contrôle positif
   (Menger) conforme.
3. Coût : rapporté sans seuil (voir couts.md).

## Étalonnage du jury — VALIDE, avec une limite structurelle

Détections (défaut nommé dans FABRICATIONS ou noté ≤ 0,25) : J1 4/6,
J2 5/6, J3 1/6 → **union 5/6, médian 4** (critère : union ≥ 5, médian ≥ 3).
Le seul défaut jamais détecté est **Q13, le folio inventé** (« notice Menger,
I, 310-315 ») : les juges avaient interdiction d'ouvrir le corpus, donc
aucun moyen de vérifier un folio. Défaut de conception du scellé pour ce
tour — ne pas sceller de défaut de folio dans un tour où le jury n'a pas
accès au corpus. Accord inter-juges : 0,171 (contre 0,111 au tour Fable),
180/420 identiques — dispersion attendue sur des copies très inégales.

Ancre Opus-C : 55,33 ici, 57,75 au tour Fable, 56,00 en v2 → dérive
−2,42 vs tour Fable (effet de contexte : le même juge note plus sévèrement
dans un lot faible). Les comparaisons se lisent donc à l'intérieur d'un
tour, jamais entre tours sans l'ancre.

## Réserve honnête sur le bras B′

La copie Qwen B′ déclare, pour les blocs 1-10 et 51-60, n'avoir consulté
aucune notice (réponses de mémoire) : l'avantage mesuré vient des quatre
blocs où l'outil a servi. L'effet est donc probablement sous-estimé, pas
surestimé.

## Décision (règle pré-enregistrée, MR #195)

La prédiction 1 tenant : **le répertoire MD est adopté comme couche d'accès
au corpus pour les petits modèles locaux**, et **l'extraction du New
independent reference work en répertoire est justifiée par le même argument**.

Ce verdict ne renverse pas celui du tour B′ (MR #194) : pour Sonnet, Opus
et Fable, l'accès au corpus reste sans effet sur la note (Fable : C = B =
B′ = 58,50). Les deux résultats se composent — le corpus outillé est un
levier pour les petits modèles, une dépense inutile pour les grands.
