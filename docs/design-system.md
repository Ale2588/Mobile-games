# Design system · Nottambuli

La vetrina dal vivo è in [`design-system/index.html`](../design-system/index.html). Questo file spiega le regole.

## File

- `design-system/tokens.css`: tutte le variabili (colori, tipografia, spazi, forme, movimento). Si cambia qui e cambia tutto.
- `design-system/components.css`: i componenti, con classi brevi e piatte e nessun framework.
- `design-system/index.html`: la vetrina, con le tre schermate chiave in finti telefoni.

## Regole d'uso

1. **Un solo pulsante primario per schermata.** È la luce: se ce ne sono due, nessuna è la luce.
2. **Il testo non scende sotto i 16 px**; 14 px solo per i metadati, 12 px solo per le etichette in maiuscolo.
3. **Le aree di tocco sono di almeno 48 px.** Le azioni principali stanno nella metà bassa dello schermo.
4. **Il bianco puro è vietato.** Il testo è `--ink-100`, color carta.
5. **Il colore non è mai l'unica informazione.** La difficoltà è fatta di lune piene e vuote, le stelle di pieni e vuoti, gli stati hanno sempre un'etichetta scritta.
6. **L'accento del gioco** si attiva con `data-game="<slug>"` su un contenitore: dentro quel contenitore `--game-accent` diventa il colore del gioco, e pulsanti primari, barre e lune lo seguono.

## Colori

| Ruolo | Variabile | Valore |
|---|---|---|
| Fondo | `--bg` | `#07080b` |
| Superfici | `--surface` | `#0c0f14` |
| Carte | `--card` | `#12161d` |
| Testo | `--text` | `#e6e2d8` |
| Testo secondario | `--text-2` | `#9aa3b2` |
| Accento (luce) | `--accent` | `#f3c76a` |
| Informazione, focus | `--moon-400` | `#8cc4ff` |
| Sbloccato | `--ok-400` | `#7fd0a0` |
| Pericolo | `--danger-400` | `#ff5a4e` |

Accenti dei giochi: Ultima Corsa `#f3c76a` (lampioni), Non voltarti `#ff8a5c` (torcia e bengala).

## Tipografia

- **Fraunces** (titoli): un serif caldo con un'aria da libro di racconti notturni. Corsivo per gli accenti emotivi ("Scegli una luce.").
- **Inter** (interfaccia e testi): leggibile in movimento e a luminosità bassa.

Scala: 44 · 32 · 24 · 19 · 16 · 14 · 12.

## Componenti

| Componente | Classe | Note |
|---|---|---|
| Pulsante | `.btn` + `--primary`, `--secondary`, `--ghost`, `--icon` | `--block` per tutta larghezza, `--lg` per le azioni principali |
| Etichetta di stato | `.badge` + `--free`, `--new`, `--unlocked`, `--soon` | sempre con testo |
| Carta gioco | `.game-card` | immagine 4:5, titolo serif, gancio, durata, difficoltà |
| Carta compatta | `.row-card` | per "Continua" e per le liste |
| Avanzamento | `.progress > i` | colore del gioco |
| Barra in alto | `.topbar`, `.logo`, `.lang` | lingua a interruttore IT/EN |
| Barra in basso | `.tabbar` | Giochi · Sfida · Progressi |
| Foglio | `.sheet`, `.sheet-backdrop` | sblocchi e conferme; sale dal basso |
| Campo | `.field`, `.input` | codice di sblocco |
| Avviso | `.toast` | conferme ed errori |

## Da decidere

- Caricare i caratteri dal sito stesso invece che da Google Fonts: più veloce e niente richieste a terzi, quindi meglio anche per la privacy.
- Icone: per ora SVG disegnati a mano nella barra in basso; da raccogliere in un unico file quando saranno più di dieci.
