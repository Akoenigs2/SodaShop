#include "test.h"

int main() {
    // Variables
    int number;

    // Welcome message
    printf("Welcome to the Basic C Program!\n");

    // Calling a function
    greetUser();

    // Get user input
    printf("Enter a number: ");
    scanf("%d", &number);

    // Process and output result
    printf("You entered: %d\n", number);
    printf("The square of the number is: %d\n", number * number);

    return 0;
}

// Function definition
void greetUser() {
    printf("Hello! Let's do something simple with numbers.\n");
}
