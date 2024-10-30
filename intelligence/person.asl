/* Initial beliefs */
status(asleep).  /* The person starts asleep */
!start.

/* Initial event */
+!start <-
    .print("The person becomes active..."); 
    .wait(1000); 
    !manage_state. 


/* Rule to sleep */
+!sleep :  
    not status(asleep)  
    <-  
        .print("The person is falling asleep.");  
        +status(asleep). 

/* Rule to wake up */
+!wake_up :  
    status(asleep)  
    <-  
        .print("The person is waking up.");  
        -status(asleep). 

/* Plan to manage the state */
+!manage_state :  
    status(asleep)  
    <-  
        .print("The person is asleep. Executing wake up plan.");  
        !wake_up. 

+!manage_state :  
    not status(asleep)  
    <-  
        .print("The person is awake. Executing sleep plan.");  
        !sleep. 


+!get_data <-
    .get_data("", X); 
    .print("The simulated data is : ", X); 
    .wait(1000); 

    .send(wearable, askHow, "+!receive_data(M)");
    .wait(2000); 
    !receive_data(X)[source(wearable)]; 
    .print("Person finishes sending the message"). 

+!sleep_command(Msg)[source(Sender)] <-
    .print("Got a message from : ", Sender, " saying : ", Msg);
    .send(person, tellHow, "+!call_person(M) <- .print(\"Message received by the person :\", M); !sleep_goal(M).");
    .wait(2000); 
    .send(person, achieve, call_person(Msg)). 

+!sleep_goal(Msg) : true  
    <-
    !manage_state. 

+!bye <-
    .print("Goodbye from Person").