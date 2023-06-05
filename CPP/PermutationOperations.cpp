#include <iostream>
#include <vector>
#include <algorithm>
#include <set>

using namespace std;

/**
 * @brief We save the number which is the current maximum in the subarray arr[0...i], a new number a[i+1] should be 
        bigger than the maximum, if it's bigger then it's the new maximum, else we want to search for an
        available index that can fix it, meaning make this number bigger than the maximum.
 * 
 * @param arr - Vector contain the numbers
 * @param printser - Vector hold the printing index for each operation
 * @param indexMy - Set contain the available index operation
 * @param n - The size of each data structer
 */
void findPermutation(vector<int> arr, vector<int> printser, set<int> indexMy, int n){

        int currMax = arr[0];

        
        for(int i=1; i<n; i++){
            if(arr[i]>currMax){//a[i] is the new maximum
                currMax = arr[i];
            }
            else{
                int tmp = currMax - arr[i];//the needed number for increasing

                auto it = indexMy.lower_bound(tmp);//search available number bigger than tmp

                printser[*it] = i+1;//we need to increase the index in place i+1

                indexMy.erase(it);//no longer can use that index
            }
        }

        for(int i=0; i<n; i++){
            if(printser[i] == -1){//if printser[i] == -1 than it never changed, meaning we don't need that index
                cout << 1 << " ";
            }
            else{
                cout << printser[i] << " ";
            }
        }
        cout << endl;

}

int main(){

    int testNum;
    int n;

    cin >> testNum;

    while (testNum--)//run testNum times
    {
        cin >> n;

        vector<int> arr(n);
        vector<int> printser(n);
        set<int> indexMy;
        

        for(int i=0; i<n; i++){
            
            cin >> arr[i];//fill the vector 
            printser[i] = -1;//initialize the printed indexes
            indexMy.insert(i+1);//insert the available indexes to a set

        }

       findPermutation(arr, printser, indexMy, n);

        
    }//end of while

    return 0;
}//end of main