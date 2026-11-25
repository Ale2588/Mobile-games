# Small Hours

Piccoli giochi per la notte: da giocare con una mano sul telefono, in 5–15 minuti.

Small games for the small hours. Piccoli giochi per le ore piccole.

## Giochi

| Gioco | Stato |
|---|---|
| **Ultima Corsa**: accendi i lampioni e porta la gente al tram prima dei vampiri. | prototipo |
| **Non voltarti**: riporta i tuoi amici a casa attraverso il bosco, con una torcia. | prototipo |

## Contenuto della repository

- [`docs/progettazione.md`](docs/progettazione.md): marchio, pubblico, mappa del sito, pagine, flussi, pagamenti, lingue, contratto tra sito e giochi, fasi.
- [`docs/design-system.md`](docs/design-system.md): le regole del design system.
- [`design-system/`](design-system/): variabili, componenti e la vetrina dal vivo (`index.html`).
- `assets/games/`: le copertine dei giochi.
- `assets/brand/`: simbolo, icone, illustrazione della Home, anteprima di condivisione.

## Il sito

```
python3 tools/build.py        # genera dist/
cd dist && python3 -m http.server 8000
```

- Pagine in `/it/` e `/en/`, giochi in `games/<slug>/` con il loro `manifest.json`.
- Testi in `i18n/it.json` e `i18n/en.json`.
- `site.config.json`: `"payments": false` tiene spenti prezzi e sblocchi (fase di prova, tutto aperto); `"feedbackEmail"` è l'indirizzo a cui arrivano i pareri (vuoto: il parere si copia e si manda a mano).
- Ogni push su `main` pubblica il sito su GitHub Pages (`.github/workflows/pages.yml`). Per attivarlo: Settings → Pages → Source: **GitHub Actions**.

## Vedere la vetrina del design system

Apri `design-system/index.html` nel browser.
