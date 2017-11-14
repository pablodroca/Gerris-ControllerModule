function act = pid_act(kProp, kInt, velError, velErrorInt)
    act = kProp*velError + kInt*velErrorInt;

