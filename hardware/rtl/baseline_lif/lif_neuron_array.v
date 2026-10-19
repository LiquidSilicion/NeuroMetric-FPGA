`timescale 1ns / 1ps
//=============================================================================
// Module: lif_neuron_array
// Description: A parameterized array of Leaky Integrate-and-Fire (LIF) neurons.
//              This serves as the baseline reference design for the 
//              NeuroMetric-FPGA benchmarking suite.
// Target: Xilinx Zynq-7020 (ZedBoard) / General FPGA
//=============================================================================

module lif_neuron_array #(
    parameter NUM_NEURONS      = 64,           // Number of neurons in the array
    parameter POTENTIAL_WIDTH  = 16,           // Bit-width for membrane potential
    parameter WEIGHT_WIDTH     = 16,           // Bit-width for synaptic weights
    parameter DEFAULT_THRESHOLD = 100,         // Firing threshold (mV equivalent)
    parameter DEFAULT_LEAK     = 2             // Leak factor per clock cycle
)(
    input  wire                         clk,
    input  wire                         rst_n,       // Active low reset
    
    // Spike Input Interface (Event-driven)
    input  wire                         spike_in_valid,
    input  wire [$clog2(NUM_NEURONS)-1:0] spike_in_id, // Target neuron index
    input  wire signed [WEIGHT_WIDTH-1:0] spike_in_weight, // Synaptic weight to add
    
    // Spike Output Interface (Telemetry)
    output wire [NUM_NEURONS-1:0]       spike_out,   // 1 if neuron fired this cycle
    
    // Debug / Telemetry Interface (Read membrane potential of a specific neuron)
    input  wire [$clog2(NUM_NEURONS)-1:0] debug_id,
    output wire signed [POTENTIAL_WIDTH-1:0] debug_potential
);

    // -------------------------------------------------------------------------
    // Internal State: Membrane Potentials for all neurons
    // -------------------------------------------------------------------------
    reg signed [POTENTIAL_WIDTH-1:0] membrane [0:NUM_NEURONS-1];
    
    // -------------------------------------------------------------------------
    // LIF Neuron Logic
    // -------------------------------------------------------------------------
    integer i;
    
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            // Reset all membrane potentials to 0
            for (i = 0; i < NUM_NEURONS; i = i + 1) begin
                membrane[i] <= 0;
            end
        end else begin
            for (i = 0; i < NUM_NEURONS; i = i + 1) begin
                // 1. Integration: Add incoming spike weight if targeted
                if (spike_in_valid && (spike_in_id == i)) begin
                    membrane[i] <= membrane[i] + spike_in_weight;
                end 
                // 2. Leakage: Decay the membrane potential every clock cycle
                else if (membrane[i] > 0) begin
                    membrane[i] <= membrane[i] - DEFAULT_LEAK;
                end else if (membrane[i] < 0) begin
                    membrane[i] <= membrane[i] + DEFAULT_LEAK; // Leak towards zero
                end

                // 3. Firing & Reset: If threshold is reached, output a spike and reset
                // Note: In a real multi-cycle pipeline, reset and fire might be separated.
                // For this baseline, we reset immediately after crossing threshold.
                if (membrane[i] >= DEFAULT_THRESHOLD) begin
                    membrane[i] <= 0; // Reset to resting potential
                end
            end
        end
    end

    // -------------------------------------------------------------------------
    // Output Logic: Spike Generation
    // -------------------------------------------------------------------------
    genvar g;
    generate
        for (g = 0; g < NUM_NEURONS; g = g + 1) begin : gen_spikes
            assign spike_out[g] = (membrane[g] >= DEFAULT_THRESHOLD) ? 1'b1 : 1'b0;
        end
    endgenerate

    // -------------------------------------------------------------------------
    // Debug Telemetry: Multiplexer to read a specific neuron's potential
    // -------------------------------------------------------------------------
    assign debug_potential = membrane[debug_id];

endmodule