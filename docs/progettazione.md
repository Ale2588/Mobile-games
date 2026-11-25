# Small Hours · Progettazione

Versione 1.0 · novembre 2026
Documenti collegati: [design system](design-system.md) · [vetrina dal vivo](../design-system/index.html)

---

## 1. Il prodotto

**Small Hours** è una collezione di piccoli giochi notturni per telefono: si giocano con una mano, in 5–15 minuti, e hanno regole da gioco da tavolo e un punteggio a fine partita. Il sito è insieme la vetrina, la sala giochi e la cassa.

**Modello:** ogni gioco ha una **sfida del giorno gratuita**, uguale per tutti e diversa ogni giorno. **Campagna e capitoli si sbloccano a pagamento**, con un acquisto unico per gioco oppure per l'intera collezione.

**Obiettivi della prima versione**
1. Chi arriva dal link gioca entro 2 tocchi e 5 secondi.
2. Almeno il 40% di chi finisce una sfida ne inizia un'altra (il gioco funziona).
3. Almeno il 3% di chi finisce una partita sblocca la campagna (il modello regge).

**Fuori dalla prima versione:** account con email e password, classifiche globali, multigiocatore, app negli store.

---

## 2. Marchio

**Nome: Small Hours.** "The small hours" sono le ore piccole della notte, più o meno dall'una alle quattro; e i giochi sono piccoli. Il nome resta in inglese in tutte le lingue.

- Sottotitolo EN: *Small games for the small hours.*
- Sottotitolo IT: *Piccoli giochi per le ore piccole.*
- Concetto: **la luce nel buio.** Il sito è la notte, ogni gioco è una luce accesa.
- Simbolo: falce di luna che tiene una lanterna accesa (`assets/brand/`).

Scartati: *Nottambuli* (solo italiano), *Nocturnal Animals* (il film), *Last Light* (troppo vicino a *Ultima Corsa*), *Lamplight* e *Night Owls* (generici).

**Prima del lancio:** verificare la disponibilità di `smallhours.games` o di un dominio simile e del marchio nelle classi 9 e 41.

### Tono di voce

| Sì | No |
|---|---|
| Frasi brevi, seconda persona: "Scegli una luce." | Gergo da videogioco: "Epic win!", "Level up!" |
| Un filo di inquietudine: "La notte è lunga." | Punti esclamativi a raffica |
| Concreto: "10 minuti · gratis" | Vago: "Un'esperienza unica" |
| Il pagamento detto chiaro: "1,99 €, una volta, per sempre" | Urgenza finta: "Solo oggi!" |

---

## 3. Per chi è

| Persona | Quando gioca | Cosa le serve |
|---|---|---|
| **Pendolare serale**, 25–45 anni | Sul tram, in piedi, con una mano | Avvio immediato, salvataggio automatico, testo leggibile in movimento |
| **Insonne curioso** | A letto, al buio | Tema scuro vero, nessun bianco accecante, niente suoni |
| **Appassionato di giochi da tavolo** | Pausa pranzo, sera | Regole chiare prima di pagare, punteggio da confrontare |

---

## 4. Mappa del sito e indirizzi

| Pagina | Italiano | Inglese |
|---|---|---|
| Home | `/it/` | `/en/` |
| Scheda gioco | `/it/giochi/<slug>/` | `/en/games/<slug>/` |
| Gioco | `/it/gioca/<slug>/` | `/en/play/<slug>/` |
| Sfida del giorno | `/it/sfida/` | `/en/daily/` |
| Progressi | `/it/progressi/` | `/en/progress/` |
| Info, privacy, termini | `/it/info/` | `/en/about/` |
| Sblocco riuscito | `/it/grazie/` | `/en/thanks/` |
| Link di una sfida | `/d/<n>` | `/d/<n>` |

`/` sceglie la lingua (§11) e reindirizza. Gli slug dei giochi sono gli stessi in tutte le lingue (`ultima-corsa`, `non-voltarti`), quindi i link si possono condividere.

**Navigazione:** una barra in basso con 3 voci (**Giochi · Sfida · Progressi**) su tutte le pagine tranne il Gioco. In alto: logo a sinistra, selettore lingua a destra.

---

## 5. Pagine nel dettaglio

Ogni pagina è descritta con contenuto, azioni e stati. La vetrina mostra le schermate principali.

### 5.1 Home

**Contenuto, dall'alto:**
1. **Copertina** con l'illustrazione della fermata del tram: data di oggi in maiuscolo, titolo "La notte è lunga. *Scegli una luce.*", pulsante primario **Gioca la sfida di oggi** e sotto, in piccolo, "Oggi: *Non voltarti* · 10 minuti · gratis".
2. **Continua** (solo se c'è una partita o una campagna in corso): carte compatte con avanzamento e stelle.
3. **I giochi**: carte gioco a tutta larghezza. Prima i nuovi, poi quelli non ancora giocati, poi gli altri.
4. **In arrivo**: carte nebbia con il titolo e il link "Avvisami" (§5.8).
5. **Piè di pagina**: lingua, Info, Privacy, Termini, © Small Hours.

**Il gioco in evidenza** ruota ogni giorno tra i giochi pubblicati, sempre nello stesso ordine.

**Stati**

| Stato | Cosa cambia |
|---|---|
| Prima visita | Niente "Continua". Sotto la copertina, una riga: "Nuovo qui? Ogni gioco ha una sfida gratis al giorno." |
| Sfida di oggi già giocata | Il pulsante diventa **Rivedi il risultato** e la riga sotto mostra stelle e punteggio. |
| Tutto sbloccato | Nessuna etichetta di prezzo sulle carte. |
| Offline | Avviso in alto: "Sei offline. I giochi già aperti funzionano." Le carte dei giochi mai aperti hanno opacità ridotta. |

### 5.2 Scheda gioco

**Contenuto:**
- immagine verticale a tutta larghezza, con freccia indietro;
- etichette di stato, titolo, gancio di 2 righe, durata e difficoltà (lune);
- pulsante primario **Gioca gratis**, che diventa **Continua: capitolo N** se il gioco è sbloccato;
- pulsante secondario **Sblocca la campagna · 1,99 €**, nascosto se il gioco è già sbloccato;
- "Come si gioca" e "Cosa c'è nella campagna", 3 righe ciascuno;
- "Le tue notti", con il miglior risultato e le stelle per capitolo.

L'accento della pagina è quello del gioco (`data-game`).

**Stati:** mai giocato / sfida di oggi già giocata / sbloccato / gioco "in arrivo" (niente pulsanti, solo "Avvisami").

### 5.3 Gioco

Il gioco occupa tutto lo schermo, senza barra in basso né logo. Il sito aggiunge solo:
- un **tasto ✕** in alto a sinistra, semitrasparente, sempre raggiungibile;
- il **foglio di conferma uscita** se la partita è in corso: "Uscire? La partita è salvata, la ritrovi in Continua." con **Esci** (secondario) e **Resta** (primario);
- il **foglio di sblocco** quando il gioco lo chiede (§5.5).

**Caricamento:** fondo nero con il simbolo che pulsa piano e il titolo del gioco. Se dopo 8 secondi il gioco non risponde: "Il gioco non si è avviato." con **Riprova**.

### 5.4 Sfida del giorno

Una lista con una riga per gioco: icona, titolo, "Sfida n° 128", durata, e lo stato di oggi (**Gioca** oppure stelle e punteggio).

In cima, un conto alla rovescia: "Nuove sfide tra 4 h 12 min". Le sfide cambiano a mezzanotte, ora di Roma.

Sotto c'è la **serie**: le notti di fila in cui hai giocato almeno una sfida, con 7 pallini per la settimana.

**Condividi il risultato:** dopo la sfida, un testo pronto da copiare, senza immagini.
```
Small Hours · Non voltarti #128
★★☆  2/3 a casa · 14 turni
smallhours.games/d/128
```

### 5.5 Sblocco (foglio, non pagina)

Si apre in tre casi: dal pulsante **Sblocca** nella scheda gioco, a fine partita gratuita (una volta per sessione), e quando nel gioco tocchi un capitolo bloccato.

**Contenuto:**
- etichetta "Ti è piaciuto?" e titolo legato al gioco ("Il bosco ha dieci notti");
- 3 punti su cosa ottieni;
- prezzo: "1,99 € una volta, per sempre";
- **Sblocca** (primario);
- **Tutta la collezione · 4,99 €** (secondario), solo quando i giochi pubblicati sono almeno 3;
- **Ho già un codice** e **Non ora**.

**Flusso:**
1. **Sblocca** apre la pagina di pagamento del fornitore: nella stessa scheda su mobile, in una nuova su desktop.
2. Pagamento riuscito: il fornitore rimanda a `/it/grazie/?code=SH-XXXX-XXXX`.
3. Il sito verifica il codice (§8), lo salva e mostra "Campagna sbloccata. Buona notte." con **Torna al gioco**.
4. Il codice arriva anche per email, per ripristinare l'acquisto altrove.

**Errori:**

| Errore | Messaggio |
|---|---|
| Codice sbagliato | "Codice non valido. Controlla le lettere e riprova." |
| Codice già attivo su 5 dispositivi | "Questo codice è già attivo su 5 dispositivi. Scrivici e lo sistemiamo." |
| Offline | "Sei offline. Lo sblocco serve la connessione, il gioco no." |
| Pagamento annullato | Il foglio si riapre, senza messaggi di colpa. |

### 5.6 Progressi

- **La tua notte:** serie di notti, stelle totali.
- **I tuoi giochi:** per ognuno, capitoli completati, stelle e miglior punteggio della sfida.
- **Sblocchi:** l'elenco dei giochi sbloccati, ognuno con il codice mascherato (SH-••••-7KQ2).
- **Ripristina acquisti:** campo codice e pulsante **Ripristina**.
- **Dati:** "I tuoi progressi sono salvati su questo telefono.", con **Esporta** (scarica un file) e **Importa**.
- **Cancella tutto**, in rosso, con conferma.

### 5.7 Info

Chi siamo in 3 righe, contatto email, privacy, termini, crediti delle immagini.

### 5.8 Avvisami

Un foglio con un campo email: "Ti scriviamo una volta, quando esce. Poi mai più." L'email va nella lista del servizio newsletter (Buttondown o simili), con consenso esplicito.

---

## 6. Flussi

**A. Prima visita da un link condiviso**
Link `/d/128` → sfida del giorno di quel gioco → partita → risultato → foglio Sblocca (si chiude con un tocco) → Home.

**B. Ritorno serale**
Home → la carta "Continua" mostra "Ultima Corsa · capitolo 4" → tocco → il gioco riparte dal salvataggio.

**C. Acquisto**
Fine partita gratuita → foglio Sblocca → pagamento → `/grazie/` → sblocco → di nuovo nel gioco, al capitolo 2.

**D. Cambio telefono**
Progressi → Ripristina acquisti → codice dall'email → sblocco attivo. Le stelle si spostano con Esporta e Importa.

**Regola d'oro:** il foglio Sblocca non compare mai prima della prima partita finita, e mai più di una volta per sessione senza che tu lo chieda.

---

## 7. Dati salvati sul dispositivo

Tutto in `localStorage`, con una chiave per argomento e un numero di versione per le migrazioni future.

```json
// sh:v1:profile
{ "lang": "it", "device": "a91f…", "firstSeen": "2026-11-25",
  "streak": { "count": 3, "last": "2026-11-25" } }

// sh:v1:unlocks
{ "non-voltarti": { "code": "SH-8F2A-7KQ2", "since": "2026-11-25" }, "all": null }

// sh:v1:game:non-voltarti
{ "save": { },                     // salvataggio opaco, lo gestisce il gioco
  "chapters": { "1": 3, "2": 2 },  // stelle per capitolo
  "daily": { "128": { "score": 2, "stars": 2, "turns": 14 } } }
```

`device` è un identificativo casuale, generato alla prima visita, che serve solo a contare le attivazioni di un codice. Il sito non manda altri dati a nessuno.

---

## 8. Pagamenti e sblocchi

**Fornitore consigliato: Lemon Squeezy.** Fa da venditore registrato, quindi gestisce IVA europea, ricevute e rimborsi, e genera **codici di licenza** con un limite di attivazioni. È la cosa più vicina a "nessun lavoro amministrativo" per un progetto piccolo.

Alternativa: **Stripe Payment Links** più una tabella di codici. Costa meno, ma IVA e codici vanno gestiti a parte.

**Prodotti**

| Prodotto | Prezzo | Cosa sblocca |
|---|---|---|
| Un gioco | 1,99 € | La campagna di quel gioco |
| Collezione | 4,99 € | Tutti i giochi, anche quelli futuri |

**Verifica:** una funzione serverless (`/api/verify`, su Vercel) riceve il codice e l'identificativo `device`, chiede al fornitore se il codice è valido e risponde con il gioco o la collezione sbloccata. Il sito salva lo sblocco; i giochi non vedono mai il codice.

**Limite onesto:** chi sa modificare il `localStorage` può sbloccare senza pagare. A questa scala va bene: impedirlo richiederebbe account e server, con un costo più alto di quello che si perde.

---

## 9. Contratto tra sito e giochi

### 9.1 Struttura

```
games/<slug>/
  index.html       il gioco, autonomo, giocabile anche aperto da solo
  manifest.json    i dati per il sito
  cover.webp       copertina 4:5
  key.webp         immagine verticale della scheda
  icon.webp        icona quadrata
```

### 9.2 Manifest

```json
{
  "slug": "non-voltarti",
  "title": { "it": "Non voltarti", "en": "Don't Look Back" },
  "hook":  { "it": "Riporta tutti a casa prima che il bosco se li prenda.",
             "en": "Get everyone home before the woods take them." },
  "howto":    { "it": ["…", "…", "…"], "en": ["…", "…", "…"] },
  "campaign": { "it": ["…", "…", "…"], "en": ["…", "…", "…"] },
  "minutes": [8, 15],
  "difficulty": 4,
  "accent": "#ff8a5c",
  "chapters": 10,
  "free": "daily",
  "price": { "eur": 1.99 },
  "status": "live",
  "released": "2026-12-01"
}
```

`status` vale `live`, `soon` oppure `hidden`.

### 9.3 Messaggi

Il sito carica il gioco in un `iframe` a tutto schermo; i due si scambiano messaggi con `postMessage`.

| Messaggio | Direzione | Contenuto | Quando |
|---|---|---|---|
| `sh:ready` | gioco → sito | `{ version }` | il gioco è caricato |
| `sh:init` | sito → gioco | `{ lang, mode: "daily" \| "campaign", daily: { n, seed }, unlocked, save, chapters }` | in risposta a `sh:ready` |
| `sh:save` | gioco → sito | `{ save, chapters }` | a ogni fine turno o capitolo |
| `sh:result` | gioco → sito | `{ mode, score, stars, summary: { it, en } }` | fine partita |
| `sh:paywall` | gioco → sito | `{ reason: "chapter" \| "end" }` | serve lo sblocco |
| `sh:unlocked` | sito → gioco | `{ unlocked: true }` | dopo l'acquisto |
| `sh:exit` | gioco → sito | `{}` | il giocatore esce dal gioco |

**Seme della sfida:** `seed = hash(slug + numero della sfida)`, dove il numero conta i giorni dal lancio. Tutti giocano la stessa notte.

**Se il gioco è aperto da solo,** senza sito, non riceve `sh:init` entro un secondo e funziona come i prototipi di oggi: salvataggio locale e tutto sbloccato. Così si può provare durante lo sviluppo.

---

## 10. Testi principali

| Chiave | IT | EN |
|---|---|---|
| `home.title` | La notte è lunga. *Scegli una luce.* | The night is long. *Pick a light.* |
| `home.cta` | Gioca la sfida di oggi | Play today's challenge |
| `home.today` | Oggi: {game} · {min} minuti · gratis | Today: {game} · {min} minutes · free |
| `home.continue` | Continua | Continue |
| `home.games` | I giochi | The games |
| `home.soon` | In arrivo | Coming soon |
| `game.play` | Gioca gratis | Play free |
| `game.continue` | Continua: capitolo {n} | Continue: chapter {n} |
| `game.unlock` | Sblocca la campagna · {price} | Unlock the campaign · {price} |
| `unlock.eyebrow` | Ti è piaciuto? | Enjoyed it? |
| `unlock.price` | una volta, per sempre | once, forever |
| `unlock.code` | Ho già un codice | I have a code |
| `unlock.later` | Non ora | Not now |
| `unlock.done` | Campagna sbloccata. Buona notte. | Campaign unlocked. Good night. |
| `daily.next` | Nuove sfide tra {h} h {m} min | New challenges in {h} h {m} min |
| `daily.streak` | {n} notti di fila | {n} nights in a row |
| `play.exit` | Uscire? La partita è salvata, la ritrovi in Continua. | Leave? Your game is saved in Continue. |
| `offline` | Sei offline. I giochi già aperti funzionano. | You're offline. Games you've opened still work. |

L'elenco completo vive in `i18n/it.json` e `i18n/en.json`.

---

## 11. Lingue

- Alla prima visita, `/` legge `navigator.languages`: se trova l'italiano manda a `/it/`, altrimenti a `/en/`.
- La scelta fatta dal selettore viene ricordata (`sh:v1:profile.lang`) e vince sulla lingua del browser.
- Ogni pagina dichiara la sua versione nell'altra lingua (`<link rel="alternate" hreflang>`).
- I giochi ricevono la lingua da `sh:init` e contengono i propri testi in entrambe le lingue.
- Date e prezzi passano da `Intl`: "25 novembre" / "25 November", "1,99 €" / "€1.99".

---

## 12. Tecnologia

| Scelta | Motivo |
|---|---|
| **Sito statico generato con Astro** | Pagine HTML veloci, nessun framework imposto ai giochi, supporto nativo per più lingue. In alternativa basta HTML scritto a mano con un piccolo script di build. |
| **Vercel** per l'hosting | Ospita il sito statico e la funzione `/api/verify`. GitHub Pages basta fino all'arrivo dei pagamenti. |
| **Lemon Squeezy** | Pagamenti, IVA, codici di licenza. |
| **Service worker** (fase 6) | Sito e giochi già aperti funzionano offline. |
| **Plausible** (fase 6) | Statistiche senza cookie, quindi niente banner per il consenso. |

### Struttura della repository

```
/design-system/       token, componenti, vetrina
/docs/                progettazione e regole
/assets/brand/        simbolo, icone, illustrazioni del marchio
/games/<slug>/        un gioco = una cartella (§9)
/src/                 pagine, layout, componenti del sito
/i18n/                it.json, en.json
/api/verify.js        verifica dei codici
```

---

## 13. Qualità

**Prestazioni**
- Home sotto i 300 KB al primo caricamento, immagini comprese.
- Largest Contentful Paint sotto i 2,5 s su 4G lento.
- Ogni gioco sotto 1 MB, con le immagini in WebP.

**Accessibilità**
- Contrasto AA su tutto il testo.
- Aree di tocco di almeno 48 px; azioni principali nella metà bassa dello schermo.
- Sito interamente navigabile da tastiera, con il focus sempre visibile.
- `prefers-reduced-motion` spegne animazioni e transizioni.
- Mai il colore come unica informazione: lune, stelle ed etichette hanno forma e testo.

**SEO e condivisione**
- Titolo e descrizione per ogni pagina e lingua.
- Anteprima social: `og-1200x630.jpg` per il sito, la copertina per ogni gioco.
- I link delle sfide (`/d/128`) mostrano nell'anteprima il gioco del giorno.

**Privacy**
- Nessun cookie di tracciamento; lo stato resta sul dispositivo.
- Email solo per "Avvisami", con consenso esplicito.

---

## 14. Fasi e criteri di completamento

| Fase | Contenuto | È finita quando… |
|---|---|---|
| **1. Fondamenta** ✓ | Design system, progettazione, marchio | La vetrina mostra token, componenti e schermate chiave |
| **2. Sito statico** | Home, schede gioco, Info, IT/EN | Si naviga su un telefono vero e i due giochi si aprono a tutto schermo |
| **3. Giochi nel contratto** | Ultima Corsa e Non voltarti parlano `sh:*`; salvataggi gestiti dal sito | Si esce e si rientra in un gioco ritrovando la partita |
| **4. Sfida del giorno** | Seme condiviso, pagina Sfida, serie, testo da condividere | Due telefoni giocano la stessa notte |
| **5. Pagamenti** | Lemon Squeezy, `/api/verify`, ripristino acquisti | Un acquisto di prova sblocca il gioco su due dispositivi |
| **6. Rifinitura** | Offline, statistiche, Avvisami, terzo gioco | Lighthouse ≥ 90 su mobile in tutte le categorie |

---

## 15. Decisioni aperte

1. **Dominio:** verificare `smallhours.games` e le alternative.
2. **Prezzo:** 1,99 € per gioco e 4,99 € per la collezione, da validare con i primi utenti.
3. **Titolo inglese di *Ultima Corsa*:** proposta *Last Tram*.
4. **Suoni:** per ora nessuno, coerente con l'uso a letto e in tram. Da rivalutare gioco per gioco.
