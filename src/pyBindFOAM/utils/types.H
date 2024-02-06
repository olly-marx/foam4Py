#include "fvCFD.H"
#include <string>

// Define a map to map string representations to types
std::map<std::string, int> typeMap = {
    {"Foam::dictionary", 1},
    {"Foam::List<Foam::scalar>", 2},
    {"Foam::word", 3},
    {"bool", 4},
    {"int", 5},
    {"unsigned", 6},
    {"double", 7}
};

// Define a struct to hold the result type
template <int N>
struct ResultType {};

// Specializations of ResultType for different types
template <>
struct ResultType<1> {
    using type = Foam::dictionary;
};

template <>
struct ResultType<2> {
    using type = Foam::List<Foam::scalar>;
};

template <>
struct ResultType<3> {
    using type = Foam::word;
};

template <>
struct ResultType<4> {
    using type = bool;
};

template <>
struct ResultType<5> {
    using type = Foam::scalar;
};

template <>
struct ResultType<6> {
    using type = Foam::scalar;
};

template <>
struct ResultType<7> {
    using type = Foam::scalar;
};

// Function to deduce the type based on the string input
template <typename T>
typename ResultType<T>::type deduceType(const std::string& type)
{
    const int typeID = typeMap.find(type)->second;
    return typename ResultType<typeID>::type();
}
