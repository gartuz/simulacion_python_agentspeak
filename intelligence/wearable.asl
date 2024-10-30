/* Initial event */
!start.
+!start 
    <-  
        .print("Wearable Starting...");  
        .wait(1000);

        .send(person, tellHow, "+!hello <- .print(\"Hello person\").");

        .print("Greeting plan added");  
        .wait(1000);

        .print("Goal: achieve Hello");  
        .send(person, achieve, hello);
        .print("Goal: achieve get_data");  
        .send(person, achieve, get_data).  


+!bye <-
    .print("Goodbye from wearable"). 

+!send_data(Data) <-
    .print("Data received from Wearable :", Data). 

+receive_data(Value) <-
    .print("Wearable receives: = ", Value). 

+!receive_data(Msg)[source(Sender)] <-
    .print("Got a message from : ", Sender, " saying : ", Msg);
    .send(wearable, tellHow, "+!call_wearable(M) <- .print(\"Message received by the wearable :\", M); !send_goal(M).");
    .wait(2000); 
    .send(wearable, achieve, call_wearable(Msg)). 

+!send_goal(Msg) : true  
    <-
    .send(server, askHow, "+!data_receiver(M)");
    .wait(2000); 
    !data_receiver(Msg)[source(server)].