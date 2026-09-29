# HARDWARE REVISION — Compute Platform Change (Jetson Orin Nano → Raspberry Pi 5)
### Supersedes the compute-related entries in the Canonical Master Solution Document and the AI Architecture Revision

---

## 1. Changes requested

1. **Compute module:** NVIDIA Jetson Orin Nano → Raspberry Pi 5
2. **Video/image transmission:** Confirmed as fiber-optic cable — already the design since the second revision (Decision D-002); no change, terminology standardized

---

## 2. Why this isn't a drop-in swap

The Jetson Orin Nano has a 512-core Ampere GPU with dedicated Tensor Cores, which is what let the AI pipeline run via TensorRT at ~7 ms/frame. The **Raspberry Pi 5 has no GPU capable of AI acceleration** — its VideoCore VII GPU is a display/media GPU, not a CUDA-class compute engine. This means:
- The inference runtime changes from TensorRT to a CPU-optimized framework (**ncnn**, the standard choice for YOLO-class models on ARM CPUs).
- Inference now competes with video encoding and telemetry handling for the same 4 CPU cores, instead of running on a separate GPU — this is a genuine new consideration, not a wash.

## 3. Revised Hardware Specification (compute entry, supersedes Master Doc Part 11)

| Component | Manufacturer | Model | Specification | Purpose | Interface | Voltage | Power | Qty | Cost (Rs.) | Source |
|---|---|---|---|---|---|---|---|---|---|---|
| Edge compute | Raspberry Pi Foundation | Raspberry Pi 5 (4GB or 8GB) | Broadcom BCM2712, quad-core Cortex-A76 @ 2.4 GHz, VideoCore VII GPU (display/media only, no AI acceleration), LPDDR4X RAM | Video/thermal handling, YOLOv8n inference (CPU, via ncnn) | CSI/USB/UART/GPIO, PCIe (for optional NVMe) | 5V (USB-C PD, requires 5V/5A = 27W-rated supply) | ~5-8W typical, up to ~12W peak under sustained load | 1 | 6,500-7,800 (4GB) or 8,500-9,500 (8GB) | Vendor pricing (ThinkRobotics, Zbotic — India retail, 2026) |
| Active cooling | Third-party (Waveshare-class) | Aluminium case with dual cooling fan | Required — Pi 5 throttles under sustained load without it; explicitly non-negotiable in Indian ambient conditions (35-45C summer) per vendor guidance | Prevents thermal throttling | Fan header / case-integrated | 5V | ~0.5-1W | 1 | 500-1,500 | Vendor guidance (Zbotic) |
| Power supply | Official/compatible | 27W USB-C PD (5V/5A) | Standard GaN/PD chargers often fail to negotiate the required 5V/5A profile — a Pi-5-rated supply is required, not assumed compatible | Power delivery | USB-C | 5V/5A | — | 1 | 800-1,200 | Vendor guidance |
| ~~Jetson Orin Nano subsystem~~ | ~~NVIDIA~~ | ~~removed~~ | — | — | — | — | — | — | ~~45,000-71,000~~ | **REMOVED** |
| ~~Jetson active-cooling fan~~ | ~~NVIDIA-ecosystem~~ | ~~removed~~ | — | — | — | — | — | — | ~~1,100~~ | **REMOVED, replaced by Pi 5 cooling above** |

**Net BOM impact: -Rs.36,300 to -Rs.61,900** (removing the Jetson line and its dedicated fan, adding the Pi 5 + cooling + PSU).

## 4. Revised Prototype Cost (supersedes Master Doc Part 30)

| Estimate stage | Value |
|---|---|
| Prior canonical total (Jetson-based) | Rs.1,12,000 - Rs.1,61,000 |
| **Revised total (Raspberry Pi 5-based)** | **Rs.51,700 - Rs.1,04,700** (8GB variant, high end of cooling/PSU range) |

This is a substantial, real cost reduction — the compute subsystem was the single largest BOM line item, and the Pi 5 plus its cooling/PSU accessories comes in under Rs.11,000 total versus the Jetson subsystem's Rs.45,000-71,000. **State this plainly to evaluators as a deliberate cost-vs-compute tradeoff**, not a free win — see Section 6 below for what's actually given up.

## 5. Revised AI Pipeline (supersedes AI Architecture Revision, Parts 9-10)

| Stage | Prior (Jetson) | Revised (Raspberry Pi 5) |
|---|---|---|
| Inference runtime | TensorRT (FP16) | **ncnn** (CPU-optimized ARM inference) |
| Inference location | Dedicated GPU (Ampere, separate from CPU workload) | **CPU (shared with video encoding and telemetry handling)** |
| Benchmarked latency, YOLOv8n | ~7 ms/frame (third-party Jetson Orin Nano benchmarks, cross-checked) | **~50 ms/frame (~20 FPS)**, per cross-checked Q-engineering ncnn benchmarks on Raspberry Pi 5 CPU |
| Margin over thermal camera's frame rate (~8.6 Hz = ~116 ms/frame budget) | Very large (~16x headroom) | **Still comfortable (~2.3x headroom)** — inference alone is not the bottleneck |
| **New consideration** | N/A — GPU and CPU workloads were independent | **CPU contention**: video encode (for the fiber tether) + telemetry passthrough + AI inference now share 4 cores. Individually each is lightweight, but this has not been measured running concurrently — flagged as a new open item, not assumed fine |

**Revised Model Selection table entry:** YOLOv8n remains the selected model (Part 10 of the AI Architecture Revision) — the reasoning (thermal-domain fine-tuning evidence, dataset availability, single-class simplicity) is unchanged. What changes is only the *runtime* (ncnn instead of TensorRT) and the *latency margin* (2.3x instead of 16x headroom). No larger model (YOLOv8s/m) should be considered on this hardware — the CPU-only path has much less headroom to spend on a bigger model than the Jetson did.

## 6. Revised Power Budget (supersedes Master Doc Part 16, compute rows only)

| Component | Prior (Jetson) | Revised (Raspberry Pi 5) |
|---|---|---|
| Compute module | ~7 W avg (5-10 W config, 25 W burst) | **~6-8 W avg (5-12 W range, CPU-bound under concurrent video+AI load)** |
| Compute cooling fan | 0.65 W (Jetson-ecosystem fan) | **~0.5-1 W (Pi 5 case fan)** |
| **Net effect on total power budget** | ~18-25 W average (prior canonical) | **~17-24 W average** — essentially a wash; the Pi 5 draws somewhat less than the Jetson's stated range, but the difference is not large enough to change the battery-sizing conclusion (Master Doc Part 16's 5000-6000 mAh pack target stands unchanged) |

## 7. What's genuinely given up (state this honestly, don't bury it)

| Trade-off | Detail |
|---|---|
| Inference latency margin | 16x headroom (Jetson) → 2.3x headroom (Pi 5) — still adequate, but with much less room to absorb a future model upgrade or added CV task |
| CPU contention | Video encoding and AI inference now share the same 4 cores — not yet measured running concurrently; this is the honest open question this swap introduces |
| No path to a larger/better model later without a hardware change | If production-phase work (AI Architecture Revision, Part 17) ever wants a bigger detector, the Pi 5 has little spare compute to absorb it — a future accelerator add-on (e.g., a Coral USB or Hailo HAT) would become a real option to evaluate at that point, not assumed necessary now |
| Ecosystem/tooling maturity | TensorRT/Jetson tooling is more purpose-built for this exact task than the ncnn/ARM-CPU path, which requires more manual optimization work from the team |

**What's gained:** ~Rs.36,000-62,000 lower prototype cost, and a materially simpler, more widely-available, better-documented single-board computer for a student team to source and debug (Raspberry Pi's software ecosystem and community support significantly exceed Jetson's for a general-purpose Linux workload).

## 8. Updated Decision Log entry (add to Master Doc Part 40)

| Decision ID | Decision | Alternatives considered | Why selected | Evidence |
|---|---|---|---|---|
| D-014 | Raspberry Pi 5 as the edge-compute module, replacing the Jetson Orin Nano | Jetson Orin Nano (prior choice); Raspberry Pi 5 + Coral/Hailo AI accelerator HAT | Cost reduction of ~Rs.36,000-62,000 is decisive for a student-team prototype budget; cross-checked benchmarks confirm YOLOv8n via ncnn still comfortably outpaces the thermal camera's frame rate on Pi 5 CPU alone, so no accelerator HAT is required for the MVP | Q-engineering ncnn benchmark tables (cross-checked across multiple model-family repos); vendor pricing (ThinkRobotics, Zbotic) |

## 9. Updated Assumption Register entry (add to Master Doc Part 41)

| Assumption ID | Assumption | Why needed | Risk | How to validate | Status |
|---|---|---|---|---|---|
| A-010 | Concurrent video encoding + telemetry handling + YOLOv8n inference on the Raspberry Pi 5's 4 CPU cores will not degrade any of the three below acceptable performance | The ncnn benchmark (~20 FPS) measures inference in isolation, not under the rover's actual concurrent workload | If contention is worse than expected, either video frame rate, inference frame rate, or telemetry latency could degrade | Bench test running all three workloads simultaneously on the actual built Pi 5, before relying on the figures in Section 5 above | **Open — new item introduced by this hardware change, should be tested early since it affects a go/no-go on the whole compute choice** |

## 10. Updated Final AI one-liner (10-second version, revised)

> "Our AI is a thermal person-detector running on a Raspberry Pi 5 — a lightweight model (YOLOv8n) that still comfortably outpaces our thermal camera's frame rate on CPU alone, at a fraction of the cost of a GPU-based board."

## 11. Fiber optic cable confirmation

No change required — this has been the primary video/thermal/control path since Decision D-002 (first hostile-review correction). Terminology across the canonical documents uses "fiber-optic tether"; "fiber optic cable" refers to the same component. No architectural, cost, or performance entries change from this second item.
