#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLUE: El Carnaval Tenebroso — Scooby-Doo Edition (CLI)
Autor: ChatGPT
Descripción:
 - Selecciona aleatoriamente 1 de 5 casos.
 - Muestra el problema general.
 - Permite al jugador hacer hasta 5 preguntas (categoría: Personaje, Lugar u Objeto).
 - Cada pregunta abre un submenú con las 5 opciones de esa categoría y devuelve una pista.
 - Tras agotar intentos, el jugador acusa: PERSONAJE + OBJETO + LUGAR.
 - Si acierta, gana y se muestra la explicación del caso; si no, fin del juego.

Instrucciones: Ejecuta este archivo con Python 3.
"""

import random
import sys
from textwrap import fill

# ============ Utilidades de impresión (versión final) ============

def hr(char="─", n=60):
    """Imprime una línea horizontal."""
    print(char * n)

def to_text(value) -> str:
    """Convierte str | list[str] | tuple[str,...] a un único string."""
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, (list, tuple)):
        return "\n".join(str(x) for x in value)
    return str(value)

def titulo(texto):
    """Título en mayúsculas con líneas =."""
    hr("=")
    print(to_text(texto).upper())
    hr("=")

def subtitulo(texto):
    """Subtítulo con líneas -."""
    hr("-")
    print(to_text(texto))
    hr("-")

def wrap(text, width=78):
    """Imprime texto envuelto. Acepta str, list[str] o tuple[str]."""
    print(fill(to_text(text), width=width))

def pedir_opcion(prompt, opciones_validas):
    """
    Lee una opción (número o texto) validando contra opciones_validas (lista de claves).
    - Acepta 1..N
    - Acepta el nombre exacto (case-insensitive)
    """
    while True:
        sel = input(prompt).strip()
        if sel.isdigit():
            idx = int(sel) - 1
            if 0 <= idx < len(opciones_validas):
                return opciones_validas[idx]
        # permitir entrada por nombre exacto (case-insensitive)
        for key in opciones_validas:
            if sel.lower() == key.lower():
                return key
        print("❌ Opción inválida. Intenta de nuevo.")

def esperar_enter():
    input("\n[Presiona ENTER para continuar] ")

# ============ Datos del juego ============

PROBLEMA_GENERAL = (
    "🌀 ¡El Núcleo Temporal ha sido robado!\n"
    "Durante el espectáculo del Carnaval Tenebroso, alguien arrancó el Núcleo de la "
    "Máquina del Tiempo del Profesor Paradox, poniendo en riesgo el pasado… ¡y el futuro!\n"
    "Scooby-Doo y su equipo están investigando, pero necesitan tu ayuda.\n"
    "Tendrás 5 oportunidades para preguntar sobre sospechosos, armas y lugares antes de dar tu acusación final.\n"
    "¡Descubre quién lo robó, con qué lo extrajo y dónde ocultó el Núcleo… antes de que el tiempo se descontrole!"
)

# Estructura general por caso:
# 'culpable'    : nombre del personaje ganador
# 'objeto_real' : arma real
# 'lugar_real'  : lugar real
# Cada categoría tiene:
#   'opciones': { nombre: {'desc': str, 'pista': str, 'real': bool } }
# Y una 'explicacion' narrativa final del caso.

CASOS = [
    # =========================
    # CASO 1 — Carpa Morada
    # =========================
    {
        'nombre': "CASO 1",
        'culpable': "Madame Murk — Bruja de Humo",
        'objeto_real': "Lente Fantasmal",
        'lugar_real': "Carpa de Magia y Apariciones",
        'explicacion': (
            "¡Jinkies! Todavía recuerdo el humo morado envolviendo la carpa como si respirara. Mientras investigábamos, Fred encontró partículas blancas suspendidas en el aire, flotando como luciérnagas sin rumbo. Scooby y Shaggy juran que escucharon susurros fantasmales pidiendo ayuda. "
            "Al revisar los registros de las luces, descubrimos que alguien apagó parte del alumbrado justo cuando el Núcleo Temporal desapareció. Eso solo dejaba una opción lógica… "
            "Madame Murk usó el Lente Fantasmal para generar una horda de espíritus ilusorios. "
            "Los espectadores creyeron que era parte del espectáculo. ¡Qué truco! "
            "Mientras la multitud gritaba por la aparición masiva, la bruja deslizó el Núcleo dentro de su vestido lleno de humo y lo sacó sin que nadie lo notara. "
            "Seguimos rastros de ceniza etérea hasta encontrar un falso compartimento bajo el escenario, oculto por telas encantadas. "
            "Allí estaba el Núcleo, latente y vibrante. "
            "Madame Murk confesó: "
            "‘Quería abrir un portal para mostrarle al mundo los trucos antiguos… los verdaderos trucos.’ "
            "Shaggy lloraba de miedo, Scooby lo consolaba con galletas… pero al final… "
            "¡Caso cerrado!”"
        ),


        'personajes': {
    "Madame Murk — Bruja de Humo": {
        'desc': "Ilusionista de humo morado y sombras múltiples.",
        'pista': (
            "Cuando le pregunté dónde estuvo, juró que pasó toda la noche practicando trucos de humo. "
            "Sin embargo, su vestido tenía un brillo extraño, como si hubiera acumulado ceniza etérea… "
            "partículas idénticas a las que encontramos en la carpa. "
            "Además, testigos aseguraron que vieron sombras múltiples alrededor de ella, incluso cuando estaba sola. "
            "Como si hubiera fantasmas… creados artificialmente."
        ),
        'real': True
    },

    "Rollo Riptide — Hombre Sirena": {
        'desc': "Guardia acuático del lago, siempre húmedo.",
        'pista': (
            "Rollo dijo que se mantuvo alrededor del lago, verificando la temperatura del agua. "
            "Su piel estaba húmeda, pero eso no prueba nada, siempre está húmedo. "
            "Lo único relevante es que vio ‘luces moradas’ provenientes de la Carpa de Magia. "
            "Eso solo confirma el espectáculo programado; no lo incrimina. "
            "Además, su oído débil lo hace incapaz de interactuar con fantasmas… confunde ecos de agua con voces."
        ),
        'real': False
    },

    "Cipher Claw — Hombre Sombra Hacker": {
        'desc': "Sombra que manipula sensores, sigiloso.",
        'pista': (
            "Cipher afirmó que trabajaba en sensores cerca de la entrada del parque. "
            "Dijo que solo vio fallas eléctricas cuando la carpa se oscureció… "
            "pero cuando revisamos los registros del panel central NO hubo manipulación. "
            "Los tornillos estaban intactos. Cipher no dejó rastro material alguno."
        ),
        'real': False
    },

    "Jinx Jingler — Payaso Espectral": {
        'desc': "Payaso ruidoso con gadgets; ama el taller.",
        'pista': (
            "Jinx asegura que estaba probando un nuevo gadget sonoro dentro de la Casa de los Espejos. "
            "Los visitantes no vieron fantasmas, sino su propia risa multiplicada por el eco. "
            "Encontramos pelusa de muñecos en sus guantes, señal de que estuvo causando caos en la zona de premios… "
            "pero NO encontramos rastros dentro de la carpa."
        ),
        'real': False
    },

    "Gargant Grimm — Gárgola de Piedra": {
        'desc': "Vigía pétreo desde lo alto de la montaña rusa.",
        'pista': (
            "El gigante pétreo alegó que se mantuvo inmóvil sobre la montaña rusa. "
            "Sus huellas estaban en los rieles, muy lejos de la carpa. "
            "Además, sus pies dejan polvo de roca, no ceniza etérea. "
            "Nada vincula a Grimm con la actividad espectral dentro de la carpa."
        ),
        'real': False
    },
},

        'lugares': {
    "Carpa de Magia y Apariciones": {
        'desc': "Lona morada con estática y telas chamuscadas bajo el estrado.",
        'pista': (
            "La lona morada parecía palpitar como si respirara. El aire allí tenía electricidad estática, "
            "y los focos chispeaban como luciérnagas inquietas. Bajo el estrado estaban apiladas telas viejas "
            "con bordes chamuscados. Encontramos ceniza etérea flotando, idéntica a la hallada durante el robo. "
            "Además, la madera tenía marcas de tela arrastrada, como si alguien hubiese escondido algo allí."
        ),
        'real': True
    },

    "Montaña Rusa “La Serpiente Nocturna”": {
        'desc': "Rieles entre luces rojas; metal vibrante.",
        'pista': (
            "Los rieles serpenteaban entre luces rojas como ojos de dragón. El aire vibraba por gritos y metal. "
            "Hubo ruidos metálicos, pero provenían del mantenimiento programado. La altura extrema haría que "
            "el Núcleo fuese inestable; nadie arriesgaría un objeto temporal allí arriba temblando entre curvas."
        ),
        'real': False
    },

    "Casa de los Espejos Distorsionados": {
        'desc': "Reflejos exagerados por doquier.",
        'pista': (
            "Reflejos torcidos devolvían versiones exageradas de nosotros. Scooby casi llora al verse con cuatro narices. "
            "Luces moradas rebotaban en los espejos, pero ese color era común en la feria. No encontramos compartimientos "
            "ocultos; los espejos son demasiado frágiles para ocultar energía temporal."
        ),
        'real': False
    },

    "Lago de Botes Chocones": {
        'desc': "Agua negra y botes diminutos.",
        'pista': (
            "El agua negra brillaba con luces verdes desde el fondo. Los botes chocaban como carritos de supermercado fantasma. "
            "Encontramos tornillos flotando, pero provenían de un bote descompuesto. Además, la humedad extrema "
            "desestabilizaría el Núcleo y podría causar un mini–tsunami temporal."
        ),
        'real': False
    },

    "Taller de Premios y Muñecos": {
        'desc': "Estantes con osos gigantes; luces parpadeantes.",
        'pista': (
            "Estantes altos sostenían osos gigantes que parecían sonreír demasiado. Luces parpadeaban nerviosas. "
            "Encontramos algodón movido, pero coincidía con reparaciones recientes. No detectamos rastros energéticos. "
            "Los escáneres temporales estaban completamente limpios."
        ),
        'real': False
    },
},

        'objetos': {
    "Lente Fantasmal": {
        'desc': "Genera hordas de fantasmas ilusorios.",
        'pista': (
            "Entre partículas blancas suspendidas bajo la carpa, hallamos fragmentos cristalinos microscópicos, "
            "típicos de material etéreo fotónico usado únicamente por lentes espectrales. Además, varios espectadores "
            "aseguraron haber visto fantasmas flotando que se desvanecieron al quitarse los lentes 3D del show. "
            "Scooby juró que uno le atravesó la cabeza sin dolor. (PISTA REAL)"
        ),
        'real': True
    },

    "Guante Cuántico Reversor": {
        'desc': "Pliega metal como origami.",
        'pista': (
            "Algunos tornillos parecían flojos, pero su forma no tenía dobleces geométricos. Si este guante hubiera sido usado, "
            "el pedestal mostraría pliegues perfectos y las barandas estarían dobladas con ángulos exactos. Nada de eso ocurrió. "
            "Shaggy intentó doblar un clavo para comprobarlo, pero solo se lastimó el dedo."
        ),
        'real': False
    },

    "Flauta de Retumbo Cronal": {
        'desc': "Afloja tornillos por vibración ultrasónica.",
        'pista': (
            "Los sensores registraron ruido, pero eran aplausos del público. Ningún tornillo cayó al piso y no hubo vibración "
            "anormal en los soportes. Scooby pensó que el sonido era 'gastritis teatral'."
        ),
        'real': False
    },


    "Bolsa Sin Fondo": {
        'desc': "Desaparece objetos pequeños al vacío.",
        'pista': (
            "Solo un tornillo faltaba, probablemente rodó hacia un hueco. Si esta bolsa hubiera intervenido, desaparecerían "
            "múltiples piezas pequeñas y el mecanismo quedaría inestable. Pero todo estaba prácticamente intacto. Shaggy "
            "buscó la supuesta bolsa… y encontró solo papas fritas."
        ),
        'real': False
    },

    "Espada Samurai Maldita": {
        'desc': "Filo que cauteriza cualquier material.",
        'pista': (
            "No se detectó ninguna marca de corte limpio en el pedestal ni en la tarima. Los bordes estaban íntegros, sin fractura "
            "ni residuos de energía de filo. Si la espada se hubiera usado, habría cortes perfectos en madera, tela y metal. "
            "Nada de eso. Scooby intentó cortar un waffle con una espátula y dijo: '¡No funciona como la katana!'"
        ),
        'real': False
    },
},
},  # ← cierre del diccionario 'objetos' (deja esta coma si el caso continúa)


    # =========================
    # CASO 2 — Lago Negro
    # =========================
{
    'nombre': "CASO 2",
    'culpable': "Rollo Riptide — Hombre Sirena",
    'objeto_real': "Bolsa Sin Fondo",
    'lugar_real': "Lago de Botes Chocones",
    'explicacion': """Jamás olvidaré lo frío que estaba el aire cerca del lago esa noche. El agua negra reflejaba luces verdes desde el fondo, como si alguien hubiera instalado focos secretos.
Mientras los botes chocaban torpemente, Velma notó algo extraño: tornillos faltaban, no aflojados, faltaban. Eso indicaba solo un arma posible: ¡la Bolsa Sin Fondo! Y solo alguien que pudiera moverse rápido bajo el agua podría evitar que lo vieran… Era Rollo Riptide.

Mientras la multitud observaba un choque controlado entre botes, él se sumergió. Como sirena, podía contener la respiración por mucho tiempo. Desapareció tornillos clave, levantó paneles, arrancó el Núcleo Temporal y lo escondió dentro del casco interior de un bote hundido, camuflado entre algas negras.

Cuando lo encontramos, Scooby se negó a nadar… hasta que ofrecimos tres Scooby-Galletas extra grandes.
Rollo confesó: 'Desde ahí puedo viajar a las profundidades del pasado… antes de que nuestro reino marino se perdiera.'
Daphne suspiró. Shaggy ya estaba seco… con secadora portátil.
¡Otro misterio resuelto!""",


        'personajes': {
    "Madame Murk — Bruja de Humo": {
        'desc': "Ilusionista que evita humedad.",
        'pista': (
            "Cuando llegué a su carpa, estaba rodeada de humo violeta, practicando apariciones espectrales. "
            "Murk aseguró que nunca va al lago, pues la humedad arruina sus trucos mágicos. "
            "Pero en una mesa vi un frasco de disipador de humedad. Ella alegó que era para el humo… "
            "pero no había niebla condensada ese día."
        ),
        'real': False
    },

    "Gargant Grimm — Gárgola de Piedra": {
        'desc': "Meditativo en lo alto; musgo en dedos.",
        'pista': (
            "Encontré a Gargant sentado en la cima de la montaña rusa, meditando. "
            "Cuando le pregunté si estuvo en el lago, respondió que el agua negra debilita sus grietas. "
            "Sin embargo, sus dedos tenían polvo de musgo verde… el mismo tipo que flota sobre el lago. "
            "Al analizarlo descubrimos que ese musgo también crece en las alturas donde él se sienta."
        ),
        'real': False
    },

    "Jinx Jingler — Payaso Espectral": {
        'desc': "Risa que rebota en el túnel.",
        'pista': (
            "Encontré a Jinx en el túnel de espejos, probando un gadget que hacía rebotar su risa como eco infinito. "
            "Él afirmó que nunca se acercaría al lago… porque su maquillaje se corre con humedad. "
            "Dijo haber escuchado un ‘chapoteo sospechoso’, pero admitió que pudo haber sido su propio zapato en un charco."
        ),
        'real': False
    },

    "Cipher Claw — Hombre Sombra Hacker": {
        'desc': "Arregla sensores; guantes con aceite.",
        'pista': (
            "Interrogar a una sombra no es fácil. Cipher juró que estuvo arreglando sensores en la entrada principal de la feria. "
            "Sus guantes tenían manchas de aceite negro… del mismo color que el agua del lago. "
            "Pero al analizarlas vimos que provenían de engranes oxidados del área mecánica."
        ),
        'real': False
    },

    "Rollo Riptide — Hombre Sirena": {
        'desc': "Se mueve bajo el agua con facilidad.",
        'pista': (
            "Encontré a Rollo sentado en el muelle, dejando caer su cola en el agua como si nada hubiera pasado. "
            "Su piel brillaba con residuos microscópicos de vectro-sal líquida, la misma que encontramos pegada en los bordes "
            "internos del pedestal. Al preguntarle, dijo que el lago tiene ‘su propia vida’… y que algunos secretos ‘solo "
            "aparecen bajo la superficie’. Cuando Shaggy lo observó mejor, notó que faltaba un pequeño engrane en su cinturón "
            "utilitario. Exactamente el mismo tipo de engrane que desapareció del pedestal cuando el Núcleo fue robado. "
            "Scooby olió el cinturón y dijo: “¡Rollo-rero!”"
        ),
        'real': True
    },
},

        'lugares': {
    "Carpa de Magia y Apariciones": {
        'desc': "Humo morado; trucos mecánicos.",
        'pista': (
            "Entramos entre nubes de humo morado. Los espectadores aún discutían sobre sombras fantasmas. "
            "Sin embargo, bajo el escenario encontramos solo viejos trucos mecánicos, telas encantadas y polvo de purpurina. "
            "Scooby encontró un sombrero gigante y se quedó trabado en él…"
        ),
        'real': False
    },

    "Casa de los Espejos Distorsionados": {
        'desc': "Reflejos inquietantes.",
        'pista': (
            "Da escalofríos ver tu reflejo con cinco narices… "
            "Exploramos detrás de los espejos. Había huecos, pero estaban vacíos. "
            "Velma encontró humedad ligera en un espejo, pero provenía de Scooby respirando cerca en pánico."
        ),
        'real': False
    },

    "Montaña Rusa “La Serpiente Nocturna”": {
        'desc': "Pasillos de mantenimiento.",
        'pista': (
            "Hay pasillos de mantenimiento bajo la montaña rusa. "
            "Ahí encontramos tornillos sueltos, pero estaban doblados, no faltantes. "
            "Eso sugiere uso de fuerza, no desaparición. "
            "Scooby se quedó atrapado en un carrito y dio tres vueltas gritando…"
        ),
        'real': False
    },

    "Lago de Botes Chocones": {
        'desc': "Agua negra, luces verdes.",
        'pista': (
            "El agua negra parecía absorber la luz. "
            "Hurgueteamos entre los botes… hasta que Velma notó piezas faltantes en un panel flotante. "
            "Luego, Fred vio lucecitas verdes bajo la superficie. "
            "Nos sumergimos (bueno, yo me sumergí… Scooby se quedó llorando con chaleco salvavidas). "
            "Entre algas negras encontramos un bote hundido cuyo casco interior estaba modificado. "
            "Dentro, oculto tras paneles, vibraba el Núcleo Temporal. (PISTA REAL)"
        ),
        'real': True
    },

    "Taller de Premios y Muñecos": {
        'desc': "Peluches y trampilla a almacén.",
        'pista': (
            "Entre muñecos gigantes con ojos inquietantes, encontramos algodón tirado y herramientas. "
            "Había una trampilla secreta, pero solo conducía a un almacén de peluches defectuosos. "
            "Scooby abrió un oso gigante… encontró galletas de algodón de azúcar."
        ),
        'real': False
    },
},

       'objetos': {
    "Lente Fantasmal": {
        'desc': "Ilusiones espectrales masivas.",
        'pista': (
            "Interrogamos al encargado de luces y cámaras. Él afirmó haber visto sombras múltiples "
            "cerca del Lago Negro, como si fantasmas rodearan los botes. Al acercarnos, descubrimos "
            "que eran simplemente visitantes reflejados por el agua iluminada.\n"
            "Además, no encontramos partículas etéreas típicas del lente.\n"
            "Scooby se asustó de su propio reflejo flotando y cayó de un bote…"
        ),
        'real': False
    },

    "Guante Cuántico Reversor": {
        'desc': "Plegado de metal sin romper.",
        'pista': (
            "Analizamos el pedestal y bordes metálicos en la zona acuática. Si el Guante hubiese sido "
            "usado, veríamos dobleces geométricos perfectos.\n"
            "¿Resultado?\n"
            "Ni una sola pieza doblada.\n"
            "Encontramos pequeñas huellas húmedas… pero eran de Scooby escapando del muelle."
        ),
        'real': False
    },

    "Flauta de Retumbo Cronal": {
        'desc': "Resonancia para aflojar tornillos.",
        'pista': (
            "El túnel del sonido estaba cerrado esa noche. Analizamos sensores auditivos "
            "alrededor del lago, buscando vibraciones ultrasónicas.\n"
            "Los datos arrojaron:\n"
            "• Aplausos\n"
            "• Pasos rápidos\n"
            "• El sonido de Shaggy gritando en pánico\n"
            "Pero NO hubo ondas suficientes para aflojar tornillos."
        ),
        'real': False
    },

    "Bolsa Sin Fondo": {
        'desc': "Desmaterializa piezas pequeñas al vacío.",
        'pista': (
            "Aquí encontramos algo inquietante. Entre las piezas faltantes del mecanismo, "
            "el pedestal tenía ranuras perfectamente vacías. No estaban sueltas, ni dobladas, "
            "ni vibradas…\n"
            "Además, en el borde del muelle encontramos residuo vacío arcano, rastros microscópicos "
            "que dejan los objetos justo antes de desmaterializarse.\n"
            "Rollo evitaba mirarnos a los ojos… Scooby olfateó el borde del pedestal y dijo:"
        ) + ' “Rollo-rero…” (PISTA REAL)',
        'real': True
    },

    "Espada Samurai Maldita": {
        'desc': "Corte místico perfecto.",
        'pista': (
            "Exploramos superficies cercanas en la zona acuática buscando cortes perfectos. "
            "Si esta espada se hubiera usado, encontraríamos:\n"
            "• Madera finamente seccionada\n"
            "• Paneles partidos\n"
            "• Bordes limpios\n"
            "Pero no hallamos ni un solo corte.\n"
            "Shaggy intentó cortar una dona para simular la espada… terminó cortándosela en la ropa."
        ),
        'real': False
    },
},
},
    # =========================
    # CASO 3 — Serpiente Nocturna
    # =========================
    {
        'nombre': "CASO 3",
        'culpable': "Gargant Grimm — Gárgola de Piedra",
        'objeto_real': "Guante Cuántico Reversor",
        'lugar_real': "Montaña Rusa “La Serpiente Nocturna”",
         'explicacion': (
            "La Montaña Rusa vibraba como si rugiera. Los rieles cercanos al pedestal metálico "
            "estaban doblados en patrones perfectos, casi como origami industrial.\n"
            "Solo un arma puede hacer eso:\n"
            "¡El Guante Cuántico Reversor!\n\n"
            "Velma lo confirmó al comparar las marcas con registros crono-geométricos.\n"
            "Y solo una criatura lo suficientemente pesada —pero sigilosa— podía moverse por los rieles "
            "sin romperlos… Gargant Grimm, la gárgola.\n\n"
            "Mientras todos gritaban emocionados en los carros, Grimm caminó por encima, plegó el soporte "
            "metálico, descolgó el Núcleo y lo llevó al punto más alto del tramo, escondiéndolo dentro de "
            "una compuerta de mantenimiento clausurada.\n\n"
            "Tuvimos que subir con arnés (Shaggy lloró), pero allí estaba el Núcleo —iluminado por luces "
            "serpenteantes.\n\n"
            "Grimm confesó:\n"
            "‘Quería retroceder el tiempo… a cuando era carne y hueso.’\n"
            "Fred asintió.\n"
            "Velma anotó.\n"
            "Scooby rugió como dragón. (No sabemos por qué.)"
        ),

                'personajes': {
            "Madame Murk — Bruja de Humo": {
                'desc': "Ilusionista que detesta vibraciones de la montaña.",
                'pista': (
                    "Encontramos a Madame Murk practicando trucos en su carpa. Juró que jamás pondría un pie en la "
                    "montaña rusa porque la vibración dispersa su humo. Su túnica estaba cubierta de ceniza etérea, "
                    "pero NO metal doblado. Dijo haber visto luces verdes parpadeando desde lejos, pero eso era parte "
                    "del show. Cuando Scooby tosió por el humo, Murk gritó: ‘¡No tengo nada que ver con esa atracción "
                    "ruidosa!’"
                ),
                'real': False
            },

            "Rollo Riptide — Hombre Sirena": {
                'desc': "Acuático; poca movilidad en rieles.",
                'pista': (
                    "Rollo estaba en el lago disfrutando la humedad nocturna. Aseguró que el metal plegado no es cosa "
                    "suya porque puede oxidarse en contacto con agua salada. Su cola estaba húmeda, pero eso es normal. "
                    "Además, no sabe caminar en superficies inclinadas… se resbala. Scooby imitó el sonido de resbalón… "
                    "Shaggy cayó inmediatamente."
                ),
                'real': False
            },

            "Cipher Claw — Hombre Sombra Hacker": {
                'desc': "Aceite de engranes en guantes.",
                'pista': (
                    "Cipher dijo que pasó toda la noche en la cabina de sensores, calibrando cámaras. Sus guantes tenían "
                    "aceite negro… pero al analizarlo descubrimos que provenía de engranes eléctricos, no metal plegado. "
                    "Cuando le preguntamos si vio algo en los rieles, dijo: ‘Las cámaras se apagaron… por interferencia "
                    "electromagnética.’ Curioso… pero no concluyente."
                ),
                'real': False
            },

            "Jinx Jingler — Payaso Espectral": {
                'desc': "Pelusa de algodón en zapatos del taller.",
                'pista': (
                    "Jinx asegura que estuvo en el Taller de Premios y Muñecos, probando chistes explosivos. Sus zapatos "
                    "tenían pelusa blanca, típica de ese lugar. Cuando le preguntamos por la montaña rusa, dijo: "
                    "‘¡Demasiado seria para mí! La Serpiente Nocturna no ríe.’ Encontramos algodón flotando cerca de la "
                    "entrada al taller… no de la montaña rusa."
                ),
                'real': False
            },

            "Gargant Grimm — Gárgola de Piedra": {
                'desc': "Vigía en lo alto de la montaña.",
                'pista': (
                    "Encontramos a Gargant descansando en la cima de La Serpiente Nocturna. Sus manos tenían partículas "
                    "microscópicas de metal plegado, idénticas a las marcas en el pedestal. Cuando le preguntamos: "
                    "‘¿Estabas EN los rieles?’ Él respondió: ‘Observo desde arriba… siempre.’ Pero Velma notó zarcillos "
                    "de metal doblado en huecos cercanos, marcados por su peso pétreo. Además, la vibración de los carros "
                    "no afectó la precisión geométrica del metal. Eso requiere fuerza y estabilidad… propias de piedra."
                ),
                'real': True
            },
        },

                'lugares': {
            "Carpa de Magia y Apariciones": {
                'desc': "Sombras teatrales y resina pirotécnica.",
                'pista': (
                    "El humo morado flotaba densamente mientras sombras teatrales bailaban al compás del espectáculo. "
                    "Bajo el escenario, encontramos resina brillante… pero correspondía a sellos de seguridad "
                    "pirotécnicos usados por Madame Murk. Además, la madera del estrado no presentaba ningún rastro "
                    "de plegado. Scooby intentó mover una tabla… terminó lleno de confeti."
                ),
                'real': False
            },

            "Casa de los Espejos Distorsionados": {
                'desc': "Refuerzos doblados irregularmente.",
                'pista': (
                    "Analizamos el subsuelo detrás de los espejos. Encontramos paneles de refuerzo doblados, pero… "
                    "el plisado no era geométrico perfecto, sino irregular. Eso indica daño por impacto, no plegado "
                    "cuántico. Además, las vibraciones distorsionaban reflejos, pero no el metal principal. Scooby vio "
                    "un reflejo de sí mismo con orejas gigantes… y huyó."
                ),
                'real': False
            },

            "Lago de Botes Chocones": {
                'desc': "Paneles corroídos por salinidad.",
                'pista': (
                    "El agua negra estilizada reflejaba luces, creando patrones serpenteantes. Al inspeccionar el "
                    "fondo rústico, encontramos paneles corroídos… pero esta corrosión ocurre por reacción salina. "
                    "No había metal doblado, solo piezas oxidadas. Además, cualquier vibración del guante habría "
                    "alertado a visitantes cercanos."
                ),
                'real': False
            },

            "Montaña Rusa “La Serpiente Nocturna”": {
                'desc': "Altura, humo artificial y luces rojas.",
                'pista': (
                    "La Serpiente Nocturna retumba como un dragón mecánico. En la parte alta del recorrido, entre luces "
                    "rojas y humo artificial, descubrimos pliegues geométricos perfectos en los soportes del pedestal. "
                    "La precisión del plegado indica uso de tecnología cuántica: sin fractura, sin cortes y sin "
                    "vibración detectable."
                ),
                'real': True
            },

            "Taller de Premios y Muñecos": {
                'desc': "Metal cortado limpio de utilería.",
                'pista': (
                    "Entre peluches con ojos inquietantes, encontramos un soporte metálico recortado, pero su borde era "
                    "limpio, como si hubiese sido cortado. Además, el soporte recortado pertenece al muñeco gigante… "
                    "NO al pedestal del Núcleo. Scooby abrazó un peluche, jurando que lo vio parpadear."
                ),
                'real': False
            },
        },

                'objetos': {
            "Lente Fantasmal": {
                'desc': "Ilusión fotónica.",
                'pista': (
                    "Mientras revisábamos el altar de proyección dentro de la Carpa de Magia, encontré pequeños prismas empañados "
                    "y lentes empaquetados para el público. Alguien había dejado un estuche abierto con marcas de dedos y una "
                    "estampilla de humo en la tela; parecía directo del camerino de un ilusionista. En la costura del estuche había "
                    "restos de una sustancia que los asistentes identificaron como ‘ceniza etérea’, y Jinx Jingler comentó que vio a "
                    "Madame Murk sosteniendo algo similar la noche anterior."
                ),
                'real': False
            },

            "Guante Cuántico Reversor": {
                'desc': "Pliega metal con precisión.",
                'pista': (
                    "Bajo la estructura metálica junto al pedestal de la Serpiente Nocturna hallamos marcas en el borde de una viga: "
                    "pliegues geométricos tan precisos que no podían ser obra de una mano normal. Además, el metal presentaba "
                    "microabolladuras en el lado opuesto, como si se hubiera doblado desde dentro hacia fuera en un patrón repetido. "
                    "Entre las grietas del pliegue quedó polvo pétreo y diminutos fragmentos de roca calcárea. Las uñas de Gargant "
                    "Grimm tenían exactamente ese mismo polvo incrustado. (PISTA REAL)"
                ),
                'real': True
            },

            "Flauta de Retumbo Cronal": {
                'desc': "Resonancia de aflojamiento.",
                'pista': (
                    "Registramos patrones de audio en la cinta de seguridad —una serie de notas a baja frecuencia— y un visitante "
                    "señaló que la música sonó extrañamente hueca. En la cabina del Túnel del Sonido alguien dejó una funda de "
                    "instrumento abierta, sucia de aceite y huellas. Cipher Claw admitió haber oído ‘una melodía rara’ durante sus "
                    "calibraciones, y dijo que alguien tocó una nota sostenida que hizo vibrar un panel."
                ),
                'real': False
            },

            "Bolsa Sin Fondo": {
                'desc': "Vacío instantáneo.",
                'pista': (
                    "En el muelle revisamos cajas, compartimientos y el borde del pedestal. Faltaban piezas pequeñas del anclaje, "
                    "pero no había restos en el lugar —como si hubieran sido instantáneamente removidos de la realidad. Encontramos, "
                    "en una tabla cercana, un rastro de arcilla húmeda y algas adheridas. Rollo Riptide tenía algas en la bota esa "
                    "noche; un testigo lo vio pasar por el muelle. Eso llevó a algunos a sugerir que fue él quien ‘tragó’ las piezas."
                ),
                'real': False
            },

            "Espada Samurai Maldita": {
                'desc': "Filo místico.",
                'pista': (
                    "En el taller contiguo hallamos cortes en una plancha metálica usada como prototipo de carrocería de atracción. "
                    "Los bordes de los cortes eran limpios, como hechos por filo superlativo. Cerca había una funda con un guardián "
                    "de tela rasgada. Un operario dijo que Jinx Jingler había estado jugueteando con objetos filosos esa noche para "
                    "un número. Algunos juraron haber visto su funda abierta."
                ),
                'real': False
            },
        },
    },
    # =========================
    # CASO 4 — Túnel del Sonido
    # =========================
    {
        'nombre': "CASO 4",
        'culpable': "Cipher Claw — Hombre Sombra Hacker",
        'objeto_real': "Flauta de Retumbo Cronal",
        'lugar_real': "Túnel del Sonido",
                'explicacion': (
            "“El Túnel del Sonido estaba inquietantemente silencioso. Tan silencioso que podías escuchar tu "
            "propio corazón. Sin embargo, los sensores marcaban vibraciones fuertes momentos antes del robo. "
            "Eso coincidía con una sola arma: ¡La Flauta de Retumbo Cronal! "
            "Lo curioso es que las cámaras cercanas registraron una sombra manipulando los controles antes de "
            "que parpadearan y murieran. Solo una sombra podía hacer eso: Cipher Claw. "
            "Mientras Scooby y Shaggy probaban micrófonos (terrible momento para hacerlo), encontramos marcas "
            "de tornillos sueltos que vibraron hasta desprenderse. "
            "El Núcleo estaba escondido detrás de una bocina gigante, camuflado entre cables que resonaban "
            "levemente con memoria temporal. "
            "Cuando lo confrontamos, Cipher confesó: ‘Quería hackear el tiempo. Corregir la única competencia "
            "que perdí.’ "
            "Velma suspiró profundamente. Daphne tomó nota. Fred sonrió inspirado. "
            "Scooby gritó, ‘Rooo–rrooo!’ —Creo que quiso decir ‘Buen trabajo’. ”"
        ),

        'personajes': {
    "Madame Murk — Bruja de Humo": {
        'desc': "Maestra de la niebla.",
        'pista': (
            "La encontramos practicando ilusiones en su carpa, rodeada de humo violeta. Cuando preguntamos por el túnel, "
            "se estremeció: ‘El eco distorsiona mi niebla… arruina mis hechizos.’ Notamos una pluma púrpura en su manga, "
            "probablemente parte del vestuario. Un guardia afirmó verla cerca de los espejos, NO del túnel."
        ),
        'real': False
    },

    "Rollo Riptide — Hombre Sirena": {
        'desc': "Baladas marinas; humedad normal.",
        'pista': (
            "Rollo juró estar en el muelle cantando una balada marina. Shaggy lo escuchó cantar… ¿en fa sostenido? "
            "Encontramos gotas de agua salada cerca de una bocina portátil rota, pero eran demasiado grandes: "
            "como si vinieran de un cubo de limpieza. Además, la humedad del túnel estaba en niveles normales."
        ),
        'real': False
    },

    "Gargant Grimm — Gárgola de Piedra": {
        'desc': "En su nido, lejos del túnel.",
        'pista': (
            "Gargant descansaba en su nido al inicio de la montaña rusa. Si hubiese estado en el túnel, el piso "
            "mostraría huellas pétreas. Solo encontramos polvo de piedra en un pasillo… proveniente de una estatua "
            "decorativa rota. Cuando le preguntamos si escuchó vibraciones, dijo: ‘La gente gritaba… como siempre.’"
        ),
        'real': False
    },

    "Jinx Jingler — Payaso Espectral": {
        'desc': "Amplificador de risas.",
        'pista': (
            "En el taller de premios, Jinx probaba un amplificador de risas. Algunos dijeron haber escuchado ecos en "
            "el túnel, pero era su gadget probándose al otro lado de la carpa. Hallamos pelusa de muñeco pegada en un "
            "cable del túnel, pero se dispersa por ventilación fácilmente. Scooby imitó su risa… retumbó por todo el pasillo."
        ),
        'real': False
    },

    "Cipher Claw — Hombre Sombra Hacker": {
        'desc': "Sombra que hackea sensores.",
        'pista': (
            "Cipher estaba inquietamente callado. Le preguntamos si había estado cerca del túnel. Su respuesta: ‘No me gustan "
            "los ecos. Revelan demasiado.’ En una consola encontramos residuos negros de aceite dieléctrico típico de sus guantes. "
            "Solo una Sombra puede manipular paneles sin ser vista, camuflar vibraciones y deshabilitar sensores temporalmente. "
            "(PISTA REAL)"
        ),
        'real': True
    },
},

       'lugares': {
    "Carpa de Magia y Apariciones": {
        'desc': "Luces púrpura y humo plateado.",
        'pista': (
            "Luces púrpura parpadeaban, y humo plateado se arremolinaba alrededor de los espectadores. "
            "Encontramos un micrófono caído en la parte trasera con manchas de humedad. Un asistente aseguró "
            "haber oído ecos aquí… pero descubrimos que eran parte del espectáculo: una grabación programada."
        ),
        'real': False
    },

    "Casa de los Espejos Distorsionados": {
        'desc': "Ecos raros por espejos curvos.",
        'pista': (
            "El sonido en este lugar rebota en los espejos curvos, produciendo ecos extraños, pero sólo a volumen controlado. "
            "Encontramos un auricular roto en el piso con marcas de presión… pero nada relacionado con vibración sub-sónica."
        ),
        'real': False
    },

    "La Montaña Rusa “La Serpiente Nocturna”": {
        'desc': "Resonancia mecánica usual.",
        'pista': (
            "Registramos sonido de vías y gritos de visitantes. Normalmente aquí hay resonancia mecánica, pero esa noche "
            "el sistema marcó una disminución sonora crítica justo cuando el Núcleo desapareció. Sin embargo, los tornillos "
            "estaban bien apretados —ninguna vibración los aflojó."
        ),
        'real': False
    },

    "Lago de Botes Chocones": {
        'desc': "Agua que absorbe sonido.",
        'pista': (
            "El agua absorbía sonido, creando silencio profundo. Encontramos un altavoz portátil mojado flotando cerca del borde, "
            "emitiendo pitidos suaves cuando Shaggy lo encendió. No hubo vibración suficiente para afectar tornillos."
        ),
        'real': False
    },

    "Túnel del Sonido": {
        'desc': "Silencio anómalo y marcas de ondas.",
        'pista': (
            "El Túnel del Sonido era inquietante. Silencioso… demasiado silencioso. En las paredes había marcas circulares, como si "
            "ondas invisibles hubieran vibrado con fuerza. Detrás de una bocina gigante encontramos memoria temporal auditiva, "
            "vibración residual y un espacio vacío del tamaño del Núcleo. También escuchamos un leve eco repitiendo eventos segundos después. "
            "(PISTA REAL)"
        ),
        'real': True
    },
},

        'objetos': {
    "Lente Fantasmal": {
        'desc': "Cristales espectrales.",
        'pista': (
            "En la Carpa de Magia recopilamos lentes y prismas usados por el público. Uno de los estuches presentaba "
            "microabrasiones en la montura y una pequeña capa de polvo que brillaba bajo luz ultravioleta. Lo curioso es "
            "que ese polvo flotaba hacia arriba y abajo con las corrientes de aire… pero al examinarlo no encontramos "
            "ninguna firma fotónica continua que indicara ilusión activa en el túnel."
        ),
        'real': False
    },

    "Guante Cuántico Reversor": {
        'desc': "Pliega metal.",
        'pista': (
            "Examinamos uniones metálicas cerca del pedestal. Si el Guante hubiera actuado aquí, veríamos micropliegues "
            "regulares y tensión interna en el metal. Las marcas encontradas eran solo abrasiones superficiales, como si "
            "alguien hubiera intentado forzar una placa sin éxito. Un empleado afirmó ver a Gargant Grimm caminando por "
            "la zona de mantenimiento con polvo metálico fresco en los dedos… pero no hubo plegado cuántico."
        ),
        'real': False
    },

    "Flauta de Retumbo Cronal": {
        'desc': "Frecuencia sub-sónica afloja tornillos.",
        'pista': (
            "Este fue el elemento decisivo. Dentro de la bocina gigante hallamos una flauta hueca conectada a un conducto "
            "sonoro secundario. En su interior había un diminuto transductor piezoeléctrico unido a un microcontrolador "
            "no autorizado. El firmware contenía una firma criptográfica idéntica al patrón encontrado en herramientas "
            "de hacking de Cipher Claw. Además, la carcasa presentaba residuo negro dieléctrico, típico de sus guantes. "
            "(PISTA REAL)"
        ),
        'real': True
    },

    "Bolsa Sin Fondo": {
        'desc': "Vacío instantáneo.",
        'pista': (
            "En una caja de utilería cerca del muelle encontramos un pedazo de tela oscura con fibras impregnadas en el "
            "interior. Pequeñas gotas salinas estaban adheridas a la costura, y un asistente dijo que vio a Rollo Riptide "
            "toquetear ese estuche horas antes. Pero no hubo desaparición instantánea de piezas en el túnel; aquí los "
            "tornillos vibraron, no se desmaterializaron."
        ),
        'real': False
    },

    "Espada Samurai Maldita": {
        'desc': "Cauteriza cortes.",
        'pista': (
            "En un taller cercano hallamos cortes limpios en una lámina de prueba, sin rebabas, como hechos por filo "
            "premium. Un operario vio una funda vieja rasgada junto a la mesa, y un asistente jura que Jinx jugaba con "
            "objetos filosos para un truco. Sin embargo, en el túnel no encontramos bordes cauterizados: aquí hubo "
            "vibración sonora, no corte místico."
        ),
        'real': False
    },
},
},
    # =========================
    # CASO 5 — Taller de Muñecos
    # =========================
    {
    'nombre': "CASO 5",
    'culpable': "Jinx Jingler — Payaso Espectral",
    'objeto_real': "Espada Samurai Maldita",
    'lugar_real': "Taller de Premios y Muñecos",
    'explicacion': """¡Zoinks! Ese taller daba escalofríos. Los muñecos parecían mirarnos con ojos cosidos. Algunos peluches tenían cortes diminutos casi invisibles… pero cuando Velma pasó la linterna, pudimos ver bordes limpios, rectos como regla.

Eso significa una sola arma:
¡la Espada Samurai Maldita!

Y solo alguien tan impredecible podría usar algo así sin pensar demasiado:
Jinx Jingler, el payaso espectral.

Entre risas retumbantes, gadgets escondidos y peluches animados, Jinx cortó discretamente la esquina del pedestal, liberó el Núcleo Temporal y lo escondió dentro del vientre hueco de un muñeco gigante.

Lo encontramos gracias al olor a tela cauterizada, quemada con filo místico.

Jinx confesó:
‘¡Imagina traer payasos legendarios del pasado para EL MEJOR SHOW! ¡Sería épico!’

Velma se ajustó los lentes:
‘Pero destruirías el flujo temporal.’

Scooby respondió:
‘Rag-ra-ragh!’
(Traducción: ‘¡Regresa esa cosa ahí mismo!’)

¡Caso cerrado!""",


        'personajes': {
    "Madame Murk — Bruja de Humo": {
        'desc': "Humo endurecido engañoso.",
        'pista': """Murk caminaba entre hilos y retazos, dejando pequeñas nubes plateadas. Juró que estaba ensayando una ilusión nueva, usando humo denso para crear manos fantasmales.
Sus guantes tenían residuo de humo cristalizado, lo que creó la ilusión de pequeñas grietas en la tela de los muñecos.
Muchos creyeron que los muñecos estaban cortados… pero realmente estaban impregnados de neblina endurecida.""",
        'real': False
    },

    "Rollo Riptide — Hombre Sirena": {
        'desc': "Charcos y humedad.",
        'pista': """Rollo ingresó al taller empapado, dejando charcos en el piso. Los peluches mojados parecían rotos, como si hubieran sido agujereados… pero la tela rasgada resultó ser daño por humedad.
Además, su cola estorbaba entre mesas angostas; imposible manipular una espada larga con esa movilidad reducida.""",
        'real': False
    },

    "Gargant Grimm — Gárgola de Piedra": {
        'desc': "Fuerza bruta.",
        'pista': """Cuando Grimm entró al taller, su peso hizo crujir el piso. Algunos muñecos mostraban desgarros gruesos en algodón y costura, parecidos a arañazos de piedra.
Sin embargo, examinamos fibras al microscopio:
—las marcas eran irregulares, dentadas, y sin borde caliente.
Esto sugiere fuerza bruta, NO filo perfecto.""",
        'real': False
    },

    "Cipher Claw — Hombre Sombra Hacker": {
        'desc': "Cables abiertos por cortocircuito.",
        'pista': """Cipher revisaba sensores de movimiento del taller. Varios cables estaban abiertos con bordes netos; parecía corte limpio… hasta que analizamos residuos:
—eran quemaduras eléctricas originadas por cortocircuitos.
Nada que ver con filo.
Sus herramientas dejan olor a plástico derretido, no a tela quemada por magia.""",
        'real': False
    },

    "Jinx Jingler — Payaso Espectral": {
        'desc': "Payaso con funda rasgada y residuo místico.",
        'pista': """Encontramos a Jinx sobre una mesa, rodeado de espadas de utilería y cuchillas retiradas.
Entre sus herramientas estaba una funda rasgada, con fibras quemadas.
Esa rasgadura coincidía exactamente con el patrón de apertura de vaina de una espada samurái.
Además:
• sus guantes tenían residuo de corte térmico místico
• los muñecos cortados presentaban borde liso al ojo humano
• bajo microscopio, hallamos partículas negras con patrón fractal mágico""",
        'real': True
    },
},

        'lugares': {
    "Carpa de Magia y Apariciones": {
        'desc': "Sombras y telas rasgadas por tensión.",
        'pista': """Luces moradas rebotaban contra la cortina, generando sombras extrañas. Encontramos telas rasgadas en un baúl de utilería. Parecían cortes… pero al analizarlos:
• bordes irregulares
• fibras rotas por tensión
• olor a humo, no quemadura mística
Scooby tropezó con un cañón de confeti y salimos cubiertos de brillitos…""",
        'real': False
    },

    "Casa de los Espejos Distorsionados": {
        'desc': "Lona en techo con zig-zag.",
        'pista': """Los espejos reflejaban versiones de nosotros con dedos gigantes, orejas largas y… ugh. Encontramos líneas en zig–zag sobre una lona en el techo.
Parecían cortes, pero resultaron ser rasgaduras por calor de reflectores.
Además, los bordes estaban serpenteados, no rectos.
Scooby vio su reflejo con cola doble y casi se desmaya.""",
        'real': False
    },

    "Lago de Botes Chocones": {
        'desc': "Flotador rasgado y humedad.",
        'pista': """El agua negra absorbía la luz. Encontramos un flotador rasgado, bordes esponjosos y mal cortados.
La humedad había deformado la fibra.
Una alumna juró que vio la espada brillar en el muelle… pero solo era reflejo de luces.
Shaggy metió un dedo en el agua y dijo:
‘¡Fría como finales de semestre!’""",
        'real': False
    },

    "Montaña Rusa “La Serpiente Nocturna”": {
        'desc': "Cortes dentados industriales.",
        'pista': """En una sección baja de la estructura hallamos paneles metálicos con cortes… pero al acercarnos:
• los cortes eran inclinados
• muestra de sierras de mantenimiento
• bordes dentados
Además, había virutas de metal, inexistentes cuando se corta con filo místico.
Scooby tragó una viruta sin querer…""",
        'real': False
    },

    "Taller de Premios y Muñecos": {
        'desc': "Muñecos con fibras selladas por calor mágico.",
        'pista': """El taller parecía sonreírnos. Con luz tenue, vimos varios muñecos abiertos con:
• cortes perfectos como regla
• fibras selladas por calor mágico
• olor a tela quemada sutilmente
Al levantar un oso gigante, sentimos hueco interno anormal.
Dentro:
• algodón térmico chamuscado
• ceniza textil mística
• cavidad del tamaño del Núcleo
Shaggy sacó medio brazo y gritó:
‘¡Bro, hay espacio para otro muñeco AQUÍ!’""",
        'real': True
    },
},

        'objetos': {
    "Lente Fantasmal": {
        'desc': "Estuche con etiqueta ‘MURK’.",
        'pista': """Revisé el proyector portátil que usan para los shows de la carpa. Había un estuche con pequeñas lentes empañadas y, junto a él, una etiqueta de utilería con la palabra ‘MURK’ escrita a mano. 
Un asistente dijo que Madame Murk la quitó de su vestuario la semana pasada mientras recogía accesorios.
La etiqueta de utilería fue hallada junto al estuche, pero no hay firma espectral continua.""",
        'real': False
    },

    "Guante Cuántico Reversor": {
        'desc': "Guante térmico de mantenimiento.",
        'pista': """Examinando las herramientas de mantenimiento en la base de la montaña rusa vimos un guante térmico muy usado.
Un empleado dijo: ‘Vi a Gargant caminando cerca de las vías con algo brillante en la mano ayer’.
Había polvo metálico en una costura, pero solo abrasión mecánica.
No hay pliegue cuántico definido.""",
        'real': False
    },

    "Flauta de Retumbo Cronal": {
        'desc': "Transductor en bocina… en otro sector.",
        'pista': """Desmontamos una bocina y hallamos un pequeño transductor incrustado en su conducto.
Alguien vio a Cipher entrar al área de sonido con una caja de herramientas la noche anterior.
Había diagramas sonoros dentro… pero insuficientes para explicar cortes térmicos del taller.
Aquí no hubo vibración afloja–tornillos.""",
        'real': False
    },

    "Bolsa Sin Fondo": {
        'desc': "Bolsa con olor a algas.",
        'pista': """En una caja de atrezzo apareció una bolsa negra con costura extraña.
Un empleado dijo que Rollo la usó para llevar utilería al muelle.
Había olor a algas en la costura.
Pero aquí no desaparecieron piezas: hubo cortes cauterizados, no vacío instantáneo.""",
        'real': False
    },

    "Espada Samurai Maldita": {
        'desc': "Filo místico que cauteriza.",
        'pista': """Cuando inspeccionamos los muñecos abiertos, los bordes tenían corte térmico: fibra sellada, sin rebabas, con micropartículas negras adheridas en la línea de corte.
Bajo la funda que Jinx dejó caer hallamos las mismas micropartículas incrustadas en la tela, además de restos de barniz oscuro que coinciden con la pátina de la espada.
Micropartículas negras de corte térmico encontradas en la funda de Jinx coinciden con las partículas del borde del muñeco. (PISTA REAL)""",
        'real': True
    },
},
},
]

PERSONAJES_LISTA = [
    "Madame Murk — Bruja de Humo",
    "Rollo Riptide — Hombre Sirena",
    "Gargant Grimm — Gárgola de Piedra",
    "Cipher Claw — Hombre Sombra Hacker",
    "Jinx Jingler — Payaso Espectral",
]

LUGARES_LISTA = [
    "Carpa de Magia y Apariciones",
    "Casa de los Espejos Distorsionados",
    "Montaña Rusa “La Serpiente Nocturna”",
    "Lago de Botes Chocones",
    "Taller de Premios y Muñecos",
]

OBJETOS_LISTA = [
    "Lente Fantasmal",
    "Guante Cuántico Reversor",
    "Flauta de Retumbo Cronal",
    "Bolsa Sin Fondo",
    "Espada Samurai Maldita",
]

# ============ Lógica de preguntas y juego ============

def mostrar_menu_principal(intentos_restantes):
    hr()
    print(f"Intentos restantes: {intentos_restantes}")
    print("¿Qué quieres preguntar?")
    opciones = ["Personajes", "Lugares", "Objetos", "Acusar ahora"]
    for i, op in enumerate(opciones, 1):
        print(f" {i}) {op}")
    return pedir_opcion("Elige opción (1-4): ", opciones)

def sub_menu_categoria(nombre_cat, opciones_dict):
    subtitulo(f"{nombre_cat} — Elige un ítem para recibir una pista")
    keys = list(opciones_dict.keys())
    for i, k in enumerate(keys, 1):
        desc = opciones_dict[k]['desc']
        print(f" {i}) {k}\n     · {desc}")
    eleccion = pedir_opcion("Selecciona (1-5 o nombre): ", keys)
    pista = opciones_dict[eleccion].get('pista_detallada') or opciones_dict[eleccion]['pista']
    hr()
    print(f"🔎 PISTA sobre {eleccion}:")
    wrap(pista)
    return eleccion

def acusar():
    subtitulo("Acusación Final — ¡Elige la combinación correcta!")
    # Seleccionar personaje
    print("\nSospechosos:")
    for i, p in enumerate(PERSONAJES_LISTA, 1):
        print(f" {i}) {p}")
    sospechoso = pedir_opcion("¿Quién lo robó?: ", PERSONAJES_LISTA)

    # Seleccionar objeto
    print("\nObjetos místicos:")
    for i, o in enumerate(OBJETOS_LISTA, 1):
        print(f" {i}) {o}")
    objeto = pedir_opcion("¿Con qué lo extrajo?: ", OBJETOS_LISTA)

    # Seleccionar lugar
    print("\nLugares del carnaval:")
    for i, l in enumerate(LUGARES_LISTA, 1):
        print(f" {i}) {l}")
    lugar = pedir_opcion("¿Dónde ocultó el Núcleo?: ", LUGARES_LISTA)

    return sospechoso, objeto, lugar

def jugar_un_caso(caso):
    titulo(caso['nombre'])
    wrap(PROBLEMA_GENERAL)
    intentos = 5
    preguntas_realizadas = 0

    while intentos > 0:
        eleccion = mostrar_menu_principal(intentos)
        if eleccion == "Acusar ahora":
            break

        if eleccion == "Personajes":
            sub_menu_categoria("PERSONAJES", caso['personajes'])
            preguntas_realizadas += 1
        elif eleccion == "Lugares":
            sub_menu_categoria("LUGARES", caso['lugares'])
            preguntas_realizadas += 1
        elif eleccion == "Objetos":
            sub_menu_categoria("OBJETOS", caso['objetos'])
            preguntas_realizadas += 1
        else:
            print("Selección no válida.")
            continue

        intentos -= 1
        if intentos > 0:
            esperar_enter()

    # Fase de acusación
    print("\n" + "="*60)
    print("¡Es momento de ACUSAR!")
    print("="*60)
    sospechoso, objeto, lugar = acusar()

    # Veredicto
    correcto = (
        sospechoso == caso['culpable']
        and objeto == caso['objeto_real']
        and lugar == caso['lugar_real']
    )

    hr()
    if correcto:
        print("🎉 ¡ACERTASTE LA COMBINACIÓN CORRECTA!")
        wrap("Explicación: " + caso['explicacion'])
        print("\nScooby-Doo: “Rooo–rooo!” 🐾")
    else:
        print("💀 Combinación incorrecta… el misterio continuará atormentando el Carnaval.")
        print("La respuesta correcta era:")
        print(f" - Culpable: {caso['culpable']}")
        print(f" - Objeto:   {caso['objeto_real']}")
        print(f" - Lugar:    {caso['lugar_real']}")
        print("\n¡Inténtalo de nuevo!")

def main():
    random.seed()  # semilla desde el sistema
    caso = random.choice(CASOS)
    jugar_un_caso(caso)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nJuego interrumpido. ¡Hasta la próxima!")
        sys.exit(0)


# ==== INYECCIÓN DE PISTAS DETALLADAS PARA CASO 5 ====
# Reemplaza/añade pistas detalladas EXACTAS del documento del usuario.

def _inyectar_pistas_detalladas_caso5(CASOS):
    caso5 = CASOS[4]  # índice 4
    # PERSONAJES
    caso5['personajes']["Madame Murk — Bruja de Humo"]['pista_detallada'] = (
        "“Murk caminaba entre hilos y retazos, dejando pequeñas nubes plateadas. Juró que estaba "
        "ensayando una ilusión nueva, usando humo denso para crear manos fantasmales.\n"
        "Sus guantes tenían residuo de humo cristalizado, lo que creó la ilusión de pequeñas grietas en la tela de los muñecos.\n"
        "Muchos creyeron que los muñecos estaban cortados… pero realmente estaban impregnados de neblina endurecida.”\n"
        "Pista: Telas rígidas y crujientes (por humo endurecido)."
    )
    caso5['personajes']["Rollo Riptide — Hombre Sirena"]['pista_detallada'] = (
        "“Rollo ingresó al taller empapado, dejando charcos en el piso. Los peluches mojados parecían rotos, "
        "como si hubieran sido agujereados… pero la tela rasgada resultó ser daño por humedad.\n"
        "Además, su cola estorbaba entre mesas angostas; imposible manipular una espada larga con esa movilidad reducida.”\n"
        "Pista: Telas abiertas por tensión húmeda."
    )
    caso5['personajes']["Gargant Grimm — Gárgola de Piedra"]['pista_detallada'] = (
        "“Cuando Grimm entró al taller, su peso hizo crujir el piso. Algunos muñecos mostraban desgarros gruesos en algodón y "
        "costura, parecidos a arañazos de piedra.\n"
        "Sin embargo, examinamos fibras al microscopio: las marcas eran irregulares, dentadas, y sin borde caliente.\n"
        "Esto sugiere fuerza bruta, NO filo perfecto.”\n"
        "Pista: Huellas de fuerza pétrea en tela."
    )
    caso5['personajes']["Cipher Claw — Hombre Sombra Hacker"]['pista_detallada'] = (
        "“Cipher revisaba sensores de movimiento del taller. Varios cables estaban abiertos con bordes netos; parecía corte limpio… "
        "hasta que analizamos residuos: eran quemaduras eléctricas originadas por cortocircuitos.\n"
        "Nada que ver con filo. Sus herramientas dejan olor a plástico derretido, no a tela quemada por magia.”\n"
        "Pista: Bordes quemados por descargas eléctricas."
    )
    caso5['personajes']["Jinx Jingler — Payaso Espectral"]['pista_detallada'] = (
        "“Encontramos a Jinx sobre una mesa, rodeado de espadas de utilería y cuchillas retiradas. "
        "Entre sus herramientas estaba una funda rasgada, con fibras quemadas. "
        "Esa rasgadura coincidía exactamente con el patrón de apertura de vaina de una espada samurái.\n"
        "Además: sus guantes tenían residuo de corte térmico místico; los muñecos cortados presentaban borde liso al ojo humano; "
        "bajo microscopio, hallamos partículas negras con patrón fractal mágico.”"
    )

    # LUGARES
    caso5['lugares']["Carpa de Magia y Apariciones"]['pista_detallada'] = (
        "“Luces moradas rebotaban contra la cortina, generando sombras extrañas. "
        "Encontramos telas rasgadas en un baúl de utilería. Parecían cortes… pero al analizarlos: "
        "bordes irregulares, fibras rotas por tensión y olor a humo, no quemadura mística.”"
    )
    caso5['lugares']["Casa de los Espejos Distorsionados"]['pista_detallada'] = (
        "“Los espejos reflejaban versiones de nosotros con dedos gigantes, orejas largas y… ugh. "
        "Encontramos líneas en zig–zag sobre una lona en el techo. Parecían cortes, pero resultaron ser "
        "rasgaduras por calor de reflectores. Además, los bordes estaban serpenteados, no rectos.”"
    )
    caso5['lugares']["Lago de Botes Chocones"]['pista_detallada'] = (
        "“El agua negra absorbía la luz. Encontramos un flotador rasgado, bordes esponjosos y mal cortados. "
        "La humedad había deformado la fibra. Una alumna juró que vio la espada brillar en el muelle… "
        "pero solo era reflejo de luces.”"
    )
    caso5['lugares']["Montaña Rusa “La Serpiente Nocturna”"]['pista_detallada'] = (
        "“En una sección baja de la estructura hallamos paneles metálicos con cortes… pero al acercarnos: "
        "los cortes eran inclinados, muestra de sierras de mantenimiento, con bordes dentados. "
        "Además, había virutas de metal, inexistentes cuando se corta con filo místico.”"
    )
    caso5['lugares']["Taller de Premios y Muñecos"]['pista_detallada'] = (
        "“El taller parecía sonreírnos. Con luz tenue, vimos varios muñecos abiertos con cortes perfectos como regla, "
        "fibras selladas por calor mágico y olor a tela quemada sutilmente. "
        "Al levantar un oso gigante, sentimos hueco interno anormal… cavidad del tamaño del Núcleo.”"
    )

    # OBJETOS
    caso5['objetos']["Lente Fantasmal"]['pista_detallada'] = (
        "“Revisé el proyector portátil que usan para los shows de la carpa. Había un estuche con pequeñas lentes empañadas "
        "y, junto a él, una etiqueta de utilería con la palabra ‘MURK’ escrita a mano. "
        "Un asistente dijo que la etiqueta la quitó Madame Murk la semana pasada mientras recogía vestuario.”"
    )
    caso5['objetos']["Guante Cuántico Reversor"]['pista_detallada'] = (
        "“Examinando las herramientas de mantenimiento en la base de la montaña rusa vimos un guante térmico muy usado. "
        "Un señor dijo: ‘Vi a Gargant caminando cerca de las vías con algo brillante en la mano ayer’. "
        "Había un poco de polvo metálico en una costura del guante.”"
    )
    caso5['objetos']["Flauta de Retumbo Cronal"]['pista_detallada'] = (
        "“Desmontamos una bocina y hallamos un pequeño transductor incrustado en su conducto. "
        "Alguien recordó ver a Cipher entrar a la sala de sonido con una caja de herramientas la noche anterior. "
        "En la funda de la caja había restos de una nota con diagramas sonoros.”"
    )
    caso5['objetos']["Bolsa Sin Fondo"]['pista_detallada'] = (
        "“Removimos cajas y cofres de utilería: en una caja de atrezzo apareció una bolsa de tela negra con costura extraña. "
        "Un empleado dijo que Rollo la había usado para llevar props al muelle algunas noches. "
        "Había olor a algas en la costura.”"
    )
    caso5['objetos']["Espada Samurai Maldita"]['pista_detallada'] = (
        "“Cuando inspeccionamos los muñecos abiertos, noté que los bordes tenían corte térmico: "
        "la fibra estaba sellada, sin rebabas, con micro-partículas negras adheridas en la línea de corte —como si un filo místico "
        "hubiera cauterizado la tela. Bajo la funda que Jinx dejó caer en una esquina del taller hallamos exactamente esas mismas "
        "micro-partículas incrustadas en la tela de la funda y restos de barniz oscuro que coinciden con la pátina de la espada "
        "samurái de utilería.”"
    )

_inyectar_pistas_detalladas_caso5(CASOS)
# ==== FIN INYECCIÓN ====\n
