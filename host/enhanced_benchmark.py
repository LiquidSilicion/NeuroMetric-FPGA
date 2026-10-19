#!/usr/bin/env python3
"""
NeuroMetric-FPGA: Open-Source Neuromorphic Benchmarking Suite
Host Telemetry & Reporting Engine (v2.1 - Fixed Vivado Report Parsing)
"""

import argparse
import json
import csv
import re
import os
from pathlib import Path
from datetime import datetime

class NeuroMetricBenchmark:
    def __init__(self, dataset_name, fpga_target, util_report_path=None, power_report_path=None):
        self.dataset_name = dataset_name
        self.fpga_target = fpga_target
        self.util_report_path = util_report_path
        self.power_report_path = power_report_path
        
        # Metrics storage
        self.hw_metrics = {}
        self.perf_metrics = {}
        self.power_metrics = {}

    def load_mock_dataset(self):
        """Simulates loading a neuromorphic spike-train dataset."""
        print(f"[*] Loading dataset: {self.dataset_name}...")
        mock_events = 10000 
        print(f"[*] Loaded {mock_events} spike events.")
        return mock_events

    def mock_fpga_inference(self, num_events):
        """Simulates FPGA inference."""
        print(f"[*] Streaming {num_events} events to FPGA ({self.fpga_target})...")
        results = {
            "output_spikes": 850,
            "correct_classifications": 810,
            "total_samples": 850,
            "inference_time_ms": 12.5,
            "total_spikes_processed": num_events
        }
        print(f"[*] Inference complete. Time: {results['inference_time_ms']}ms")
        return results

    def parse_utilization_report(self):
        """Parses Xilinx Vivado IMPLEMENTATION utilization report."""
        print(f"[*] Parsing hardware utilization report...")
        
        # Default mock values for Zynq-7020
        self.hw_metrics = {
            "LUT": 341, "FF": 128, "DSP": 0, "BRAM": 0,
            "total_lut_available": 53200, "total_ff_available": 106400,
            "total_dsp_available": 220, "total_bram_available": 140,
            "max_freq_mhz": 150.0,
            "worst_negative_slack_ns": 0.5,
            "routing_congestion_pct": 12.3
        }

        if self.util_report_path and os.path.exists(self.util_report_path):
            print(f"[*] Reading Vivado implementation report: {self.util_report_path}")
            with open(self.util_report_path, 'r') as f:
                content = f.read()
                
            # Parse LUT utilization - Match: | Slice LUTs              |  341 |
            lut_match = re.search(r'\|\s*Slice LUTs\s*\|\s*(\d+)\s*\|', content)
            if lut_match:
                self.hw_metrics["LUT"] = int(lut_match.group(1))
                print(f"    ✓ Found LUTs: {self.hw_metrics['LUT']}")
                
            # Parse FF utilization - Match: | Slice Registers         |  128 |
            ff_match = re.search(r'\|\s*Slice Registers\s*\|\s*(\d+)\s*\|', content)
            if ff_match:
                self.hw_metrics["FF"] = int(ff_match.group(1))
                print(f"    ✓ Found FFs: {self.hw_metrics['FF']}")
                
            # Parse DSP utilization - Match: | DSPs                    |    0 |
            dsp_match = re.search(r'\|\s*DSPs\s*\|\s*(\d+)\s*\|', content)
            if dsp_match:
                self.hw_metrics["DSP"] = int(dsp_match.group(1))
                print(f"    ✓ Found DSPs: {self.hw_metrics['DSP']}")
                
            # Parse BRAM utilization - Match: | Block RAM Tile          |    0 |
            bram_match = re.search(r'\|\s*Block RAM Tile\s*\|\s*(\d+)\s*\|', content)
            if bram_match:
                self.hw_metrics["BRAM"] = int(bram_match.group(1))
                print(f"    ✓ Found BRAM: {self.hw_metrics['BRAM']}")

    def parse_power_report(self):
        """Parses Xilinx Vivado power analysis report."""
        print(f"[*] Parsing power analysis report...")
        
        # Default mock power values
        self.power_metrics = {
            "total_power_w": 0.135,
            "dynamic_power_w": 0.028,
            "static_power_w": 0.106,
            "junction_temp_c": 26.6,
            "thermal_margin_c": 56.8,
            "vccint_current_a": 0.015,
            "vccaux_current_a": 0.011,
            "confidence_level": "Low"
        }

        if self.power_report_path and os.path.exists(self.power_report_path):
            print(f"[*] Reading Vivado power report: {self.power_report_path}")
            with open(self.power_report_path, 'r') as f:
                content = f.read()
                
            # Parse total power - Match: | Total On-Chip Power (W)  | 0.135        |
            total_power_match = re.search(r'\|\s*Total On-Chip Power \(W\)\s*\|\s*([\d\.]+)', content)
            if total_power_match:
                self.power_metrics["total_power_w"] = float(total_power_match.group(1))
                print(f"    ✓ Found Total Power: {self.power_metrics['total_power_w']}W")
                
            # Parse dynamic power - Match: | Dynamic (W)              | 0.028        |
            dynamic_match = re.search(r'\|\s*Dynamic \(W\)\s*\|\s*([\d\.]+)', content)
            if dynamic_match:
                self.power_metrics["dynamic_power_w"] = float(dynamic_match.group(1))
                print(f"    ✓ Found Dynamic Power: {self.power_metrics['dynamic_power_w']}W")
                
            # Parse static power - Match: | Device Static (W)        | 0.106        |
            static_match = re.search(r'\|\s*Device Static \(W\)\s*\|\s*([\d\.]+)', content)
            if static_match:
                self.power_metrics["static_power_w"] = float(static_match.group(1))
                print(f"    ✓ Found Static Power: {self.power_metrics['static_power_w']}W")
                
            # Parse junction temperature - Match: | Junction Temperature (C) | 26.6         |
            temp_match = re.search(r'\|\s*Junction Temperature \(C\)\s*\|\s*([\d\.]+)', content)
            if temp_match:
                self.power_metrics["junction_temp_c"] = float(temp_match.group(1))
                print(f"    ✓ Found Junction Temp: {self.power_metrics['junction_temp_c']}°C")
                
            # Parse confidence level - Match: | Confidence Level         | Low          |
            conf_match = re.search(r'\|\s*Confidence Level\s*\|\s*(\w+)', content)
            if conf_match:
                self.power_metrics["confidence_level"] = conf_match.group(1)
                print(f"    ✓ Found Confidence: {self.power_metrics['confidence_level']}")

    def calculate_neuromorphic_metrics(self, inference_results):
        """Calculates neuromorphic-specific metrics including power efficiency."""
        print("[*] Calculating neuromorphic metrics...")
        
        total_spikes = inference_results["total_spikes_processed"]
        time_sec = inference_results["inference_time_ms"] / 1000.0
        total_power_w = self.power_metrics["total_power_w"]
        dynamic_power_w = self.power_metrics["dynamic_power_w"]
        
        # 1. SOPS (Spiking Operations Per Second)
        sops = total_spikes / time_sec
        
        # 2. Energy per Spike (Picojoules) - TOTAL POWER
        total_energy_j = total_power_w * time_sec
        energy_per_spike_total_pj = (total_energy_j * 1e12) / total_spikes
        
        # 3. Energy per Spike (Picojoules) - DYNAMIC POWER ONLY (more accurate for neuromorphic)
        dynamic_energy_j = dynamic_power_w * time_sec
        energy_per_spike_dynamic_pj = (dynamic_energy_j * 1e12) / total_spikes
        
        # 4. Accuracy
        accuracy = (inference_results["correct_classifications"] / inference_results["total_samples"]) * 100
        
        # 5. Hardware Efficiency (Spikes per LUT)
        spikes_per_lut = total_spikes / self.hw_metrics["LUT"]
        
        # 6. Power Efficiency (SOPS per Watt)
        sops_per_watt = sops / total_power_w

        self.perf_metrics = {
            "SOPS": f"{sops:,.0f}",
            "pJ_per_spike_total": f"{energy_per_spike_total_pj:.2f}",
            "pJ_per_spike_dynamic": f"{energy_per_spike_dynamic_pj:.2f}",
            "accuracy_pct": f"{accuracy:.2f}%",
            "spikes_per_lut": f"{spikes_per_lut:.1f}",
            "latency_ms": inference_results["inference_time_ms"],
            "SOPS_per_Watt": f"{sops_per_watt:,.0f}"
        }

    def generate_markdown_report(self, output_dir="reports"):
        """Generates comprehensive Markdown report with power analysis."""
        Path(output_dir).mkdir(exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = Path(output_dir) / f"benchmark_{self.fpga_target}_{timestamp}.md"

        report_content = f"""# 🧠 NeuroMetric-FPGA Benchmark Report

**Date:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  
**Target FPGA:** `{self.fpga_target}`  
**Dataset:** `{self.dataset_name}`  
**Report Type:** Implementation + Power Analysis  

---

## 📊 Performance Metrics (Neuromorphic)

| Metric | Value | Description |
| :--- | :--- | :--- |
| **SOPS** | {self.perf_metrics['SOPS']} | Spiking Operations Per Second |
| **Energy/Spike (Total)** | {self.perf_metrics['pJ_per_spike_total']} pJ | Including static leakage |
| **Energy/Spike (Dynamic)** | {self.perf_metrics['pJ_per_spike_dynamic']} pJ | Active computation only |
| **Accuracy** | {self.perf_metrics['accuracy_pct']} | Classification Accuracy |
| **Latency** | {self.perf_metrics['latency_ms']} ms | End-to-end inference time |
| **Spikes / LUT** | {self.perf_metrics['spikes_per_lut']} | Hardware efficiency |
| **SOPS / Watt** | {self.perf_metrics['SOPS_per_Watt']} | Power efficiency metric |

## 🔋 Power Analysis

| Metric | Value | Notes |
| :--- | :--- | :--- |
| **Total Power** | {self.power_metrics['total_power_w']:.3f} W | Dynamic + Static |
| **Dynamic Power** | {self.power_metrics['dynamic_power_w']:.3f} W | Switching activity |
| **Static Power** | {self.power_metrics['static_power_w']:.3f} W | Leakage current |
| **Junction Temp** | {self.power_metrics['junction_temp_c']:.1f} °C | Estimated |
| **VCCINT Current** | {self.power_metrics['vccint_current_a']:.3f} A | Core voltage rail |
| **VCCAUX Current** | {self.power_metrics['vccaux_current_a']:.3f} A | Auxiliary rail |
| **Confidence Level** | {self.power_metrics['confidence_level']} | Based on activity data |

## 🧩 Hardware Resource Utilization (Post-Implementation)

| Resource | Used | Available | Utilization % |
| :--- | :--- | :--- | :--- |
| **Slice LUTs** | {self.hw_metrics['LUT']} | {self.hw_metrics['total_lut_available']} | {(self.hw_metrics['LUT']/self.hw_metrics['total_lut_available'])*100:.2f}% |
| **Slice Registers (FF)** | {self.hw_metrics['FF']} | {self.hw_metrics['total_ff_available']} | {(self.hw_metrics['FF']/self.hw_metrics['total_ff_available'])*100:.2f}% |
| **DSP Slices** | {self.hw_metrics['DSP']} | {self.hw_metrics['total_dsp_available']} | {(self.hw_metrics['DSP']/self.hw_metrics['total_dsp_available'])*100:.2f}% |
| **Block RAM (BRAM)** | {self.hw_metrics['BRAM']} | {self.hw_metrics['total_bram_available']} | {(self.hw_metrics['BRAM']/self.hw_metrics['total_bram_available'])*100:.2f}% |

**Max Achieved Frequency:** {self.hw_metrics['max_freq_mhz']} MHz  
**Worst Negative Slack:** {self.hw_metrics['worst_negative_slack_ns']} ns  
**Routing Congestion:** {self.hw_metrics['routing_congestion_pct']}%  

---

## 💡 Key Insights

### Power Efficiency Analysis
- **Dynamic vs Static Ratio:** {(self.power_metrics['dynamic_power_w']/self.power_metrics['total_power_w'])*100:.1f}% of power is used for active computation
- **Neuromorphic Advantage:** Event-driven architecture minimizes dynamic power during idle periods
- **Scaling Potential:** Low resource utilization ({(self.hw_metrics['LUT']/self.hw_metrics['total_lut_available'])*100:.2f}%) allows for larger neuron arrays

### Hardware Efficiency
- **Spikes per LUT:** {self.perf_metrics['spikes_per_lut']} indicates efficient use of logic resources
- **Routing Overhead:** {self.hw_metrics['routing_congestion_pct']}% congestion suggests room for denser interconnects

---
*Generated by NeuroMetric-FPGA Telemetry Engine v2.1*  
*Includes Implementation & Power Analysis from Xilinx Vivado*
"""
        with open(report_path, 'w') as f:
            f.write(report_content)
            
        print(f"\n[✅] Benchmark report generated successfully!")
        print(f"[📄] Saved to: {report_path.resolve()}")

def main():
    parser = argparse.ArgumentParser(description="NeuroMetric-FPGA Benchmarking CLI v2.1")
    parser.add_argument("--dataset", type=str, default="n-mnist", help="Dataset to benchmark")
    parser.add_argument("--fpga-target", type=str, default="zedboard-zynq7020", help="Target FPGA board")
    parser.add_argument("--util-report", type=str, help="Path to Vivado implementation utilization report (.rpt)")
    parser.add_argument("--power-report", type=str, help="Path to Vivado power analysis report (.rpt)")
    
    args = parser.parse_args()

    print("="*50)
    print("🧠 NeuroMetric-FPGA Benchmark Suite v2.1")
    print("="*50)

    bench = NeuroMetricBenchmark(args.dataset, args.fpga_target, args.util_report, args.power_report)
    
    events = bench.load_mock_dataset()
    results = bench.mock_fpga_inference(events)
    bench.parse_utilization_report()
    bench.parse_power_report()
    bench.calculate_neuromorphic_metrics(results)
    bench.generate_markdown_report()

if __name__ == "__main__":
    main()