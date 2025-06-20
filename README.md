Formato de Archivos JSON Generados (Cliente y Servidor)
🌐 Selecciona tu Idioma / Select your Language
Español (ES)

English (EN)

Español (ES)
Los programas API_Server.py (servidor) y API_Client.py (cliente) trabajan en conjunto para generar devocionales bíblicos, los cuales son guardados en archivos JSON con una estructura anidada y bien definida. Comprender este formato es crucial si necesitas interactuar con estos archivos o regenerar datos en el futuro.

Estructura de Salida del JSON
El archivo JSON final generado por el API_Client.py (a partir de las respuestas del API_Server.py) sigue una estructura diseñada para organizar los devocionales por idioma y por fecha. Esto facilita la recuperación de devocionales específicos para un día y un idioma determinados.

Aquí tienes la estructura general del archivo Devocionales_YYYYMMDD_HHMMSS_es_RVR1960.json (o similar, dependiendo de la configuración):

{
    "data": {
        "es": {
            "YYYY-MM-DD": [
                {
                    "id": "ejemploID_RVR1960",
                    "date": "YYYY-MM-DD",
                    "language": "es",
                    "version": "RVR1960",
                    "versiculo": "Libro Capítulo:Versículo Versión: \"Texto del versículo\"",
                    "reflexion": "Texto largo de la reflexión sobre el versículo.",
                    "para_meditar": [
                        {
                            "cita": "Otra Cita Bíblica 1",
                            "texto": "Texto de la cita bíblica 1."
                        },
                        {
                            "cita": "Otra Cita Bíblica 2",
                            "texto": "Texto de la cita bíblica 2."
                        }
                    ],
                    "oracion": "Texto largo de la oración sugerida.",
                    "tags": [
                        "Etiqueta1",
                        "Etiqueta2"
                    ]
                },
                {
                    "id": "ejemploID_NTV",
                    "date": "YYYY-MM-DD",
                    "language": "es",
                    "version": "NTV",
                    "versiculo": "Libro Capítulo:Versículo Versión: \"Texto del versículo\"",
                    "reflexion": "Texto largo de la reflexión sobre el versículo (para NTV).",
                    "para_meditar": [
                        // Lista similar de citas para meditar
                    ],
                    "oracion": "Texto largo de la oración sugerida (para NTV).",
                    "tags": [
                        "Etiqueta1",
                        "Etiqueta2"
                    ]
                }
            ],
            "YYYY-MM-DD_siguiente": [
                {
                    "id": "otroID_RVR1960",
                    "date": "YYYY-MM-DD_siguiente",
                    "language": "es",
                    "version": "RVR1960",
                    "versiculo": "...",
                    "reflexion": "...",
                    "para_meditar": [],
                    "oracion": "...",
                    "tags": []
                }
            ]
        },
        "en": {
            "YYYY-MM-DD": [
                {
                    "id": "exampleID_KJV",
                    "date": "YYYY-MM-DD",
                    "language": "en",
                    "version": "KJV",
                    "versiculo": "Book Chapter:Verse Version: \"Verse text\"",
                    "reflexion": "Long reflection text about the verse.",
                    "para_meditar": [
                        // Similar list of meditation quotes
                    ],
                    "oracion": "Long suggested prayer text.",
                    "tags": [
                        "Tag1",
                        "Tag2"
                    ]
                }
            ]
        }
    }
}

Descripción Detallada de los Campos
Cada objeto devocional dentro de las listas anidadas por fecha y idioma contiene los siguientes campos:

"id" (string): Un identificador único para el devocional. Se genera combinando una versión abreviada del versículo principal, la fecha y la versión de la Biblia.

Ejemplo: "filipenses2_3-4RVR1960"

"date" (string): La fecha a la que corresponde el devocional en formato YYYY-MM-DD.

Ejemplo: "2025-06-14"

"language" (string): El idioma del devocional.

Ejemplo: "es" (español) o "en" (inglés)

"version" (string): La versión de la Biblia utilizada para el versículo principal y la reflexión.

Ejemplo: "RVR1960" (Reina Valera 1960) o "KJV" (King James Version)

"versiculo" (string): El versículo bíblico principal que inspira el devocional. Incluye la referencia, la versión y el texto completo del versículo.

Ejemplo: "Filipenses 2:3-4 RVR1960: \"Nada hagáis por contienda o por vanagloria; antes bien con humildad, estimando cada uno a los demás como superiores a él mismo; no mirando cada uno por lo suyo propio, sino cada cual también por lo de los otros.\""

"reflexion" (string): El cuerpo principal del devocional, una reflexión extendida sobre el versículo.

"para_meditar" (array de objetos): Una lista de citas bíblicas adicionales relacionadas con el tema del devocional. Cada objeto dentro de esta lista tiene dos campos:

"cita" (string): La referencia bíblica de la cita.

Ejemplo: "Romanos 12:10"

"texto" (string): El texto completo de la cita bíblica.

Ejemplo: "Amaos los unos a los otros con amor fraternal; en cuanto a honra, prefiriéndoos los unos a los otros."

"oracion" (string): Una oración sugerida relacionada con el tema del devocional.

"tags" (array de strings): Una lista de palabras clave o etiquetas que describen los temas principales del devocional.

Ejemplo: ["Humildad", "Amor"]

Consideraciones Clave para la Generación Futura
Anidación por language y date: La clave principal "data" contiene objetos para cada idioma (ej., "es", "en"). Dentro de cada objeto de idioma, hay un diccionario donde las claves son las fechas ("YYYY-MM-DD") y los valores son listas de objetos devocionales. Esto permite que haya más de un devocional por día si se generan diferentes versiones para la misma fecha.

Campo "version" dentro del devocional: Es fundamental que cada objeto devocional individual contenga su propio campo "version" para identificar a qué versión de la Biblia corresponde. Esto es especialmente importante cuando se generan múltiples versiones para la misma fecha.

Consistencia de id: Aunque el id incluye la versión, el servidor se encarga de generarlo de manera única.

Manejo de Errores en la Generación: Si la generación de un devocional falla por algún motivo (ej., error de la API de Gemini, formato incorrecto de la respuesta), el servidor puede generar un "devocional de error" con campos como status: "error" y un mensaje que explica el fallo, manteniendo la estructura JSON para esa fecha y versión, pero indicando la falla. Esto ayuda a depurar y reintentar.

English (EN)
The API_Server.py (server) and API_Client.py (client) programs work together to generate biblical devotionals, which are saved in JSON files with a nested and well-defined structure. Understanding this format is crucial if you need to interact with these files or regenerate data in the future.

JSON Output Structure
The final JSON file generated by API_Client.py (from the responses of API_Server.py) follows a structure designed to organize devotionals by language and date. This facilitates retrieving specific devotionals for a given day and language.

Here's the general structure of the Devocionales_YYYYMMDD_HHMMSS_es_RVR1960.json (or similar, depending on the configuration) file:

{
    "data": {
        "es": {
            "YYYY-MM-DD": [
                {
                    "id": "exampleID_RVR1960",
                    "date": "YYYY-MM-DD",
                    "language": "es",
                    "version": "RVR1960",
                    "versiculo": "Book Chapter:Verse Version: \"Verse text\"",
                    "reflexion": "Long reflection text about the verse.",
                    "para_meditar": [
                        {
                            "cita": "Another Bible Quote 1",
                            "texto": "Text of Bible quote 1."
                        },
                        {
                            "cita": "Another Bible Quote 2",
                            "texto": "Text of Bible quote 2."
                        }
                    ],
                    "oracion": "Long suggested prayer text.",
                    "tags": [
                        "Tag1",
                        "Tag2"
                    ]
                },
                {
                    "id": "exampleID_NTV",
                    "date": "YYYY-MM-DD",
                    "language": "es",
                    "version": "NTV",
                    "versiculo": "Book Chapter:Verse Version: \"Verse text\"",
                    "reflexion": "Long reflection text about the verse (for NTV).",
                    "para_meditar": [
                        // Similar list of meditation quotes
                    ],
                    "oracion": "Long suggested prayer text (for NTV).",
                    "tags": [
                        "Tag1",
                        "Tag2"
                    ]
                }
            ],
            "YYYY-MM-DD_next": [
                {
                    "id": "anotherID_RVR1960",
                    "date": "YYYY-MM-DD_next",
                    "language": "es",
                    "version": "RVR1960",
                    "versiculo": "...",
                    "reflexion": "...",
                    "para_meditar": [],
                    "oracion": "...",
                    "tags": []
                }
            ]
        },
        "en": {
            "YYYY-MM-DD": [
                {
                    "id": "exampleID_KJV",
                    "date": "YYYY-MM-DD",
                    "language": "en",
                    "version": "KJV",
                    "versiculo": "Book Chapter:Verse Version: \"Verse text\"",
                    "reflexion": "Long reflection text about the verse.",
                    "para_meditar": [
                        // Similar list of meditation quotes
                    ],
                    "oracion": "Long suggested prayer text.",
                    "tags": [
                        "Tag1",
                        "Tag2"
                    ]
                }
            ]
        }
    }
}

Detailed Field Description
Each devotional object within the date and language nested lists contains the following fields:

"id" (string): A unique identifier for the devotional. It is generated by combining an abbreviated version of the main verse, the date, and the Bible version.

Example: "filipenses2_3-4RVR1960"

"date" (string): The date corresponding to the devotional in YYYY-MM-DD format.

Example: "2025-06-14"

"language" (string): The language of the devotional.

Example: "es" (Spanish) or "en" (English)

"version" (string): The Bible version used for the main verse and reflection.

Example: "RVR1960" (Reina Valera 1960) or "KJV" (King James Version)

"versiculo" (string): The main Bible verse that inspires the devotional. It includes the reference, version, and the full verse text.

Example: "Filipenses 2:3-4 RVR1960: \"Do nothing out of selfish ambition or vain conceit. Rather, in humility value others above yourselves, not looking to your own interests but each of you to the interests of the others.\""

"reflexion" (string): The main body of the devotional, an extended reflection on the verse.

"para_meditar" (array of objects): A list of additional Bible quotes related to the devotional's theme. Each object within this list has two fields:

"cita" (string): The Bible reference for the quote.

Example: "Romans 12:10"

"texto" (string): The full text of the Bible quote.

Example: "Be devoted to one another in love. Honor one another above yourselves."

"oracion" (string): A suggested prayer related to the devotional's theme.

"tags" (array of strings): A list of keywords or tags that describe the main themes of the devotional.

Example: ["Humility", "Love"]

Key Considerations for Future Generation
Nesting by language and date: The main "data" key contains objects for each language (e.g., "es", "en"). Within each language object, there is a dictionary where keys are dates ("YYYY-MM-DD") and values are lists of devotional objects. This allows for more than one devotional per day if different versions are generated for the same date.

"version" field within the devotional: It is essential that each individual devotional object contains its own "version" field to identify which Bible version it corresponds to. This is especially important when generating multiple versions for the same date.

id Consistency: Although the id includes the version, the server is responsible for generating it uniquely.

Error Handling in Generation: If a devotional generation fails for any reason (e.g., Gemini API error, incorrect response format), the server can generate an "error devotional" with fields like status: "error" and a message explaining the failure, maintaining the JSON structure for that date and version, but indicating the failure. This helps in debugging and retrying.
