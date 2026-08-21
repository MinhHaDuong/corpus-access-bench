> Redacted under the naming policy (PROTOCOL.md): the two reference
> works are described by role, never named. The unredacted original is
> sealed with the instrument and recorded in `instrument/MANIFEST.sha256`.

# Protocole pré-enregistré — mesure v2 de la carte du champ HET

Date de gel : 2026-08-20, avant tout tirage. Ce document est committé avant le
lancement des bras ; les prédictions ci-dessous ne peuvent plus être ajustées
après coup. Les questions, les copies, le corrigé et la clé d'anonymat restent
hors du dépôt (répertoire de travail de session) : une session future qui les
lirait fausserait toute reprise.

## Ce que la mesure décide

La cartographie d'ouvrages de référence (le *the independent reference work*, ~1 890 notices,
serait le prochain chantier) se poursuit si, sur les strates périphérie +
adjacence (40 questions), le bras carte dépasse le bras PDF-sans-index d'au
moins 2 points chez Sonnet. En dessous, la carte n'apporte pas assez au-dessus
de la simple détention du corpus pour justifier le coût d'extraction.

## Leçon de la mesure v1

La v1 (STATE.md, 20/08) a classé quatre bras dans un intervalle de trois
points : toutes ses questions étaient canoniques, donc à portée de la mémoire
paramétrique. Preuve par l'écart : le même modèle à froid a fait 2,5/20 sur le
questionnaire d'appareil (écarté par l'auteur) et 16,92/20 sur le questionnaire
canonique — quatorze points portés par le seul choix des questions.
L'instrument mesurait la main de son auteur. D'où la stratification.

## Dispositif

**60 questions, trois strates de 20**, mélangées et non étiquetées sur la
feuille servie aux bras (l'appartenance de strate reste dans un fichier hors de
leur portée) :

- **Canon (C)** — strate de contrôle : programme doctoral standard. Le bras à
  froid doit y réussir ; sinon c'est le dispositif qui déraille.
- **Périphérie (P)** — figures mineures, textes peu traduits, querelles
  locales : couverture réelle dans les ouvrages de référence, faible dans les
  manuels et l'entraînement.
- **Adjacence (A)** — où les choses se situent : filiations, fronts, passeurs.
  La strate où un appareil de renvois croisés devrait porter.

**Quatre bras**, mêmes définitions que la v1 :

| Bras | Moyens |
|---|---|
| A′ carte | `.knowledge.toml` → canon → carte → pages du reference work ; pas de web |
| B PDF | les trois volumes du reference work, `pdftotext` ; ni web ni carte |
| C froid | rien : lit les questions, répond |
| D web | WebSearch/WebFetch seuls ; aucun fichier local |

**Deux campagnes** : les quatre bras en `sonnet`, puis les quatre en `opus`.
Un tirage par bras et par modèle ; la longueur (60 questions, n=20 par strate)
tient lieu de réduction de variance — limite assumée : pas d'estimation de
variance intra-bras.

**Interdictions communes, déclarées ex ante** (contrôle par grep des appels
d'outil de chaque bras AVANT correction ; violation = copie invalide) :
`article-het/`, tout `*.tex`, `refs.bib`, `STATE.md`, `tickets/`,
`conception/` (sauf, pour A′ seul, `reference work-canon.md` et `reference work-map.md`),
les répertoires d'évaluation, et le web pour les bras non-D. Aucune question ne
touche l'objet du manuscrit (la cohérence de cycle) ; la question v1 qui s'en
approchait est retirée.

**Plafond** : 200 appels d'outil par bras. Coûts (tokens, appels, durée)
rapportés par bras et par strate de la note.

## Correction

**Trois correcteurs `fable`** — décorrélés des deux modèles candidats — en
aveugle, avec accès web, sur la grille v1 (barème 0-1 par pas de 0,25,
abstention honnête 0,50-0,75, fabrication 0,00 + signalement, aveuglement
partiel assumé et neutralisé par consigne). Trois angles : grille nue, chasse à
la fabrication, substance historiographique. Sortie par question, agrégée par
strate.

**Copie salée** : une cinquième copie, fabriquée après réception des vraies
copies dans leur style, porte 6 défauts documentés à l'avance dans un fichier
scellé hors de portée des juges — date fausse plausible, référence inexistante,
référence réelle détournée, notice/folio inventé, paternité inversée, citation
forgée. **Validité du jury** : l'union du panel détecte ≥ 5/6 et le juge médian
≥ 3/6. En dessous, les verdicts du panel sur les vraies copies sont réputés
non informatifs et la correction est refaite avec d'autres juges — la
conclusion ne change pas, le jury change.

## Prédictions gelées

Campagne Sonnet :
1. Canon : les quatre bras ≥ 15/20 ; écart max ≤ 2,5 (strate non discriminante
   par construction).
2. Périphérie : à froid ≤ 10/20 ; carte et PDF ≥ à froid + 4 ; web
   intermédiaire.
3. Adjacence : carte ≥ PDF ≥ web, et carte ≥ web + 3.
4. Global : carte > PDF ; l'ordre web/froid n'est pas prédit — la v1 a donné
   web < froid, contre l'intuition ; la v2 teste la réplication.
5. Coût : PDF > carte > web > froid en tokens (réplication v1).

Campagne Opus : mêmes ordres, écarts de périphérie resserrés (ligne de base
paramétrique plus haute), canon saturé (≥ 18 partout).

**Seuils d'invalidation** : une strate où les quatre bras tiennent dans
2 points est non discriminante ; si périphérie ET adjacence sont non
discriminantes chez Sonnet, le questionnaire v2 a échoué comme la v1 et se
refait — sans toucher aux prédictions ci-dessus, qui restent le verdict de
cette tentative-ci.

## Validation des questions, avant tirage

Les strates P et A portent des présupposés factuels que l'auteur du
questionnaire ne peut pas tous garantir de tête. Avant le lancement, un agent
valideur (web + texte du *independent reference work*, indépendant du corpus des bras) vérifie
chaque présupposé et signale toute question mal posée ; les questions
signalées sont corrigées ou remplacées avant tout tirage. Le corrigé de
référence est ensuite construit depuis le *independent reference work* — pas depuis le reference work
sur lequel travaillent les bras — pour casser la circularité corpus/corrigé.

## Artefacts

Hors dépôt, dans le répertoire de session : questions par strate, feuille
mélangée, mapping des strates, copies, notes des juges, clé d'anonymat,
défauts de la copie salée, agrégats. Dans le dépôt : ce protocole seul.
