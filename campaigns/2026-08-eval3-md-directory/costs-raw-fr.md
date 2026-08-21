# Coûts — tour B′ (eval3), 60 questions, 2026-08-20

Effort : bras et juges Claude à l'effort de session « high » (hérité) ; Qwen sans réglage d'effort.

| Bras | Tokens | Appels réels | Auto-déclaré | Durée |
|---|---|---|---|---|
| B′ MD Sonnet | 309 312 | 115 | 84 | 911 s |
| B′ MD Opus | 539 835 | 61 | 61 | 944 s |

Rappel v2 (bras B, PDF + extraits texte + grep) :
| B Sonnet | 158 184 | 25 | — | 701 s |
| B Opus | 240 754 | 62 | — | 1 246 s |

Contamination : zéro violation sur les deux bras (grep des appels d'outil du
transcript contre la liste interdite ; contrôle éprouvé sur étalon positif).
Prédiction 2 du pré-enregistrement (B′ < B en tokens et appels) : FALSIFIÉE
sur les tokens dans les deux campagnes (×1,96 et ×2,24) ; appels : Sonnet ×4,6,
Opus égalité. Lecture de notices entières ≫ fenêtres grep.

## Qwen 3.8 27B (Q4_K_M, llama.cpp sur padme) — bras C à froid

| Bras | Tokens entrée | Tokens génération | Durée | Vitesse |
|---|---|---|---|---|
| C Qwen | 2 781 | 26 135 (dont ~18k raisonnement) | 859 s | 30,4 tok/s |

Comptage serveur (usage llama-server), conforme §5. Quatre tentatives :
trois avortées par l'instabilité du service systemd naissant (documentée par
la session de déploiement, unité corrigée MR padme#71), la quatrième propre.
Adaptation protocolaire : pas d'outils côté API nue — la feuille de questions
est inlinée dans le prompt (équivalent « lis ce fichier et lui seul »).
