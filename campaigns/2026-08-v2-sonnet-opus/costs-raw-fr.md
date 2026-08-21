> Redacted under the naming policy (PROTOCOL.md): the two reference
> works are described by role, never named. The unredacted original is
> sealed with the instrument and recorded in `instrument/MANIFEST.sha256`.

# Coût par bras — mesure v2, 60 questions

## Campagne Sonnet

| Bras | Tokens | Appels | Durée |
|---|---|---|---|
| C à froid | 79 341 | 1 | 379 s |
| D web | 139 535 | 64 | 509 s |
| B PDF sans index | 158 184 | 25 | 701 s |
| A carte → reference work | 252 510 | 74 | 985 s |

## Campagne Opus

| Bras | Tokens | Appels | Durée |
|---|---|---|---|
| C à froid | 73 633 | 1 | 432 s |
| D web | 126 584 | 78 | 1 143 s |
| B PDF sans index | 240 754 | 62 | 1 246 s |
| A carte → reference work | 246 721 | 55 | 905 s |

Contamination : zéro violation sur les huit bras (grep des appels d'outil
contre les listes interdites déclarées ex ante). Plafond de 200 appels
respecté partout (max 78).

Note : le bras D Opus a signalé un budget WebSearch épuisé avant sa première
requête — tout son accès web est passé par WebFetch sur des pages nommées de
mémoire (essentiellement Wikipédia). À rapporter avec la mesure : son coût et
sa couverture ne sont pas ceux d'un bras avec recherche pleine.
