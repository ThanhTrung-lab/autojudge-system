#include <iostream>
#include <vector>
using namespace std;

vector<int> sang_NT(int n) {
    vector<bool> f(n + 1, true);

    if (n >= 0) f[0] = false;
    if (n >= 1) f[1] = false;

    // Loại các số chẵn > 2
    for (int i = 4; i <= n; i += 2)
        f[i] = false;

    int p = 3;
    while (p * p <= n) {
        if (f[p]) {
            for (int i = p * p; i <= n; i += p)
                f[i] = false;
        }
        p++;
    }

    vector<int> res;
    for (int i = 2; i <= n; i++)
        if (f[i])
            res.push_back(i);

    return res;
}

int main() {
    int n;
    cin >> n;

    vector<int> kq = sang_NT(n);

    for (int x : kq)
        cout << x << " ";

    return 0;
}