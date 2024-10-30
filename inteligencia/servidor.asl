/* Creencias iniciales */
calidad(9).  /* El servidor asume que la persona tiene una calidad de sueno alta */
!start.

+!start <-
    .print("El servidor esta esperando por el plan desde wearable...").


+!receptor_datos(Msg)[source(Sender)] <-
  .print("Obtuvo el mensaje desde el : ", Sender, " diciendo : ", Msg);
  .send(servidor,tellHow, "+!call_server(M) <- .print(\"Mensaje recibido por el servidor :\", M); !some_goal(M).");
  .wait(2000);
  .send(servidor, achieve, call_server(Msg)).


+!bye <-
    .print("Bye by Server").

+!some_goal(Msg) : true
    <-  
    .hacer_prediccion(Msg,X);
    .print("La calidad de sueno alcanzada es :",X);
    !update_calidad(X);
    !verify_quality.

+!update_calidad(NewQuality)
    : calidad(CurrentQuality)  /* Verifica que ya haya un valor */
<- -calidad(CurrentQuality);   /* Elimina la creencia anterior */
   +calidad(NewQuality).       /* Agrega la nueva creencia */

+!verify_quality
    : calidad(T) & T < 6
    <- .print("Creo que necesitas al medico virtual para mejorar tus habitos para dormir mejor");
    .send(medico_virtual,askHow, "+!contacta_medico(M)");
    .wait(2000);
    !contacta_medico(T)[source(medico_virtual)].

+!verify_quality
    : calidad(T) & T > 5
    <- .print("Continua con tu vida normal tienes buenos habitos para dormir").
