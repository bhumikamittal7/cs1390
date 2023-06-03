#include <iostream>
#include <fstream>
#include <string>
#include "Eigen/Dense"

using namespace std;
using namespace Eigen;

void saveDatasetToCsv(MatrixXd dataset, string filename) {
    ofstream file(filename);
    if (file.is_open()) {
        for (int i = 0; i < dataset.rows(); i++) {
            for (int j = 0; j < dataset.cols(); j++) {
                file << dataset(i, j);
                if (j < dataset.cols() - 1) {
                    file << ",";
                }
            }
            file << endl;
        }
        file.close();
    }
}

int main() {
    int dimensions[5][2] = {{100, 100}, {1000, 1000}, {10000, 10000}, {10000, 50000}, {50000, 50000}};
    for (int i = 0; i < 5; i++) {
        int m = dimensions[i][0];
        int n = dimensions[i][1];
        MatrixXd dataset = MatrixXd::Random(m, n);
        string filename = "dataset_" + to_string(m) + "x" + to_string(n) + ".csv";
        saveDatasetToCsv(dataset, filename);
    }
    return 0;
}
