# 🧠 NeuroMetric-FPGA

[![Hacktoberfest 2026](https://img.shields.io/badge/Hacktoberfest-2026-orange?style=for-the-badge)](https://hacktoberfest.com/)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg?style=for-the-badge)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.9+-yellow?style=for-the-badge&logo=python)](https://www.python.org/)
[![Verilog](https://img.shields.io/badge/HDL-Verilog/SystemVerilog-red?style=for-the-badge)](https://en.wikipedia.org/wiki/Verilog)
[![DEV Community](https://img.shields.io/badge/DEV-Community-black?style=for-the-badge&logo=dev.to)](https://dev.to/)

> **Standardizing performance, power, and area evaluation for Spiking Neural Networks (SNNs) and neuromorphic architectures on FPGA hardware.**

---

## 🚀 The Mission

Traditional AI benchmarks (like MLPerf) measure dense matrix multiplication in TOPS (Tera Operations Per Second). But **neuromorphic computing is sparse, event-driven, and asynchronous**. Measuring a Spiking Neural Network (SNN) with traditional metrics is like measuring a sports car's fuel efficiency in gallons per hour instead of miles per gallon.

**NeuroMetric-FPGA** is an open-source benchmarking suite designed to evaluate neuromorphic FPGA designs using metrics that actually matter:
- ⚡ **Spiking Operations Per Second (SOPS)**
- 🔋 **Energy-per-Spike (pJ/spike)**
- 🧩 **Neuron & Synapse Density (per Logic Element / LUT)**
- ⏱️ **Event-to-Event Inference Latency**
- 🎯 **Temporal Classification Accuracy**

This project is an official submission for the **Hacktoberfest 2026 Open-Source AI Challenge**. We are building the tooling that will help the next generation of edge-AI hardware engineers validate, compare, and optimize brain-inspired architectures.

---

## 🏗️ Architecture

The suite is divided into three modular layers, making it easy to swap out components or add new FPGA targets:

1. **`workloads/`**: Standardized, pre-converted neuromorphic datasets (e.g., N-MNIST, DVS Gesture, Spiking Heidelberg Digits) formatted as spike-train CSVs or binary files.
2. **`rtl/`**: Reference Spiking Neural Network implementations in Verilog/SystemVerilog (e.g., a baseline Leaky Integrate-and-Fire (LIF) neuron array, or wrappers for open-source cores like Catalyst N1).
3. **`host/`**: A Python-based CLI telemetry engine that programs the FPGA, streams inference results via UART/PCIe, parses Vivado/Quartus utilization reports, and auto-generates a Markdown/JSON benchmark report.

---

## 📊 Key Metrics Tracked

| Metric | Description | Why it matters for Neuromorphic |
| :--- | :--- | :--- |
| **SOPS** | Spiking Operations Per Second | Measures true event-driven throughput, not idle clock cycles. |
| **pJ / Spike** | Picojoules per synaptic event | The ultimate metric for ultra-low-power edge AI and battery-operated devices. |
| **Routing Congestion** | % of routing resources used | SNNs are highly interconnected; routing is often the true bottleneck, not logic. |
| **BRAM / LUT Ratio** | Memory vs. Logic utilization | Indicates how efficiently the design maps synaptic weights to on-chip memory. |

---

## 🛠️ Quick Start

### Prerequisites
- Python 3.9+
- Xilinx Vivado or Intel Quartus (for RTL synthesis and bitstream generation)
- An FPGA development board (Currently tested on: *Xilinx PYNQ-Z2, Basys 3. More welcome!*)

### Installation
```bash
# Clone the repository
git clone https://github.com/[Your-Username]/NeuroMetric-FPGA.git
cd NeuroMetric-FPGA

# Install Python dependencies for the host telemetry tool
pip install -r host/requirements.txt
```

### Running Your First Benchmark
```bash
# 1. Synthesize the reference LIF baseline (example for Vivado)
cd rtl/baseline_lif
vivado -mode batch -source run_synth.tcl

# 2. Run the Python benchmarking harness
cd ../../host
python benchmark.py --dataset nmnist --fpga-target pynq-z2 --generate-report
```
*This will output a `benchmark_report.md` with accuracy, latency, and a parsed resource utilization summary.*

---

## 🤝 Contributing (Hacktoberfest 2026 🎃)

We welcome contributions from FPGA engineers, ML researchers, and software developers! This project is designed to be modular, so you can contribute without needing to understand the entire codebase.

Check out our [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines. Here are some great ways to get started:

- 🟢 **[good first issue]**: Add a parser for a new FPGA toolchain report (e.g., Lattice Diamond, Intel Quartus).
- 🟢 **[good first issue]**: Write a Python script to convert a new dataset (e.g., CIFAR10-DVS) into our standard spike-train format.
- 🟡 **[help wanted]**: Implement a new reference RTL core (e.g., a simplified Izhikevich neuron model).
- 🟡 **[help wanted]**: Add support for a new FPGA development board (e.g., Lattice iCE40, Xilinx ZCU104).
- 🔵 **[documentation]**: Improve the telemetry API docs or write a tutorial on deploying custom SNNs.

*All valid Pull Requests merged during October will be celebrated, and contributors will be added to our Hall of Fame!*

---

## 🗺️ Roadmap

- [x] **Phase 1**: Core Python telemetry engine and baseline LIF Verilog module.
- [x] **Phase 2**: Integration with N-MNIST dataset and automated Vivado report parsing.
- [ ] **Phase 3**: Support for PCIe-based high-throughput telemetry (for larger FPGAs).
- [ ] **Phase 4**: Integration with open-source neuromorphic frameworks (e.g., Intel Lava, snnTorch) as a validation backend.
- [ ] **Phase 5**: Web-based dashboard for visualizing community-submitted benchmark results.

---

## 📚 References & Inspiration

- [NeuroBench](https://neurobench.ai/): The foundational algorithmic and system-level benchmarking framework for neuromorphic computing.
- [Catalyst N1/N2](https://github.com/catalyst-neuromorphic): Open-source neuromorphic processors with Loihi parity, validated on FPGA.
- [Lava Framework](https://github.com/lava-nc/lava): Intel's open-source software framework for neuro-inspired applications.

---

## 📝 License

This project is licensed under the **Apache License 2.0** – see the [LICENSE](LICENSE) file for details. We chose this license to ensure maximum freedom for both academic research and commercial hardware adoption.

---

## 🌟 Acknowledgments

Built with ❤️ for the open-source hardware community and submitted for the **Hacktoberfest 2026 Open-Source AI Challenge**. 

*If you find this project useful, please consider giving it a ⭐️ on GitHub and sharing it with your fellow FPGA engineers!*
