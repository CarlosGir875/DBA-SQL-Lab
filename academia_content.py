# -*- coding: utf-8 -*-
"""
========================================================================================================================
  CODEX TITAN - BASE DE CONOCIMIENTO ACADÉMICO
  Archivo: academia_content.py
  Descripción: Contiene toda la teoría, lecciones y diccionarios para la sección Academia.
========================================================================================================================
"""

class Codex:
    """
    ENCICLOPEDIA INTERNA.
    Aquí se almacenan los módulos de aprendizaje.
    """
    
    @staticmethod
    def get_lesson_content(module_id: str) -> dict:
        """Retorna el contenido de una lección específica."""
        
        # ----------------------------------------------------------------------------------
        # MÓDULOS DE INGLÉS
        # ----------------------------------------------------------------------------------
        if module_id == "TO_BE":
            return {
                "title": "Verbo To Be (Ser/Estar)",
                "desc": "La base del inglés. Aprende a decir quién eres y dónde estás.",
                "content": """
                ### 📘 Concepto Básico
                El verbo **To Be** es el camaleón del inglés. Cambia de forma según la persona.
                
                ### 📊 Tabla de Conjugación (Presente)
                | Pronombre | Verbo | Ejemplo | Traducción |
                | :--- | :--- | :--- | :--- |
                | I (Yo) | **am** | I [am](soy/estoy) happy. | Yo estoy feliz. |
                | You (Tú) | **are** | You [are](eres/estás) my friend. | Tú eres mi amigo. |
                | He/She/It | **is** | She [is](es/está) smart. | Ella es lista. |
                | We (Nosotros) | **are** | We [are](somos/estamos) ready. | Estamos listos. |
                | They (Ellos) | **are** | They [are](son/están) here. | Ellos están aquí. |
                """
            }
            
        elif module_id == "PRESENT_CONT":
            return {
                "title": "Presente Continuo",
                "desc": "Acciones que están ocurriendo AHORA MISMO.",
                "content": """
                ### 📘 Estructura
                La fórmula matemática es: 
                **Sujeto + Verbo To Be + Verbo con ING**
                
                ### 📝 Ejemplos
                * I **am** [working](trabajando) right now.
                * She **is** [eating](comiendo) pizza.
                """
            }
            
        elif module_id == "FUTURE":
            return {
                "title": "Futuro (Will vs Going To)",
                "desc": "Dos formas de ver el mañana.",
                "content": """
                ### 🔮 WILL (Espontáneo)
                * "I forgot my wallet." -> "I **will** pay."
                
                ### 📅 GOING TO (Planificado)
                * "I am **going to** fly to Paris."
                """
            }

        # ----------------------------------------------------------------------------------
        # MÓDULOS DE SQL
        # ----------------------------------------------------------------------------------
        elif module_id == "SQL_BASICS":
            return {
                "title": "SQL Fundamentos",
                "desc": "CRUD Básico.",
                "content": """
                ### 🧱 Los 4 Fantásticos
                1. **SELECT**: Leer datos.
                2. **INSERT**: Crear datos.
                3. **UPDATE**: Actualizar datos.
                4. **DELETE**: Borrar datos.
                """
            }
            
        elif module_id == "JOINS":
            return {
                "title": "Joins",
                "desc": "Uniones de tablas.",
                "content": """
                ### 🤝 Tipos de Uniones
                * **INNER JOIN**: Solo coincidencias.
                * **LEFT JOIN**: Todo lo de la izquierda.
                * **FULL JOIN**: Todo de ambos lados.
                """
            }
            
        elif module_id == "ACID":
            return {
                "title": "Transacciones ACID",
                "desc": "Seguridad de datos.",
                "content": """
                ### 🧪 A.C.I.D.
                * **A**tomicidad (Todo o nada).
                * **C**onsistencia (Reglas).
                * **I**solation (Aislamiento).
                * **D**urabilidad (Guardado permanente).
                """
            }
            
        return {"title": "Error", "desc": "Módulo no encontrado", "content": "N/A"}

    @staticmethod
    def get_irregular_verbs():
        """Lista de Verbos Irregulares Organizados."""
        return {
            "🥷 Los Ninjas (No Cambian)": [
                {"verb": "Cost", "past": "Cost", "participle": "Cost", "meaning": "Costar", "example": "It [cost](costó) $5."},
                {"verb": "Cut", "past": "Cut", "participle": "Cut", "meaning": "Cortar", "example": "I [cut](corté) it."},
                {"verb": "Hit", "past": "Hit", "participle": "Hit", "meaning": "Golpear", "example": "He [hit](golpeó) me."},
                {"verb": "Hurt", "past": "Hurt", "participle": "Hurt", "meaning": "Doler", "example": "It [hurt](dolió)."},
                {"verb": "Put", "past": "Put", "participle": "Put", "meaning": "Poner", "example": "[Put](pon) it there."},
                {"verb": "Read", "past": "Read", "participle": "Read", "meaning": "Leer", "example": "I [read](leí) it."},
                {"verb": "Shut", "past": "Shut", "participle": "Shut", "meaning": "Cerrar", "example": "[Shut](cierra) it."}
            ],
            "👯 Los Gemelos (Pasado = Part.)": [
                {"verb": "Bring", "past": "Brought", "participle": "Brought", "meaning": "Traer", "example": "She [brought](trajo) food."},
                {"verb": "Buy", "past": "Bought", "participle": "Bought", "meaning": "Comprar", "example": "I [bought](compré) it."},
                {"verb": "Catch", "past": "Caught", "participle": "Caught", "meaning": "Atrapar", "example": "He [caught](atrapó) it."},
                {"verb": "Feel", "past": "Felt", "participle": "Felt", "meaning": "Sentir", "example": "I [felt](sentí) bad."},
                {"verb": "Find", "past": "Found", "participle": "Found", "meaning": "Encontrar", "example": "I [found](encontré) it."},
                {"verb": "Get", "past": "Got", "participle": "Got", "meaning": "Obtener", "example": "I [got](obtuve) it."},
                {"verb": "Have", "past": "Had", "participle": "Had", "meaning": "Tener", "example": "I [had](tuve) time."},
                {"verb": "Hear", "past": "Heard", "participle": "Heard", "meaning": "Oír", "example": "I [heard](oí) you."},
                {"verb": "Keep", "past": "Kept", "participle": "Kept", "meaning": "Guardar", "example": "[Keep](guarda) it."},
                {"verb": "Make", "past": "Made", "participle": "Made", "meaning": "Hacer", "example": "She [made](hizo) it."},
                {"verb": "Pay", "past": "Paid", "participle": "Paid", "meaning": "Pagar", "example": "I [paid](pagué)."},
                {"verb": "Say", "past": "Said", "participle": "Said", "meaning": "Decir", "example": "He [said](dijo) no."},
                {"verb": "Sell", "past": "Sold", "participle": "Sold", "meaning": "Vender", "example": "He [sold](vendió) it."},
                {"verb": "Send", "past": "Sent", "participle": "Sent", "meaning": "Enviar", "example": "I [sent](envié) it."},
                {"verb": "Sit", "past": "Sat", "participle": "Sat", "meaning": "Sentarse", "example": "[Sit](siéntate) down."},
                {"verb": "Sleep", "past": "Slept", "participle": "Slept", "meaning": "Dormir", "example": "I [slept](dormí) well."},
                {"verb": "Tell", "past": "Told", "participle": "Told", "meaning": "Contar", "example": "She [told](contó) me."},
                {"verb": "Think", "past": "Thought", "participle": "Thought", "meaning": "Pensar", "example": "I [thought](pensé) so."},
                {"verb": "Win", "past": "Won", "participle": "Won", "meaning": "Ganar", "example": "We [won](ganamos)."}
            ],
            "👽 Los Mutantes (Todo Cambia)": [
                {"verb": "Be", "past": "Was/Were", "participle": "Been", "meaning": "Ser/Estar", "example": "I [was](fui)."},
                {"verb": "Begin", "past": "Began", "participle": "Begun", "meaning": "Empezar", "example": "It [began](empezó)."},
                {"verb": "Break", "past": "Broke", "participle": "Broken", "meaning": "Romper", "example": "It [broke](se rompió)."},
                {"verb": "Choose", "past": "Chose", "participle": "Chosen", "meaning": "Elegir", "example": "I [chose](elegí)."},
                {"verb": "Come", "past": "Came", "participle": "Come", "meaning": "Venir", "example": "He [came](vino)."},
                {"verb": "Do", "past": "Did", "participle": "Done", "meaning": "Hacer", "example": "I [did](hice) it."},
                {"verb": "Drink", "past": "Drank", "participle": "Drunk", "meaning": "Beber", "example": "He [drank](bebió)."},
                {"verb": "Drive", "past": "Drove", "participle": "Driven", "meaning": "Conducir", "example": "I [drove](manejé)."},
                {"verb": "Eat", "past": "Ate", "participle": "Eaten", "meaning": "Comer", "example": "I [ate](comí)."},
                {"verb": "Fall", "past": "Fell", "participle": "Fallen", "meaning": "Caer", "example": "He [fell](cayó)."},
                {"verb": "Fly", "past": "Flew", "participle": "Flown", "meaning": "Volar", "example": "It [flew](voló)."},
                {"verb": "Forget", "past": "Forgot", "participle": "Forgotten", "meaning": "Olvidar", "example": "I [forgot](olvidé)."},
                {"verb": "Give", "past": "Gave", "participle": "Given", "meaning": "Dar", "example": "She [gave](dio)."},
                {"verb": "Go", "past": "Went", "participle": "Gone", "meaning": "Ir", "example": "He [went](fue)."},
                {"verb": "Know", "past": "Knew", "participle": "Known", "meaning": "Saber", "example": "I [knew](sabía)."},
                {"verb": "See", "past": "Saw", "participle": "Seen", "meaning": "Ver", "example": "I [saw](vi)."},
                {"verb": "Speak", "past": "Spoke", "participle": "Spoken", "meaning": "Hablar", "example": "He [spoke](habló)."},
                {"verb": "Take", "past": "Took", "participle": "Taken", "meaning": "Tomar", "example": "He [took](tomó)."},
                {"verb": "Wear", "past": "Wore", "participle": "Worn", "meaning": "Usar", "example": "She [wore](usó)."},
                {"verb": "Write", "past": "Wrote", "participle": "Written", "meaning": "Escribir", "example": "I [wrote](escribí)."}
            ]
        }

    @staticmethod
    def get_regular_verbs():
        """50 Verbos Regulares Esenciales."""
        return [
            {"verb": "Ask", "past": "Asked", "meaning": "Preguntar", "example": "I [asked](pregunté)."},
            {"verb": "Answer", "past": "Answered", "meaning": "Responder", "example": "He [answered](respondió)."},
            {"verb": "Call", "past": "Called", "meaning": "Llamar", "example": "[Call](llama) me."},
            {"verb": "Clean", "past": "Cleaned", "meaning": "Limpiar", "example": "I [cleaned](limpié)."},
            {"verb": "Close", "past": "Closed", "meaning": "Cerrar", "example": "[Close](cierra) it."},
            {"verb": "Cook", "past": "Cooked", "meaning": "Cocinar", "example": "I [cooked](cociné)."},
            {"verb": "Cry", "past": "Cried", "meaning": "Llorar", "example": "She [cried](lloró)."},
            {"verb": "Dance", "past": "Danced", "meaning": "Bailar", "example": "We [danced](bailamos)."},
            {"verb": "Decide", "past": "Decided", "meaning": "Decidir", "example": "I [decided](decidí)."},
            {"verb": "Enjoy", "past": "Enjoyed", "meaning": "Disfrutar", "example": "I [enjoyed](disfruté) it."},
            {"verb": "Explain", "past": "Explained", "meaning": "Explicar", "example": "He [explained](explicó)."},
            {"verb": "Finish", "past": "Finished", "meaning": "Terminar", "example": "I [finished](terminé)."},
            {"verb": "Help", "past": "Helped", "meaning": "Ayudar", "example": "He [helped](ayudó)."},
            {"verb": "Hope", "past": "Hoped", "meaning": "Esperar", "example": "I [hoped](esperaba)."},
            {"verb": "Jump", "past": "Jumped", "meaning": "Saltar", "example": "He [jumped](saltó)."},
            {"verb": "Kiss", "past": "Kissed", "meaning": "Besar", "example": "She [kissed](besó)."},
            {"verb": "Laugh", "past": "Laughed", "meaning": "Reír", "example": "We [laughed](reímos)."},
            {"verb": "Learn", "past": "Learned", "meaning": "Aprender", "example": "I [learned](aprendí)."},
            {"verb": "Like", "past": "Liked", "meaning": "Gustar", "example": "I [liked](me gustó)."},
            {"verb": "Listen", "past": "Listened", "meaning": "Escuchar", "example": "I [listened](escuché)."},
            {"verb": "Live", "past": "Lived", "meaning": "Vivir", "example": "I [lived](viví)."},
            {"verb": "Look", "past": "Looked", "meaning": "Mirar", "example": "He [looked](miró)."},
            {"verb": "Love", "past": "Loved", "meaning": "Amar", "example": "I [loved](amé)."},
            {"verb": "Miss", "past": "Missed", "meaning": "Extrañar", "example": "I [missed](extrañé)."},
            {"verb": "Move", "past": "Moved", "meaning": "Mover", "example": "We [moved](nos mudamos)."},
            {"verb": "Need", "past": "Needed", "meaning": "Necesitar", "example": "I [needed](necesitaba)."},
            {"verb": "Open", "past": "Opened", "meaning": "Abrir", "example": "I [opened](abrí)."},
            {"verb": "Paint", "past": "Painted", "meaning": "Pintar", "example": "She [painted](pintó)."},
            {"verb": "Play", "past": "Played", "meaning": "Jugar", "example": "We [played](jugamos)."},
            {"verb": "Rain", "past": "Rained", "meaning": "Llover", "example": "It [rained](llovió)."},
            {"verb": "Remember", "past": "Remembered", "meaning": "Recordar", "example": "I [remembered](recordé)."},
            {"verb": "Smile", "past": "Smiled", "meaning": "Sonreír", "example": "She [smiled](sonrió)."},
            {"verb": "Start", "past": "Started", "meaning": "Comenzar", "example": "It [started](empezó)."},
            {"verb": "Stop", "past": "Stopped", "meaning": "Parar", "example": "He [stopped](paró)."},
            {"verb": "Study", "past": "Studied", "meaning": "Estudiar", "example": "I [studied](estudié)."},
            {"verb": "Talk", "past": "Talked", "meaning": "Hablar", "example": "We [talked](hablamos)."},
            {"verb": "Travel", "past": "Traveled", "meaning": "Viajar", "example": "I [traveled](viajé)."},
            {"verb": "Try", "past": "Tried", "meaning": "Intentar", "example": "I [tried](intenté)."},
            {"verb": "Use", "past": "Used", "meaning": "Usar", "example": "[Use](usa) it."},
            {"verb": "Visit", "past": "Visited", "meaning": "Visitar", "example": "[Visit](visita) me."},
            {"verb": "Wait", "past": "Waited", "meaning": "Esperar", "example": "[Wait](espera) here."},
            {"verb": "Walk", "past": "Walked", "meaning": "Caminar", "example": "I [walk](camino)."},
            {"verb": "Want", "past": "Wanted", "meaning": "Querer", "example": "I [want](quiero) it."},
            {"verb": "Watch", "past": "Watched", "meaning": "Ver", "example": "[Watch](mira) this."},
            {"verb": "Work", "past": "Worked", "meaning": "Trabajar", "example": "Good [work](trabajo)."}
        ]

    @staticmethod
    def get_idioms():
        """50 Modismos."""
        return [
            {"idiom": "Piece of cake", "meaning": "Pan comido (Muy fácil)"},
            {"idiom": "Break a leg", "meaning": "¡Buena suerte!"},
            {"idiom": "Cost an arm and a leg", "meaning": "Cuesta un ojo de la cara"},
            {"idiom": "Hit the sack", "meaning": "Irse a dormir"},
            {"idiom": "Under the weather", "meaning": "Sentirse enfermo"},
            {"idiom": "Spill the beans", "meaning": "Revelar el secreto"},
            {"idiom": "Once in a blue moon", "meaning": "Muy de vez en cuando"},
            {"idiom": "See eye to eye", "meaning": "Estar de acuerdo"},
            {"idiom": "Kill two birds with one stone", "meaning": "Matar dos pájaros de un tiro"},
            {"idiom": "Let the cat out of the bag", "meaning": "Revelar un secreto"},
            {"idiom": "Feeling blue", "meaning": "Sentirse triste"},
            {"idiom": "Time flies", "meaning": "El tiempo vuela"},
            {"idiom": "Speak of the devil", "meaning": "Hablando del rey de Roma"},
            {"idiom": "Call it a day", "meaning": "Terminar por hoy"},
            {"idiom": "Better late than never", "meaning": "Más vale tarde que nunca"},
            {"idiom": "So far so good", "meaning": "Hasta ahora todo bien"},
            {"idiom": "No pain, no gain", "meaning": "Sin dolor no hay ganancia"},
            {"idiom": "Hang in there", "meaning": "¡No te rindas!"},
            {"idiom": "Make a long story short", "meaning": "Resumiendo"},
            {"idiom": "Miss the boat", "meaning": "Perder la oportunidad"},
            {"idiom": "It's not rocket science", "meaning": "No es tan difícil"},
            {"idiom": "Get out of hand", "meaning": "Salirse de control"},
            {"idiom": "Easy does it", "meaning": "Hazlo con cuidado"},
            {"idiom": "A penny for your thoughts", "meaning": "¿En qué piensas?"},
            {"idiom": "Actions speak louder than words", "meaning": "Los hechos valen más que palabras"}
        ]