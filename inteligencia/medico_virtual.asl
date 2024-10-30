+!contacta_medico(Msg)[source(Sender)] <-
  .print("obtuvo un mensaje de : ", Sender, " diciendo : ", Msg);
  .send(medico_virtual,tellHow, "+!call_medico(M) <- .print(\"Mensaje recibido por el medico virtual :\", M); !send_instructions(M).");
  .wait(2000);
  .send(medico_virtual, achieve, call_medico(Msg)).

  +!send_instructions(Msg) : true 
    <- 
    .print("Hola soy su medico virtual");
    .print("Estoy aqui para recomendarle mejorar sus habitos para dormir");
    .print("Veo que obtuvo una calificacion de :", Msg);
    .print("CONSEJO: Un consejo fundamental para mejorar la calidad de tu sueño es mantener un horario regular para dormir");
    .print("Persona mi consejo es que vayas a dormir ya");
    .wait(1000);

    .send(persona,askHow, "+!mandato_dormir(M)");
    .wait(2000);
    !mandato_dormir("Ve a dormir")[source(persona)];
    .print("El medico termina de enviar el mensaje para que se duerma la persona").