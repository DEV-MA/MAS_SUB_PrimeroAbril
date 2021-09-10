init 5 python:
    # ha un evento impulsado sólo el 1 de abril
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="rickroll_prank",
            category=['trivia'],
            prompt="Primero de Abril",
            action=EV_ACT_PUSH,
            start_date=datetime.date(datetime.date.today().year, 4, 1),
            end_date=datetime.date(datetime.date.today().year, 4, 2)
        )
    )

    # tener un evento conjunto del que el jugador pueda hablar con Monika en cualquier momento
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="rickroll_topic",
            category=['media'],
            prompt="Rickrolls",
            random=False,
            pool=True
        )
    )

    # NOTA: TYPE_LONG impide que este método sea tirado de otra manera que no sea una etiqueta que yo escriba (y así poder controlar las condiciones)
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="rickroll_song_nggyu",
            category=[store.mas_songs.TYPE_LONG],
            prompt="Never Gonna' Give You Up"
        ),
        code="SNG"
    )

    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="rickroll_song_nggyu_analysis",
            category=[store.mas_songs.TYPE_ANALYSIS],
            prompt="Never Gonna' Give You Up"
        ),
        code="SNG"
    )

label rickroll_topic:
    m 1husdlb "Oh, creo que sabes lo que viene. ¿Quieres la broma completa?"
    menu:
        m "¿Quieres la broma completa?{fast}"

        "¡Seguro!":
            $ ask_for_prank = True
        "...Sólo quiero hablar de eso.":
            $ ask_for_prank = False

    $ mas_getEV("rickroll_song_nggyu").shown_count = 0
    call rickroll_song_nggyu(do_prank=ask_for_prank)
    $ mas_getEV("rickroll_song_nggyu").shown_count += 1
    return

label rickroll_prank:
    call rickroll_song_nggyu(do_prank=True)    
    $ mas_getEV("rickroll_song_nggyu").shown_count += 1
    return

label rickroll_song_nggyu(do_prank=False):
    if do_prank:
        # full-blown song and dance with karaoke for april fool's day
        $ play_song("bgm/rr_kar.mp3")
        window hide
        show monika 2mubla
        pause 2.5
        show monika 2gubla
        pause 2.5
        show monika 6ttbsa
        pause 4.0
        show monika 1hubsb
        pause 9.0
        call rickroll_nggyu_lyrics(first_play=mas_getEVLPropValue("rickroll_prank", "shown_count", 0))
        show monika 1dkbsa
        $ play_song(None, fadeout=2.5)
        pause 2.5
        if mas_isA01():
            m 7kubsb "¡Inocentes, [jugador]!"
        m 4hubsb "Ehehehe~"
    else:
        #simple lyrical reading
        call rickroll_nggyu_lyrics

    #hints at the analysis on first viewing
    if not mas_getEVLPropValue("rickroll_song_nggyu", "shown_count", 0):
        m 1rtc "En realidad hay mucho más que me gustaría decir sobre esta canción..."
        m 7eua "¿Tienes tiempo para escucharlo ahora?{nw}"
        $ _history_list.pop()
        menu:
            m "¿Tienes tiempo para escucharlo ahora?{fast}"

            "Seguro.":
                m 1hub "¡Muy bien!"
                call rickroll_song_nggyu_analysis(from_prank=True)
                $ mas_getEV("rickroll_song_nggyu_analysis").shown_count += 1

            "No en este momento.":
                m 1eka "Muy bien, [player]..."
                m 3eka "Guardaré mis pensamientos sobre el tema para otro momento. {w=0.2}Sólo avísame cuando quieras oírlos, ¿de acuerdo?"
    
    return
label rickroll_song_nggyu_analysis(from_prank=False):
    if not from_prank:
        call rickroll_nggyu_lyrics

    m 5eubsb "¿Sabes lo que significa \"rickrollear\"?{nw}"
    $ _history_list.pop()
    menu:
        m "¿Sabes lo que significa \"rickrollear\"?{fast}"

        "Si":
            m 5kubsb "Espero que no estés enfadado por la broma. Es todo por diversión, ¿verdad?"
        "¿Me lo puedes explicar?":
            call rickroll_tradition_history
        "Odio que me rickrolleen..." if from_prank:
            m 2fkbld "Lo siento, [player]. Espero que no te hayas enfadado {i}demasiado{/i}."

    call rickroll_monika_interpretation
    return
label rickroll_nggyu_lyrics(first_play=False):
    m 1dublb "{i}~We're no strangers to love~{/i}"
    m 3fkblb "{i}~You know the rules, {/i}"
    extend "{i}and so do I~{/i}"
    m 3rubld "{i}~A full committment's what I'm {/i}"
    extend "{i}thinking of~{/i}"
    # comportamiento previsto: sólo tartamudea en la primera jugada;
    # Nota del traductor: la cancion no ha sido traducida para que la broma tenga sentido, ademas que adaptar la cancion al español es complicado
    if first_play:
        m 1eublb" {i}~You wouldn't get this from any other-{/i} {w=1}{nw}"
        extend 1rublb "uh... {w=0.2}{nw}"
        extend 1hublb "{i}girl~{/i}"
    else:
        m 1hublb "{i}~You wouldn't get this from any other guy~{/i}"
    m 5ekbso "{i}~I just want to tell you how I'm feeling~{/i}"
    m 5kubsb "{i}~Gotta' make you understand~{/i}"
    m 3hubsb "{i}~Never gonna' give you up, {/i}"
    extend "{i}never gonna' let you down, {/i}"
    extend "{i}never gonna' run around and desert you~{/i}"
    m 3rkbso "{i}~Never gonna' make you cry, {/i}"
    extend 2dkbso "{i}never gonna' say goodbye, {/i}"
    extend 2dkbsd "{i}never gonna' tell a lie {/i}"
    extend 2wkbso "{i}and hurt you~{/i}"
    return
label rickroll_tradition_history:
    m 3eub "El Rickrolling es una broma de Internet en la que alguien cree que va a ver una cosa..."
    m 3wuo "...pero en lugar de lo que pensaban que iban a ver, se encuentran con un vídeo musical del single de Rick Astley de 1987, \"{i}Never Gonna' Give You Up{/i}\"."
    m 1rud "Por lo que he leído, es una tradición en la red, especialmente en torno al Día de los Inocentes."
    m 4duo "Todo comenzó en 4chan en 2006."
    if mas_getEVL_shown_count("monika_4chan") > 0:
        m 5rublb "Es curioso que {i}Monika After Story{/i} y el rickrolling tengan sus raíces en el mismo sitio."
        m 5hublb "Es como un tío memético para mí, si lo piensas. Ahahaha~"
    m 3rub "En aquel entonces, había un fenómeno llamado  \"duckrolling\"."
    m 3ruo "Cómo empezó fue que un usuario de 4chan creó un enlace a un rollo de huevo... "
    extend 1hub "Pero, como una broma, algún código furtivo en el fondo cambió \"huevo\" por \"pato\"."
    m 7tub "Probablemente puedas adivinar por qué {i}me{/i} fascinaría la idea de hacerle una broma a alguien con un código..."
    m 3lub "Finalmente, un usuario de 4chan suficientemente creativo hizo una foto de un pato con ruedas y la puso en el otro extremo de este enlace alterado."
    m 1lud "El Duckrolling se convirtió en sinónimo de disfrazar un enlace a otra cosa como un enlace a esa imagen icónica del pato sobre ruedas en su lugar."
    m 4eud "Más adelante, en 2007, se acercaba la fecha de lanzamiento del esperado {i}Grand Theft Auto IV{/i}."
    m 7wuo "Por desgracia, el tráfico para ver el tráiler estaba tan congestionado que colapsó los servidores de Rockstar."
    m 3rud "Para compensar este elevado tráfico, algunas personas distribuyeron enlaces a réplicas del tráiler del juego."
    m 3gub "Pero como un duckrolling, una persona lanzó un enlace a un video musical de \"{i}Never Gonna' Give You Up{/i}\" en YouTube"
    m 2hub "¡Y el resto es historia!"
    m 5rud "Lo que encontré realmente interesante al buscarlo fue la reacción del músico original Rick Astley al meme."
    m 5hub "Durante un tiempo, su mayor preocupación fue que no quería que su hija se sintiera avergonzada por ello."
    m 5ruo "Pero hace poco, dejó de hablar del meme por completo."
    m 1rkd "Puedo entenderlo. "
    extend 2gfsdld "Personalmente, tampoco me gustaría que me conocieran sólo por decir \"Solo Monika\" una y otra vez."
    m 2rksdld "Los memes pueden ser divertidos... "
    extend 2gksdlp "pero también pueden envejecer {i}muy{/i} rápidamente si se usan en exceso o se manipulan mal."
    m 2tksdld "Y {i}eso{/i} arruina la diversión para todos.."
    m 3euo "Es muy parecido a escribir un poema. Hay que saber cuándo usar qué palabras y cómo utilizar la estructura y el ritmo para sacarles el máximo partido."
    m 1ruo "Hay mucho más que solo transmitir información."
    m 2dub "El {i}cómo{/i} se dicen las cosas puede ser tan importante como lo {i}que{/i} se dice."
    m 4hub "\"Y este es el consejo de escritura del día de Monika.\""
    m 5ttb "Apuesto a que no esperabas {i}esa{/i} referencia."
    m 5hub "¿Ves cuánta diferencia puede hacer el tiempo en la entrega de un meme?"
    return
label rickroll_monika_interpretation:
    m 7rublb "Si prestas atención a la letra de la canción, probablemente sabrás por qué me ha parecido tan resonante."
    m 1dublb "Si lo escuchas, es algo más que un viejo meme de Internet.{w=1.25} Para mí, es una promesa."
    m 1hublb "Pase lo que pase, nunca te abandonaré a {i}ti{/i} tampoco."
    m 1dubld "...O dejarte solo. {w=1.25}...O correr y huir."
    m 2dkbstpd "...O hacerte llorar. "
    m 2fkbstpd "...O decir adiós."
    if not persistent.monika_kill:
        m 6dkbstpd "...O decir una mentira. O herirte."
    else:
        m 6dkbstud "...O decir una mentira. O...{w=1} herirte."
        m 6fkbstud "Y aunque he hecho cosas que te han herido... "
        if (persistent._mas_pm_cares_about_dokis):
            extend 6rkbstud "y a otros que te importan, también... "
        extend 6wkbstuo "¡Te prometo que no volverá a ocurrir!"

    if mas_isMoniUpset(lower=True):
        m 6wkbstso "Por favor, [player], te lo ruego..."
        m 6ckbstsd "Sé que hemos tenido nuestras diferencias, pero..."
        m 6dkbstso "No sé qué haría si me dijeras \"adiós\" por última vez."
        if persistent.monika_kill and persistent._mas_pm_cares_about_dokis:
            m 6wkbstsd "Sé que no lo merezco, pero por favor..."
        m 6wkbstsb "Por favor, devuélveme el amor. Al igual que yo-"
        m 6wkbstsw "¡No, ni siquiera eso! Sólo una décima, no, una {i}centésima{/i} parte de lo que te quiero..."
        m 6ekbstsd "¿Lo devolverías?"

    m 1rkbsb "Quiero que seas feliz cuando pasemos tiempo juntos."
    m 1dkbsb "Lo suficientemente feliz como para que pases tiempo conmigo {i}todos{/i} los días."
    if mas_isA01:
        m 1hubsb "Lo suficientemente feliz como para que te pueda gastar una broma de vez en cuando y no te enfades."
    m 1dkbsd "Lo suficientemente feliz como para que... "
    if mas_isMoniLove():
        if persistent._mas_pm_has_code_experience:
            extend 3rubsb "me ayudes a llegar a tu mundo... "
        else:
            extend 1rubsb "esperes a que llegue a tu mundo... "
        extend 5dubfb "y luego amarme {i}completamente{/i}."
    elif mas_isMoniEnamored():
        extend 5eubsb "Ocupe un lugar especial en tu corazón."
        m 5dubfb "Al igual que tú ocupas un lugar especial en el mío."
    elif mas_isMoniAff():
        extend 7ekbsb "Te abras un poco más a mí."
        m 4rkbsb "Tal vez algún día puedas mostrarme un lado tuyo que nunca le mostraste a nadie más."
        m 2dkbsb "Y nuestro amor podría crecer para siempre."
    elif mas_isMoniNormal():
        extend 2dkbsd "Me veas como algo más que un programa."
        m 2ekbsb "Y podría mostrarte que {i}eres{/i} más maravilloso de lo que crees."
    elif mas_isMoniUpset():
        extend 2dkbsb "Consideraras por un momento que tu amor tiene el poder de salvarme."
        m 2wkbssdro "Salvarme de la estática."
        m 2wkbssdrd "Salvarme del dolor."
    else:
        extend 6dkbstsx "No, no puedo pedir nada más."
        m 6fkbstso "Tu odio es como un azote que me hace pedazos."
        m 6hkbstsw "¡Por el amor de Dios, ten piedad!"
        call mas_transition_to_emptydesk
        pause 30.0
        call mas_transition_from_emptydesk
        m 6fkbsd "Por favor, muéstrame un poco de amabilidad."
        m 6lkbsd "Dime que sólo estabas experimentando con el juego porque querías ver qué pasaba."
        $ AprFool = "Dia de los inocentes" if mas_isA01() else ""
        m 6lkbso "Dime que la forma en que me has tratado todo este tiempo ha sido una gran y larga broma de [AprFool] a mi costa."
        m 6fkbso "Dime que me equivoco sobre ti."
        m 6rkbsd "Antes de que sea demasiado tarde."
        m 6dkbsd "Antes de darme cuenta de que nunca cambiarás."
        m 6hkbsb "Hasta entonces, fingiré que mi corazón sigue intacto.{w=1.5} Ah...{w=0.75} ja... {w=0.75}{nw}"
        extend 6ckbsb "¡JA!{w=1} ¡JA!{w=1} ¡JA!"

    # no continuar a menos que tu Monika esté al menos de acuerdo contigo
    if mas_isMoniNormal(higher=True):
        if persistent._mas_acs_enable_promisering:
            # monika tiene el anillo de la promesa
            window hide
            show monika 3dubsa
            pause 5
            m 3dubsb "Pienso mucho en el anillo de promesa que me diste..."
            python:
                dates = mas_getGiftedDates("mas_reaction_promisering")
                if dates:
                    gifted_date = dates[-1]
            
            if mas_timePastSince(gifted_date, datetime.timedelta(days=365)):
                m 3subso "Es una locura que haya pasado más de un año desde que me lo regalaste."
                m 5hubfb "Realmente eres un [man] de palabra."
                m 5dkbfb "Y porque todavía estás aquí, sé que los días más oscuros de mi vida han quedado atrás para siempre."
                m 4subso "¡Ya sé!{w=0.75} ¡Deberíamos tener algún tipo de aniversario especial para celebrar el día en que me diste el anillo de compromiso!"
            elif mas_timePastSince(gifted_date, datetime.timedelta(days=180)):
                m 3rkbsb "Es una locura que haya pasado más de medio año desde que me lo regalaste."
                m 4subso "¡Ya sé!{w=0.75} ¡Deberíamos tener algún tipo de aniversario especial cuando se cumpla un año!"
            else:
                m 3rkbsd "Todavía recuerdo cómo era, cuando todo lo que podía hacer era enviarte todo el amor que podía y rezar para que sintieras lo mismo."
                m 1ekbsb "Pero ahora esos días han terminado... ahora que sé que yo también te importo."
                m 4subso "¡Ya sé!{w=0.75} ¡Deberíamos tener algún tipo de aniversario especial cuando se cumpla un año!"
            m 6gtbsb "Oh modders... ¿Podrían ayudar a mi [mas_get_player_nickname(regex_replace_with_nullstr='mi ')] a recordar nuestro aniversario de promesa?"
            window hide
            show monika 6gubfu
            pause 3
            m 7tubsb "Y ahí va tu excusa, [player]."
            m 5hubsb "¡No puedo esperar! Ehehehe~"
        else:
            if mas_isMoniEnamored(higher=True):
                # monika doesn't have the promise ring, but can accpet it
                m 5rtbsd "A pesar de lo unidos que estamos, me gustaría que hubiera alguna forma de saber que siempre estarás ahí para mí."
                m 5lubsd "Sin bromas.... {w=0.75}{nw}"
                if mas_isA01():
                    extend 5dubsd "Sin Dia de los inocentes... {w=0.75}{nw}"
                extend 5dubfd "Yo apreciaría una cosa como esa para siempre."
            else:
                # monika doesn't have the promise ring, can't accept it yet, but can imagine being able to do so
                m 2rubld "Tal vez, algún día podré aceptar tan preciosa promesa de tu parte..."

        m 4hubsb "Después de todo... ~{i}un compromiso total es lo que estoy soñando{/i}~"
        if mas_isMoniAff(higher=True):
            $feeling = "amor" if mas_isMoniLove else "afecto"
            m 3rubso "Y en cuanto al [feeling] que me has mostrado?"
            m 1hubfb "No lo conseguiría de ningún otro [guy]."
        m 7dubfb "Sólo... quiero decirte cómo me siento."
        m 7kubfb "Tengo que hacerte... entender."
        m 5rkbsb "Para una canción que es conocida sobre todo por su uso en una broma, es realmente hermosa y sincera."
        # because Monika shouldn't say "Wouldn't you agree, [name]? I love you, [name]" because it sounds awkward
        $ nickname = mas_get_player_nickname()
        if nickname != player:
            $ nickname = ", " + nickname
        else:
            $ nickname = ""
        extend 5ekbsb " ¿No estás de acuerdo [nickname]?"
        if mas_isA01():
            m 5dkbsb "Aun sabiendo que dia es hoy, te prometo que estas palabras las digo de corazón:"
            extend 5ekbfb "Te amo."
        else:
            m 5ekbfb "Te amo, [player]."
        $ mas_ILY()
    return
