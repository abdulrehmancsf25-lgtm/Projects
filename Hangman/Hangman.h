#pragma once
#include "ConsoleFunctions.h"
class Hangman {
    int x, y, stage;
    ConsoleFunctions cfunc;
public:
    Hangman();
    Hangman(int x, int y);
    void nextStage();  
    void draw();   
    void resetStage();
    const int& getStage() const;
    ~Hangman();
};