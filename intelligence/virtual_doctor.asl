+!contact_doctor(Msg)[source(Sender)] <-
    .print("Got a message from : ", Sender, " saying : ", Msg);
    .send(virtual_doctor, tellHow, "+!call_doctor(M) <- .print(\"Message received by the virtual doctor :\", M); !send_instructions(M).");
    .wait(2000); 
    .send(virtual_doctor, achieve, call_doctor(Msg)). 

+!send_instructions(Msg) : true  
    <-  
    .print("Hello, I am your virtual doctor");
    .print("I am here to recommend that you improve your sleep habits");
    .print("I see that you obtained a rating of :", Msg);
    .print("ADVICE: A fundamental tip to improve the quality of your sleep is to maintain a regular sleep schedule");
    .print("Person, my advice is that you go to sleep now");
    .wait(1000);

    .send(person, askHow, "+!sleep_command(M)");
    .wait(2000); 
    !sleep_command("Go to sleep")[source(person)];
    .print("The doctor finishes sending the message for the person to go to sleep").