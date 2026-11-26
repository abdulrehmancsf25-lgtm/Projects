#include"Game.h"
#include"ConsoleFunctions.h"
#include<iostream>
#include<fstream>
#include<ctime>
#include<cstdlib>
using namespace std;

Game::Game():hangman(40, 7) { // Ctor

	for (int i = 0; i < 26; i++) {
		letterCheck[i] = 0;
	}

	this->tries = 0;  // tries are 0 at first 
	ifstream read("Words.txt");
	if (!read.is_open()) {
		cout << "File loading error!" << endl;
		return;
	}
	for (int i = 0; i < 50; i++) { // loading words  in wordList
		char buffer[15];
		read >> buffer; 
		int len = this->StrLen(buffer);
		this->wordList[i] = new char[len + 1];
		int j = 0;
		for (; j < len; j++)
			wordList[i][j] = buffer[j];
		wordList[i][len] = '\0';
	}
}

int Game::StrLen(char* buffer) { // To check lenght of words
	int len = 0;
	for (int i = 0; i < 15 && buffer[i] != '\0'; i++) {
		len++;
	}
	return len;
}
Game::~Game(){  // Dtor
	for (int i = 0; i < 50; i++)
		delete[] this->wordList[i];
}
void Game::selectWord() { // random word selection 
	srand(time(0));
	int min = 0;
	int max = 49;
	int index = min + rand() % (max - min + 1);
	this->secretWord = this->wordList[index];
}
bool Game::verifyCharacter(char ch) {
	bool isPresent = false;
	if (ch > 96 && ch < 123) //converting to upper case
		ch = char(ch - 32);

	for (int i = 0; i < StrLen(this->secretWord); i++) {
		if (ch == secretWord[i]) {
			letterCheck[ch - 'A'] = 1;
			isPresent = true;
		}
	}
	if (!isPresent) {
		letterCheck[ch - 'A'] = -1;
	}
	return isPresent;
}
void Game::takeInput() { // taking input
	char ch;
	cin >> ch;  // character input 

	if (!verifyCharacter(ch)) {
		tries++; 
		hangman.nextStage();
	}
}
void Game::startGame() { // start game function
	selectWord();
	while (true) {
		display();
		if (isWin()) { 
			cfunc.SetCursorAt(0, 16); cout << "YOU WON!" << endl;
		if (this->reStart()) {
			cfunc.clearConsole();
			this->reset_game_elements();
			this->selectWord();
			continue;
		}
		else
		  return; 
		}
		if (isGameOver()) {
			cfunc.SetCursorAt(0, 16);
			cout << "Game Over! (You Lose)\nThe secret word was: " << secretWord << endl;
			if (this->reStart()) {
				cfunc.clearConsole();
				this->reset_game_elements();
				this->selectWord();
				continue;
			}
			else
				return;
		}
		cfunc.SetCursorAt(0, 14);
		cout << "Next guess please? ";
		takeInput();
	}
}
bool Game:: reStart() { // asking user to restart or not
	char ch;
	cout << "Press R to restart game" << endl;
	cin >> ch;
	return (ch == 'R' || ch == 'r');
}
void Game::reset_game_elements() { // resetting data members

	for (int i = 0; i < 26; i++) {
		this->letterCheck[i] = 0;
	}
    this->tries = 0; 
	this->hangman = Hangman(40, 7);
	cfunc = ConsoleFunctions();

}
void Game::display() { // displaying all game main page
	cfunc.clearConsole();
	cfunc.SetColor(white, black);

	cfunc.SetCursorAt(0, 0);
	cout << "The Hangman Game";
	cfunc.SetCursorAt(0, 2);
	cout << "Welcome to Hangman! I have selected a secret word, and your goal is to guess it\n"
		"letter by letter before you run out of lives.";

	cfunc.SetCursorAt(0, 5);
	for (int i = 0; i < 26; i++) {
		if (letterCheck[i] == 1)
			cfunc.SetColor(green, black);
		else if (letterCheck[i] == -1) 
			cfunc.SetColor(red, black);
		cout << char('A' + i);
		cfunc.SetColor(white, black);
		cout << ' ';
		if (i == 12) 
			cfunc.SetCursorAt(0, 6);
	}

	cfunc.SetCursorAt(0, 8);
	cout << "Secret Word:";
	cfunc.SetCursorAt(0, 9);
	int len = StrLen(secretWord);
	for (int i = 0; i < len; i++)
		cout << (letterCheck[secretWord[i] - 'A'] == 1 ? secretWord[i] : '_') << ' ';
	cout << "(" << len << " letters)";

	cfunc.SetCursorAt(0, 11);
	cout << "Incorrect Guesses: ";
	if (tries == 0) cout << "None";
	else for (int i = 0; i < 26; i++)
		if (letterCheck[i] == -1) 
			cout << char('A' + i) << ' ';

	cfunc.SetCursorAt(0, 12);
	cout << "Lives Left: " << 7 - tries;

	hangman.draw();
}

bool Game::isGameOver() { 
	return tries == 7;
}
bool Game::isWin() {
	for (int i = 0; i < StrLen(secretWord); i++) {
		if (!(letterCheck[secretWord[i] - 65] == 1))
			return false;
	   }
	return true;
}