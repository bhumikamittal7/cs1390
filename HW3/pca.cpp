//include libraries
#include <iostream>
#include <fstream>
#include <string>
#include <chrono>
#include "Eigen/Dense"
#include "Eigen/Eigenvalues"

//use namespace
using namespace Eigen;      // to use the Eigen library

//generate random dataset
Eigen::MatrixXd generateRandomDataset(int m, int n) {
    Eigen::MatrixXd dataset(m, n);                  // m rows, n columns
    dataset = Eigen::MatrixXd::Random(m, n);        // fill with random numbers
    return dataset;                                 // return the matrix
}

//pca stuff
Eigen::MatrixXd performPCA(Eigen::MatrixXd dataset, int numComponents) {
    Eigen::MatrixXd centered = dataset.rowwise() - dataset.colwise().mean();         // center the data around the mean - normalize the data
    Eigen::MatrixXd cov = centered.adjoint() * centered;                            // calculate the covariance matrix
    Eigen::SelfAdjointEigenSolver<Eigen::MatrixXd> eig(cov);                       // calculate the eigenvalues and eigenvectors
    Eigen::MatrixXd eigenVectors = eig.eigenvectors();                            // get the eigenvectors
    return eigenVectors.rightCols(numComponents);                                // return the rightmost columns of the eigenvectors - because these are the ones with the highest variance - the principal components
}

//main function
int main()
{
    int m = 100;
    int n = 100;
    int numComponents = static_cast<int>(n * 0.1);                                     // 10% of the number of columns of the dataset
    MatrixXd dataset = MatrixXd::Random(m, n);                                        // generate a random dataset
    
    auto start = std::chrono::high_resolution_clock::now();
    MatrixXd principalComponents = performPCA(dataset, numComponents);               // perform PCA on 0.1% of the dataset
    auto stop = std::chrono::high_resolution_clock::now();

    std::cout << "Principal components:\n" << principalComponents << std::endl;     // print the principal components
    
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(stop - start);
    std::cout << "Time taken by function: " << duration.count() << " microseconds" << std::endl;

    return 0;
}

