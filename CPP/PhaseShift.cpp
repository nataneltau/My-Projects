#include <iostream>
#include <algorithm>
#include <map>

using namespace std;

/*int findAvailableCell(int arr[]){

}*/

/**
 * @brief this function check if adding the mapping curr->charWanted will close a circle, if so it return true,
 * if there will not be a circle closed, then it return false
 * 
 * @param curr - The key we want to add to the map
 * @param charVal - The value we want to map curr
 * @param encryptChars - the map we search for possible circle if we add the mapping curr->charVal
 * @return true - If adding the mapping curr->charVal will close a circle
 * @return false - If adding the mapping curr->charVal will not close a circle
 */
bool circleClose(char curr, char charVal, map<char, char> encryptChars){

    char charWanted = charVal;

    while(true){

        if(auto search = encryptChars.find(charWanted); search != encryptChars.end()){//there is a mapping for charWanted
            charWanted = search->second;//move to the next char
        }//end of if
        else{//there is no map for curr char, so there is no circle, return false
            return false;
        }

        if(charWanted == curr){//if we will add the wanted mapping then there will be a circle and we don't allow it
            return true;
        }
    }//end of while

    return false;
    
}//end of circleClose


void resetArray(int *arr, int size){

    //cell j is available iff arr[j] == -1, so if we want to reset the array
    //we need to assign all cells value to -1
    for(int i=0; i<size; i++)
        arr[i] = -1;
    return;
}//end of resetArray

int main(){

    int testNum;
    int n;//string size
    string encry, result;
    char curr;
    int size;//array busy cells
    int availableChars[26];//cells of available char that wasn't mapped yet
    map<char, char> encryptChars;
    

    cin >> testNum;

    while(testNum--){
        cin >> n;

        //reset variables and structures 
        resetArray(availableChars, 26);
        encryptChars.clear();
        size = 0;
        result = "";

        cin >> encry;//read the string


        /**
         * @brief algorithm idea: we iterate through all the characters in the encry string
         * for each char we check if there is mapping for him, if there is then we use that mapping
         * if there isn't mapping, we create one. we search for a char that can fit all
         * the question requests and its lexicographical value is the smallest, when we find
         * this char we make mapping for him (he is the value no the kay). 
         * 
         */
        for(int i =0; i<n; i++){
            curr = encry[i];//get the i char

            if(auto search = encryptChars.find(curr); search != encryptChars.end()){//there is map for curr char
                result +=search->second;
            }//end of if
            else{
                //there is no mapping for curr char

                for(int j=0; j<26; j++){

                    if(curr == j+'a'){//don't map same char to each other for example: 'a'->'a' isn't allowed
                        continue;
                    }//end of if

                    if(availableChars[j] == -1){//the j cell is available, means there is no char mapped to it

                        if( size < 25 && circleClose(curr, j+'a', encryptChars)){
                            //if add the mapping curr->j+'a' circle may be close
                            //when size is 25 there is one cell left in the array and circle will be close for sure, this we allow
                            continue;
                        }//end of if

                        //add the mapping curr->j+'a' wiil not close a circle
                        encryptChars.insert({curr, j+'a'});//insert curr->j+'a' map
                        size++;//increase the busy cells size
                        availableChars[j] = curr-'a';//cell j get the value of curr-'a'
                        break;//we find a letter, stop the search

                    }//end of if

                }//end of for

                result +=encryptChars.find(curr)->second;

            }//end of else

        }//end of for
        cout << result << endl;
    }//end of while




    return 0;
}//end of main