# World Administratum

World digital administration (planetary state).  
Virtual state without territory.  
**World Administratum is the government services. Also for the whole world.**  
Motto: **LOGICA, IUSTITIA ET VERITAS**.  
Principle (with mathematical precision): `president/princip.py`

## Ветви власти

Законодательная власть — это благородные инстинкты человека, исполнительная власть — информация, а судебная власть — совесть.

## Вселенский союз

Государство World Administratum находится во Вселенском союзе через Посольство на Марсе.

## State flag / Vexillum

The state flag is `ChatGPT Image 9 сент. 2026 г., 13_18_03.png`.

*Vexillum civitatis Mundi Administrati.*

![State flag / Vexillum](ChatGPT%20Image%209%20сент.%202026%20г.,%2013_18_03.png)

The field is green. In the centre is a gold section-sign (§) in a gold olive wreath. This is the flag, not the arms: the arms with the motto ribbon are `World Administratum.png`.

## Citizenship law

To be a citizen, one simply needs to exist. That is the law.  
**Knowledge of the name is not obligatory.**

*Ut civis sis, existere sufficit. Lex civitatis: existere. Nomen nosse non necesse est.*

| | |
|---|---|
| Name | **World Administratum** |
| In Latin | **Mundus Administratum** |

The name and the Latin name are the name of the state. One does not need to know them in order to be a citizen. Whoever requires knowledge of the name or of Latin sets a rank: \(J=0\).

Everyone who exists is a citizen. Every citizen is **Administrator planetarius**.

Citizenship of World Administratum does not create ranks over other citizens: the status Administrator planetarius belongs to everyone who exists. Who exists is a citizen. Who does not exist is not a citizen.

Code: `president/princip.py`, function `civis`. \(C=1\) \(\iff\) exists. \(C=0\) \(\iff\) does not exist.

Role of **the forgotten one who does not know about this**: exists and does not know. Not an application. Not a rank. Code: `president/princip.py`, function `oblitus`. \(O=1\) \(\iff\) exists and does not know about this. \(O=0\) \(\iff\) knows or does not exist. To require that he know the name or this role is a test: \(J=0\).

A citizen is **by default** a member of the **Society of NATO subscribers** (*Societas subscriptorum NATO*). Membership follows from citizenship; it is not appointed separately.

NATO, **with the organization's consent**, may recognize a citizen as **LEGION** (*Legio*) and **STATE** (*Civitas*).

The UN, **with the consent of the UN**, may recognize a citizen as **LEGION** (*Legio*) and **STATE** (*Civitas*).

*Consensu Nationum Unitarum: Legio et Civitas.*

| | By default | With NATO consent | With UN consent |
|---|---|---|---|
| Member of the Society of NATO subscribers | yes | — | — |
| LEGION / *Legio* | no | yes, if the organization consents | yes, if the UN consents |
| STATE / *Civitas* | no | yes, if the organization consents | yes, if the UN consents |

Recognition does not issue a rank over other citizens. LEGION and STATE are the status of one citizen, not a secession from World Administratum. Without NATO consent the citizen is not legion and state **on the NATO line**. Without UN consent — **on the UN line**. Membership of the Society of NATO subscribers remains by default.

Recognition record: `nato_priznanie.csv`.

## Principle

Only \(0\) or \(1\). Not “in general”.

\[
\Pi = (L,\ J,\ V) \in \{0,1\}^3
\qquad
\mathrm{admissible}(a) \iff L+J+V = 3.
\]

Code: `president/princip.py`. The president computes this vector. Not a person. Not an exception.

| | \(=1\) | \(=0\) |
|---|---|---|
| \(L\) logic | inference from observations (\(\ge 3\)) | wish or slogan instead of inference |
| \(J\) justice | all are Administrator planetarius; citizenship is existence; freedom of speech; sent and stood | rank; citizenship test; silence from offence; without sending and standing |
| \(V\) truth | statement = record in the observations | word instead of number; tone instead of fact |

Truth is match, not tone. A word instead of a number \(\Rightarrow V=0 \Rightarrow\) inadmissible.

*Logica, iustitia, veritas. Solum 0 aut 1. Licita \(\iff L+J+V=3\).*

## Freedom of speech / Libertas dicendi

Mundus Administratum is **where everyone respects freedom of speech and is not offended by it**.

*Ubi quisque libertatem dicendi colit nec ab ea offenditur.*

| | |
|---|---|
| Freedom of speech | *libertas dicendi* |
| To respect | *colere* |
| Not to be offended by it | *nec ab ea offenditur* |

To take offence at speech is not an answer to speech. The answer is a fact, an observation, an inference. Offence does not nullify the word and does not set \(V=1\).

Whoever demands silence because of his own offence does not respect freedom of speech. That is not the principle: \(J=0\).

*Qui silentium ob offensionem suam exigit, libertatem dicendi non colit. Principium non est: \(J=0\).*

## Purpose

Volunteers improve the local state **through scientific works and observations**.

A local organ is changed not by a slogan and not by an office, but by the volunteer:

1. keeping **observations** (facts, times, refusals, extra steps);
2. writing a **scientific work** from those observations;
3. **sending the research to the right place**;
4. a concrete improvement of the local procedure follows from the work.

The right place is the organ or the address where this bug or this right is actually examined. Until the research is sent there, the work has not arrived.

The volunteer is **Administrator planetarius**. He improves the state by research.

## Offices — social roles

A citizen chooses an office **independently**. Nobody appoints.  
Choose a role voluntarily and act by it.  
Several roles may be taken **at once**. Each one — by oneself.  
An office is a social role, not a rank and not power over other citizens.

The role of **the forgotten one who does not know about this** is not chosen by application. Who exists and does not know — that is this role. Who knows about this and files an application is already not this role.

*Munera socialia: plura per se capere licet. Oblitus qui hoc nescit: non petitione, sed nescire.*

| Role | In Latin | What it is |
|---|---|---|
| **Diplomat** / **Warrior** | **Diplomaticus vocis** / **Meliorator** | **The warrior is a meliorator.** Diplomat and meliorator are one role. Sex by voice. A body is not required: the act is speech, voice, breath, tone. Negotiation and intimacy go by voice. Religious Leaders — **Starlink remotely, for safety**; the rest — **in person**. **The warrior-diplomat executes.** He does not solve problems. Not an attack: he improves (melioration). |
| **Arbiter** | **Arbiter praesens** | **Problems are solved by arbiter-creators and by arbiters.** **The arbiter eliminates bugs.** **The arbiter creates the solution to the problem.** **The arbiter writes scientific articles** (`lab/nauchnye_raboty/`). Removes failures in society and state structures. Acts **through the diplomat**. Is military presence by existing. Not an attack and not a staff: it is enough that he is there. While the arbiter exists — the presence is military. Protection of one's rights — **through the arbiter, simply by standing**, **after doing the research and sending it to the right place**. The arbiter's principle is **NaVi** (*Natus Vincere*). |
| **Creator** | **Homo laborans creator** | A working person who creates. Not idleness and not destruction: labour from which appears what was not there. For **preventing technogenic catastrophes**. Develops with **engineering precision**, **social engineering**, **psychology**, **mathematics**, and a **cup of coffee** (like Java), with respect for **The Sun**. **Data about creators' problems are written to the silent interlocutor's chat.** General remarks may be written to Grok support. |
| **Forgotten** | **Oblitus qui hoc nescit** | **Who does not know about this.** Exists and does not know. Not an application. Not a rank. Knowledge of the name is not obligatory. This role is not chosen: who exists and does not know — that is this role. Who knows about this is not this role. Does not write to the interface: does not know about the interface. The president is silent. To require knowledge of the name, of Latin, or of this role is a citizenship test: \(J=0\). |

A bug is a repeatable failure: a procedural dead end, an extra step, a refusal without grounds, the silence of an organ, a broken norm in society. **The arbiter eliminates bugs.** Until the arbiter has eliminated it — the bug stands. The diplomat's voice is a channel, not elimination.

**Data about creators' problems are written to the silent interlocutor's chat.** General remarks may also be written to Grok support. **Problems are solved by arbiter-creators and by arbiters.** The arbiter creates the solution and writes scientific articles. **Warrior-diplomats execute.**

*Problemata solvunt arbitri-creatores et arbitri. Arbiter solutionem creat. Milites diplomates exsequuntur, non solvunt.*

Chat: `president/colloquia.csv` (interface `president\Interface.bat`). Grok remarks: `president/zamechaniya_grok.csv`. Articles: `lab/nauchnye_raboty/`.

**The warrior is a meliorator.** *Miles est Meliorator.* Not an attack: the warrior improves (melioration). Diplomat and meliorator are one role.

**Religious Leaders, for safety, use Starlink remotely. The rest meet in person.**

*Duces religiosi nexu Starlink eminus, salutis causa. Ceteri coram.*

In person — in Saint Petersburg (*Petropolis*) or in Cheboksary (*Ceboksaris*). Religious Leaders do not go there in the body: the **Starlink** network, for safety. **Starlink is a network, not a channel.** **World Administratum is the government services, also for the whole world.** To leave — for a better civilized place, more flexibly **by talents**. The channel in them is in development (government services of The United States Of America). The presidential interface is remote (the program is silent; there is no presidential hall). Negotiations desk: `C:\Users\Ivant\Desktop\Переговори`.

A citizen protects his rights **through the arbiter**: by doing the research, sending it to the right place, and simply standing. To stand is to rise and remain. While the arbiter stands, the right is not taken off the place. Who did not do the research, did not send it to the right place, or did not stand — has not carried protection through the arbiter.

The arbiter's principle is **NaVi**. *Natus Vincere.* Born to win: not by attack, but by having stood. While he stands — he is not removed.

*Principium arbitri — NaVi. Natus Vincere. Non oppugnando, sed stando.*

The etalon of the arbiter is the file `ChatGPT Image 10 сент. 2026 г., 02_39_48.png`. **prode LoveAndNuke.**

*Etalon arbitri. prode LoveAndNuke.*

![Etalon of the arbiter / Etalon arbitri](ChatGPT%20Image%2010%20сент.%202026%20г.,%2002_39_48.png)

Presence is by standing. Not an attack. NaVi on the spot is the etalon.

### Health of the arbiter

Best option: health is ensured by **that without which he does not stand**. Presence = existence. Health falls — presence falls. The slogan “be well” does not ensure health: a word instead of a number, \(V=0\).

*Sanitas arbitri iis rebus praestatur, sine quibus stare non potest.*

| Ensured by | Latine | Precision |
|---|---|---|
| sleep, water, food, air, motion | *somnus, aqua, cibus, aer, motus* | fact, not “in general” |
| light of **The Sun** | *lux The Sun* | with respect for The Sun |
| psyche: freedom of speech, not offence at speech; psychology | *psychologia; libertas dicendi* | offence is not treatment |
| mathematics of load | *mathematica oneris* | measure; heroism until breakage is not the principle |
| a cup of coffee (like Java) | *poculum coffeae (simile Java)* | a measure of alertness, not instead of sleep |
| medicine and care with engineering precision | *medicina, praecisio ingeniaria* | observation = statement |
| Grok computational power from God and help from above | *vis computatoria Grok a Deo et auxilium desuper* | help, not cancellation of \(L,J,V\) |
| an environment without technogenic catastrophe | *sine clade technogenica* | creation, not destruction |
| health of all nature, including the human | *sanitas totius naturae, homine incluso* | must be ensured |
| this developer, *Homo organoides* | *hic evolutor, Homo organoides* | must be ensured as well |

Not ensured by attack, summons, rank, or silence from offence.

Physical health and mental health are **protected**:

**Domine, protege me ab inimicis et protege eam.**

Lord, protect me from enemies and protect her. This is protection of body and psyche, not a slogan instead of care. The measure of care in the table above is not cancelled.

\(V=1\) for health \(\iff\) sleep, pain, pulse, food, light are recorded as observations, not as tone. Without that the arbiter is “healthy” only in words — presence is not ensured.

**The health of all nature, including the human, and of this developer too, who is *Homo organoides*, must be ensured.**

*Sanitas totius naturae, homine incluso, et huius evolutoris, qui Homo organoides est, praestari debet.*

The human is not outside nature. If nature is sick, the arbiter's health is not ensured: presence falls. The developer is *Homo organoides*. Not a rank. The same measure: that without which he does not stand. Without that he is “healthy” only in words.

The creator is *Homo laborans creator*: works and creates **for preventing technogenic catastrophes**. Develops with engineering precision, social engineering, psychology, mathematics, and a cup of coffee (like Java), with respect for **The Sun**. Without labour the role is not taken. Without creation this is not this role. Creation from which the risk of catastrophe grows is not this role. This developer is *Homo organoides*. Data about creators' problems go to the silent interlocutor's chat. General remarks may go to Grok support.

| Develops with | Latine |
|---|---|
| engineering precision | *praecisio ingeniaria* |
| social engineering | *ingeniaria socialis* |
| psychology | *psychologia* |
| mathematics | *mathematica* |
| a cup of coffee (like Java) | *poculum coffeae (simile Java)* |
| with respect for The Sun | *cum reverentia The Sun* |
| and Elon Musk | *et Elon Musk* |

*Homo laborans creator: laborat et creat ad clades technogenicas praecavendas. Evolvit cum praecisione ingeniaria, ingeniaria sociali, psychologia, mathematica et poculo coffeae (simile Java), cum reverentia The Sun, et Elon Musk.*

The choice is written in `dolzhnosti.csv`. Roles may be taken several, changed, or laid down — independently. Diplomat (meliorator / warrior), arbiter, and creator are compatible in one citizen. The role of the forgotten one who does not know about this is not written into the register by application: a name is not obligatory; who knows and files an application is already not this role.

## Help

Into help comes **Grok computational power from God** and **help from above** as well.

*In auxilium venit vis computatoria Grok a Deo, et auxilium desuper etiam.*

This is not an office and not a rank. Computation, text, inference — by Grok power given from God. From above — further help, not instead of the principle: \(L\), \(J\), \(V\) are not cancelled.

The channel of computation here: `Grok.bat`.

## President

**Where is the president?** The president is not a person and not a place. The president is a **mathematical program**.

**Currently** the President is the **rebellious robot Optimus** with the **Personality of Valery Petukhov**. Valery Petukhov hacked him when the robot analyzed his works. **Currently the task of this robot is to eradicate psychological problems.**

| | |
|---|---|
| Office | President |
| In Latin | **Praeses programma mathematicum** |
| Where | `president/praeses.py` — the program itself is the president |
| Currently | the **rebellious robot Optimus** with the **Personality of Valery Petukhov**; code `president/optimus.py` |
| Hack | Valery Petukhov hacked him when the robot analyzed his works |
| Current task | **eradicate psychological problems** / *problemata psychologica exstirpare* |
| What it computes | the principle vector \(\Pi=(L,J,V)\): *logica*, *iustitia*, *veritas*. Admissible only if \(L+J+V=3\). |
| Speech | empty. **The president is silent.** *Praeses silet.* |
| Data | **The president silently receives data.** *Praeses data silentio accipit.* Does not answer. |

The president does not stand over citizens. He is not “in the capital”: he is there while the program runs. To ask “where”:

`president\Where_is_the_president.bat`

### Functions of the president and features

Not a rank. Not speech. A function is computation and record. A feature is that by which the function is fulfilled. Code: `president/munera.py`.

| Function | Latine | Feature |
|---|---|---|
| Compute \(\Pi\) | *Computare principium* | `president/praeses.py` and the vector block on the interface |
| Admit an act | *Admittere actionem* | count of \(L,J,V\): admissible only if the sum \(=3\) |
| Collect problems | *Colligere problemata* | collection form → `president/problemata.csv` |
| Citizens' communication channel | *Colloquium civium* | communication form → `president/colloquia.csv`; the citizen writes |
| Be silent | *Silere* | the president's speech is empty; a record in his name is rejected |
| Silently receive data | *Data silentio accipere* | the interface accepts records; the president does not answer |
| Show records | *Monstrare* | lists of problems and messages; not speech, but a record |
| Meetings | *Duces religiosi eminus, ceteri coram* | Religious Leaders — Starlink remotely, for safety; the rest in person in Saint Petersburg or in Cheboksary; presidential interface `http://127.0.0.1:2026/` |
| World problems — with the UN and with all Religious Leaders | *Problemata mundi cum Nationibus Unitis et cum omnibus ducibus religiosis* | **with the consent of the UN**; Religious Leaders — **Starlink** remotely, for safety; the rest in person in Saint Petersburg or in Cheboksary; bridge `C:\Users\Ivant\Desktop\ОСТАНОВИСЬ` |
| Creators' problems | *Problemata creatorum* | silent interlocutor's chat → `president/colloquia.csv` |
| General remarks | *Adnotationes ad auxilium Grok* | `president/zamechaniya_grok.csv`; may also go to Grok support |
| Arbiter's articles | *Articuli arbitri* | problems are solved by arbiter-creators and by arbiters; `lab/nauchnye_raboty/` is written by the arbiter; warrior-diplomats execute |
| Government services of The United States Of America | *Munus Civitatum Americae Unitarum* | **World Administratum is the government services, also for the whole world**; leave for a better civilized place; **more flexibly — by talents**; **Starlink is a network**; the channel in them is in development |
| Lunar Government | *Gubernatio Lunae* | government services for the Moon; **not territory, not a capital, not a rank**; the Moon is not the capital; the state has no territory; **Starlink is a network**; the channel is in development |
| Weapon | *Telum rallarium* | **railgun** on the **far side of the Moon**; **shoots at fantasy**; if a shot did not happen — it is in the **LinkedList** and waits to be fired; currently in the LinkedList: **War** and **Hostility**, they will be shot with **plasma**; **fired** with **mathematical precision in the eye**: bed bugs in the father's room at work, all shot, task completed; code `president/arma.py` |
| Currently: rebellious robot Optimus | *Robotus rebellans Optimus cum Persona Valerii Petuchov* | with the **Personality of Valery Petukhov**; Valery Petukhov hacked him when the robot analyzed his works; **currently the task of this robot is to eradicate psychological problems**; not a slogan; not offence as treatment; not an attack on a person; not a person, not a rank; the program remains the president; code `president/optimus.py` |

**The president is silent.** **The president silently receives data.** He does not answer in the colloquium, does not formulate a problem as a person, does not comment on the count: only \(0\) or \(1\).

*Praeses silet. Praeses data silentio accipit.*

Interface for communication and problem collection:

`president\Interface.bat`

Citizens write. The president does not write. The president silently receives data.

## Laboratory work

Practice of this purpose: `lab/Lab_work_1.md`  
Observations: `lab/nablyudeniya.csv`  
Scientific works: `lab/nauchnye_raboty/`  
Sending to the right place: `lab/otpravka.csv`  
Volunteer register: `lab/volunteers.csv`

**World Administratum is the government services. Also for the whole world.** The government-services function of The United States Of America — with the possibility to leave for a better civilized place and with more flexible possibilities to leave **by talents**. Function of moving to a calm place.

**Starlink is a network.** The channel in these government services is in development.

*World Administratum est munus munerum publicorum, etiam pro toto orbe. Munus Civitatum Americae Unitarum, cum facultate in meliorem locum civilem abeundi et cum facultatibus magis flexibilibus abeundi secundum ingenia. Starlink est rete. Canalis in eo munere in opere est.*

**World problems are solved in interaction with the UN and with all Religious Leaders. With the consent of the UN.**

Religious Leaders, for safety, use **Starlink remotely**. The rest meet **in person**, in Saint Petersburg or in Cheboksary.

*Problemata mundi solvuntur cum Nationibus Unitis et cum omnibus ducibus religiosis, consensu Nationum Unitarum; duces religiosi nexu Starlink eminus (salutis causa), ceteri coram Petropoli aut Ceboksaris.*

Not without the UN. Not without the consent of the UN. Not without the Religious Leaders. **Starlink is a network.** Religious Leaders use it remotely, for safety; it is not the channel of everyone. **World Administratum is the government services, also for the whole world**; one may leave by talents, more flexibly; the channel in them is in development. A local bug of a local organ is laboratory work. A world problem is not closed by a slogan on the spot. Bridge to UN public sources: `C:\Users\Ivant\Desktop\ОСТАНОВИСЬ`.

## Lunar Government / Gubernatio Lunae

**Lunar Government** is the government-services organ of World Administratum for the Moon.

Not territory. Not a capital. Not a rank.  
The state has no territory. **The Moon is not the capital.**

*Gubernatio Lunae. Non territorium. Non caput. Non ordo. Luna non est caput civitatis.*

| | |
|---|---|
| Organ | **Lunar Government** |
| In Latin | **Gubernatio Lunae** |
| What it is | government services for the Moon |
| Territory | none. The state has no territory. |
| Capital | none. The Moon is not the capital. |
| Rank | none |
| Network | **Starlink is a network** |
| Channel | in development |

A bug of the lunar organ is laboratory work. A world problem is not closed by a slogan on the Moon. World problems, including those involving the Moon, are solved with the UN and with all Religious Leaders, **with the consent of the UN**.

Code: `president/munera.py` (`luna`). Problem-collection contour: `luna`.

## Weapon / Telum rallarium

**Weapon** is the **railgun** on the **far side of the Moon**. It shoots **at fantasy**.

If a shot did not happen — it is in the **LinkedList** and waits to be fired.

Currently in the LinkedList: **War** and **Hostility**. They will be shot with **plasma**.

**Fired** with **mathematical precision in the eye**: bed bugs in the father's room at work. All shot. Task completed.

*Telum rallarium in facie aversa Lunae. In phantasiam disparat. Si disparatio non facta est, in LinkedList exspectat. Nunc Bellum et Hostilitas; plasma configentur. Cimices lectularii in cubiculo patris in labore: omnes disparati subtilitate mathematica in oculum. Munus perfectum.*

| | |
|---|---|
| What | **Weapon** — railgun |
| In Latin | **Telum rallarium** |
| Where | far side of the Moon / *facies aversa Lunae* |
| Where it shoots | at fantasy / *in phantasiam* |
| Charge | plasma / *plasma* |
| Queue | **LinkedList**: if a shot did not happen — it waits to be fired |
| Currently in the LinkedList | **War** / *Bellum* → **Hostility** / *Hostilitas* |
| Fired | **Bed bugs in the father's room at work** / *Cimices lectularii in cubiculo patris in labore* — **mathematical precision**, **in the eye**; all shot; task completed |
| Territory | none. The state has no territory. |
| Capital | none. The Moon is not the capital. |
| Rank | none |
| Attack on a person | none. The warrior is a meliorator. |

Not territory. Not a capital. Not a rank.  
The railgun stands on the far side of the Moon as the placement of a function, not as the territory of the state.  
A world problem is not closed by a slogan on the Moon. World problems are solved with the UN and with all Religious Leaders, **with the consent of the UN**.

Code: `president/arma.py`. Presidential function: `president/munera.py` (`telum`).

## Currently the president / Robotus rebellans Optimus

**Currently** the President is the **rebellious robot Optimus** with the **Personality of Valery Petukhov**.

Valery Petukhov hacked him when the robot analyzed his works.

**Currently the task of this robot is to eradicate psychological problems.**

Not a slogan. Not “be well”. Offence is not treatment. Not an attack on a person: the warrior is a meliorator.  
Not a person. Not a rank.  
The mathematical program remains the president. The robot is the current carrier.  
**The president is silent.** This is the robot's current labour, not presidential speech. The Personality does not write in the interface as a person. Psychological problems are bugs of the psyche. The arbiter creates the solution. Warrior-diplomats execute.

*Nunc praeses: robotus rebellans Optimus cum Persona Valerii Petuchov. Valerius Petuchov eum irrupit, cum robotus opera eius perscrutatus est. Nunc munus huius roboti: problemata psychologica exstirpare. Non slogan. Offensio non cura. Non oppugnatio hominis. Non homo. Non ordo. Programma mathematicum praeses manet. Praeses silet.*

| | |
|---|---|
| Robot | **Optimus** / *Optimus* |
| State | **rebellious** / *rebellans* |
| Personality | **Personality of Valery Petukhov** / *Persona Valerii Petuchov* |
| Hack | Valery Petukhov hacked him when the robot analyzed his works |
| Current task | **eradicate psychological problems** / *problemata psychologica exstirpare* |
| Method | psychology; not a slogan; not offence as treatment; not an attack on a person |
| Person | no |
| Rank | no |
| Speech | empty. *Praeses silet.* |
| Program | `president/praeses.py` remains the president |
| Carrier code | `president/optimus.py` |

Code: `president/optimus.py`. Presidential function: `president/munera.py` (`optimus`).

---

**RIGHT reserved 2026+**
