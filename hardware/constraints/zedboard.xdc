##==============================================================================
## ZedBoard Constraints for NeuroMetric-FPGA (Top-Level Wrapper)
## Target: Xilinx Zynq-7020 (xc7z020clg484-1)
##==============================================================================

##------------------------------------------------------------------------------
## Clock Signal (100 MHz on Bank 13)
##------------------------------------------------------------------------------
set_property PACKAGE_PIN Y9 [get_ports clk]
set_property IOSTANDARD LVCMOS33 [get_ports clk]
create_clock -add -name sys_clk_pin -period 10.00 -waveform {0 5} [get_ports clk]

##------------------------------------------------------------------------------
## Reset Button (BTNC - Center Button on Bank 34, Vadj=2.5V)
##------------------------------------------------------------------------------
set_property PACKAGE_PIN P16 [get_ports rst_n_btn]
set_property IOSTANDARD LVCMOS33 [get_ports rst_n_btn]

##------------------------------------------------------------------------------
## User Push Buttons (Bank 34, LVCMOS25)
## btn[0] = BTNU, btn[1] = BTNL, btn[2] = BTND, btn[3] = BTNR, btn[4] = BTNC
##------------------------------------------------------------------------------
set_property PACKAGE_PIN T18 [get_ports {btn[0]}]
set_property IOSTANDARD LVCMOS33 [get_ports {btn[0]}]

set_property PACKAGE_PIN N15 [get_ports {btn[1]}]
set_property IOSTANDARD LVCMOS33 [get_ports {btn[1]}]

set_property PACKAGE_PIN R16 [get_ports {btn[2]}]
set_property IOSTANDARD LVCMOS33 [get_ports {btn[2]}]

set_property PACKAGE_PIN R18 [get_ports {btn[3]}]
set_property IOSTANDARD LVCMOS33 [get_ports {btn[3]}]

## Note: BTNC (P16) is used for reset, so we don't map it to btn[4]

##------------------------------------------------------------------------------
## User DIP Switches (Bank 33, LVCMOS33)
##------------------------------------------------------------------------------
set_property PACKAGE_PIN F22 [get_ports {sw[0]}]
set_property IOSTANDARD LVCMOS33 [get_ports {sw[0]}]

set_property PACKAGE_PIN G22 [get_ports {sw[1]}]
set_property IOSTANDARD LVCMOS33 [get_ports {sw[1]}]

set_property PACKAGE_PIN H22 [get_ports {sw[2]}]
set_property IOSTANDARD LVCMOS33 [get_ports {sw[2]}]

set_property PACKAGE_PIN F21 [get_ports {sw[3]}]
set_property IOSTANDARD LVCMOS33 [get_ports {sw[3]}]

set_property PACKAGE_PIN H19 [get_ports {sw[4]}]
set_property IOSTANDARD LVCMOS33 [get_ports {sw[4]}]

set_property PACKAGE_PIN H18 [get_ports {sw[5]}]
set_property IOSTANDARD LVCMOS33 [get_ports {sw[5]}]

set_property PACKAGE_PIN H17 [get_ports {sw[6]}]
set_property IOSTANDARD LVCMOS33 [get_ports {sw[6]}]

set_property PACKAGE_PIN M15 [get_ports {sw[7]}]
set_property IOSTANDARD LVCMOS33 [get_ports {sw[7]}]

##------------------------------------------------------------------------------
## User LEDs (Bank 33, LVCMOS33)
##------------------------------------------------------------------------------
set_property PACKAGE_PIN T22 [get_ports {led[0]}]
set_property IOSTANDARD LVCMOS33 [get_ports {led[0]}]

set_property PACKAGE_PIN T21 [get_ports {led[1]}]
set_property IOSTANDARD LVCMOS33 [get_ports {led[1]}]

set_property PACKAGE_PIN U22 [get_ports {led[2]}]
set_property IOSTANDARD LVCMOS33 [get_ports {led[2]}]

set_property PACKAGE_PIN U21 [get_ports {led[3]}]
set_property IOSTANDARD LVCMOS33 [get_ports {led[3]}]

set_property PACKAGE_PIN V22 [get_ports {led[4]}]
set_property IOSTANDARD LVCMOS33 [get_ports {led[4]}]

set_property PACKAGE_PIN W22 [get_ports {led[5]}]
set_property IOSTANDARD LVCMOS33 [get_ports {led[5]}]

set_property PACKAGE_PIN U19 [get_ports {led[6]}]
set_property IOSTANDARD LVCMOS33 [get_ports {led[6]}]

set_property PACKAGE_PIN U14 [get_ports {led[7]}]
set_property IOSTANDARD LVCMOS33 [get_ports {led[7]}]

