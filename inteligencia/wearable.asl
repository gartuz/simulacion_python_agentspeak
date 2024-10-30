!start.

+!start
    <- 
        .print("Wearable Iniciando...");
        .wait(1000);

        .send(persona,tellHow, "+!hello <- .print(\"Hola persona\").");

        .print("Se agrego el plan saludo");
        .wait(1000);

        .print("Objetivo lograr Hello");
        .send(persona,achieve,hello);
        .print("Objetivo Lograr get_data");
        .send(persona,achieve,get_data).
        

+!bye <-
    .print("Adios desde wereable").

+!send_data(Data) <-
  .print("Dato recibido de Wearable :", Data).

+recibir_datos(Valor) <-
    .print("Wearable recibe: = ", Valor).

+!recibir_datos(Msg)[source(Sender)] <-
  .print("obtuvo un mensaje de : ", Sender, " diciendo : ", Msg);
  .send(wearable,tellHow, "+!call_wearable(M) <- .print(\"Mensaje recibido por el wearable :\", M); !send_goal(M).");
  .wait(2000);
  .send(wearable, achieve, call_wearable(Msg)).

+!send_goal(Msg) : true 
  <-
  .send(servidor,askHow, "+!receptor_datos(M)");
  .wait(2000);
  !receptor_datos(Msg)[source(servidor)].