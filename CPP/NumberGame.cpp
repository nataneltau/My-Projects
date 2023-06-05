#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

//some of the line that are cout<<... are for debuging


/**
 * @brief - The function run a game when Alice and Bob play optimally for some k (currK), the
 * function return true if Alice won and false if she lost 
 * 
 * @param arr - contain the n integers
 * @param currK - The k Alice Choose
 * @return true - The currK Alice choose was one she won with
 * @return false - The currK Alice choose was one she lose with
 */
bool aliceCanWin(vector<int> arr, int currK){
    /**
     * @brief - The idea is that: for Alice to play optimally she want to choose
     * the biggest integer that is smaller than currK-i, for Bob to play optimally
     * he want to choose the smallest integer, because all the integer are bigger
     * or equal to 1, when he increase the smallest in currK-i, in the next and all of the 
     * incoming turns Alice will not be able to choose that integer anymore
     * 
     */
    int currMax =0;
    int newVal;

    for(int i=0; i<currK; i++){//The k turns of the game

        currMax =0;

        vector<int> :: iterator it = arr.end();
        //cout << "a" << endl;

        for(auto iter = arr.begin(); iter !=arr.end(); iter++){//search the largest number smaller than currK-i
            if(*iter >= currMax && *iter <= currK-i){
                currMax = *iter;
                it = iter;
            }
        }

        //cout << "b" << endl;
        
        if(it == arr.end()){//there is no number smaller than currK-i, Alice lose
            return false;
        }
        arr.erase(it);//Alice remove the element

        //now Bob search the min and incearse it
        auto min = min_element(arr.begin(), arr.end());
        newVal = *min + currK-i;

        //cout << "k" << endl;

        if(min == arr.end()){//if there is no more elements in the vector, Alice won (happen in vector with only one element)
            return true;
        }

        arr.erase(min);
        arr.push_back(newVal);
    
    }//end of for

    //Alice won
    return true;

}//end of aliceCanWin

int main(){

    int testNum;
    int n;
    int max;
    bool result;


    cin >> testNum;

    while (testNum--)//run testNum times
    {
        cin >> n;
        

        vector<int> arr(n);

        for(int i=0; i<n; i++){//fill the vector
            cin >> arr[i];
        }
        
    
        max = n;//max k cann't be bigger than n
        
        //cout << "d" << endl;
        while(max != 0){

            result = aliceCanWin(arr, max);
            //cout << "e"<< endl;
            if(result){//result == true
                //if restult is true then alice can win with this max number, he is the biggest
                //because she cann't win with max+1
                break;
            }
            max--;
        }//end of inner while

        cout << max << endl;
        //cout << "c" << endl;
    }//end of while

    return 0;

}//end of main