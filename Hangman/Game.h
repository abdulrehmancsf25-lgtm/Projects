#pragma once
#include"Hangman.h"
#include"ConsoleFunctions.h"
class Game {
	Hangman hangman;
	ConsoleFunctions cfunc;
	int tries;
	char* wordList[50];
	char* secretWord;
	int  letterCheck[26]; // 0 deafult -1 for wrong and 1 for correct

	// Member functions
	void reset_game_elements();
	bool reStart();
	int StrLen(char*);
	void display();
	bool isWin();
	void takeInput();
	void  selectWord();
	bool isGameOver();
	bool verifyCharacter(char);
	
public:
	Game();
	void startGame();
	~Game();
};