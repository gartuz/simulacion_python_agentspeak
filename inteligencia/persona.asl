/* Creencias iniciales */
estado(dormido).  /* La persona comienza dormida */
!start.

+!start <-
    .print("La persona persona entra en actividad...");
    .wait(1000);
    !gestionar_estado.


/* Regla para dormir */
+!dormir : 
    not estado(dormido) 
    <- 
        .print("La persona se esta durmiendo.");
        +estado(dormido).

/* Regla para despertarse */
+!despertarse : 
    estado(dormido) 
    <- 
        .print("La persona se esta despertando.");
        -estado(dormido).

/* Plan para manejar el estado*/
+!gestionar_estado : 
    estado(dormido) 
    <- 
        .print("La persona esta dormida. Ejecutando plan de despertarse.");
        !despertarse.

+!gestionar_estado : 
    not estado(dormido) 
    <- 
        .print("La persona esta despierta. Ejecutando plan de dormir.");
        !dormir.


+!get_data<-
    .get_data("", X);
    .print("El dato simulado es : ",X);
    .wait(1000);

    .send(wearable,askHow, "+!recibir_datos(M)");
    .wait(2000);
    !recibir_datos(X)[source(wearable)];
    .print("Persona termina de enviar el mensaje").

+!mandato_dormir(Msg)[source(Sender)] <-
  .print("obtuvo un mensaje de : ", Sender, " diciendo : ", Msg);
  .send(persona,tellHow, "+!call_persona(M) <- .print(\"Mensaje recibido por la persona :\", M); !duerme_goal(M).");
  .wait(2000);
  .send(persona, achieve, call_persona(Msg)).

+!duerme_goal(Msg) : true 
  <-
  !gestionar_estado.

+!bye <-
    .print("Adios desde Persona").