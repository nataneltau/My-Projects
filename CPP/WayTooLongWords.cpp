#include <iostream>
#include <string>

using namespace std;

//help with string concatenation: https://stackoverflow.com/questions/191757/how-to-concatenate-a-stdstring-and-an-int


/**
 * @brief This function get a word that is at least 11 letters length, we save the first
 *          and last letters, then calculate how many letters are between them, then return
 *          a string as asked in the question
 * 
 * @param longWord - Word that is at least 11 letters length (>10)
 * 
 * @return string that is contain the first and last
 *      letters and between and number of letters as wanted
 */
string fixLongWord(string longWord){

    string notLongWord;
    int numberOfLetters;

    numberOfLetters = longWord.length() -2;//we count the words letter not including the 
    //first and last letter, so its the word length - 2

    notLongWord = longWord[0] + to_string(numberOfLetters) + longWord[numberOfLetters+1];
    //numberOfLetters+1 is longWord.length() -1 and its access to the last letter, and that way 
    //we don't call length() function, its more cheaper in run time aspect

    return notLongWord;


}//end of fixLongWord


int main(){
    int n;
    string word;

    cin >> n;

    while(n--){//iterate n times
        cin >>word;

        if(word.length() > 10){//if the word is too long we fix it
            word = fixLongWord(word);
        }

        //now we have not a long word whether we enter the if block or not
        cout << word << endl;//print the word and make a new line

    }//end of while

}//end of main