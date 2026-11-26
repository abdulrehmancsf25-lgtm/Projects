#include<iostream>
#include"Hangman.h"
#include"ConsoleFunctions.h"
using namespace std;

ConsoleFunctions cfunc;

Hangman::Hangman() {
	x = y = stage = 0;
}

Hangman::Hangman(int x, int y) {
	stage = 0;
	this->x = x;
	this->y = y;
}

void Hangman::draw() {

	cfunc.SetCursorAt(x, y);
  // first set cursot at console
	cout << "+---+";

	cfunc.SetCursorAt(x , y+1);
	cout << "|   ";
	if (this->stage > 0)
		cout << "|";
	else
		cout << " ";

	cfunc.SetCursorAt(x , y+2);
	cout << "|   ";
	if (this->stage > 1)
		cout << "O";
	else
		cout << " ";

	cfunc.SetCursorAt(x , y+3);
	cout << "|  ";
	if (this->stage > 2)
		cout << "/";
	else
		cout << " ";
	if (this->stage > 3)
		cout << "|";
	else
		cout << " ";
	if (this->stage > 4)
		cout << "\\";
	else
		cout << " ";

	cfunc.SetCursorAt(x , y+4);
	cout << "|  ";
	if (this->stage > 5)
		cout << "/ ";
	else
		cout << " ";
	if (this->stage > 6)
		cout << "\\";
	else
		cout << "  ";

	cfunc.SetCursorAt(x , y+5);
	cout << "|";
	cfunc.SetCursorAt(x , y+6);
	cout << "=======";
}

// Hangman.cpp
void Hangman::nextStage() { if (stage < 7) stage++; }
void Hangman::resetStage() { stage = 0; }
const int& Hangman::getStage() const {
	return this->stage;
}

Hangman::~Hangman(){}
