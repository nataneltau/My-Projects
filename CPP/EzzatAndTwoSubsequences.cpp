#include <iostream>
#include <iomanip>

using namespace std;

int main(){
    int testNum;
    int n;
    int tmp;
    int sum, max;
    double avg;    

    cin >> testNum;

    while (testNum--)//run testNum times
    {
        cin >> n;
        avg = 0;
        //sum = 0;
        //double arr[n];

        cin >> tmp;
        avg += tmp;
        max = tmp;

        for(int i=1; i<n; i++){
            cin >> tmp;
            avg += tmp;
            if(max<tmp){
                max = tmp;
            }
        }
        //max = findMax(arr, n);
        avg -= max;
        avg = avg/(n - 1.0);
        cout << fixed << showpoint << setprecision(9) << (avg+max) << endl;
    }
    
    return 0;

}//end of main