# Coûts — tours eval4 (colonnes Fable et Qwen), 60 questions, 2026-08-20/21

Effort : bras et juges Claude à l'effort de session « high » (hérité par les
sous-agents) ; Qwen (27B Q4_K_M, llama.cpp/padme) sans réglage d'effort.

## Colonne Fable (effort high)

| Bras | Tokens | Appels réels | Durée |
|---|---|---|---|
| C à froid | 73 762 | 1 | 652 s |
| D web | 83 901 | 18 | 888 s |
| B PDF+extraits | 122 418 | 26 | 854 s |
| A carte | 227 460 | 41 | 981 s |
| B′ répertoire MD | 277 433 | 34 | 1 094 s |

Caveat bras D : budget WebSearch de session épuisé (200/200) — repli sur
WebFetch de pages nommées de mémoire (Wikipédia, hetwebsite) ; coût et
couverture non comparables à une recherche pleine (même défaut que D-Opus v2).
Contamination : zéro violation réelle sur les cinq bras (deux faux positifs
qualifiés sur pièce : étiquette echo « extraits » ; appel ToolSearch).

## Colonne Qwen

| Bras | Tokens génération | Appels | Durée | Notes |
|---|---|---|---|---|
| C à froid | 26 135 (entrée 2 781) | 0 | 859 s | comptage serveur |
| B′ répertoire MD | en cours | — | — | runner par blocs de 10 q. |
| B / A / D | file séquentielle sur padme | — | — | --parallel 1 |

## Tour de jury colonne Fable — résultats (moyenne de 3 juges, panel mixte Opus/Fable/Sonnet, effort high)

| Copie | Moy/60 | C/P/A |
|---|---|---|
| C-fable | 58,50 | 19,6/19,1/19,8 |
| B-fable | 58,50 | 19,7/19,2/19,6 |
| B′-fable | 58,50 | 19,7/19,5/19,3 |
| ancre C-opus-v2 | 57,75 | (v2 : 56,00 — dérive jury +1,75) |
| A-fable | 57,08 | |
| D-fable | 56,83 | |
| salée | 50,58 | coulée (J1 41,25) |

Étalonnage : union des détections 6/6 (J2 seul fait 6/6 ; J1 ~5 par les
scores ; J3 1 ferme + 1 suspectée) ; médian ≈ 5 ≥ 3 → panel VALIDE.
Accord inter-juges : 0,111 ; 264/420 identiques. Verdict colonne Fable :
l'accès ne change RIEN à la note (C = B = B′ = 58,50 ; carte et web
légèrement en dessous) — Fable sature à froid, plus nettement encore
qu'Opus. Caveat J3 : dossier réécrit par un fork interne puis corrigé sur
pièce (copie-6) — limite documentée.

## Colonne Qwen — coûts mesurés (comptage serveur, runner par blocs)

| Bras | Tokens génération | Appels outils | Durée | Incidents |
|---|---|---|---|---|
| C | 26 135 | 0 | 859 s | 3 tentatives perdues (service naissant) |
| B′ MD | 138 834 + 26 135* | 135 | 6 109 s + re-run | bloc 21-30 vide (rumination 24k), re-run /no_think |
| B PDF-extraits | 166 259 + ~38k* | 71+1 | 6 472 s + re-runs | bloc 1-10 vide ; re-runs 1-5 puis 6-10 (mémoire seule sur 1-5) |
| A carte | 145 432 | 95 | 7 207 s | aucun |
| D web | en cours | — | — | web DDG/fetch best-effort |

*re-runs inclus. Défaut de classe documenté : sur certains blocs le modèle
épuise tout max_tokens (24k) en raisonnement sans émettre de contenu ; le
correctif (retry « /no_think ») est dans les runners archivés. Contamination :
structurelle par construction (outils du runner verrouillés sur les
ressources du bras ; aucun autre accès n'existe côté API).

## Incident de préparation — tour Qwen, copie D (2026-08-21)

La réparation du bras D (re-run du bloc 51-60) avait ajouté le bloc APRÈS la
ligne « TOOL CALLS », qui sert de marqueur de fin à la fonction
d'anonymisation : les dix questions ont donc été tronquées à l'aveugle. Le
juge substance l'a signalé de lui-même (« copie-1 s'interrompt, 51-60
absentes ») — c'est ce signalement, non un contrôle automatique, qui a
révélé le défaut : mon contrôle de complétude portait sur la copie source,
pas sur la copie anonymisée servie aux juges. Correctif : contrôler la
complétude APRÈS anonymisation, sur le fichier réellement servi.
Réparation : trailer déplacé en fin de fichier, copie ré-anonymisée
(60/60), et complément de notation demandé aux trois juges sur ces dix
questions seulement, chacun reprenant son propre dossier.
