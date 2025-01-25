from typing import List, Literal

from openai import OpenAI
from pydantic import BaseModel

client = OpenAI()


class Item(BaseModel):
    von: str
    art: Literal["Leerfahrt", "Beladen", "Entladen"]
    anzahl_paletten: int


class ItemList(BaseModel):
    items: List[Item]


def extract_data_from_image(base64_image_url):
    """
    Extract structured transportation data from an image.

    This function processes a base64-encoded image URL to generate a structured list of
    transportation items based on predefined rules and constraints.

    Args:
        base64_image_url (str): A base64-encoded image URL containing the transportation data.

    Returns:
        list: A list of dictionaries representing structured transportation items,
              with fields: "Von", "Art", and "Anzahl Paletten".
    """
    prompt = {
        "system": (
            """Du bekommst als input ein Bild, das du auslesen sollst und basierend darauf ein die Felder im Output Format ausfüllst. Bei der Datei handelt es sich um einen Dispositinsverlauf. Jedes Item in der Liste entspricht dabei einer Teil-Fahrt.
            Das Feld "von" entspricht dem nur Stadtnamen wo die Teilfahrt startet (ohne Postleitzahl). "art" entspricht der Art und "anzahl_paletten" entspricht der Anzahl der stellplätze die bei dieser Teilfahrt transportiert werden. Erstelle mehrere Array einträge.
            Es wird immer in Lampertheim mit einer Leerfahrt gestartet.
            Es endet immer mit einer Leerfahrt nach Lampertheim.
            Achte außerdem auf vereinfachungen, also wenn zweimal am gleichen ort beladen werden soll, kann das als ein Eintrag zusammengefasst werden."""
        )
    }

    messages = [
        {"role": "system", "content": prompt["system"]},
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Hier ist das Input Bild"},
                {"type": "image_url", "image_url": {"url": base64_image_url}},
            ],
        },
    ]

    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=messages,
        response_format=ItemList,
    )

    transformed_output = _convert_output_data(completion.choices[0].message.parsed)
    return transformed_output


def _convert_output_data(parsed_data):
    """
    Transform parsed structured output into a list of dictionaries.

    Example input:
        items=[
            Item(von='Lampertheim', art='Leerfahrt', anzahl_paletten=0),
            Item(von='Dietzenbach', art='Beladen', anzahl_paletten=33),
            Item(von='Marburg', art='Entladen', anzahl_paletten=18),
            Item(von='Kaiserslautern', art='Entladen', anzahl_paletten=15),
            Item(von='Lampertheim', art='Leerfahrt', anzahl_paletten=0)
        ]

    Example output:
        [
            {"Von": "Lampertheim", "Art": "Leerfahrt", "Anzahl Paletten": 0},
            {"Von": "Dietzenbach", "Art": "Beladen", "Anzahl Paletten": 33},
            {"Von": "Marburg", "Art": "Entladen", "Anzahl Paletten": 18},
            {"Von": "Kaiserslautern", "Art": "Entladen", "Anzahl Paletten": 15},
            {"Von": "Lampertheim", "Art": "Leerfahrt", "Anzahl Paletten": 0}
        ]

    Args:
        parsed_data (ItemList): Parsed data containing a list of Item objects.

    Returns:
        list: A list of dictionaries representing structured transportation items.
    """
    return [
        {"Von": item.von, "Art": item.art, "Anzahl Paletten": item.anzahl_paletten}
        for item in parsed_data.items
    ]
