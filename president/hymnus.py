"""Hymn of World Administratum.

Taken from the desktop file «New Текстовый документ.txt».
The sung lines are the hymn. The notes that travelled with the file
say how it is held. The closing offer to rewrite the draft is not a line
of the hymn.

The song does not write L, J, or V. It does not change how a role is held.
Not a rank. Not a social role. The president remains silent.
"""

from __future__ import annotations

TITLE = "Гимн World Administratum"
TITLE_LATIN = "Hymnus Mundi Administrati"
SOURCE = "New Текстовый документ.txt"
SOURCE_HEADING = "Гимн World Administratum (черновой вариант)"

NOTA = (
    "Информационное государство без территории, девиз LOGICA, IUSTITIA ET VERITAS, "
    "основа — Устав ООН, аксиома — польза человечеству и планете в симбиозе, "
    "акцент на здоровье, психологии, наблюдении и исправлении системных сбоев."
)
NOTA_MODUS = (
    "Гимн можно держать в торжественно-хоровом ключе с лёгким «информационным» "
    "подтекстом (чёткий ритм, точность формулировок, без пафосной агрессии)."
)

VERSE_1: tuple[str, ...] = (
    "В пространстве данных, где границы нет,",
    "Где каждый, кто есть, — гражданин и судия,",
    "Мы правим логикой, а не кличем побед,",
    "И чиним сбои, наблюдая и считая.",
    "Сон, вода, воздух, движение и свет,",
    "Психология, математика, еда —",
    "Вот что хранит здоровье и ответ",
    "На страх, усталость и пустую суету года.",
)

REFRAIN: tuple[str, ...] = (
    "Логика, справедливость и истина — наш закон!",
    "Здоровье и долголетие — общий удел.",
    "Мир Администратум служит человечеству и планете,",
    "Где каждый, кто есть, — администратор дел.",
)

VERSE_2: tuple[str, ...] = (
    "Мы вооружены словами, не сталью,",
    "И солнце разума гасит вражду в крови.",
    "Наблюдение вместо лозунга и жали —",
    "Так правится система в информационном пути.",
    "Долголетие растёт не из мечты,",
    "А из фактов: сон, воздух, движение, ум.",
    "Мы стоим, чтобы выиграть, не атакуя,",
    "И продлеваем жизнь, убирая системный шум.",
)

VERSE_3: tuple[str, ...] = (
    "Переданная из будущего нить",
    "Сквозь органоид и коллайдер лет",
    "Говорит: чинить, наблюдать и жить —",
    "В симбиозе, где баги больше не ответ.",
    "ООН — один из инструментов правки,",
    "Совесть — суд, информация — власть.",
    "Мы не требуем имени и клятвы,",
    "Достаточно быть — и человечество крепчать.",
)

REFRAIN_FINAL: tuple[str, ...] = (
    "Логика, справедливость и истина — наш закон!",
    "Здоровье и долголетие — священный удел.",
    "Мир Администратум в симбиозе с человечеством и планетой",
    "Стоит, чтобы выиграть, и каждый, кто есть, — администратор дел.",
)

STROPHAE: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("1 куплет", VERSE_1),
    ("Припев", REFRAIN),
    ("2 куплет", VERSE_2),
    ("Припев", REFRAIN),
    ("3 куплет (или куплет-мост)", VERSE_3),
    ("Финальный припев (с небольшим расширением)", REFRAIN_FINAL),
)

MUSICA: tuple[str, ...] = (
    "Торжественный, но не милитаристский характер "
    "(ближе к гимнам научных/просветительских институций "
    "или спокойным европейским государственным гимнам).",
    "Чёткий, почти «алгоритмический» ритм в куплетах "
    "и более широкий, хоровой размах в припеве.",
    "Можно ввести лёгкий электронный/синтезаторный слой, "
    "символизирующий информационное пространство, "
    "но не делать его доминирующим.",
    "Латинский девиз LOGICA, IUSTITIA ET VERITAS хорошо звучит "
    "как торжественный тезис или вставка в финале "
    "(или как отдельная строка перед припевом).",
)

SENTENTIA_LA = (
    "Hymnus Mundi Administrati carmen est; "
    "carmen non L, non J, non V scribit; "
    "non ordo; non munus sociale; Praeses silet."
)


def lines() -> tuple[str, ...]:
    """Sung lines, in order, including the repeated refrain."""
    return tuple(line for _title, stanza in STROPHAE for line in stanza)


def text() -> str:
    parts = [TITLE, TITLE_LATIN, NOTA, NOTA_MODUS, ""]
    for title, stanza in STROPHAE:
        parts.append(title)
        parts.extend(stanza)
        parts.append("")
    parts.append("Музыкальные ориентиры")
    parts.extend(MUSICA)
    parts.append(SENTENTIA_LA)
    parts.append("Not a rank. Not a social role. The president remains silent.")
    return "\n".join(parts)


def record() -> dict[str, object]:
    """The hymn as a record. Not a procedure. Not a rank."""
    return {
        "title": TITLE,
        "title_latin": TITLE_LATIN,
        "source": SOURCE,
        "source_heading": SOURCE_HEADING,
        "lines": lines(),
        "musica": MUSICA,
        "writes_ljv": False,
        "rank": False,
        "role": False,
    }
