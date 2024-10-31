/* Initial beliefs */
quality(9).  /* The server assumes the person has a high sleep quality */
!start.

/* Initial event */
+!start <-
    .print("The server is waiting for the plan from the wearable..."). 


+!data_receiver(Msg)[source(Sender)] <-
    .print("Got the message from : ", Sender, " saying : ", Msg);
    .send(server, tellHow, "+!call_server(M) <- .print(\"Message received by the server :\", M); !predict_goal(M).");
    .wait(2000); 
    .send(server, achieve, call_server(Msg)). 


+!bye <-
    .print("Bye by Server"). 

+!predict_goal(Msg) : true
    <-  
    .make_prediction(Msg, X);
    .print("The achieved sleep quality is :", X); 
    !update_quality(X); 
    !verify_quality. 

+!update_quality(NewQuality)
    : quality(CurrentQuality)  /* Verify that there is already a value */
    <- -quality(CurrentQuality);   /* Remove the previous belief */
    +quality(NewQuality).        /* Add the new belief */

+!verify_quality
    : quality(T) & T < 6
    <- .print("I think you need the virtual doctor to improve your sleep habits");
    .send(virtual_doctor, askHow, "+!contact_doctor(M)");
    .wait(2000); 
    !contact_doctor(T)[source(virtual_doctor)]. 

+!verify_quality
    : quality(T) & T > 5
    <- .print("Continue with your normal life, you have good sleep habits").
