# Progettazione del sito

Versione 0.1 · novembre 2026

## 1. Il prodotto in una frase

Una collezione di piccoli giochi notturni da giocare con una mano sul telefono, in 5–15 minuti. Ogni gioco ha una sfida gratuita; campagna e capitoli si sbloccano a pagamento.

## 2. Marchio

**Concetto: la luce nel buio.** Tutti i giochi della collezione girano attorno alla luce: il lampionaio di *Ultima Corsa*, la torcia di *Non voltarti*. Il sito è una notte, ogni gioco è una luce accesa.

**Nome: Small Hours.** "The small hours" sono le ore piccole della notte, più o meno dall'una alle quattro; e i giochi sono piccoli. Il nome è in inglese e resta uguale in tutte le lingue. Sottotitolo: "Small games for the small hours" / "Piccoli giochi per le ore piccole".

Scartati: *Nocturnal Animals* (troppo legato al film di Tom Ford e al thriller), *Last Light* (troppo vicino a *Ultima Corsa*), *Lamplight* e *Night Owls* (generici).

Da fare prima del lancio: verificare dominio e marchio registrato. Il nome è in un solo punto (`--brand-name` e il file delle traduzioni).

**Tono di voce:** frasi brevi, seconda persona, un po' di inquietudine e niente gergo da videogioco. "La notte è lunga. Scegli una luce." Mai "Epic!", mai punti esclamativi a raffica.

## 3. Per chi è

- **Pendolare serale** (25–45 anni). Gioca in tram, una mano sola, partite interrotte. Gli servono avvio immediato, salvataggio automatico e testo leggibile in piedi.
- **Insonne curioso.** Gioca a letto, al buio. Gli servono un tema scuro vero, niente bianchi accecanti e luminosità bassa.
- **Appassionato di giochi da tavolo.** Riconosce le meccaniche e apprezza regole chiare e punteggi. Gli servono regole leggibili prima di pagare e una sfida del giorno da confrontare.

## 4. Mappa del sito

```
/                      Home (lingua dal browser, poi /it/ o /en/)
/it/                   Home italiana
/it/giochi/<slug>/     Scheda gioco
/it/gioca/<slug>/      Il gioco a schermo intero
/it/sfida/             Le sfide del giorno di tutti i giochi
/it/sblocca/<slug>/    Acquisto e codice di sblocco
/it/progressi/         Le mie stelle, i miei sblocchi, ripristino acquisti
/it/info/              Chi siamo, privacy, termini, contatti
/en/...                Stessa struttura: /en/games/, /en/play/, /en/daily/, /en/unlock/, /en/progress/, /en/about/
```

Navigazione mobile: **barra in basso a 3 voci** (Giochi · Sfida · Progressi), raggiungibile col pollice. La lingua si cambia dal menu in alto a destra, non dalla barra.

## 5. Pagine

### Home
1. **Copertina**: il marchio, una riga di concetto e una sola azione, "Gioca la sfida di oggi", che porta alla sfida del gioco in evidenza.
2. **Scaffale**: le carte dei giochi in verticale, a tutta larghezza. Ogni carta ha immagine, titolo, una riga di gancio, durata, difficoltà e lo stato (Nuovo · Gratis oggi · Sbloccato).
3. **In arrivo**: i giochi futuri, in grigio, con "Avvisami".
4. **Piè di pagina**: lingua, info, privacy.

### Scheda gioco
Copertina verticale, titolo e gancio, poi due azioni: **Gioca gratis** (primaria) e **Sblocca la campagna · 1,99 €** (secondaria). Sotto: come si gioca in 3 righe, cosa c'è nella campagna, le tue stelle e i tuoi capitoli.

### Gioca
Schermo intero, senza barra del sito. In alto c'è solo un tasto ✕ per uscire, che chiede conferma se la partita è in corso. Il gioco gira in una pagina a sé (vedi §8).

### Sblocca
Un foglio che sale dal basso, non una pagina nuova. Contiene cosa ottieni (elenco breve), il prezzo, un pulsante di pagamento e il link "Ho già un codice".

### Progressi
Stelle per gioco, sblocchi attivi e "Ripristina acquisti", inserendo il codice ricevuto per email.

## 6. Flussi principali

**Prima visita:** Home → "Gioca la sfida di oggi" → partita → fine partita con punteggio → "Ti è piaciuto? La campagna ha 10 capitoli" → foglio Sblocca.

Il momento per chiedere di pagare è **dopo una partita finita**, mai prima. Il foglio si chiude con un tocco e non torna fino alla partita successiva.

**Ritorno:** Home → la carta del gioco mostra "Continua: capitolo 4" → si gioca direttamente.

**Cambio dispositivo:** Progressi → "Ripristina acquisti" → codice → sblocco attivo. Le stelle restano sul dispositivo; la sincronizzazione arriva in una versione successiva.

## 7. Pagamenti e sblocchi

Proposta per partire senza costruire un backend:

- Sito **statico** (GitHub Pages o Vercel).
- Pagamento con **Lemon Squeezy** oppure **Stripe Payment Links**. Entrambi gestiscono IVA e ricevute e inviano al cliente un **codice di licenza**.
- Lo sblocco si salva sul dispositivo. Il codice si può reinserire su un altro telefono: è la funzione "Ripristina acquisti".
- La verifica del codice si fa con una funzione serverless minima (Vercel) che interroga il fornitore di pagamento. Funziona senza account utente.

Prezzi da testare: **1,99 € per gioco**, oppure **4,99 € per la collezione**. Su un acquisto da 0,99 € la commissione fissa pesa troppo, quindi lo eviterei.

Limite onesto: chi sa smanettare può sbloccare in locale senza pagare. A questa scala va bene; il costo di impedirlo è più alto di quanto si perde.

## 8. Contratto tra sito e giochi

Ogni gioco vive in `games/<slug>/` ed è autonomo. Ha:

```json
// games/<slug>/manifest.json
{
  "slug": "non-voltarti",
  "title": { "it": "Non voltarti", "en": "Don't Look Back" },
  "hook":  { "it": "Riporta tutti a casa prima che il bosco se li prenda.", "en": "..." },
  "minutes": [8, 15],
  "difficulty": 3,
  "accent": "#f3c76a",
  "cover": "cover.jpg",
  "free": "daily",
  "price": { "eur": 1.99 },
  "status": "live"
}
```

Il sito carica il gioco in un `iframe` a schermo intero e si parla con lui tramite `postMessage`:

| Dal gioco al sito | Dal sito al gioco |
|---|---|
| `nt:ready` | `nt:init { lang, unlocked, daily, save }` |
| `nt:score { total, stars }` | `nt:unlocked` dopo l'acquisto |
| `nt:paywall { reason }` | |
| `nt:save { data }` | |
| `nt:exit` | |

Così ogni gioco resta un unico file HTML, come i prototipi attuali, e si può provare anche da solo.

## 9. Lingue

- Ogni pagina esiste in `/it/` e `/en/`. La prima visita sceglie la lingua dal browser e poi la ricorda.
- I testi del sito stanno in `i18n/it.json` e `i18n/en.json`. I testi dei giochi stanno nei giochi, che ricevono `lang` da `nt:init`.
- I titoli dei giochi si traducono, il marchio Small Hours no.

## 10. Vincoli tecnici e qualità

- **Mobile first**: progettato a 360–430 px, con il pollice in basso. Su desktop il contenuto resta in una colonna da 480 px, centrata.
- **Leggerezza**: Home sotto i 300 KB al primo caricamento, immagini in WebP, niente framework obbligatori.
- **Accessibilità**: contrasto AA sul testo, aree di tocco di almeno 44 px, rispetto di `prefers-reduced-motion`, nessuna informazione affidata solo al colore (le basi colorate dei giochi hanno anche forma o lettera).
- **Si può giocare offline** una volta caricato (service worker, fase 2).

## 11. Fasi

1. **Ora**: design system, progettazione, vetrina.
2. Home e schede gioco statiche, con i due giochi attuali dentro il contratto `postMessage`.
3. Sfida del giorno condivisa e pagina Progressi.
4. Pagamenti e codici di sblocco.
5. Offline, statistiche anonime, nuovi giochi.

## 12. Decisioni aperte

- Nome definitivo del marchio.
- Prezzo per gioco o per collezione.
- Dominio e hosting (GitHub Pages è gratuito, Vercel serve per la funzione di verifica).
