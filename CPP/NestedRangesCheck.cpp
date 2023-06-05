#include <iostream>
#include <algorithm>
#include <vector>

using namespace std;


typedef struct range{
    int x;
    int y;
    int indexInInput;//the vector is sorted so we need to know the original index for printing
}range;

bool compareRange(range p1, range p2){//order by x then by y

    if(p1.x == p2.x){
        return (p1.y > p2.y);
    }

    return (p1.x < p2.x);
}//end of compareRange

/**
 * @brief The vector is sorted by x then by y so the last element is the one with the biggest x and smallest y
 *      which contain no one, then we going back in the vector because the an element i can contain only range's 
 *      which have x bigger or equal to his and y smaller or equal to his, so it cann't be before him since before
 *      him there is only x smaller than his or y bigger than his, and since we know all the range's after him have
 *      a bigger or equal x to his, we just need to remember  the range with the smallest y.
 * 
 * @param sortVec - Sorted vector of range's
 * @param n - number of range's
 */
void containOtherRange(vector<range> sortVec, int n){

    int arr[n];//the array that we will use to print
    vector<range> :: iterator iter;

    //the last element contain no one
    iter = sortVec.end()-1;
    int minY = iter->y;

    //the vector is sorted so we need to know the original index for printing
    arr[iter->indexInInput] = 0;
    iter--;

    while(iter!=sortVec.begin()){
        if(minY<=iter->y){//meaning the element iter can contain someone
            arr[iter->indexInInput]=1;
        }
        else{//the smallest y is bigger then iter->y
            arr[iter->indexInInput]=0;
            minY = iter->y;
        }
        
        iter--;
    }

    //same check for the first element
    if(minY<=iter->y){
        arr[iter->indexInInput]=1;
    }
    else{
        arr[iter->indexInInput]=0;
    }

    for(int i =0; i<n; i++){//print the result
        cout << arr[i] << " ";
    }

    cout << endl;
}//end of containOtherRange

/**
 * @brief Same idea with the previos function, this time we save the maximum y, as we always grow bigger
 *      in x, there is a range that contain me iff I have a smaller y then the maximum y behind me, which
 *      also have a smaller x than me
 * 
 * @param sortVec - Sorted vector of range's
 * @param n - number of range's
 */
void otherContainMe(vector<range> sortVec, int n){

    vector<range> :: iterator iter;
    int arr[n];//the array that we will use to print

    //no one contain the first element
    int maxY = sortVec[0].y;
    iter = sortVec.begin();

    //the vector is sorted so we need to know the original index for printing
    arr[iter->indexInInput] = 0;

    iter++;

    while(iter!=sortVec.end()){
        if(maxY>=iter->y){//there is some range that can contain me
            arr[iter->indexInInput]=1;
        }
        else{//x is biggest so far (vector sorted by x) now iter->y also bigger then maxY
            arr[iter->indexInInput] = 0;
            maxY = iter->y;
        }
        
        iter++;
    }

    for(int i =0; i<n; i++){//print the result
        cout << arr[i] << " ";
    }
    
    cout << endl;

}//end of otherContainMe

int main(){

    int n;

    cin >> n;

    vector<range> sortedByX(n);

    for(int i=0; i<n; i++){//read input
        cin >> sortedByX[i].x;
        cin >> sortedByX[i].y;
        sortedByX[i].indexInInput = i;//the order of the range in the input

    }//end of for

    sort(sortedByX.begin(), sortedByX.end(), compareRange);

    containOtherRange(sortedByX, n);//search which range's contains other range's

    otherContainMe(sortedByX, n);//search which rang'e has range that contains it


    return 0;
}//end of main