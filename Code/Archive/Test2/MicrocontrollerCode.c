#include <stdio.h>
#include "pico/stdlib.h"

// GPIO pins
#define BUTTON_INC 2
#define BUTTON_DEC 3
#define BUTTON_TOGGLE 4
#define OUTPUT_FREQ 5
#define OUTPUT_TOGGLE 6

// Variable to control frequency output
float frequency_time = 1.0; // Default to 1 second
bool output_toggle_state = false; // State for second output

// Debounce handling
const uint DEBOUNCE_DELAY_MS = 200;
uint64_t last_inc_press_time = 0;
uint64_t last_dec_press_time = 0;
uint64_t last_toggle_press_time = 0;

void setup_gpio() {
    // Initialize input buttons
    gpio_init(BUTTON_INC);
    gpio_set_dir(BUTTON_INC, GPIO_IN);
    gpio_pull_up(BUTTON_INC);

    gpio_init(BUTTON_DEC);
    gpio_set_dir(BUTTON_DEC, GPIO_IN);
    gpio_pull_up(BUTTON_DEC);

    gpio_init(BUTTON_TOGGLE);
    gpio_set_dir(BUTTON_TOGGLE, GPIO_IN);
    gpio_pull_up(BUTTON_TOGGLE);

    // Initialize output GPIOs
    gpio_init(OUTPUT_FREQ);
    gpio_set_dir(OUTPUT_FREQ, GPIO_OUT);

    gpio_init(OUTPUT_TOGGLE);
    gpio_set_dir(OUTPUT_TOGGLE, GPIO_OUT);

    // Set outputs to default LOW
    gpio_put(OUTPUT_FREQ, 0);
    gpio_put(OUTPUT_TOGGLE, 0);
}

void handle_buttons() {
    uint64_t now = to_ms_since_boot(get_absolute_time());

    // Increment button
    if (!gpio_get(BUTTON_INC) && (now - last_inc_press_time > DEBOUNCE_DELAY_MS)) {
        frequency_time += 0.25; // Increment by 0.25
        last_inc_press_time = now;
        if (frequency_time > 10.0) frequency_time = 10.0; // Cap at 10 seconds
        printf("Frequency time: %.2f seconds\n", frequency_time);
    }

    // Decrement button
    if (!gpio_get(BUTTON_DEC) && (now - last_dec_press_time > DEBOUNCE_DELAY_MS)) {
        frequency_time -= 0.25; // Decrement by 0.25
        last_dec_press_time = now;
        if (frequency_time < 0.25) frequency_time = 0.25; // Minimum 0.25 seconds
        printf("Frequency time: %.2f seconds\n", frequency_time);
    }

    // Toggle button
    if (!gpio_get(BUTTON_TOGGLE) && (now - last_toggle_press_time > DEBOUNCE_DELAY_MS)) {
        output_toggle_state = !output_toggle_state; // Toggle state
        gpio_put(OUTPUT_TOGGLE, output_toggle_state); // Update second output
        last_toggle_press_time = now;
        printf("Second output toggled: %s\n", output_toggle_state ? "ON" : "OFF");
    }
}

void control_output_frequency() {
    gpio_put(OUTPUT_FREQ, 1); // Set HIGH
    sleep_ms(frequency_time * 1000);
    gpio_put(OUTPUT_FREQ, 0); // Set LOW
    sleep_ms(frequency_time * 1000);
}

int main() {
    stdio_init_all();
    setup_gpio();

    printf("Raspberry Pi Pico Frequency Controller\n");

    while (1) {
        handle_buttons();
        control_output_frequency();
    }

    return 0;
}
