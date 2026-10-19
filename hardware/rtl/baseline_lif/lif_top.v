`timescale 1ns / 1ps
//=============================================================================
// Module: zedboard_lif_top
// Description: ZedBoard-specific wrapper for the LIF neuron array.
//              Maps the 64-neuron design down to 8 neurons to fit the 
//              ZedBoard's 8 user LEDs, and uses buttons/switches for input.
//=============================================================================

module zedboard_lif_top (
    input  wire        clk,           // 100 MHz oscillator
    input  wire        rst_n_btn,     // BTNC (Center Button, active high on board)
    input  wire [4:0]  btn,           // BTNU, BTNL, BTND, BTNR, and one more
    input  wire [7:0]  sw,            // SW0-SW7
    output wire [7:0]  led            // LD0-LD7
);

    // -------------------------------------------------------------------------
    // Reset Logic (Button is active-high on board, design needs active-low)
    // -------------------------------------------------------------------------
    wire rst_n = ~rst_n_btn;

    // -------------------------------------------------------------------------
    // Map Buttons to Spike Inputs
    // btn[0] = BTNU  -> spike_in_valid (Press to inject a spike)
    // btn[4:1]       -> spike_in_id (Select which of the 8 neurons to spike)
    // -------------------------------------------------------------------------
    wire spike_in_valid = btn[0];
    wire [2:0] spike_in_id = btn[3:1]; // 3 bits = 0 to 7

    // -------------------------------------------------------------------------
    // Map Switches to Spike Weight
    // Use 8 switches for the lower 8 bits of the 16-bit weight.
    // Upper 8 bits tied to 0 (positive weights only for baseline).
    // -------------------------------------------------------------------------
    wire signed [15:0] spike_in_weight = {8'b00000000, sw};

    // -------------------------------------------------------------------------
    // Instantiate LIF Neuron Array (Scaled to 8 neurons for ZedBoard LEDs)
    // -------------------------------------------------------------------------
    lif_neuron_array #(
        .NUM_NEURONS       (8),
        .POTENTIAL_WIDTH   (16),
        .WEIGHT_WIDTH      (16),
        .DEFAULT_THRESHOLD (100),
        .DEFAULT_LEAK      (2)
    ) u_lif_array (
        .clk               (clk),
        .rst_n             (rst_n),
        .spike_in_valid    (spike_in_valid),
        .spike_in_id       (spike_in_id),
        .spike_in_weight   (spike_in_weight),
        .spike_out         (led),            // 8 spike outputs -> 8 LEDs
        .debug_id          (3'b000),         // Tie off debug (not used on board)
        .debug_potential   ()                // Leave unconnected
    );

endmodule