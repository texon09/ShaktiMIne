# MASTER SOLUTION DOCUMENT

### Project
ShaktiMine — AI-Powered Underground Mine Safety, Monitoring and Rescue System

### SIH Problem Statement
SIH26039 — "AI-Powered Underground Mine Safety, Monitoring and Rescue System" (Theme: Smart Automation; Category: Hardware)

### Version
v1.0 (Canonical)

### Document Status
Canonical Technical Reference — supersedes all prior drafts, reviews, and red-team notes produced during this project's design process. Where earlier drafts conflict with this document, this document governs.

### Last Updated
2026-09-26

### Purpose
Single source of truth for the complete project — problem, architecture, hardware, communications, AI, data, software, security, cost, validation, and evaluator defense — sufficient for any team member, mentor, or LLM to understand, implement, extend, or defend this project without access to prior conversations.

### Intended Users
SIH team; hardware engineers; software/backend developers; AI/ML engineers; designers; mentors; researchers; future LLM instances; SIH evaluators.

---

# PART 1 — EXECUTIVE PROJECT IDENTITY

**1.1 One-line description:** A tethered, sensor-equipped rescue rover that explores hazardous underground coal-mine tunnels ahead of human rescuers, detecting toxic gas, flooding, and trapped workers, and streaming live video and thermal imagery to a surface control station.

**1.2 30-second description:** After a mine incident — gas leak, roof-fall, or flooding — rescue teams cannot safely enter until conditions are known. ShaktiMine is a tracked rover that goes in first: it senses methane, carbon monoxide, oxygen level, temperature, humidity, and standing water; it carries a thermal camera to spot a trapped worker's body heat and an RGB camera for visual reconnaissance; and it sends all of this, live, to a control station at the surface over a fiber-optic tether (with a wireless backup for alerts if the tether is lost). A rescue-team lead uses that feed to decide where it's safe to send people, and where to prioritize the search.

**1.3 100-word description:** ShaktiMine is a hardware-first response to SIH26039: a tracked underground rescue rover carrying three independent combustible-gas sensing technologies (semiconductor, catalytic-bead, and infrared), an electrochemical oxygen sensor, a water-level probe, an RGB camera, and a thermal camera, all managed by an edge-compute module (NVIDIA Jetson Orin Nano) and an independent safety-interlock microcontroller (ESP32). Video, thermal imagery, and control commands travel over a fiber-optic tether — the same approach used by real mine-rescue robots (Sandia's Gemini-Scout, the MSHA Wolverine) — with a LoRa radio link as a telemetry-only backup if the tether is severed. A deterministic rule engine, not a machine-learning model, is the final safety authority.

**1.4 Technical summary:** Tracked ground rover; edge compute (Jetson Orin Nano) + safety MCU (ESP32); triple-redundant, oxygen-arbitrated combustible-gas sensing (MQ-series semiconductor + catalytic-bead pellistor + NDIR) plus electrochemical O2 and a water-level probe; RGB + thermal (FLIR Lepton) cameras; RPLIDAR A1 2D LiDAR for clear-air obstacle mapping only; fiber-optic tether (primary video/control) with LoRa 865-867 MHz backup telemetry; local (no-cloud-required) surface dashboard; deterministic hazard-threshold rule engine as safety authority, with a lightweight thermal-blob detector for trapped-worker detection as human-supervised decision support, never an autonomous trigger.

**1.5 Core problem:** Rescue teams responding to a Jharkhand underground coal-mine incident (gas leak, tunnel collapse, or flooding) cannot safely assess conditions before entering, which increases risk to rescuers and delays response.

**1.6 Target users:** Rescue-team operator (teleoperates the rover, reads the live feed at the surface control station).

**1.7 Stakeholders:** Rescue-team lead / mine safety officer (uses the rover's data to make the entry/no-entry decision); trapped or injured workers (the beneficiaries of a faster, safer response); DGMS - Directorate General of Mines Safety (a potential consumer of post-incident logs, not a real-time system integration requirement).

**1.8 Deployment environment:** Underground coal-mine tunnels, typically 2-2.5 m ceiling height, GPS-denied, RF-hostile (surrounded by lossy/conductive rock), possible dust and smoke, possible standing water, possible rubble/debris obstruction, ambient temperature and humidity that can approach or exceed human body temperature and near-saturation respectively (exact figures unmeasured - see Part 41).

**1.9 Desired outcome:** A human rescue-team lead can make an informed go/no-go entry decision, and prioritize where to search, using the rover's live sensor and video feed - without any person having entered the hazard zone first.

**1.10 Why the problem matters:** Underground coal mining incidents in India cause fatalities from gas, roof-falls, and flooding every year; the specific value of a rover-first approach is removing the single highest-risk moment in a rescue - the first human entry into an unassessed hazard zone - and replacing it with a remotely operated assessment.

---

# PART 2 — OFFICIAL PROBLEM STATEMENT

**PS ID:** SIH26039
**Title:** AI-Powered Underground Mine Safety, Monitoring and Rescue System

**Structured summary of the official PS (paraphrased, not reproduced verbatim in full):** Jharkhand's underground coal mines face toxic gas leaks, tunnel collapses, flooding, and poor visibility. During emergencies, rescue teams lack real-time information about underground conditions, which increases risk and delays response. The PS asks for an intelligent robotic system - a rugged ground rover or a compact aerial drone - capable of operating in hazardous underground mining conditions, equipped with gas sensors, thermal/night-vision cameras, environmental sensors, and wireless communication, to detect toxic gases, monitor temperature/humidity, identify hazards, and assist in locating trapped workers. The system should transmit real-time monitoring data plus live video and thermal imaging to a surface control station, explore inaccessible areas, and provide situational awareness - reducing risk to human rescuers and improving emergency response speed.

### Problem Requirements Table

| ID | Requirement | Source | Type | Priority |
|---|---|---|---|---|
| R-001 | System is a rugged ground rover OR compact aerial drone | PS | Explicit | Critical |
| R-002 | Real-time toxic gas monitoring | PS | Explicit | Critical |
| R-003 | Temperature and humidity monitoring | PS | Explicit | Critical |
| R-004 | Structural condition monitoring | PS | Explicit | High |
| R-005 | Flooding detection | PS | Explicit | High |
| R-006 | Live video transmission to surface control station | PS | Explicit | Critical |
| R-007 | Live thermal imaging transmission to surface control station | PS | Explicit | Critical |
| R-008 | Explore inaccessible underground areas | PS | Explicit | Critical |
| R-009 | Detect hazards | PS | Explicit | Critical |
| R-010 | Assist in locating trapped workers | PS | Explicit | Critical |
| R-011 | Provide situational awareness to rescue teams | PS | Explicit | High |
| R-012 | Reduce risk/exposure to human rescuers | PS | Explicit (stated rationale) | Critical |
| R-013 | Operate despite GPS denial underground | PS | Implied | High |
| R-014 | Operate despite RF-hostile tunnel geometry | PS | Implied | High |
| R-015 | Tolerate dust, humidity, and possible water immersion | PS | Implied | High |
| R-016 | Operable by rescue personnel without robotics expertise | PS | Implied | Medium |
| R-017 | Hazard-threshold alerting | - | Recommended | Medium |
| R-018 | Post-incident data logging in a DGMS-report-compatible format | - | Recommended | Low |
| R-019 | Mine-wide fixed sensor network | - | Optional (explicitly not required) | N/A |
| R-020 | Worker-wearable ecosystem | - | Optional (explicitly not required) | N/A |
| R-021 | Fleet-scale multi-rover deployment | - | Optional (explicitly not required) | N/A |

---

# PART 3 — PROBLEM ANALYSIS

**3.1 Current situation:** When an underground coal-mine incident occurs, rescue teams stage at the surface/pit-head. Ventilation may be disrupted, in-mine communication and lighting may be damaged, and the mine's condition after the incident is unknown even though its layout (from mine survey) is known.

**3.2 Existing workflow:** Rescue teams currently rely on fixed gas-monitoring instrumentation (where installed and surviving), radio communication with anyone still inside, and, historically, human reconnaissance teams entering with personal gas detectors and breathing apparatus once conditions are judged tolerable enough to risk entry.

**3.3 Problems in the current workflow:** The riskiest step - the first human entry to assess conditions - happens before conditions are actually known, which is the core problem the PS is naming.

**3.4 Root causes:** No remote-sensing capability exists that can enter a hazard zone before a human does; fixed mine instrumentation may be damaged or absent in the affected area; radio communication with people already inside may be lost.

**3.5 Stakeholder pain points:** Rescuers bear direct physical risk from unknown gas/structural/flooding conditions; rescue-team leads must make life-or-death entry decisions with incomplete information; trapped workers' survival depends on how quickly and safely they can be located.

**3.6 Technical challenges:** GPS denial; RF-hostile tunnel geometry (documented coal-mine measurements show usable wireless range as low as 13-29 m - see Part 13); dust/smoke degrading both camera and LiDAR sensing; humidity causing sensor condensation; an explosive-gas atmosphere that constrains what electronics can safely be used without certification.

**3.7 Environmental challenges:** Low ceiling height (2-2.5 m typical), uneven/rubble-strewn/possibly flooded floor, ambient temperature/humidity that may reduce the thermal contrast a thermal camera depends on for detecting a person (see Part 12).

**3.8 Operational challenges:** Who trains to operate the rover; who maintains/charges/calibrates it; how it is transported to the incident site; how it is retrieved if disabled underground (see Part 26, Part 31).

**3.9 Data challenges:** Balancing the need for high-bandwidth live video against the poor wireless propagation characteristics of a coal-mine tunnel (see Part 13, Part 14).

**3.10 Why existing approaches are insufficient:** Fixed mine-wide sensor networks (where they exist) don't move and can't provide visual reconnaissance or search a collapsed area; a human reconnaissance team is exactly the risk the PS wants removed; prior mine-rescue robots (Gemini-Scout, Wolverine, Numbat - Part 5) demonstrate the concept works but were lab-built, expensive, and in Numbat's case never operationally deployed, showing this remains an open engineering problem, not a solved one.

---

# PART 4 — USER & STAKEHOLDER MODEL

| Stakeholder | Role | Needs | Problems | Interaction |
|---|---|---|---|---|
| Rescue-team operator (primary user) | Teleoperates the rover from the surface control station | A responsive, intuitive control interface; a trustworthy live feed; clear alerts | Untrained on complex robotics interfaces; must act under time pressure | Direct - joystick/game-controller-style teleop, dashboard viewing |
| Rescue-team lead / mine safety officer (secondary user, decision-maker) | Makes the entry/no-entry decision | Trustworthy, unambiguous hazard state; awareness of sensor confidence/faults | Cannot afford a false "all clear" | Views the dashboard, receives alerts, is the final human authority - the system never auto-authorizes entry |
| Trapped/injured workers | Indirect beneficiary | To be located and characterized before rescuers physically arrive | Cannot self-report if unconscious or without communication | No direct interaction - detected via thermal signature |
| DGMS (Directorate General of Mines Safety) | Regulatory / data consumer | Post-incident data for investigation; assurance that any deployed system meets safety certification standards | Certification of hazardous-area electronics is a real, unresolved requirement for production (see Part 31) | Consumes logs in a DGMS-report-compatible format (production-phase feature, not MVP) |
| Maintenance/technician role (operational, not named in PS) | Charges battery, maintains tether, calibrates gas sensors | Needs a defined procedure (see Part 31 operational feasibility) | Not currently a formally assigned role - an open operational question | Pre/post-mission checks |

---

# PART 5 — EXISTING SOLUTIONS

| Solution | Technology | Strength | Limitation | Relevance |
|---|---|---|---|---|
| Sandia National Laboratories Gemini-Scout Mine Rescue Robot (2011) | Tracked dual-body rover, MSHA-approved multi-gas sensor, thermal + pan/tilt camera, explosion-proof electronics housings, fords 18 in of standing water, wired multi-channel video link | Field-proven concept closely matching this PS; validated sensor suite and water tolerance | Lab-institution-built, high cost, not reproducible on a student budget; not a wireless-video system | Direct precedent for our sensor suite and - critically - our choice of a tethered (not RF) video link |
| MSHA Wolverine (adapted ANDROS military EOD platform) | ~500 kg tracked platform, fiber-optic tether for video | Extreme ruggedness | 500 kg and tethered - poor rapid-deployability, exactly the complaint the PS implicitly responds to | Confirms tethered video as a real, used approach, while showing the failure mode (deployability) our lighter design must avoid |
| CSIRO Numbat (late 1990s) | Teleoperated situational-awareness tool for coal-mine emergencies | Early proof that teleoperated reconnaissance robots are viable for this use case | Never operationally deployed - an open industry question about reliability under real incident conditions | Justifies treating "operational reliability under failure" as a first-class design concern (Part 26/27), not an afterthought |
| Fixed wireless mine-monitoring networks (WPAN/WLAN/LoRa field trials in a working coal mine) | Fixed-node RF instrumentation | Continuous monitoring once installed | Measured usable range only 13 m (WPAN), 17 m (WLAN/Wi-Fi), 28.82 m (LoRa w/ 50 dB gateway antenna) in an actual coal mine | Directly informs our communication architecture decision (Part 13/14) - this is why we do not rely on RF for video |

**We do not claim "no existing solution exists."** Multiple credible prior systems solve close to this exact problem; our contribution is a cost-realistic, India-buildable version with a communication architecture and gas-sensing redundancy design corrected against real coal-mine RF and sensor-failure-mode evidence, not a novel concept.

---

# PART 6 — FINAL PROBLEM-SOLUTION GAP

| Existing Problem | Why Existing Approach Fails | Our Solution | Improvement |
|---|---|---|---|
| Human reconnaissance is the first assessment step | Puts a person into unknown-hazard conditions | Rover-first reconnaissance | Removes the highest-risk moment from the rescue workflow |
| Prior rescue robots (Gemini-Scout, Wolverine) are lab-institution-scale, high-cost systems | Not reproducible/deployable by a resource-constrained team or organization | A ~Rs.1.1-1.6 lakh prototype using COTS components, following the same sensing/tether-video architecture | Demonstrates the same functional concept at a fraction of the cost, with an explicit MVP-to-production roadmap (Part 32) |
| Fixed mine networks don't provide mobile visual reconnaissance | Static instrumentation can't search or see | A mobile rover carrying RGB + thermal cameras | Adds the mobile, visual search capability fixed networks cannot provide |
| Single-technology gas sensors can fail silently (semiconductor sensors have no self-diagnostic fault signal) | A "safety" system with an undetectable failure mode is not actually safe | Triple-redundant, dissimilar-technology gas sensing with oxygen-based arbitration logic (Part 23/24) | Converts an undetectable single point of failure into a system that flags its own sensor disagreement |
| RF video links are commonly assumed reliable underground without evidence | Coal-mine field data shows Wi-Fi/WLAN range as low as 17 m - shorter than what a useful mission radius needs | Fiber-optic tether as the primary, not backup, video/control path | Matches validated precedent (Gemini-Scout, Wolverine) instead of an unproven RF assumption |

---

# PART 7 — FINAL SOLUTION OVERVIEW

**7.1 Concept:** A tethered rover that senses, sees, and reports - the "eyes and sensors" a rescue team would otherwise risk sending in a person to be.

**7.2 Core idea:** Split the problem by data type: low-bandwidth safety-critical telemetry travels over a radio link that survives even if the physical tether is cut; high-bandwidth video/thermal travels over a guaranteed wired path; and the safety-critical hazard logic runs independently of the "smart" compute board, so a software crash cannot silence the alarm system.

**7.3 How it works:** The rover is driven into the tunnel by an operator at the surface, guided by its own live video/thermal feed. Onboard sensors continuously measure gas, oxygen, temperature, humidity, vibration/shock, and water presence. A deterministic rule engine evaluates these readings against fixed regulatory-style thresholds and raises alerts. A thermal-blob detector flags candidate human heat signatures for the operator's attention. All of this - video, thermal, telemetry, alerts - reaches a surface dashboard in real time.

**7.4 Inputs:** CH4/CO/combustible-gas concentration (three independent sensing technologies), O2 concentration, temperature, humidity, vibration/shock (IMU, sampled while stationary), water presence (staged probe), RGB video, thermal video, operator control commands (outbound).

**7.5 Processing:** Sensor polling and the safety-critical rule engine run on an independent MCU (ESP32); video encoding, thermal-frame processing, and the thermal-blob detector run on an edge-compute module (Jetson Orin Nano).

**7.6 AI/ML intelligence:** A lightweight thermal-blob detector (classical image processing, or a small CNN if time permits) flags candidate human heat signatures, biased toward high recall (fewer missed detections, more false alarms accepted as the safer trade-off). An EWMA (exponentially weighted moving average) statistical layer detects gas-concentration trends before they cross a hard alarm threshold. Neither of these is the safety authority - see 7.7.

**7.7 Decision logic:** A deterministic, auditable rule engine is the sole safety authority. It evaluates fixed thresholds (e.g., CH4 >= 1% = warning, >= 2.5% = evacuate - Part 24) and an oxygen-based arbitration rule that determines which combustible-gas sensor's reading to trust at any given moment (Part 24). AI outputs (thermal detection, EWMA trend) are decision support surfaced to the human operator - never an autonomous trigger for any safety action.

**7.8 Outputs:** Live RGB video, live thermal video, real-time telemetry readout, hazard-state indicator (four-level: Normal -> Warning -> Critical -> Emergency), thermal-detection alerts, sensor-fault/disagreement alerts, mission logs.

**7.9 Human interaction:** A rescue-team operator drives the rover and reads the dashboard; a rescue-team lead uses the dashboard's hazard state and video/thermal feed to make the entry/no-entry and prioritization decision. The system never authorizes human entry itself.

**7.10 End-to-end workflow:**
**INPUT** (gas/temp/humidity/shock/water/video/thermal sensors) -> **PROCESSING** (ESP32 sensor polling + Jetson video/thermal handling) -> **INTELLIGENCE** (deterministic rule engine + thermal-blob detector + EWMA trend) -> **DECISION** (four-level hazard state + sensor-arbitration outcome, human-readable) -> **OUTPUT** (dashboard: video, thermal, telemetry, alerts) -> **ACTION** (human rescue-team lead's go/no-go and prioritization decision).

---

# PART 8 — REQUIREMENT-TO-SOLUTION TRACEABILITY

| Req ID | Requirement | Solution Component | Implementation | Validation Method | Status |
|---|---|---|---|---|---|
| R-001 | Rover or drone | Tracked ground rover (Part 9.3/11) | Chassis + motors + tracks | Mobility test (Part 33) | Prototype planned |
| R-002 | Toxic gas monitoring | MQ-4/MQ-7 + pellistor + NDIR + O2 cell (Part 11/12) | Sensor suite wired to ESP32 ADC | Calibration-gas bench test (Part 33) | Prototype planned |
| R-003 | Temp/humidity | DHT22/SHT31 (Part 11) | I2C sensor | Bench comparison to reference thermometer | Prototype planned |
| R-004 | Structural condition | IMU, stationary-sample shock-event flag (Part 12) | MPU6050 on chassis | Shock-event bench test | Prototype planned - capability is explicitly limited, see Part 41 A-006 |
| R-005 | Flooding | Conductive water-level probe (Part 11) | GPIO staged dry/wet/submerged | Water-tray bench test | Prototype planned |
| R-006 | Live video | RGB camera over fiber tether (Part 13) | CSI/USB camera, tether-carried | Glass-to-glass latency test | Prototype planned |
| R-007 | Live thermal | FLIR Lepton over fiber tether (Part 11/12) | SPI+I2C camera, tether-carried | Frame-rate/latency test | Prototype planned |
| R-008 | Explore inaccessible areas | Tracked mobility + teleop | Chassis + RGB/thermal-guided teleop | Obstacle-course mobility test | Prototype planned |
| R-009 | Detect hazards | Deterministic rule engine (Part 24) | ESP32 firmware | Calibration-gas / bench threshold test | Prototype planned |
| R-010 | Locate trapped workers | Thermal-blob detection (Part 20/23) | Jetson-side inference | Recall-focused bench trial (Part 21/33) | Requires validation - no dataset/measurement exists yet (Part 21) |
| R-011 | Situational awareness | Surface dashboard (Part 17) | Local web app | Operator usability walkthrough | Prototype planned |
| R-012 | Reduce rescuer exposure | Entire rover-first architecture | - | N/A - architectural, not a testable subsystem | Implemented by design |
| R-013 | GPS-denied operation | No GNSS dependency anywhere in the design | LiDAR/video-based teleop instead | N/A | Implemented by design |
| R-014 | RF-hostile tolerance | Fiber tether as primary link, LoRa telemetry-only backup (Part 13/14) | - | On-site RF range measurement (Part 33) | Prototype planned; range is unmeasured (Part 41 A-001) |
| R-015 | Dust/humidity/water tolerance | IP-rated enclosure (with the thermal-path correction, Part 11/28) | Passive heatsink through enclosure wall | Environmental exposure test | Prototype planned |
| R-016 | Operable without robotics expertise | Game-controller-style teleop UI (Part 17) | Web dashboard + gamepad input | Operator usability walkthrough | Prototype planned |
| R-017 | Hazard alerting | Four-level hazard state (Part 24) | Rule engine output | Threshold-crossing bench test | Prototype planned |
| R-018 | DGMS-compatible logging | Timestamped CSV/JSON log export | Local append-only log file | Log-format review | Production-only (MVP logs locally in a compatible format but does not integrate live with any DGMS system) |
| R-019 | Mine-wide sensor network | - | - | - | Explicitly out of scope - not required by PS |
| R-020 | Worker wearables | - | - | - | Explicitly out of scope - not required by PS |
| R-021 | Fleet scale | - | - | - | Explicitly out of scope - not required by PS |

---

# PART 9 — SYSTEM ARCHITECTURE

**9.1 High-level architecture:**
```
Physical hazard environment (gas, heat, water, obstacles, trapped worker)
        |
        v
[Sensor Layer] - on-rover: gas x3, O2, temp/humidity, IMU, water, RGB cam, thermal cam, 2D LiDAR
        |
        v
[Edge Compute Layer] - ESP32 (safety-critical polling + rule engine) + Jetson Orin Nano (video/thermal/AI)
        |
        v
[Communication Layer] - Fiber-optic tether (primary: video+thermal+control) + LoRa 865-867 MHz (backup: telemetry+alerts only)
        |
        v
[Surface Control Station] - local dashboard app (no cloud dependency for MVP)
        |
        v
[Human Decision] - rescue-team lead: go/no-go, prioritization
```

**9.2 Component architecture:** See Part 11 (Hardware Specification) for the full component table with interfaces, protocols, and dependencies.

**9.3 Hardware architecture:** Tracked chassis; Jetson Orin Nano (compute); ESP32 (safety MCU); three combustible-gas sensors + one O2 sensor + one temp/humidity sensor + one IMU + one water probe (sensing); RGB camera + FLIR Lepton thermal camera (imaging); RPLIDAR A1 (clear-air mapping aid only); fiber-optic tether + manual-rewind spool (primary comms); SX1276-based LoRa module x2 (backup comms); Li-ion battery pack; passive-heatsink-equipped enclosure.

**9.4 Software architecture:** ESP32 firmware (sensor polling, rule engine, LoRa packet handling); Jetson-side application (video/thermal capture and encode, thermal-blob inference, tether communication handler); surface-station local web application (dashboard frontend + lightweight backend server + local database) - see Part 17.

**9.5 AI architecture:** See Part 20.

**9.6 Communication architecture:** See Part 13/14.

**9.7 Data architecture:** See Part 15, Part 19.

**9.8 Deployment architecture:** MVP = single rover + single surface-station laptop, no cloud, no mine-wide infrastructure. Production = same core architecture plus certified (Ex-rated) hardware and a DGMS-compatible logging/reporting pipeline - see Part 32.

### Component Table (Name / Purpose / Input / Output / Interface / Protocol / Dependencies / Failure Behavior)

| Component | Purpose | Input | Output | Interface | Protocol | Dependencies | Failure behavior |
|---|---|---|---|---|---|---|---|
| ESP32 safety MCU | Poll sensors, run rule engine, manage LoRa | Raw sensor signals | Aggregated frame to Jetson; LoRa packets | ADC/I2C/UART/SPI | Custom binary/JSON over UART | Power, sensors | Continues independently if Jetson fails; never substitutes a "safe" default for a faulted channel |
| Jetson Orin Nano | Video/thermal handling, thermal-blob inference | RGB/thermal frames, ESP32 telemetry frame | Encoded video/thermal to tether, inference results | CSI/USB (camera), SPI+I2C (thermal), UART (ESP32) | RTSP/MJPEG (video), custom binary (telemetry passthrough) | Power, cameras, ESP32 link | On crash: ESP32 keeps safety logic alive; video feed drops, dashboard shows explicit "NO VIDEO" state |
| Fiber-optic tether | Primary video/control link | Encoded video/thermal/control from Jetson | Signal to surface station | Optical fiber | Standard fiber-optic video/data transport | Physical integrity (bend radius, no fracture) | On cut: automatic fallback to LoRa telemetry-only; rover halts and holds position |
| LoRa module (SX1276-based) x2 | Backup telemetry/alerts | Batched sensor frame | RF packet | UART to radio IC | LoRa PHY, custom application-layer packet | India 865-867 MHz band availability | On loss: local buzzer/LED, onboard flash logging continues |
| Surface dashboard app | Operator/decision-maker interface | Video, thermal, telemetry, alerts | Visual/audio display | Local network/USB from tether receiver + LoRa receiver | HTTP/WebSocket (local) | Receiver hardware, local server | Explicit "NO DATA" / "TETHER LOST" states, never a silent freeze |

---

# PART 10 — COMPLETE END-TO-END DATA FLOW

| Stage | Data format | Frequency | Payload | Latency | Protocol | Security | Processing | Output |
|---|---|---|---|---|---|---|---|---|
| Sensors -> ESP32 | Raw analog/digital | 0.5-2 Hz per channel | N/A (raw signal) | <100 ms | ADC/I2C/UART | N/A (physical link) | Threshold/rule evaluation, sensor-arbitration logic | Aggregated JSON/binary frame |
| ESP32 -> Jetson | Aggregated frame incl. SENSOR_FAULT/SENSOR_DISAGREEMENT/LOW_O2_UNRELIABLE flags | 1 Hz | ~20-30 bytes | <200 ms | UART serial | Local wired link, no external exposure | Passthrough + logging | Frame relayed toward tether/LoRa |
| Jetson -> Surface (video/thermal/control) | H.264 video, raw/compressed thermal frame, control commands | 30 fps video / ~8.6 Hz thermal | ~1-3 Mbps video (engineering estimate), ~72-290 kbps thermal | Target <500 ms glass-to-glass (unmeasured) | RTSP/MJPEG over fiber | Pre-shared key pairing (Part 25) | Display, recording | Live dashboard feed |
| Jetson/ESP32 -> LoRa | Batched telemetry + alert packet | ~every 5 s (subject to India duty-cycle verification, Part 41 A-002), immediate on alarm | ~20-30 bytes/packet | Target <1 s for alert | Custom binary over SX1276 | HMAC packet authentication (Part 25) | Store-and-forward with bounded retry (max 2 retries, Part 24) | Dashboard telemetry/alert update |
| Surface receiver -> Dashboard backend | Combined feed | Real-time | N/A | Local (negligible) | HTTP/WebSocket (local) | Local network only for MVP | Aggregation, logging to local DB | Rendered UI |
| Dashboard -> Human | Visual/audio | Real-time | N/A | N/A | UI | N/A | N/A | Go/no-go decision (human) |

---

# PART 11 — HARDWARE SPECIFICATION

| Component | Manufacturer | Model | Specification | Purpose | Interface | Voltage | Power | Qty | Cost (Rs.) | Source |
|---|---|---|---|---|---|---|---|---|---|---|
| Combustible-gas sensor (MOS) | Hanwei Electronics | MQ-4 | 200-10,000 ppm CH4, ~750 mW heater, 24h+ burn-in required | Fast/cheap CH4 trend sensing | Analog/ADC | 5V | 750 mW | 1 | 150-250 | MQ-4 datasheet |
| CO sensor (MOS) | Hanwei Electronics | MQ-7 | Calibrated at 200 ppm ref, 60s/90s heat cycle | CO trend sensing | Analog/ADC | 5V | 350 mW | 1 | 150-250 | MQ-7 datasheet |
| Combustible-gas sensor (catalytic bead) | Generic pellistor module (industrial-equivalent) | - | Requires >=10% vol O2 to function correctly; does not fail-safe | Second, dissimilar-technology combustible-gas check | Analog | 5V | ~200-400 mW | 1 | 1,500-2,500 | Industrial Scientific / Frontline Safety / Fluid Handling Pro technical notes |
| Combustible-gas sensor (NDIR) | Generic NDIR CH4 module | - | Optical absorption, oxygen-independent | Third, oxygen-independent combustible-gas channel - the arbitration backbone | Analog/I2C (module-dependent) | 3.3-5V | ~150-300 mW (engineering estimate) | 1 | 3,000-6,000 | General NDIR sensor technical literature |
| O2 sensor | Generic electrochemical galvanic module | - | 0-25% range, seconds-scale response | Oxygen deficiency detection; arbitrates which combustible-gas channel to trust | Analog | 3.3-5V | ~5 mW | 1 | 800-1,500 | Electrochemical O2 cell technical literature |
| Temp/humidity sensor | Sensirion/Aosong-class | SHT31/DHT22 | +/-0.5C, +/-2-3% RH | Environmental monitoring | I2C/1-wire | 3.3-5V | <5 mW | 1 | 150-400 | Manufacturer datasheet |
| IMU | InvenSense | MPU6050 | +/-16g accel, gyro drift a few deg/s | Stationary-sample shock-event detection | I2C | 3.3V | <50 mW | 1 | 150-600 | Manufacturer datasheet |
| Water-level probe | Generic conductive/float | - | Staged dry/wet/submerged | Flooding detection | GPIO | 3.3-5V | <5 mW | 1 | 100-300 | Generic component |
| RGB camera | Generic CSI/USB module | 1080p-class | 1080p, ~30 fps | Live video reconnaissance | CSI/USB | 5V | ~250 mW | 1 | 1,000-2,500 | Generic component |
| Thermal camera | Teledyne FLIR | Lepton FS (160x120, non-radiometric) or Lepton 3.5 (80x60, radiometric) | LWIR 8-14 um, ~8.6-8.7 Hz frame rate, 150 mW operating / 650 mW during shutter recalibration / 5 mW standby | Trapped-worker heat-signature detection, hot-spot/fire detection | SPI (video) + I2C (control) | 3.3V (module-dependent) | 150 mW operating | 1 | 8,000 (FS) - 28,000 (3.5) | FLIR Lepton datasheet |
| 2D LiDAR | Slamtec | RPLIDAR A1 | 0.15-12 m range, 8000 samples/s, 5.5-10 Hz scan, 360 deg, 785 nm laser triangulation | Clear-air obstacle mapping/teleop assist only (not relied upon for navigation - Part 12) | UART | 5V | 0.5 W, 100 mA | 1 | ~20,000 (landed, import-dependent) | RPLIDAR A1 datasheet |
| Edge compute | NVIDIA | Jetson Orin Nano 4GB (module+carrier+storage+power subsystem) | 6-core Cortex-A78AE, 512-core Ampere GPU, 20 TOPS standard (25-34 TOPS Super mode), 5-10 W (25 W burst) | Video/thermal handling, thermal-blob inference | CSI/USB/UART/GPIO | 5V/12V (module-dependent) | 5-10 W avg | 1 | 45,000-71,000 | NVIDIA/ecosystem-partner documentation |
| Jetson active cooling | NVIDIA-ecosystem (Seeed Studio/Waveshare-class) | Jetson Orin Nano/NX cooling fan | 5V, 0.65 W, ~5500 RPM, PWM speed control | Prevents thermal throttling (Jetson ships with no integrated thermal solution) | 5V header | 5V | 0.65 W | 1 | ~1,100 | Waveshare/Zbotic listing |
| Safety MCU | Espressif | ESP32-WROOM-32 | Dual-core, integrated Wi-Fi/BLE (Wi-Fi unused in this design), ADC/I2C/UART peripherals | Independent sensor polling + rule engine | ADC/I2C/UART/SPI | 3.3V | ~150-250 mW active | 1 | 350-500 | Espressif datasheet |
| LoRa radio module | Semtech-based (e.g., RFM95W/Ra-02) | SX1276-based | 865-867 MHz (India band), up to +20 dBm TX, up to -148 dBm RX sensitivity | Backup telemetry/alerts | UART/SPI to MCU | 3.3V | ~0.1 W avg (idle/short-burst TX) | 2 (rover + base) | 400 each | Semtech SX1276 datasheet |
| Chassis | Generic tracked skid-steer | - | Debris/rubble clearance | Mobility | - | - | - | 1 set | 8,000-15,000 | Generic component/vendor |
| Battery | Generic Li-ion pack + BMS | ~5000-6000 mAh, 3S/4S | Sized to ~24-36 Wh mission energy need + margin | Power | - | 11.1-14.8V nominal | - | 1 | 4,000-6,000 | Generic component |
| Fiber tether + spool | Generic single/multi-mode fiber + manual-rewind reel | Length matched to mission radius (e.g., 100-200 m) | Primary video/control transport | - | Optical | - | - | 1 | 3,000-8,000 | Engineering estimate; needs vendor quote |
| Enclosure | Generic project box + passive heatsink panel | IP54/65-rated body with a thermally-bonded external heatsink panel (not a sealed box with an internal fan/vent) | Dust/splash protection with a resolved thermal path | - | - | - | - | 1 | 1,500-3,000 | Engineering design |
| Prototyping PCB | Generic (small-run board) | - | Sensor integration board | - | - | - | - | 1 | 1,500-3,000 | Generic vendor pricing |
| Calibration gas kit | Generic reference-gas cylinder set | CH4, CO reference concentrations matching alarm thresholds | Required for the team's own validation tests (Part 33) | - | - | - | - | 1 | 2,000-5,000 | Generic vendor pricing |

**Prototype total: approx Rs.1,12,000 - Rs.1,61,000** (see Part 30 for the full cost breakdown and its revision history).

---

# PART 12 — SENSOR ENGINEERING

### Combustible gas (MOS - MQ-4/MQ-7)
- **Measurement principle:** Change in electrical resistance of a tin-dioxide semiconductor surface on exposure to a reducing gas.
- **Operating range:** MQ-4: 200-10,000 ppm CH4. MQ-7: calibrated at 200 ppm CO reference.
- **Sampling rate:** Continuous analog read, polled at 0.5-2 Hz by the ESP32.
- **Accuracy:** Not independently certifiable off-the-shelf - requires per-unit calibration against reference gas; treated as a trend indicator, not a certified absolute reading (low confidence on absolute accuracy).
- **Environmental limitations:** Humidity-sensitive; cross-sensitive to other reducing gases; requires 24-48 hours of continuous power to stabilize (cannot be power-cycled immediately before use); **has no self-diagnostic fault signal - can fail silently (drift, "sleep" state, poisoning).**
- **Calibration:** Bench calibration against a known reference-gas concentration before each mission/demo; recalibration needed if power-cycled.
- **Power:** MQ-4 ~750 mW (heater), MQ-7 ~350 mW (heater, cycled).
- **Why this sensor:** Low cost, fast response, widely documented, appropriate as one of three redundant channels - not as a sole gas-detection method.
- **Source:** Hanwei Electronics MQ-4/MQ-7 datasheets.

### Combustible gas (catalytic bead / pellistor)
- **Measurement principle:** Flameless catalytic combustion of the target gas on a heated bead, sensed via the resulting resistance change.
- **Operating range:** Standard LEL-range combustible-gas detection (methane, propane, hydrogen, and others).
- **Critical limitation:** **Requires >=10% vol. O2 for the catalytic reaction to proceed correctly; below that, readings become falsely low, and - like the MOS sensor - the pellistor does not fail-safe (no fault signal is raised).** This means both gas-sensing technologies can be simultaneously unreliable in an oxygen-deficient emergency, which is why a third, oxygen-independent channel (NDIR) and an oxygen-based arbitration rule are included in this design.
- **Poisoning:** Susceptible to silicone, sulfur, and lead compound poisoning, same failure class as MOS in this respect.
- **Source:** Industrial Scientific/OH&S Online ("Why Do You Need 10% Vol Oxygen to Operate a Catalytic Bead LEL Sensor?"); Frontline Safety; Fluid Handling Pro.

### Combustible gas (NDIR)
- **Measurement principle:** Optical absorption of infrared light by the target gas at a characteristic wavelength - does not require a chemical/catalytic reaction with the target gas, and therefore is **not oxygen-dependent** in the way MOS/pellistor sensors are.
- **Role in this design:** The channel the rule engine falls back on when the O2 reading indicates the pellistor may be unreliable (Part 24).
- **Limitation:** Still does not self-report every possible fault condition - cross-checked against the other two channels' agreement, not treated as infallible.
- **Source:** General NDIR gas-sensor technical literature (industry-standard alternative to catalytic sensing for exactly this failure mode).

### Oxygen (electrochemical)
- **Measurement principle:** Galvanic/electrochemical cell producing a current proportional to O2 concentration.
- **Operating range:** 0-25% typical.
- **Why this sensor class specifically:** Unaffected by the oxygen-dependency issue that affects the combustible-gas sensors, making it the correct arbiter for the sensor-fusion logic in Part 24.

### Thermal camera (FLIR Lepton)
- **Measurement principle:** Uncooled microbolometer array sensing long-wave infrared (LWIR) radiation, 8-14 um.
- **Resolution:** 80x60 px (Lepton 2.5/3.5) or 160x120 px (Lepton FS).
- **Frame rate:** ~8.6-8.7 Hz.
- **Power:** 150 mW operating, 650 mW during a periodic shutter recalibration event, 5 mW standby.
- **Detection geometry (Johnson's Criteria, Lepton 2.5, ~50 deg horizontal FOV, person critical width 0.75 m):** approx 46 m for mere detection (1.5 px across target), approx 11.5 m for recognition as human (6 px across target) - **valid only if the person-to-background thermal contrast is >=2C**, the standard assumption behind Johnson's-Criteria-derived DRI figures.
- **Critical environmental limitation:** Underground mines are thermally stable (isolated from large outdoor-style temperature gradients), which can reduce person-to-background contrast below the 2C assumption these range figures depend on - a documented failure mode for thermal imaging specifically in mine environments. **No detection range number should be presented to evaluators without an on-site or bench-measured delta-T.**
- **Source:** FLIR Lepton datasheet; Johnson's Criteria per Axis/Dahua/FLIR-ecosystem technical documentation; CMU Robotics Institute Field Robotics Center seminar (Bartels) on mine-rescue robot perception limitations.

### 2D LiDAR (RPLIDAR A1)
- **Measurement principle:** 785 nm laser triangulation ranging.
- **Range:** 0.15-12 m. **Sample rate:** 8000 samples/s. **Scan rate:** 5.5-10 Hz, configurable. **Angular coverage:** 360 deg. **Accuracy:** <=1% error to 3 m, <=2% error 3-5 m, <=2.5% error 5-12 m (datasheet).
- **Environmental limitations (critical):** Documented to degrade or fail in dust, smoke, and high humidity/condensation - exactly the condition class the PS's own incident scenario (gas leak -> dust; roof-fall -> dust; flooding -> standing water/humidity) implies. Standing water can also cause laser mirroring/false returns.
- **Role in this design:** Clear-air obstacle-mapping aid for the SIH demo only - **not relied upon as the primary navigation dependency**, which is instead the tether-guaranteed RGB/thermal video feed.
- **Source:** RPLIDAR A1 datasheet; DARPA SubT Finals technical report (Team CERBERUS); underground-mine LiDAR condensation case study (Emesent); Rhino autonomous mine-mapping paper.

---

# PART 13 — COMMUNICATION ENGINEERING

### Technology comparison

| Technology | Range (this environment) | Data rate | Power | Latency | Cost | Suitability |
|---|---|---|---|---|---|---|
| LoRa (865-867 MHz, India) | 13-29 m measured in an actual coal mine (contrast: >1000 m in an unrelated hard-rock waveguide geometry) | Very low (bps-low kbps, overhead-dominated at small payloads) | Very low | Seconds-scale acceptable for telemetry | Low | Telemetry/alerts only - cannot carry video |
| Wi-Fi (2.4 GHz) | 17 m measured (WLAN) in the same coal-mine study - **shorter** than the LoRa figure above | High (Mbps-class) | Moderate-high | Low | Low-moderate | Bandwidth matches video, but measured underground range in coal is not dependable, and is not obviously better than LoRa's |
| Fiber-optic tether | Bounded by spool length (deterministic, not RF-propagation-limited) | Very high (effectively wired) | N/A (no RF power draw) | Very low | Moderate (reel/spool hardware) | **Selected as the primary video/control path** - matches real precedent (Gemini-Scout, Wolverine) |
| BLE/Zigbee | Shorter range than Wi-Fi typically, not evaluated further | Low-moderate | Low | Low | Low | Not selected - no advantage over LoRa for telemetry, no bandwidth advantage over Wi-Fi for video |
| NB-IoT/4G/5G cellular | Underground cellular coverage in an active/incident-affected mine cannot be assumed | Moderate-high | Moderate | Moderate | Requires infrastructure/subscription | Not selected - depends on infrastructure that may not exist or survive the incident |

### Why fiber tether, not RF, for video (decision rationale)
The two real mine-rescue robots closest to this exact PS - Sandia's Gemini-Scout and the MSHA Wolverine - both use a wired/fiber link for video, not RF. Independently, the one coal-mine-specific field measurement available shows Wi-Fi's own underground range (17 m) is **shorter**, not longer, than LoRa's (28.82 m) in that environment - meaning switching to Wi-Fi for bandwidth reasons does not actually guarantee more usable range than the technology being replaced. A tether sidesteps this uncertainty entirely for the data stream (video) that most needs guaranteed delivery for a life-safety decision, at the cost of a bounded mission radius and a mechanical (not RF) failure mode.

### LoRa/SX1276 parameters
- **Frequency (India):** 865-867 MHz, de-licensed under DoT/WPC Short Range Device exemption rules (2021), <=1 W ERP.
- **TX power (design point):** +17 dBm, derated from the SX1276's +20 dBm maximum for margin.
- **RX sensitivity:** Up to -148 dBm (SF12).
- **Bandwidth:** 125 kHz (standard).
- **Spreading factor:** SF9 as the working design point (balance of range and airtime); SF12 available for maximum range at the cost of airtime.
- **Coding rate:** 4/5 (standard default).
- **Airtime consideration:** Real achieved throughput is meaningfully lower than the theoretical bit rate once preamble/header/CRC overhead is counted (a documented real-world 32-byte SF12 packet achieves ~161 bps against a ~293 bps theoretical figure). Packets are batched (multiple sensor channels per packet, ~every 5 s) to amortize this fixed overhead rather than sending one packet per channel.
- **Duty cycle:** **UNKNOWN - REQUIRES VALIDATION.** Whether India's 865-867 MHz de-licensed band carries a duty-cycle restriction analogous to EU868's ~1% has not been independently confirmed against the current WPC notification text in this research. This must be resolved before finalizing the transmission interval (see Part 41, A-002).
- **Antenna:** A compact omni/whip antenna mounted away from the rover's metal chassis body (proximity to a large metal structure detunes and reduces effective antenna gain relative to free-space datasheet figures - basic antenna/ground-plane theory, not something the SX1276 datasheet accounts for).
- **Range (design baseline):** **13-29 m, per the coal-mine field measurement - used as the design baseline in preference to the >1000 m hard-rock figure, because this PS describes a coal mine, not a hard-rock mine.** The team's own on-site RSSI-vs-distance measurement is mandatory before any range figure is presented to evaluators (see Part 33).
- **Retry policy:** Capped at 2 retries per packet, then drop - bounds total airtime regardless of measured packet loss, and regardless of the still-unresolved duty-cycle question.

### Wi-Fi (evaluated, not selected for video)
Standard 2.4 GHz 802.11n/ac parameters apply generically; not used in the final architecture because the one coal-mine-specific field measurement available shows its underground range underperforming LoRa's in that environment, and no on-site measurement supporting a better outcome exists for this project. Retained in this document only as a rejected alternative, for traceability (see Part 40).

### Cellular (evaluated, not selected)
Not selected - underground cellular coverage cannot be assumed to survive an incident, and no infrastructure dependency should be built into a life-safety system's primary path.

---

# PART 14 — LINK BUDGET (LoRa telemetry channel)

**Formula:** Link budget (dB) = TX power (dBm) - RX sensitivity (dBm)

| Parameter | Value | Basis |
|---|---|---|
| TX power | +17 dBm | Design point, derated from SX1276's +20 dBm max |
| RX sensitivity | -148 dBm (SF12) / less negative at lower SF | SX1276 datasheet |
| Theoretical link budget (best case, SF12) | 165 dB (17 - (-148)) | Datasheet arithmetic |
| Antenna gain (both ends) | ~2-3 dBi each, compact omni | Typical for small omni antennas |
| Installed-system correction | Subtract ~3-6 dB for a chassis-mounted antenna's real-world gain loss vs. an idealized isotropic radiator | Engineering estimate - no source gives an exact figure for this specific mounting; **requires an on-site RSSI-vs-distance measurement** |
| Path loss model | Not a simple free-space model - tunnel geometry produces either a waveguide gain zone (hard-rock precedent) or steep NLoS attenuation after a bend (documented two-zone structure in tunnel RF propagation research) | Research-derived, site-dependent |
| **Real-world range used as design baseline** | **13-29 m** (coal-mine field measurement) | **This is the number to plan a mission radius around - not the 165 dB theoretical ceiling, which is a chip-level figure, not an installed-system range** |
| Fade margin | Not separately quantified - folded into the conservative use of the field-measured range rather than the theoretical link budget | Requires experimental characterization |

---

# PART 15 — DATA BUDGET

| Stream | Rate | Payload/sample | Data rate |
|---|---|---|---|
| Telemetry (gas x3, O2, temp, humidity, shock flag, water) - LoRa | Batched, 1 packet/~5 s | ~20-30 bytes/packet | ~4-6 bytes/s = ~32-48 bps - well within LoRa's throughput even after overhead |
| Video (RGB, H.264) - tether | 1080p @ 30 fps compressed | N/A (streamed) | ~1-3 Mbps (engineering estimate, encoder/scene-dependent) |
| Thermal - tether | 80x60 or 160x120 px @ ~8.6 Hz, 14-bit raw | ~8.4 kbit/frame (80x60) to ~33.6 kbit/frame (160x120) | ~72 kbps (80x60) to ~290 kbps (160x120) |
| **Total tether bandwidth need** | - | - | **~1.1-3.3 Mbps**, comfortably within standard fiber-optic video/data transport capacity |
| Local log storage (surface station) | Continuous telemetry + event log, no raw video archived by default in MVP | ~50 bytes/s telemetry log | ~4.3 MB/day telemetry-only - negligible; video recording, if enabled, is the dominant storage driver and sized per mission duration and codec bitrate at deployment time |

---

# PART 16 — POWER BUDGET

| Component | Active power | Idle power | Duty cycle | Average power |
|---|---|---|---|---|
| Jetson Orin Nano | 5-10 W (25 W burst) | ~2-3 W (estimate) | Continuous during mission | ~7 W |
| Jetson cooling fan | 0.65 W | 0.65 W (typically always-on during operation) | Continuous | 0.65 W |
| ESP32 | ~0.2-0.25 W | ~0.05 W | Continuous | ~0.2 W |
| RPLIDAR A1 | 0.5 W | N/A | Continuous when active | 0.5 W |
| FLIR Lepton | 0.15 W operating, 0.65 W during shutter events, 0.005 W standby | 0.005 W | Continuous when active | ~0.15-0.2 W |
| RGB camera | ~0.25 W | ~0.05 W | Continuous | 0.25 W |
| Gas sensor heaters (MQ-4 + MQ-7 + pellistor) | ~1.3-1.5 W combined | N/A (heaters run continuously) | Continuous | ~1.3-1.5 W |
| O2 electrochemical cell | ~0.005 W | ~0.005 W | Continuous (passive) | ~0.005 W |
| NDIR sensor | ~0.15-0.3 W (engineering estimate) | - | Continuous | ~0.2 W |
| LoRa module | ~0.1 W avg (idle/short-burst TX) | ~0.01 W | Mostly idle, brief TX bursts | ~0.1 W |
| Motors (driving) | 8-15 W | ~0 W (stopped) | Variable, terrain-dependent | requires measurement on built chassis |
| **Total average (moving + sensing + streaming)** | - | - | - | **~18-25 W** (aggregate engineering estimate) |
| **Peak (motor stall + shutter event + burst inference)** | - | - | - | **~35-40 W** (aggregate engineering estimate) |

**Battery sizing:** For a target 60-90 minute mission (engineering assumption, not PS-specified) at ~20-25 W average: energy needed approx 20-37.5 Wh. A 5000-6000 mAh Li-ion pack (~55-65 Wh nominal, ~70% usable after derating) covers this with margin for peak draw.

**Theoretical calculation vs. measured prototype result:** All figures in this table are calculated/datasheet-derived. **No measured runtime exists yet.** This must be tested on the built chassis (Part 33) before any runtime figure is presented as fact rather than a target.

---

# PART 17 — SOFTWARE ARCHITECTURE

### Frontend (Surface Dashboard)
- **Framework:** A lightweight local web application (plain HTML/JS or a minimal React app), served locally - no cloud dependency required for the MVP.
- **Pages:** (1) Live view - video + thermal feed side by side; (2) Telemetry panel - gas/O2/temp/humidity/shock/water readouts with the current hazard state (Normal/Warning/Critical/Emergency); (3) Alert log - timestamped history of alerts and sensor-fault/disagreement events; (4) Control panel - teleop input (gamepad-style) and rover status (battery, link state: tether/LoRa-fallback).
- **State management:** Simple client-side state reflecting the latest received telemetry frame and connection status; no complex state library required at MVP scale.
- **Visualization:** Live video/thermal panels; a simple time-series readout for gas trend (supporting the EWMA-based early-warning feature, Part 20); a four-level hazard-state indicator (color-coded).

### Backend
- **Framework:** A lightweight local server (e.g., a minimal Python-based HTTP/WebSocket server) running on the same laptop as the dashboard - receives data from the tether interface and the LoRa receiver, forwards it to the frontend, and writes to the local database.
- **Services:** Telemetry ingestion service; video/thermal relay service; alert/log service.
- **APIs:** See Part 18.
- **Authentication:** Not required for the MVP (single-operator, local-network-only tool); see Part 25 for what security is actually needed at this scale.
- **Processing:** Applies the rule engine's already-computed hazard state (computed on the ESP32, not recomputed in software) - the backend's role is display/logging, not re-deriving safety-critical decisions.

### Database
- **Technology:** SQLite (local file-based) for the MVP - sufficient for a single-operator, single-mission tool with no concurrent multi-user access requirement. See Part 19 for schema. Production phase would move to PostgreSQL/TimescaleDB for multi-mission, multi-team, DGMS-reporting-compatible storage (not required for MVP).

### Infrastructure
- **Cloud:** None required for MVP - deliberately, to avoid a network dependency the mine environment cannot guarantee. Production phase may add cloud/DGMS-reporting integration as a separate, non-safety-critical service.
- **Edge:** ESP32 (safety logic) + Jetson Orin Nano (video/AI) - both physically on the rover.
- **Storage:** Local disk on the surface-station laptop for the MVP.
- **Deployment:** Local application run directly on the operator's laptop; no server infrastructure to provision.
- **Monitoring:** Basic health indicators in the dashboard itself (link status, battery level, sensor-fault flags) - no separate monitoring stack required at this scale.

---

# PART 18 — API SPECIFICATION

*(Local API, surface-station backend <-> frontend - not internet-exposed for the MVP)*

### GET /api/telemetry/latest
- **Method:** GET
- **Authentication:** None (local-only, MVP)
- **Input:** None
- **Output (example):**
```json
{
  "timestamp": "2026-09-26T10:15:32Z",
  "gas": {"ch4_mos_ppm": 850, "ch4_ndir_ppm": 900, "combustible_pellistor_pct_lel": 12, "co_ppm": 15},
  "o2_pct": 20.5,
  "temp_c": 29.4,
  "humidity_pct": 88,
  "water_state": "dry",
  "shock_event": false,
  "hazard_state": "NORMAL",
  "sensor_flags": {"ch4_sensor_disagreement": false, "low_o2_unreliable": false, "sensor_fault": []},
  "link_status": {"tether": "connected", "lora": "standby"}
}
```
- **Validation:** Timestamp and hazard_state are required fields; malformed frames are logged and discarded, not displayed as if valid.
- **Error responses:** 503 if no telemetry received within the expected interval (surfaces the "NO DATA" dashboard state described in Part 10).
- **Purpose:** Feeds the dashboard's telemetry panel.

### GET /api/alerts
- **Method:** GET
- **Authentication:** None (local-only, MVP)
- **Input:** Optional query params `since` (timestamp)
- **Output:** Array of alert objects `{timestamp, type, message, hazard_state}`
- **Purpose:** Feeds the alert log panel.

### POST /api/control
- **Method:** POST
- **Authentication:** Pre-shared key header (Part 25) - this is the one endpoint that actually commands the rover, so it is the one endpoint given the authentication mechanism
- **Input:** `{"command": "forward|backward|left|right|stop", "duration_ms": 200}`
- **Output:** `{"status": "accepted"}` or `{"status": "rejected", "reason": "..."}`
- **Validation:** Command must be one of the allowed enum values; duration capped to a safe maximum.
- **Error responses:** 401 if the pre-shared key is missing/invalid; 400 for a malformed command.
- **Purpose:** Sends teleop commands from the dashboard to the rover over the tether.

### GET /api/video and GET /api/thermal
- **Method:** GET (stream)
- **Authentication:** None (local-only, MVP)
- **Output:** MJPEG/RTSP stream
- **Purpose:** Feeds the live video/thermal panels.

---

# PART 19 — DATABASE SPECIFICATION

**Technology:** SQLite (MVP) -> PostgreSQL/TimescaleDB (production, not required for MVP)

### Table: sensor_readings
| Field | Datatype | Key | Constraints | Purpose |
|---|---|---|---|---|
| id | INTEGER | PK | AUTOINCREMENT | Row identifier |
| timestamp | TEXT (ISO 8601) | - | NOT NULL | When the reading was taken |
| ch4_mos_ppm | REAL | - | - | MQ-4 reading |
| ch4_ndir_ppm | REAL | - | - | NDIR reading |
| combustible_pellistor_pct_lel | REAL | - | - | Pellistor reading |
| co_ppm | REAL | - | - | MQ-7 reading |
| o2_pct | REAL | - | - | Electrochemical O2 reading |
| temp_c | REAL | - | - | Temperature |
| humidity_pct | REAL | - | - | Humidity |
| water_state | TEXT | - | ENUM('dry','wet','submerged') | Flood detection state |
| shock_event | INTEGER (bool) | - | - | IMU stationary-sample shock flag |
| hazard_state | TEXT | - | ENUM('NORMAL','WARNING','CRITICAL','EMERGENCY') | Rule-engine output |

### Table: alerts
| Field | Datatype | Key | Constraints | Purpose |
|---|---|---|---|---|
| id | INTEGER | PK | AUTOINCREMENT | Row identifier |
| timestamp | TEXT | - | NOT NULL | When raised |
| type | TEXT | - | ENUM('HAZARD','SENSOR_FAULT','SENSOR_DISAGREEMENT','LOW_O2_UNRELIABLE','THERMAL_DETECTION','LINK_LOST') | Alert category |
| message | TEXT | - | - | Human-readable description |
| hazard_state | TEXT | - | - | Hazard state at time of alert |

### Table: missions
| Field | Datatype | Key | Constraints | Purpose |
|---|---|---|---|---|
| id | INTEGER | PK | AUTOINCREMENT | Mission identifier |
| start_time | TEXT | - | NOT NULL | Mission start |
| end_time | TEXT | - | - | Mission end |
| operator_notes | TEXT | - | - | Free-text operator log |

### Table: sensor_calibration_log
| Field | Datatype | Key | Constraints | Purpose |
|---|---|---|---|---|
| id | INTEGER | PK | AUTOINCREMENT | Row identifier |
| sensor | TEXT | - | NOT NULL | Which sensor was calibrated |
| calibration_timestamp | TEXT | - | NOT NULL | When calibration was performed |
| reference_gas_ppm | REAL | - | - | Reference concentration used |
| notes | TEXT | - | - | Calibration notes |

**Relationships:** `sensor_readings` and `alerts` both belong to a `missions` row via a `mission_id` foreign key (omitted above for brevity, added at implementation time).

---

# PART 20 — AI/ML ARCHITECTURE

**Data acquisition:** Thermal frames from the FLIR Lepton, captured during bench tests and (if scheduled) an on-site/mock-tunnel test.

**Dataset:** **None exists yet.** No thermal-detection training or validation dataset has been collected as of this document's writing. See Part 21.

**Data preprocessing:** For the MVP (rule-based blob detection): background subtraction/thresholding on the thermal frame within a temperature band consistent with human skin (~30-37C surface, accounting for clothing), followed by size/shape filtering to reject small non-human hot spots (e.g., electrical equipment). For the stretch-goal CNN approach: frame normalization and resizing to the model's expected input size.

**Feature engineering:** For the rule-based approach, the "feature" is simply the thresholded blob's pixel-count and aspect ratio. For the CNN approach, features are learned by the network.

**Model selection - decision rationale:**
| Approach | Considered for | Selected? | Why |
|---|---|---|---|
| Rule-based thresholding + blob filtering | Thermal person detection (MVP) | **Yes** | Simple, explainable, requires no training data, deployable immediately, appropriate given the dataset gap (Part 21) |
| Lightweight CNN (MobileNet-class, <5 MB) | Thermal person detection (stretch goal) | Conditional - only if time and a labeled dataset permit | Could improve accuracy over pure thresholding but requires data the team does not yet have |
| EWMA (statistical) | Gas concentration trend detection | **Yes** | Cheap to compute on ESP32, adds early-warning value on top of deterministic thresholds without replacing them |
| Rule-based deterministic thresholds | Hazard alarm logic (gas, water, shock) | **Yes** | Thresholds are already defined by regulation/physics; a rule engine is fully auditable to a safety inspector, unlike a black-box classifier, for a life-safety decision |
| Random Forest / XGBoost / SVM / LSTM / Transformer | Any subsystem | **No** | Rejected across the board - gas/water/shock signals are low-dimensional with physically-derived thresholds (a classical-ML/deep-learning model would be disproportionate complexity, i.e. "AI for AI's sake"); thermal detection's data gap makes any trained model currently unvalidatable regardless of architecture |

**Training:** N/A for the MVP rule-based detector (no training required). If the CNN stretch goal is pursued: transfer learning from a MobileNet-class backbone, fine-tuned on the team's own collected thermal dataset once it exists.

**Validation / Testing:** See Part 21, Part 22, Part 33.

**Inference:** Runs on the Jetson Orin Nano (edge inference - no cloud dependency, consistent with the no-cloud-for-MVP architecture decision).

**Deployment:** Onboard the rover, as part of the Jetson-side application (Part 9.4).

**Monitoring:** The dashboard surfaces every thermal-detection alert to the human operator, who confirms or dismisses it - this human-in-the-loop step is itself the monitoring mechanism for model performance during operation (formal drift/monitoring infrastructure is out of scope for MVP).

**Model specification (thermal-blob detector, MVP rule-based version):**
- **Architecture:** Threshold + connected-component blob analysis (not a neural network).
- **Inputs:** Single thermal frame (80x60 or 160x120 px, per the selected Lepton variant).
- **Outputs:** Bounding box(es) around candidate human-heat-signature blobs, with a confidence proxy derived from blob size/temperature consistency.
- **Parameters:** Temperature threshold band, minimum/maximum blob size (in pixels), aspect-ratio filter - all tunable constants, not learned weights.
- **Computational requirements:** Negligible relative to the Jetson's capacity - this runs comfortably even without invoking the GPU.
- **Model size:** N/A (not a trained model).
- **Latency:** **UNKNOWN - REQUIRES MEASUREMENT** (Part 33).
- **Metrics:** See Part 22.

---

# PART 21 — AI DATASET

- **Dataset source:** None collected yet.
- **Number of samples:** 0.
- **Classes:** Intended: "person present" / "person absent," with sub-cases for partial occlusion and low thermal contrast.
- **Labels:** None yet - would be manually annotated bounding boxes on collected thermal frames.
- **Sampling:** Not yet defined.
- **Class balance:** Expected imbalance (far more "absent" than "present" frames in any bench collection) - the team should deliberately over-sample "present, partially occluded, low-contrast" cases specifically, since that is the highest-risk failure mode.
- **Train/validation/test split:** Not yet defined - no data exists to split.
- **Augmentation:** Not yet planned.
- **Synthetic data:** Not used; not currently planned.
- **Limitations:** **This is the single largest unresolved gap in the AI portion of the project.** No accuracy, precision, recall, or any other performance number should be presented in any external-facing document (including the SIH PPT) until this dataset is collected and a bench trial is run (Part 33).
- **Expected domain shift:** A dataset collected in a bench/room setting will not automatically generalize to an actual mine tunnel's thermal background (different clutter, different baseline ambient temperature) - this is stated as an open validation gap, not implied to be solved by a bench test alone.

---

# PART 22 — AI PERFORMANCE

| Metric | Literature | Target | Actual |
|---|---|---|---|
| Thermal detection recall | Not independently benchmarked for this exact sensor/environment combination in the sources reviewed | Bias design toward high recall (accept more false positives to minimize missed detections) - no specific numeric target set, pending Part 33's bench trial | N/A - requires experiment |
| Thermal detection precision | - | Secondary to recall for this application | N/A - requires experiment |
| Detection/recognition range (Johnson's Criteria geometry) | ~46 m detection / ~11.5 m recognition (geometric calculation, assuming >=2C contrast) | Same, contingent on a measured delta-T meeting that assumption | N/A - requires on-site/bench delta-T measurement |
| Inference latency (Jetson) | - | Sub-second, informal target | N/A - requires measurement |
| EWMA gas-trend false-positive rate (on stable readings) | - | Low enough not to desensitize the operator to alerts | N/A - requires bench test |

**No literature result should be read as our achieved result. No target should be read as our achieved result. Every "Actual" cell above is honestly N/A because no experiment has been run yet.**

---

# PART 23 — ALGORITHMS

### Algorithm 1 - Deterministic Hazard Rule Engine (runs on ESP32)
**Purpose:** Sole safety authority; converts raw sensor readings into a four-level hazard state.
**Inputs:** ch4_mos_ppm, ch4_ndir_ppm, combustible_pellistor_pct_lel, co_ppm, o2_pct, temp_c, humidity_pct, water_state, shock_event.
**Outputs:** hazard_state in {NORMAL, WARNING, CRITICAL, EMERGENCY}, plus sensor_flags.

**Pseudocode:**
```
function evaluate_hazard(readings):
    flags = {}

    # Oxygen-based arbitration (Part 24 detail)
    if readings.o2_pct < 10.0:
        flags["low_o2_unreliable"] = True
        trusted_combustible = max(readings.ch4_mos_ppm_normalized, readings.ch4_ndir_ppm_normalized)
        # pellistor reading is disregarded when O2 < 10% per its documented failure mode
    else:
        flags["low_o2_unreliable"] = False
        trusted_combustible = median(readings.ch4_mos_ppm_normalized,
                                      readings.ch4_ndir_ppm_normalized,
                                      readings.combustible_pellistor_pct_lel_normalized)

    # Sensor disagreement check
    if abs(readings.ch4_mos_ppm_normalized - readings.ch4_ndir_ppm_normalized) > DISAGREEMENT_THRESHOLD:
        flags["sensor_disagreement"] = True
    else:
        flags["sensor_disagreement"] = False

    # Deterministic thresholds
    if trusted_combustible >= EVACUATE_THRESHOLD or readings.o2_pct < 19.5 or readings.water_state == "submerged":
        state = "EMERGENCY"
    elif trusted_combustible >= WARNING_THRESHOLD or readings.o2_pct < 20.5 or readings.water_state == "wet" or flags["sensor_disagreement"]:
        state = "WARNING"
    elif flags["low_o2_unreliable"]:
        state = "WARNING"   # treat sensor-trust degradation itself as a warning-level event
    else:
        state = "NORMAL"

    return state, flags
```
**Complexity:** O(1) per evaluation cycle - negligible on an ESP32.
**Edge cases:** A sensor read timeout is treated as SENSOR_FAULT, which is itself folded into at least a WARNING state - never silently ignored or defaulted to "safe."

### Algorithm 2 - EWMA Gas Trend Detector (runs on ESP32 or Jetson)
**Purpose:** Early-warning trend detection below hard alarm thresholds.
**Formula:** `EWMA_t = alpha * reading_t + (1 - alpha) * EWMA_(t-1)`, with alpha a tunable smoothing constant (requires bench tuning - no source specifies a universal correct value for this application).
**Alert condition:** If `(EWMA_t - EWMA_(t-n)) / n` exceeds a rate-of-change threshold (requires experimental determination), raise a "rising trend" advisory distinct from the hard-threshold hazard state.

### Algorithm 3 - Thermal Blob Detection (runs on Jetson)
**Purpose:** Flag candidate human heat signatures.
**Pseudocode:**
```
function detect_person(thermal_frame):
    mask = threshold(thermal_frame, T_MIN_SKIN, T_MAX_SKIN)  # e.g., ~30-37 C band
    blobs = connected_components(mask)
    candidates = []
    for blob in blobs:
        if MIN_BLOB_SIZE <= blob.pixel_count <= MAX_BLOB_SIZE and blob.aspect_ratio_within(HUMAN_RANGE):
            candidates.append(blob)
    return candidates  # surfaced to operator as alerts, never auto-actioned
```
**Complexity:** O(pixels) per frame - trivial for the Jetson's compute budget.
**Edge cases:** A blob at the temperature band's edge, or one whose size fluctuates near the threshold, should generate a lower-confidence flag rather than being silently dropped - biasing toward recall as designed.

---

# PART 24 — DECISION ENGINE

**Thresholds (deterministic, auditable):**
- Combustible gas (trusted channel, see arbitration below): WARNING >= 1% (of LEL-equivalent concentration), EMERGENCY >= 2.5% - consistent with international regulatory precedent (methane LEL is 5-15% by volume; alarm thresholds are set with a large safety margin below that).
- O2: WARNING < 20.5%, EMERGENCY < 19.5% (standard atmospheric O2 is ~20.9%; these are conservative early-warning margins, engineering assumption pending confirmation against the current India-specific DGMS regulation text, which was not independently re-verified in this research pass).
- Water: WARNING = "wet," EMERGENCY = "submerged."
- Sensor disagreement between MOS and NDIR combustible-gas channels beyond a defined tolerance: WARNING (treated as a trust-degradation event, not a hazard-magnitude event, but escalated regardless because an untrustworthy reading is itself unsafe to act on confidently).

**Confidence:** Not a probabilistic confidence score in this design - the rule engine is deterministic. "Confidence" in the practical sense is represented by the sensor_flags (e.g., low_o2_unreliable) that tell the operator how much to trust the displayed reading, not a numeric percentage.

**Sensor-channel arbitration logic (the core fix identified during red-team review):** The electrochemical O2 reading determines which combustible-gas channel(s) the rule engine trusts:
- **O2 >= 10%:** All three combustible-gas channels (MOS, pellistor, NDIR) are valid; the rule engine uses their median to reduce the influence of any single sensor's drift.
- **O2 < 10%:** The pellistor's documented failure mode (falsely low readings below this O2 threshold) makes it untrustworthy; the rule engine automatically **excludes the pellistor** and uses the maximum of the MOS and NDIR readings (biasing toward the more conservative/higher reading when sensor trust is reduced, consistent with a fail-conservative design philosophy).
- This arbitration outcome is itself surfaced to the operator (low_o2_unreliable flag) - never silently handled in the background.

**Prioritization:** EMERGENCY-level conditions override WARNING-level display priority on the dashboard; multiple simultaneous WARNING conditions (e.g., gas trend + sensor disagreement) are all displayed, not merged into a single ambiguous indicator.

**Escalation:** State transitions are logged with timestamps (Part 19, alerts table); no automatic notification beyond the local dashboard is part of the MVP (e.g., no automatic SMS/radio dispatch - that is a human action taken after seeing the dashboard, not a system feature).

**Human override:** The system never autonomously authorizes rover progression past a hazard or authorizes human entry - every consequential action (continuing the mission, deciding to send rescuers) is a human decision informed by, not made by, this system.

---

# PART 25 — SECURITY

Scoped deliberately to what a single-operator, local-network, life-safety field tool actually needs - not a generic enterprise security checklist.

- **Device identity / authentication:** Pre-shared key pairing between the rover's control-command channel and the operator console - prevents accidental or malicious control by another radio/device in range.
- **Encryption:** Not applied to the local video/telemetry display path (local physical/tether link, not internet-exposed); the LoRa backup channel's alert/telemetry packets carry a lightweight HMAC (computable cheaply even on the ESP32) for authentication, since these are the packets that survive tether loss and could otherwise be spoofed by another radio.
- **TLS:** Not applicable - no internet-facing API exists in the MVP.
- **API security:** The one command-issuing endpoint (POST /api/control, Part 18) requires the pre-shared key; read-only local endpoints do not, since they are not internet-exposed and pose no actuation risk.
- **RBAC:** Not implemented for MVP - a single-operator, single-rover field tool has no multi-user access-control requirement; this belongs to a production multi-team deployment.
- **Database security:** Local SQLite file, not network-exposed; production-phase migration to a networked database would require standard credential/access controls at that time.
- **Key management:** Pre-shared key stored locally on both the rover's MCU and the operator console; rotated per mission as a simple operational procedure (no PKI infrastructure needed at this scale).
- **Firmware security:** Not hardened against sophisticated attack in the MVP - the threat model here is accidental interference (another radio in range), not a nation-state adversary; stated honestly rather than over-engineered.
- **Logging / audit:** Append-only local log file (Part 19 alerts/sensor_readings tables) with timestamps - a DGMS-relevant audit trail at low implementation cost.
- **Privacy:** No personal data is collected about the operator or any bystander; thermal imagery of a located worker is used solely for the rescue purpose and retained only in mission logs, not transmitted or stored beyond the local system in the MVP.

---

# PART 26 — FAILURE MODES

| Failure | Detection | Effect | Mitigation | Recovery |
|---|---|---|---|---|
| MOS gas sensor fails silently (poisoning, "sleep" state, humidity saturation) | No self-diagnostic - detected only via disagreement with the NDIR channel | Could produce an undetected false "all clear" if used alone | Median/arbitration logic across three dissimilar sensors (Part 24) | Replace/recalibrate sensor post-mission |
| Pellistor reads falsely low in O2-deficient atmosphere | O2 reading < 10% triggers automatic exclusion | Would otherwise mask a real high gas concentration during exactly the worst-case scenario | O2-threshold arbitration logic (Part 24) excludes the pellistor below 10% O2 | N/A - architectural fix, not a repair |
| Noisy/drifting sensor reading generally | Rule engine's disagreement check | Could trigger false WARNING states | Disagreement is itself surfaced as an alert, not hidden - operator is informed rather than misled | Recalibration |
| Fiber tether cut/severed | Sudden total loss of video with telemetry still alive via LoRa (distinct signature) | Loss of the primary situational-awareness feed | Automatic fallback to LoRa telemetry-only; rover halts and holds position rather than continuing blind | Manual retrieval and tether replacement - not fixable mid-mission |
| Fiber tether fractured internally with no visible external damage | Pre-mission optical continuity check (mandatory procedure); mid-mission, same signature as a clean cut | Same as above | Same as above, plus the pre-mission check catches this before the mission starts | Same as above |
| LoRa link also lost (worst case, both channels down) | No telemetry at all reaches the dashboard | Total loss of remote awareness | Local buzzer/LED on the rover (audible/visible to anyone nearby); onboard flash logging continues for post-recovery data retrieval | Physical retrieval of the rover |
| LiDAR degraded by dust/smoke/condensation | Not specifically instrumented - treated as an accepted limitation, not something to detect and compensate for | Loss of the (non-critical) clear-air mapping aid | Operator relies on the tether-guaranteed RGB/thermal video feed for navigation instead - LiDAR was never the primary navigation dependency | N/A |
| Thermal false negative (missed detection, e.g., low-contrast environment) | Not self-detecting - mitigated by human supervision | A trapped worker could be missed by the automated detector | Human operator watches the live thermal feed directly; detector is recall-biased to minimize (not eliminate) this risk | N/A - inherent limitation, disclosed |
| Jetson software crash | ESP32 continues independently | Loss of video/AI, safety logic unaffected | Rule engine keeps running on the ESP32 regardless of Jetson state | Jetson restart |
| Battery depletion mid-mission | Low-charge telemetry warning well before depletion | Mission must be aborted | Tether can assist physical retrieval - an acknowledged, industry-wide unsolved problem for teleoperated rovers, not claimed solved here | Physical retrieval |
| Mechanical/hardware damage (rover stuck, flipped, submerged beyond rating) | Loss of expected telemetry/mobility response | Mission abort | Accepted, disclosed limitation shared by real precedent systems (Gemini-Scout, Wolverine) | Physical retrieval |
| Cyberattack on the control link | Pre-shared key / HMAC authentication failure | Command rejected | See Part 25 | N/A |
| Enclosure thermal failure (Jetson throttles/shuts down due to inadequate cooling) | Jetson performance/telemetry degradation | Video/AI degradation | Passive heatsink bonded through the enclosure wall (Part 11/28), not a sealed box with no thermal path | Design-time fix, not a runtime recovery |

---

# PART 27 — RELIABILITY

- **Redundancy:** Three dissimilar combustible-gas sensing technologies with oxygen-based arbitration (Part 24); an independent safety MCU (ESP32) separate from the AI/video compute (Jetson); a wireless backup (LoRa) for the primary wired link (tether).
- **Retries:** LoRa packet retries capped at 2 attempts, then dropped - bounds airtime rather than retrying indefinitely.
- **Buffering:** Onboard flash logging on the rover continues even if both communication links are lost, for post-recovery data retrieval.
- **Offline mode:** The rover's rule engine and local logging function entirely independently of any communication link - communication loss degrades remote awareness, not onboard safety logic.
- **Watchdog:** The ESP32's independent operation from the Jetson is itself a watchdog-equivalent design - a Jetson crash does not silence the safety system.
- **Health monitoring:** Sensor-fault, sensor-disagreement, and low-O2-unreliable flags are continuously computed and surfaced, not just checked at startup.
- **Fail-safe behavior:** The system is designed to escalate toward WARNING/EMERGENCY when sensor trust degrades (Part 24), rather than defaulting to "safe" - fail-conservative, not fail-permissive.
- **Recovery:** Physical retrieval is the recovery mechanism for most hardware-level failures (tether break, battery depletion, mechanical entrapment) - this is a disclosed, real limitation shared by precedent systems, not a solved problem.

---

# PART 28 — ENVIRONMENTAL / DEPLOYMENT CONDITIONS

| Condition | Value/requirement | Evidence basis |
|---|---|---|
| Temperature | 15-40C operating range assumed | Engineering estimate - no single authoritative source for this specific mine's ambient conditions; requires site data |
| Humidity | Up to near-saturation | Engineering estimate, consistent with general underground coal-mine conditions described in the PS narrative |
| Dust | Present, potentially heavy after an incident (roof-fall, gas event) | PS narrative; corroborated by mine-rescue-robotics literature (Part 12 LiDAR discussion) |
| Rain/water | Standing water possible (flooding is explicitly named in the PS) | PS explicit requirement |
| Vibration | Present during rover movement (motor/track-induced); factored into the IMU's stationary-sample-only design (Part 12) | Engineering reasoning |
| Physical obstruction | Rubble/debris possible post-incident | PS narrative |
| Electromagnetic interference | Not separately characterized; the RF range figures used (Part 13/14) are field measurements from occupied/working mines, which may already reflect some ambient RF noise, but this was not isolated as a separate variable in the cited studies | Unknown - requires site-specific RF survey |
| Enclosure / IP rating | IP54/65-rated body **with a resolved thermal path** - a finned heatsink thermally bonded through the enclosure wall rather than an internal fan behind a sealed panel, so the claimed ingress rating is not undermined by a cooling vent | Design requirement, corrected during red-team review (Part 40, D-009) |
| Installation requirements | None - this is a mobile, deployed-per-incident system, not fixed infrastructure | By design (explicitly out of scope: mine-wide fixed installation) |

---

# PART 29 — SCALABILITY

The PS describes a single rescue tool, not a fleet system - R-021 (Part 2) explicitly scopes fleet deployment as optional/out-of-scope. This section is provided for completeness per the requested document structure, not because the PS requires it.

| Scale | Network traffic | Storage | Compute | Database load | Gateway requirements | Cloud requirements | Cost implication |
|---|---|---|---|---|---|---|---|
| 1 unit (this project's actual scope) | As specified in Part 15 | Negligible (local SQLite) | Single Jetson per rover | Single local SQLite file | None (direct tether/LoRa to a laptop) | None | As specified in Part 30 |
| 10 units | 10x the single-unit LoRa traffic if operated simultaneously in the same mine - would require frequency/channel planning to avoid interference, not evaluated here | 10x local storage, still small | 10x edge compute (one Jetson per rover, unchanged per-unit) | Would benefit from a shared networked database rather than 10 separate SQLite files | A proper LoRa gateway (not point-to-point radios) would be needed | Likely still no cloud requirement for a single-incident, single-site deployment | Roughly linear in hardware cost; not evaluated in this document since it is out of the PS's scope |
| 100-10,000 units | Would require a genuine multi-hop mesh network architecture, dedicated gateway infrastructure, and almost certainly cloud-based aggregation and a proper time-series database (e.g., the PostgreSQL/TimescaleDB production path named in Part 17) | Requires networked, not local, storage | Requires fleet-management tooling not designed in this document | Requires a production-grade database, not SQLite | Requires dedicated gateway hardware and RF planning across the deployment | Would require cloud infrastructure | This is a materially different product (mine-wide monitoring infrastructure) from the single-rescue-tool this PS asks for, and is explicitly **not** part of this project's scope or cost estimate |

**Architectural bottleneck at scale:** The MVP's point-to-point LoRa link and single-laptop local dashboard are deliberately not designed to scale past a handful of simultaneous units - this is a correct scoping decision for this PS, not an oversight, and should be stated as such if an evaluator asks about scalability (see Part 44).

---

# PART 30 — COST MODEL

### Prototype BOM
See the full itemized table in Part 11. **Total: approx Rs.1,12,000 - Rs.1,61,000.**

**Cost estimate revision history (for transparency, not evasion):**
| Estimate stage | Value | Reason for change |
|---|---|---|
| Original team PPT | Rs.35,000-Rs.72,000 | Initial estimate, understated LiDAR/thermal import costs |
| First technical redesign | approx Rs.81,000 | Corrected for realistic LiDAR/thermal import pricing |
| Post-hostile-review revision | Rs.1,01,500-Rs.1,38,500 | Corrected Jetson-subsystem pricing (bare module -> full working subsystem) and added the fiber-tether/reel line item |
| Post-red-team revision (current, canonical) | **Rs.1,12,000-Rs.1,61,000** | Added the NDIR sensor, Jetson active-cooling fan, prototyping PCB, calibration-gas kit, and a revised (simpler, manual-rewind) tether mechanism cost |

### Production BOM
**Cannot be credibly estimated without an Ex-certification/manufacturing-partner quote.** Requires certified intrinsically-safe (Ex-rated) versions of every electronic component, a ruggedized/certified enclosure, and a DGMS-type-approval process - this is not a linear scale-up of the prototype BOM. Stated as a limitation, not guessed.

### Deployment cost
Not separately estimated - deployment (getting the unit to an incident site) is assumed to use existing rescue-team transport/logistics; no new infrastructure cost is implied by this design (explicitly, since a mine-wide fixed network was scoped out - Part 2, R-019).

### Operational cost
Battery replacement/charging (consumable, low recurring cost); gas-sensor recalibration consumables (reference gas, periodic); tether replacement if damaged (per-incident consumable risk, cost not separately itemized - engineering estimate would require a per-unit tether cost from Part 11, Rs.3,000-8,000 per replacement).

### Maintenance cost
Not separately itemized - a defined technician/maintenance role is named as an open operational question in Part 4 and Part 31, not yet costed.

**Schedule risk (cost-adjacent):** The FLIR Lepton has a documented ~14-week manufacturer lead time - this should be ordered immediately regardless of final BOM sign-off, since it is the single longest lead-time item.

---

# PART 31 — FEASIBILITY

| Dimension | Evidence | Risk | Mitigation | Final assessment |
|---|---|---|---|---|
| Technical | Every named sensing/compute/tether component has a datasheet-backed specification (Part 11/12) | Communication range and thermal-detection performance are both currently unmeasured (Part 41) | On-site/bench measurement plan defined in Part 33 | Feasible for the sensing/compute/tethered-video core; two specific claims remain open pending measurement, not architecturally blocked |
| Hardware | All components available through standard Indian electronics distributors/importers | FLIR Lepton's 14-week lead time is a real schedule risk | Order immediately | Feasible, with an explicit schedule dependency |
| Software | Local web-app + SQLite architecture is standard, well-documented technology | None significant at this scale | N/A | Feasible |
| AI | Rule-based hazard logic requires no training data and is straightforward to implement; thermal detection's rule-based MVP version is similarly straightforward | No validated dataset/performance number exists yet for thermal detection (Part 21) | Run the bench trial in Part 33 before any accuracy claim is made | Feasible for the MVP scope; the CNN stretch goal is conditional on data collection, not guaranteed |
| Communication | Fiber tether is a proven, precedent-backed approach (Gemini-Scout, Wolverine); LoRa is a proven low-bandwidth technology | Underground RF range for the LoRa backup is genuinely site-dependent and unmeasured for this specific mine; India duty-cycle rule for the chosen band is unverified | Mandatory on-site RF test (Part 33); resolve duty-cycle question against the current WPC text before final submission | Feasible, contingent on the above two verifications |
| Economic | Itemized BOM (Part 11/30) reflects realistic current component pricing | Cost has been revised upward three times during this project's own review process | Present the revision history transparently (Part 30) rather than hiding it | Feasible at the stated (revised) prototype budget; production cost is explicitly not estimable without external input |
| Operational | A trained rescue-team member can plausibly learn teleop quickly, per Gemini-Scout's own design philosophy of borrowing familiar game-controller interfaces | Roles for battery/tether/firmware maintenance are not yet formally assigned | Named as an open question rather than assumed away | Partially feasible - the core operating concept is sound, supporting roles are undefined |
| Deployment | Both real precedent systems required purpose-built explosion-proof housings this student prototype does not have | Intrinsic-safety certification is a genuine, unresolved gap | Explicit MVP/production split (Part 32) | Not feasible for real underground deployment without a certification phase - stated plainly |
| Scalability | Not required by the PS (Part 2, R-021) | N/A | N/A | Out of scope by design, not a feasibility gap |
| Regulatory | DGMS is named as a potential data consumer, not a real-time integration requirement, in the PS | Production-phase Ex-rated certification (IS/ATEX-equivalent) is a real, lengthy, costly regulatory process not undertaken by this project | Stated as future work | Not addressed at the prototype stage - correctly scoped as production-only |

---

# PART 32 — MVP

### MUST BUILD
- Tracked chassis with mobility sufficient for the demo obstacle course.
- ESP32 safety MCU running the deterministic rule engine (Part 23, Algorithm 1) and the sensor-arbitration logic (Part 24).
- Three combustible-gas sensors (MOS, pellistor, NDIR) + electrochemical O2 sensor + temp/humidity + water probe + IMU.
- Jetson Orin Nano with passive-heatsink cooling, running video/thermal handling.
- RGB and thermal (Lepton) cameras.
- Fiber-optic tether (manual-rewind spool) as the primary video/control link.
- LoRa backup telemetry link with automatic tether-loss fallback.
- Local surface dashboard (video, thermal, telemetry, hazard state, alerts, teleop control).
**Why:** These directly implement the PS's explicit requirements (R-001 through R-012, Part 2) and the red-team-validated safety architecture.

### SHOULD BUILD
- Thermal-blob detection (rule-based, per Part 20/23 Algorithm 3), with a genuine bench-measured recall figure before the final demo.
- EWMA gas-trend early-warning layer.
- 2D LiDAR-assisted obstacle visualization, explicitly scoped as a clear-air demo aid, not a navigation dependency.
**Why:** These strengthen the R-009/R-010/R-011 requirements but are not architecturally load-bearing - the system functions (with reduced situational-awareness richness) without them.

### CAN SIMULATE
- The "incident" itself, for demo purposes: calibration-gas puffs standing in for a real gas leak, a heated object standing in for a trapped worker, a water tray standing in for flooding.
- A mock rubble/obstacle course standing in for post-collapse debris.
**Why:** A real hazardous-gas atmosphere cannot and should not be used for a student demo; simulated inputs test the real sensing/detection/alerting pipeline safely.

### FUTURE PRODUCTION
- Ex-rated/intrinsically-safe certified versions of all electronics and the battery.
- Certified (MSHA/DGMS-approved) gas-sensing module, replacing the COTS triple-redundant sensor suite.
- Dedicated geotechnical instrumentation for genuine structural-collapse-risk sensing (beyond the MVP's stationary-shock-event IMU proxy).
- DGMS-compatible live reporting integration.
- Any multi-rover/fleet capability (explicitly out of this project's scope, Part 2 R-021).
**Why:** These require certification processes, specialized instrumentation, or infrastructure investment beyond a hackathon prototype's realistic scope - named explicitly so no one mistakes the MVP for a deployment-ready system.

---

# PART 33 — VALIDATION & EXPERIMENTAL PLAN

| Claim | Experiment | Equipment | Metric | Target | Actual | Status |
|---|---|---|---|---|---|---|
| Gas sensors respond correctly and agree within tolerance | Bench exposure to calibration gas at 1% and 2.5% CH4-equivalent reference concentrations | Calibration gas cylinders (Part 11) | Sensor reading vs. reference; cross-sensor agreement | Within manufacturer-stated tolerance post-calibration; agreement within a defined band | N/A - not yet run | Pending |
| Sensor-disagreement alert fires correctly | Deliberately disconnect/fault one gas sensor during a bench test | Same as above | SENSOR_DISAGREEMENT flag correctly raised | Flag fires within one polling cycle | N/A | Pending |
| O2-arbitration logic correctly excludes the pellistor below 10% O2 | Bench test with a controlled low-O2 gas mixture | Calibration gas + O2-depleted reference mixture | LOW_O2_UNRELIABLE flag and correct fallback to MOS/NDIR max | Flag and fallback both fire correctly | N/A | Pending |
| LiDAR ranging accuracy | Static test, known-distance markers | RPLIDAR A1, tape measure | Measured vs. actual distance | <=1% error to 3 m, <=2.5% error 5-12 m (datasheet spec) | N/A | Pending |
| Thermal detection - measured contrast and recall | Controlled dark room, person at varying distances/poses (some occluded), measured delta-T against background | FLIR Lepton, thermometer for reference delta-T | Recall, false-negative rate, measured delta-T | Team-defined after seeing the measured delta-T - **no number invented before this test** | N/A | Pending - this is the single highest-priority experiment in the entire project |
| LoRa telemetry range/reliability | On-site or best-available tunnel/basement-proxy walk-test | LoRa modules, packet counter, RSSI logger | Packet delivery ratio, RSSI, SNR vs. distance | Establish the team's own measured curve (13-29 m coal-mine field data used as the planning baseline, per Part 13) | N/A | Pending - **mandatory before any range claim is presented to evaluators** |
| Video/thermal tether latency | Rover at increasing distance | Timer/frame-timestamp comparison | Glass-to-glass latency, frame-drop rate | Target <500 ms (engineering assumption) | N/A | Pending |
| Fiber tether continuity/fracture detection | Pre-mission optical continuity check procedure; repeated payout/retraction cycling | Optical continuity tester | Snag rate, fiber integrity after N cycles | No fracture after a defined number of test cycles | N/A | Pending |
| Battery runtime under load | Full mission-profile run on the built chassis, including motor draw on real terrain | Rover, stopwatch, battery monitor | Measured runtime | Compare against the ~60-90 min calculated target (Part 16) | N/A | Pending - this is the number every evaluator is most likely to ask about first |
| End-to-end drill | Simulated incident (gas + hidden thermal target + water tray + obstacle course), full mission from launch to alert to operator decision, including a run where the tether is cut mid-mission | Full assembled prototype | Time from simulated hazard occurrence -> detection -> operator alert; correct fallback behavior on tether cut | Team-defined SLA, reported honestly | N/A | Pending |
| India LoRa duty-cycle compliance | Direct review of the current WPC SRD notification text | Regulatory document | Confirmed duty-cycle limit (if any) applicable to 865-867 MHz | Compliant transmission interval | N/A | Pending - **this is a document-review task, not a lab experiment, and should be completed first since it may constrain the design of the other communication tests** |

---

# PART 34 — EXPECTED VS MEASURED PERFORMANCE

| Parameter | Research reference | Engineering target | Prototype measurement | Production goal |
|---|---|---|---|---|
| LoRa underground range | 13-29 m (coal mine, per Part 42 REF-002) vs. >1000 m (hard-rock, per Part 42 REF-001 - not applicable to this coal-mine PS) | Plan mission radius around the coal-mine figure (13-29 m) as the conservative baseline | N/A - requires on-site test | A certified, professionally site-surveyed communication system appropriate to the specific deployment mine |
| Thermal detection range | ~46 m (detection) / ~11.5 m (recognition), Johnson's-Criteria geometric calculation, contingent on >=2C contrast | Same, pending confirmation of the contrast assumption | N/A - requires measured delta-T | Refined with real incident/field data over time |
| Battery runtime | N/A (no literature figure for this specific build) | 60-90 minutes (engineering assumption) | N/A - requires measurement | Extended runtime and/or field-swappable battery packs |
| Prototype cost | N/A | Rs.1,12,000-Rs.1,61,000 (Part 30) | N/A (actual procurement not yet completed as of this document) | Not estimable without a manufacturing-partner/certification-body quote |
| Gas sensor response time | MQ-7: ~90 s to reach a stable reading at the low-heat cycle endpoint (datasheet); pellistor: typically <10 s per general catalytic-sensor literature | Design around the slower (MOS) figure for a conservative alert-latency estimate | N/A - requires bench measurement | Certified module response times per its own datasheet |

---

# PART 35 — INNOVATION

| Existing approach | Problem with existing approach | Our innovation | Technical mechanism | Measurable improvement | Evidence |
|---|---|---|---|---|---|
| Single-sensor combustible-gas detection (common in low-cost DIY gas-monitoring projects) | Semiconductor and catalytic-bead sensors can each fail silently - a poisoned/O2-starved sensor gives no fault signal | Triple-redundant, dissimilar-technology gas sensing with an oxygen-based arbitration rule | The rule engine uses the O2 reading to decide, in real time, which combustible-gas channel(s) to trust, and surfaces disagreement as its own alert category | A single point of undetected sensor failure becomes a system that flags its own reduced trust, rather than silently reporting a false "all clear" | Industrial Scientific, Frontline Safety, Fluid Handling Pro (pellistor O2-dependency and fail-unsafe documentation) |
| Assuming a single wireless technology can carry both telemetry and video underground | RF bandwidth-vs-range trade-offs are frequently unexamined in student projects; a naive "use LoRa for everything" or "use Wi-Fi for bandwidth" design fails once the actual coal-mine RF data is checked | Split-by-data-type communication architecture: fiber tether (deterministic, high-bandwidth) for video/control, LoRa (low-bandwidth, resilient) for telemetry/alerts, with automatic fallback | Removes the single largest unproven assumption in most comparable student designs by grounding the choice in an actual coal-mine field measurement (17 m Wi-Fi vs. 28.82 m LoRa) rather than a marketing-level "LoRa is low-power IoT" justification | The video path is guaranteed by physics (a wired connection) rather than hoped-for RF propagation; the telemetry path survives even if the tether is physically severed | PMC8088201 (coal-mine WPAN/WLAN/LoRa field measurement); Gemini-Scout/Wolverine precedent |
| Treating "AI-powered" as a checkbox feature | Generic AI/IoT/cloud usage claims add complexity without demonstrable benefit and are frequently penalized by technically literate evaluators | Disciplined **non-use** of machine learning for gas/water/shock thresholds (a rule engine instead, because the thresholds are already regulation-derived and a rule engine is fully auditable), reserving ML-adjacent methods (thermal blob detection, EWMA trend) only where they add genuine value as human-supervised decision support | Rule engine as sole safety authority; AI outputs are never an autonomous trigger | A more defensible, explainable safety architecture than "AI decides," and one that survives the "why isn't this just AI for the sake of AI" evaluator question proactively | Standard safety-engineering practice (defense-in-depth/deterministic interlock), applied specifically and correctly here rather than claimed generically |

**What we do not claim as innovation:** Using AI, IoT, or a dashboard, by themselves - these are standard practice, not a differentiator, and are not presented as such anywhere in this document.

---

# PART 36 — RISKS

| Risk | Probability | Impact | Detection | Mitigation | Backup |
|---|---|---|---|---|---|
| LoRa/tether range underground is worse than the design baseline in this specific mine | Medium (RF propagation is genuinely site-dependent, per Part 13's conflicting studies) | High (limits mission radius) | On-site measurement (Part 33) | Plan mission radius conservatively around the coal-mine field-measured range (13-29 m), not the theoretical link budget | Fiber tether length itself sets a hard, known bound regardless of RF uncertainty |
| Fiber tether snags/fractures in rubble | Medium | High (loss of primary video path) | Pre-mission continuity check; mid-mission signature (video loss, telemetry alive) | Automatic LoRa fallback | Manual retrieval procedure |
| FLIR Lepton's 14-week lead time slips the build schedule | Medium-High if not ordered immediately | High (no thermal channel for the demo) | Procurement tracking | Order immediately; commit to the cheaper Lepton FS to reduce cost/lead-time risk together | None - this is a hard external dependency |
| India LoRa duty-cycle rule turns out to restrict the chosen transmission interval | Unknown (unverified) | Medium (would require re-tuning the telemetry interval, not a redesign) | Direct review of WPC SRD notification | Batch packets regardless to minimize transmissions/hour | Resolve before final submission - see Part 33 |
| Thermal detection performs poorly due to low mine ambient-to-body contrast | Medium-High (a documented failure mode for this exact application) | High (undermines the R-010 trapped-worker-location requirement) | Bench delta-T measurement (Part 33) | Recall-biased detector design; human operator as the final check | State the limitation honestly to evaluators rather than overclaiming |
| Gas sensors give unreliable readings at demo time due to insufficient burn-in | Medium (an easy operational mistake if not planned for) | Medium (undermines the demo's credibility, not the underlying design) | Team awareness/checklist | Power the gas-sensor subsystem continuously from ~48 hours before the demo | N/A - purely a logistics fix |
| Prototype cost exceeds the current estimate a fourth time | Medium (given the pattern across three prior revisions) | Low-Medium (budget/fundraising impact, not a design flaw) | Itemized BOM review (Part 11/30) | Present the revision history transparently rather than presenting a falsely stable number | N/A |
| Intrinsic-safety certification gap is challenged by an evaluator | High (near-certain to be asked, per Part 44) | Reputational (if answered defensively) | N/A | Name the gap proactively as production-phase work, before being asked | Cite the same limitation shared by real precedent systems (Gemini-Scout, Wolverine required purpose-built explosion-proof housings) |

---

# PART 37 — IMPLEMENTATION ROADMAP

### Milestone 1 - Core hardware
**Deliverable:** Assembled chassis with motors, battery, and enclosure (with resolved thermal path). **Dependencies:** Component procurement (Part 11), especially the long-lead-time Lepton. **Acceptance criteria:** Chassis moves under remote control on a flat surface; battery holds charge; enclosure passes a basic dust/splash check. **Failure condition:** Motors/chassis cannot support the sensor/compute payload weight, or the enclosure's thermal path fails a basic heat-soak test.

### Milestone 2 - Sensor acquisition
**Deliverable:** All sensors (three gas channels, O2, temp/humidity, IMU, water probe, RGB, thermal, LiDAR) wired to the ESP32/Jetson and producing readable data. **Dependencies:** Milestone 1 (physical mounting). **Acceptance criteria:** Each sensor's raw output is visible in a debug console; gas sensors have completed their 24-48h burn-in at least once. **Failure condition:** Any sensor's interface (I2C address conflict, ADC noise, etc.) cannot be resolved within the available development time.

### Milestone 3 - Communication
**Deliverable:** Fiber tether carrying video/thermal/control; LoRa backup carrying telemetry with automatic fallback on tether loss. **Dependencies:** Milestone 2 (data to transmit). **Acceptance criteria:** Video/thermal visible at the surface end of the tether; LoRa telemetry received at the base station; fallback triggers correctly when the tether is manually disconnected in a bench test. **Failure condition:** Tether-to-Jetson interface cannot achieve the required video bandwidth reliably, or LoRa modules cannot establish a link at all in a basic bench test.

### Milestone 4 - Backend
**Deliverable:** Local server ingesting telemetry/video/thermal and serving the dashboard APIs (Part 18). **Dependencies:** Milestone 3 (data arriving at the surface). **Acceptance criteria:** /api/telemetry/latest, /api/alerts, and the video/thermal stream endpoints return correct data; SQLite database populated correctly (Part 19). **Failure condition:** Data loss or corruption between the communication layer and the database.

### Milestone 5 - AI
**Deliverable:** Deterministic rule engine (Algorithm 1) and sensor-arbitration logic (Part 24) running on the ESP32; rule-based thermal-blob detector (Algorithm 3) running on the Jetson. **Dependencies:** Milestone 2 (sensor data), Milestone 4 (a place to display alerts). **Acceptance criteria:** Rule engine correctly transitions hazard states in a bench test with simulated readings; thermal detector flags a heated test object in a bench trial. **Failure condition:** Rule engine logic errors that would produce an unsafe "all clear" during a known-hazardous simulated condition - this is treated as a blocking defect, not a minor bug.

### Milestone 6 - Integration
**Deliverable:** All subsystems operating together on the assembled rover. **Dependencies:** Milestones 1-5. **Acceptance criteria:** A full teleop run with live video/thermal/telemetry and correct hazard-state display. **Failure condition:** Any subsystem interferes with another (e.g., motor electrical noise corrupting gas-sensor ADC readings) in a way not resolved before the testing phase.

### Milestone 7 - Testing
**Deliverable:** Completion of the validation plan in Part 33 - gas calibration, LiDAR accuracy, thermal contrast/recall, LoRa range, tether latency/continuity, battery runtime, end-to-end drill. **Dependencies:** Milestone 6. **Acceptance criteria:** Every row in Part 33's table has moved from "Pending" to a reported measured value. **Failure condition:** A critical safety-relevant test (gas calibration, sensor-arbitration logic) cannot be completed before the demo date - this would require descoping the claim in the final PPT rather than presenting an untested number as fact.

### Milestone 8 - Final demonstration
**Deliverable:** A rehearsed demo run on the simulated-incident obstacle course (Part 32, "CAN SIMULATE"). **Dependencies:** Milestone 7. **Acceptance criteria:** The full INPUT->PROCESSING->INTELLIGENCE->DECISION->OUTPUT->ACTION workflow (Part 7.10) executes correctly and repeatably. **Failure condition:** Any single-point-of-failure discovered during rehearsal that was not already covered in Part 26's failure-mode table - this is itself a signal that the failure-mode analysis needs updating before the actual evaluation.

---

# PART 38 — FINAL SYSTEM SPECIFICATION

| Category | Parameter | Final specification | Evidence | Confidence | Status |
|---|---|---|---|---|---|
| Platform | Locomotion | Tracked ground rover | PS allows rover or drone; rover chosen for low-ceiling/rubble/flooding reasons (Part 40, D-001) | Medium (reasoned choice) | Design decided |
| Gas sensing | Combustible-gas channels | MOS (MQ-4) + catalytic-bead (pellistor) + NDIR, oxygen-arbitrated | Part 12, Part 24 | High (architecture) / Low (absolute accuracy, unmeasured) | Design decided; validation pending |
| Gas sensing | O2 sensing | Electrochemical galvanic cell | Part 12 | High | Design decided |
| Gas sensing | Alarm thresholds | WARNING >=1%, EMERGENCY >=2.5% (combustible-gas equivalent); O2 WARNING <20.5%, EMERGENCY <19.5% | Part 24 | High (logic) / Low (India-specific DGMS exact figures not independently re-verified) | Design decided; regulatory text cross-check pending |
| Environmental sensing | Temp/humidity | SHT31/DHT22 class | Part 11/12 | High | Design decided |
| Structural sensing | Shock detection | Stationary-sample IMU flag only (not continuous trend) | Part 12, corrected from an earlier over-claim | Engineering assumption | Design decided |
| Flood sensing | Water probe | Staged dry/wet/submerged conductive probe | Part 11/12 | High | Design decided |
| Imaging | RGB | 1080p-class, ~30 fps | Part 11 | High | Design decided |
| Imaging | Thermal | FLIR Lepton (FS or 3.5), ~8.6 Hz, 150 mW operating | Part 12 | High (hardware) / Low (effective detection range, contrast-dependent and unmeasured) | Design decided; validation pending |
| Mapping | LiDAR | RPLIDAR A1, clear-air demo aid only, not a navigation dependency | Part 12 | High (limitation), design correctly scoped | Design decided |
| Compute | Edge module | Jetson Orin Nano 4GB, passive-heatsink cooled | Part 11 | High | Design decided |
| Compute | Safety MCU | ESP32-WROOM-32 | Part 11 | High | Design decided |
| Communication | Primary (video/control) | Fiber-optic tether, manual-rewind spool | Part 13 | High (architecture) / Engineering assumption (mass/mechanism specifics) | Design decided |
| Communication | Backup (telemetry/alerts) | LoRa, 865-867 MHz, India band | Part 13/14 | High (technology) / Low (real-world range in this specific mine, unmeasured) | Design decided; validation mandatory |
| Communication | India duty-cycle compliance | Unresolved | Part 41, A-002 | Unknown | **Action required before final submission** |
| Software | Dashboard | Local web app, no cloud dependency for MVP | Part 17 | High | Design decided |
| Software | Database | SQLite (MVP) | Part 19 | High | Design decided |
| Power | Average draw | ~18-25 W | Part 16 | Engineering assumption (calculated, not measured) | Validation pending |
| Power | Battery | 5000-6000 mAh Li-ion | Part 16 | Engineering assumption | Validation pending |
| Cost | Prototype total | Rs.1,12,000-Rs.1,61,000 | Part 30 | High (itemized) | Current, subject to procurement confirmation |
| Certification | Intrinsic safety | Not implemented in the prototype; named as production-phase work | Part 31/32 | High (honest scoping) | Explicitly out of MVP scope |

---

# PART 39 — TERMINOLOGY / GLOSSARY

- **LiDAR:** Light Detection and Ranging - a sensor that measures distance by timing/triangulating reflected laser light.
- **PRF:** Pulse Repetition Frequency - how many laser pulses a LiDAR emits per second (not separately specified for the RPLIDAR A1, which uses continuous-wave triangulation rather than pulsed time-of-flight ranging).
- **LoRa:** Long Range - a low-power, long-range (in favorable conditions) radio modulation technique.
- **SF (Spreading Factor):** A LoRa parameter trading data rate for range/robustness - higher SF means longer range and lower data rate.
- **RSSI:** Received Signal Strength Indicator - a measure of radio signal power at the receiver.
- **SNR:** Signal-to-Noise Ratio.
- **MQTT:** Message Queuing Telemetry Transport - a lightweight publish/subscribe messaging protocol commonly used in IoT (not used in this project's MVP, which uses direct HTTP/WebSocket on a local network instead).
- **API:** Application Programming Interface.
- **F1 (F1 score):** The harmonic mean of precision and recall - a standard classifier evaluation metric (not yet computable for this project's thermal detector, since no dataset/experiment exists yet - Part 21/22).
- **Inference:** Running a trained (or, in this project's MVP, rule-based) model on new data to produce an output.
- **Edge computing:** Running compute (here, video processing and thermal detection) on the device itself (the Jetson) rather than in the cloud.
- **NDIR:** Non-Dispersive Infrared - a gas-sensing technique using optical absorption at a characteristic infrared wavelength, oxygen-independent unlike catalytic combustion sensing.
- **Pellistor / catalytic bead sensor:** A combustible-gas sensor that detects gas via the heat released when it is catalytically combusted on a heated bead - requires ambient oxygen to function correctly.
- **MOS sensor:** Metal-Oxide Semiconductor gas sensor - detects gas via a change in electrical resistance of a heated metal-oxide surface (e.g., the MQ-series sensors used in this project).
- **LEL:** Lower Explosive Limit - the minimum concentration of a gas in air that can ignite; methane's LEL is 5-15% by volume.
- **EWMA:** Exponentially Weighted Moving Average - a statistical smoothing technique used here for gas-concentration trend detection.
- **Johnson's Criteria:** A widely used methodology (originating in 1950s military sensor research) for estimating the range at which a thermal/optical sensor can detect, recognize, or identify a target, based on pixels-on-target.
- **DGMS:** Directorate General of Mines Safety (India) - the regulatory body for mine safety.
- **WPC:** Wireless Planning & Coordination Wing, India's Department of Telecommunications body governing spectrum use, including the de-licensed 865-867 MHz band used by this project's LoRa link.
- **Ex-rated / intrinsically safe:** Hardware certified safe for use in an explosive atmosphere - a certification this prototype does not have and explicitly does not claim (Part 31/32).

---

# PART 40 — DECISION LOG

| Decision ID | Decision | Alternatives considered | Why selected | Evidence |
|---|---|---|---|---|
| D-001 | Ground rover, not aerial drone | Compact aerial drone (PS-permitted alternative) | Low ceilings, rubble, and flooding all favor ground locomotion; a rover can carry more payload (gas+thermal+RGB+tether) at lower power cost | First-principles reasoning; Part 4 |
| D-002 | Fiber-optic tether as primary video/control path | 2.4 GHz Wi-Fi; LoRa for video; cellular | Real precedent systems (Gemini-Scout, Wolverine) both tether video; a coal-mine field measurement shows Wi-Fi's own underground range (17 m) is shorter than LoRa's (28.82 m) in that environment, undermining the "use Wi-Fi for bandwidth" logic | PMC8088201; Gemini-Scout/Wolverine records; Part 13 |
| D-003 | LoRa (865-867 MHz) as telemetry-only backup | BLE, Zigbee, NB-IoT/cellular | Matches the low-bandwidth telemetry data type; India de-licensed band available with no subscription/infrastructure dependency; low power | Part 13 comparison table |
| D-004 | Triple-redundant, oxygen-arbitrated gas sensing (MOS + pellistor + NDIR) | Single-sensor (MOS-only, as in the original team design); dual-sensor (MOS + pellistor, as in an earlier revision) | MOS sensors fail silently with no fault signal; pellistors additionally fail (falsely low) below 10% O2 - exactly the worst-case emergency scenario; NDIR is oxygen-independent and closes this gap when arbitrated against the O2 reading | Industrial Scientific, Frontline Safety, Fluid Handling Pro (Part 12) |
| D-005 | Deterministic rule engine as sole safety authority (not ML) | A trained classifier for hazard-state determination | Gas/water/shock thresholds are already regulation/physics-derived; a rule engine is fully auditable to a safety inspector, unlike a black-box classifier, for a life-safety decision | Part 20 model-selection rationale |
| D-006 | Rule-based (not CNN) thermal-blob detection for the MVP | A trained CNN person-detector | No labeled thermal dataset currently exists (Part 21); a rule-based approach is deployable immediately without training data | Part 20/21 |
| D-007 | Local (no-cloud) surface dashboard for the MVP | Cloud-hosted dashboard with remote access | A mine incident cannot be assumed to have reliable internet connectivity; no multi-team/multi-site access requirement exists at MVP scale | Part 17 |
| D-008 | SQLite database for the MVP | PostgreSQL/TimescaleDB | Single-operator, single-mission tool has no concurrent multi-user access requirement at this stage; simpler to deploy with zero infrastructure | Part 19 |
| D-009 | Passive heatsink bonded through the enclosure wall (not a sealed box with an internal fan, and not an unsealed vented box) | Fully sealed IP65 enclosure (as in an earlier revision, before this contradiction was found); an internal fan behind a sealed panel | The Jetson Orin Nano ships with no integrated thermal solution and documented active-cooling accessories exist specifically because it throttles without one; a sealed box has no airflow path, and a vent defeats the claimed IP rating | NVIDIA/Connect Tech/Seeed Studio thermal documentation; Part 11/28 |
| D-010 | IMU used only for stationary-sample shock-event detection, not continuous structural-trend monitoring | Continuous vibration-trend monitoring while the rover moves (as in an earlier revision) | A rover-mounted IMU's own locomotion vibration dominates any real environmental signal while moving; only a stationary reading isolates a genuine external shock event | First-principles sensor-mounting reasoning, Part 12 |
| D-011 | Manual-rewind tether spool, not a motorized reel | Motorized auto-retracting reel | Motorized reels add cost, mass, and their own mechanical failure point for a capability (auto-retraction) the PS does not require | Engineering reasoning |
| D-012 | LoRa retry policy capped at 2 attempts | Retry-until-success | Bounds total airtime regardless of measured packet loss and the still-unresolved India duty-cycle question | Part 13/24 |

---

# PART 41 — ASSUMPTION REGISTER

| Assumption ID | Assumption | Why needed | Risk | How to validate | Status |
|---|---|---|---|---|---|
| A-001 | Real-world LoRa range in this specific mine falls within the 13-29 m coal-mine field-measurement range, not the >1000 m hard-rock figure | Needed to plan mission radius and set expectations for evaluators | If wrong (either direction), the communication design's assumed operating envelope is incorrect | On-site or best-available tunnel-proxy RSSI-vs-distance measurement (Part 33) | **Open - mandatory before final submission** |
| A-002 | India's 865-867 MHz de-licensed band carries no duty-cycle restriction that would conflict with the chosen ~5 s telemetry interval | Needed to confirm regulatory compliance | If a restriction exists and is violated, the system would be non-compliant, not just suboptimal | Direct review of the current WPC SRD exemption notification text | **Open - action item, not a lab experiment; should be resolved first among all pending items** |
| A-003 | Mine ambient temperature is stable enough, and close enough to human skin temperature, that thermal-camera-to-background contrast may fall below the 2C threshold Johnson's-Criteria range estimates assume | Determines whether the stated ~46 m/~11.5 m thermal detection ranges are meaningful at all | If contrast is too low, no reliable detection range exists without additional measures (active cooling of background, sensor fusion, etc.) | Bench/on-site delta-T measurement (Part 33) | **Open - highest-priority AI-adjacent experiment in the project** |
| A-004 | Rover average power draw is ~18-25 W and mission runtime is 60-90 minutes | Needed to size the battery | If motor draw on real terrain is higher than estimated, runtime could be significantly shorter than planned | Full mission-profile test on the built chassis (Part 33) | **Open** |
| A-005 | Prototype mission duration target of 60-90 minutes is an appropriate single-sortie length | Needed to size the battery and plan the demo | Not PS-specified; a reasonable engineering assumption, not a requirement | Team decision, informed by the battery test above | Open, but lower-stakes than A-001 through A-004 |
| A-006 | A stationary-sample IMU shock-event flag has genuine value as a coarse "something happened nearby" indicator, despite not being a true structural-instability predictor | Determines how much credit this subsystem can honestly claim toward the PS's "structural condition" requirement (R-004) | If overstated to evaluators, this becomes an overclaim risk (Part 44) | State the limitation explicitly in the final PPT; no further experiment resolves this, since it is a scoping question, not a measurement question | Resolved by explicit honest framing, not by further testing |
| A-007 | Fiber tether length of 100-200 m is an appropriate mission-radius target | Needed to size the spool and estimate its cost/mass | Not PS-specified; depends on the expected demo/deployment scenario | Team decision based on the specific demo course or deployment scenario | Open |
| A-008 | Ambient underground coal-mine operating temperature falls within 15-40C | Needed for general environmental-tolerance design | If actual conditions differ significantly, enclosure/component temperature ratings may need revision | Site data or literature specific to Jharkhand coal mines (not obtained in this research pass) | Open |

---

# PART 42 — SOURCE & REFERENCE LIBRARY

**REF-001**
Title: Measurements and Models of 915 MHz LoRa Radio Propagation in an Underground Gold Mine
Authors: P. Branch
Year: 2022
Publisher/Journal: Sensors (MDPI), 22(22):8653
Source type: Peer-reviewed research
Relevant finding: LoRa achieved >1000 m NLoS range with <15% packet loss in a hard-rock gold mine, attributed to a tunnel waveguide effect
Where used: Part 5, Part 13, Part 14, Part 40 (D-002)

**REF-002**
Title: New approach for localization and smart data transmission inside underground mine environment
Authors: Not independently re-confirmed in this research pass (PMC record ID: PMC8088201)
Year: (per PMC record)
Publisher/Journal: PMC (PubMed Central)
Source type: Peer-reviewed research
Relevant finding: Measured coal-mine ranges of 13 m (WPAN), 17 m (WLAN/Wi-Fi), and 28.82 m (LoRa with a 50 dB gateway antenna)
Where used: Part 5, Part 13, Part 14, Part 40 (D-002)

**REF-003**
Title: Low-Cost Path-Loss Characterization for Underground Mine Tunnels Using LoRa Transceivers at 915 MHz
Authors: Not independently re-confirmed
Year: 2026
Publisher/Journal: Applied Sciences (MDPI)
Source type: Peer-reviewed research
Relevant finding: Two-zone path-loss structure in tunnel RF propagation - a line-of-sight waveguide-gain zone followed by steep non-line-of-sight attenuation; demonstrates a low-cost LoRa-as-measurement-instrument methodology
Where used: Part 13, Part 33 (methodology reference for the team's own range test)

**REF-004**
Title: Gemini-Scout Mine Rescue Robot
Authors: J. Garretson
Year: 2012
Publisher/Journal: Society for Mining, Metallurgy & Exploration (SME) / OneMine
Source type: Technical/industry report
Relevant finding: MSHA-approved multi-gas sensor, thermal + pan/tilt camera, explosion-proof electronics housings, fords 18 in of standing water, wired multi-channel video link, game-controller-style teleop interface for usability
Where used: Part 1, Part 5, Part 6, Part 13, Part 31, Part 40 (D-002)

**REF-005**
Title: (Survey of mine rescue robots, covering the MSHA Wolverine and CSIRO Numbat)
Authors: R. Green
Year: 2013
Publisher/Journal: CSIR ResearchSpace
Source type: Technical survey
Relevant finding: Wolverine (~500 kg, fiber-optic tether); Numbat (teleoperated situational-awareness tool, never operationally deployed)
Where used: Part 5, Part 6, Part 13, Part 27, Part 40

**REF-006**
Title: SX1276/77/78/79 Datasheet, Rev. 7
Authors: Semtech Corporation
Year: 2020
Publisher/Journal: Semtech (manufacturer datasheet)
Source type: Manufacturer datasheet
Relevant finding: TX power up to +20 dBm, RX sensitivity to -148 dBm, 168 dB theoretical maximum link budget
Where used: Part 11, Part 13, Part 14

**REF-007**
Title: RPLIDAR A1 Datasheet
Authors: Slamtec
Year: (manufacturer documentation, undated in this research pass)
Publisher/Journal: Slamtec (manufacturer datasheet)
Source type: Manufacturer datasheet
Relevant finding: 0.15-12 m range, 8000 samples/s, 5.5-10 Hz scan rate, 785 nm wavelength, 0.5 W power, accuracy specifications by distance band
Where used: Part 11, Part 12

**REF-008**
Title: Lepton 2.5 / Lepton FS module specifications
Authors: Teledyne FLIR
Year: (manufacturer documentation, undated in this research pass)
Publisher/Journal: Teledyne FLIR (manufacturer datasheet)
Source type: Manufacturer datasheet
Relevant finding: 80x60 (Lepton 2.5/3.5) or 160x120 (Lepton FS) resolution, ~8.6-8.7 Hz frame rate, 150 mW operating / 650 mW shutter / 5 mW standby power
Where used: Part 11, Part 12

**REF-009**
Title: MQ-4 and MQ-7 Gas Sensor Datasheets
Authors: Hanwei Electronics
Year: (manufacturer documentation, undated in this research pass)
Publisher/Journal: Hanwei Electronics (manufacturer datasheet)
Source type: Manufacturer datasheet
Relevant finding: MQ-4 200-10,000 ppm CH4 range, ~750 mW heater, 24h+ burn-in; MQ-7 200 ppm CO calibration reference, 60s/90s heat cycle
Where used: Part 11, Part 12, Part 34

**REF-010**
Title: NVIDIA Jetson Orin Nano 4GB Module specifications
Authors: NVIDIA (and ecosystem partner documentation)
Year: (product documentation, undated in this research pass)
Publisher/Journal: NVIDIA / ecosystem partners
Source type: Manufacturer datasheet
Relevant finding: 20 TOPS standard (25-34 TOPS Super mode), 5-10 W power range (25 W burst), no integrated thermal solution shipped standard
Where used: Part 11, Part 16, Part 28

**REF-011**
Title: Jetson Orin Nano/NX Active Cooling accessory documentation
Authors: Connect Tech; Seeed Studio; Waveshare
Year: (product documentation, undated in this research pass)
Publisher/Journal: Respective manufacturers
Source type: Manufacturer/vendor documentation
Relevant finding: Confirms the Jetson Orin Nano requires an added active-cooling accessory to avoid thermal throttling; provides pricing (~Rs.1,100 in India)
Where used: Part 11, Part 28, Part 40 (D-009)

**REF-012**
Title: Why Do You Need 10% Vol Oxygen to Operate a Catalytic Bead LEL Sensor?
Authors: Not independently re-confirmed (industry technical article)
Year: 2018
Publisher/Journal: Occupational Health & Safety (OHS Online) / Industrial Scientific Corporation
Source type: Industry technical documentation
Relevant finding: Catalytic bead (pellistor) sensors are not recommended below 10% vol. O2; readings become unreliable/falsely low
Where used: Part 12, Part 23, Part 24, Part 40 (D-004)

**REF-013**
Title: Understanding Catalytic Bead Sensor Technology: How it Works and Why it Matters in Gas Detection
Authors: Not independently re-confirmed
Year: (undated in this research pass)
Publisher/Journal: Frontline Safety
Source type: Industry technical documentation
Relevant finding: Confirms pellistor oxygen-dependency and poisoning vulnerability (silicone, lead, sulphur compounds)
Where used: Part 12, Part 40 (D-004)

**REF-014**
Title: What's the Difference Between a Pellistor and an IR Sensor?
Authors: Not independently re-confirmed
Year: (undated in this research pass)
Publisher/Journal: Fluid Handling Pro
Source type: Industry technical documentation
Relevant finding: Confirms pellistors do not fail-safe (no fault notification on instrument failure)
Where used: Part 12, Part 26, Part 40 (D-004)

**REF-015**
Title: Upgrading from MOS to Electrochemical Sensors for H2S Gas Detection (White Paper)
Authors: MSA Safety
Year: (undated in this research pass)
Publisher/Journal: MSA Safety
Source type: Industry/manufacturer white paper
Relevant finding: MOS sensors are not fail-safe (no fault signal on failure/poisoning); can enter a "sleep" state
Where used: Part 12, Part 26, Part 40

**REF-016**
Title: DARPA Subterranean Challenge Finals technical report (Team CERBERUS)
Authors: Team CERBERUS
Year: 2022
Publisher/Journal: arXiv (2207.04914)
Source type: Peer-reviewed/conference technical report
Relevant finding: Smoke/dust caused visual feature loss and LiDAR/vision degradation for a state-of-the-art funded robotics team in a subterranean environment
Where used: Part 5, Part 12

**REF-017**
Title: Mapping an Underground, Waterlogged Mine with LiDAR (technical case study)
Authors: Not independently re-confirmed
Year: (undated in this research pass)
Publisher/Journal: Emesent (technical blog/case study)
Source type: Industry technical documentation
Relevant finding: High humidity causes LiDAR scanner condensation; standing water causes laser mirroring/false returns
Where used: Part 12, Part 28

**REF-018**
Title: CMU Robotics Institute Field Robotics Center Seminar (Bartels) - sensing and perception in visually degraded mine environments
Authors: J. Bartels
Year: (seminar, undated in this research pass)
Publisher/Journal: Carnegie Mellon University Robotics Institute
Source type: Academic seminar/technical talk
Relevant finding: Thermal imaging succeeds best where large thermal gradients exist; underground mines' thermal stability is a documented failure mode for thermal-imaging-based detection specifically
Where used: Part 12, Part 33, Part 41 (A-003)

**REF-019**
Title: Johnson's Criteria methodology (as documented by thermal-camera manufacturers/integrators)
Authors: Various (Axis Communications, Dahua, Hikvision, FLIR-ecosystem technical documentation)
Year: Various
Publisher/Journal: Respective manufacturer technical white papers
Source type: Industry technical documentation, based on original 1950s military sensor research (J. Johnson)
Relevant finding: Standard pixels-on-target methodology for estimating detection/recognition/identification range, requiring >=2C contrast between target and background
Where used: Part 12, Part 22, Part 34

**REF-020**
Title: DoT/WPC Short Range Device (SRD) exemption rules for the 865-867 MHz band
Authors: Department of Telecommunications, Government of India / Wireless Planning & Coordination Wing
Year: 2021 (notification year as referenced in this research)
Publisher/Journal: Government of India
Source type: Government/regulatory source
Relevant finding: 865-867 MHz band is de-licensed for short-range devices at up to 1 W ERP
Where used: Part 11, Part 13, Part 41 (A-002) - **note: the exact duty-cycle provisions of this notification were not independently re-verified in this research pass and remain an open item (A-002)**

**REF-021**
Title: LoRa airtime vs. bit-rate community technical documentation
Authors: LoRa/LoRaWAN developer community (The Things Network forum contributors)
Year: Various
Publisher/Journal: The Things Network community forum
Source type: Community technical documentation (not peer-reviewed, but consistent with and explanatory of the underlying LoRa PHY specification)
Relevant finding: Real achieved LoRa throughput is meaningfully lower than the theoretical bit rate due to preamble/header/CRC overhead, especially for small payloads
Where used: Part 13

**REF-022 through REF-025**
General regulatory-precedent sources for methane alarm thresholds (1% warning / 2.5% evacuate) and methane LEL (5-15% by volume), drawn from internationally referenced mining-safety regulatory practice. **The India-specific DGMS numeric threshold was not independently re-verified against current DGMS regulation text in this research pass - flagged in Part 41/Part 44 as requiring direct confirmation before final submission.**

---

# PART 43 — SOURCE-TO-CLAIM MATRIX

| Claim ID | Technical claim | Source | Exact evidence | Used in |
|---|---|---|---|---|
| C-001 | LoRa's real-world coal-mine range is 13-29 m, far short of its theoretical link budget | REF-002 | Measured WPAN/WLAN/LoRa ranges in an actual coal-mine field trial | Part 13, 14, 33, 41 |
| C-002 | Wi-Fi's coal-mine range (17 m) is shorter than LoRa's (28.82 m) in the same study | REF-002 | Same source, same trial | Part 6, 13, 40 (D-002) |
| C-003 | Fiber tether is the video/control link used by both Gemini-Scout and Wolverine | REF-004, REF-005 | Direct system descriptions | Part 5, 6, 13, 40 (D-002) |
| C-004 | Pellistor sensors require >=10% vol. O2 and don't fail-safe | REF-012, REF-013, REF-014 | Direct statements in industry technical documentation | Part 12, 23, 24, 26, 40 (D-004) |
| C-005 | MOS sensors don't fail-safe and can "sleep"/be poisoned silently | REF-015 | MSA Safety white paper | Part 12, 26, 40 (D-004) |
| C-006 | Jetson Orin Nano ships with no integrated thermal solution | REF-010, REF-011 | NVIDIA/ecosystem partner documentation | Part 11, 28, 40 (D-009) |
| C-007 | Thermal detection range depends on >=2C contrast (Johnson's Criteria) | REF-019 | Standard DRI methodology documentation | Part 12, 22, 34 |
| C-008 | Underground mines have low thermal-gradient stability, a documented failure mode for thermal imaging | REF-018 | CMU RI seminar | Part 12, 33, 41 (A-003) |
| C-009 | LiDAR/vision degrade in dust and smoke even for a top-tier funded robotics team | REF-016 | DARPA SubT Finals technical report | Part 5, 12 |
| C-010 | LiDAR scanners suffer condensation and laser mirroring in humid/waterlogged mine conditions | REF-017 | Emesent case study | Part 12, 28 |
| C-011 | India's 865-867 MHz band is de-licensed at <=1 W ERP | REF-020 | DoT/WPC notification | Part 11, 13 |
| C-012 | LoRa real achieved throughput is lower than theoretical due to overhead | REF-021 | LoRa community technical documentation | Part 13 |
| C-013 | SX1276 TX power/RX sensitivity/link budget figures | REF-006 | Semtech datasheet | Part 11, 13, 14 |
| C-014 | RPLIDAR A1 range/rate/accuracy specifications | REF-007 | Slamtec datasheet | Part 11, 12 |
| C-015 | FLIR Lepton resolution/frame-rate/power specifications | REF-008 | FLIR datasheet | Part 11, 12 |
| C-016 | MQ-4/MQ-7 detection range/power/calibration specifications | REF-009 | Hanwei datasheets | Part 11, 12, 34 |

---

# PART 44 — SIH EVALUATOR DEFENSE

### Top 30 Technical Questions

1. **Q: Your pellistor sensor requires >10% oxygen to function - what happens to your gas readings in exactly the low-oxygen emergency this PS is about?**
   Short answer: The rule engine automatically excludes the pellistor below 10% O2 and relies on the oxygen-independent NDIR and the MOS sensor instead.
   Detailed answer: See Part 24's arbitration logic and Part 12's sensor-limitation documentation.
   Evidence: REF-012, REF-013, REF-014.
   Architecture component: Part 23 Algorithm 1, Part 24.
   Experiment: Part 33's low-O2 bench test.

2. **Q: Your compute module needs active cooling - how does that coexist with your dust/splash-rated enclosure?**
   Short answer: A passive heatsink is thermally bonded through the enclosure wall, so heat is conducted out through solid metal, not through an air vent that would break the IP rating.
   Detailed answer: Part 11, Part 28, Part 40 (D-009).
   Evidence: REF-010, REF-011.
   Architecture component: Enclosure design.
   Experiment: A basic heat-soak test under full load (not yet run - Part 41).

3. **Q: Why fiber tether over RF, when tethers famously snag and break in rubble?**
   Short answer: Because the two closest real precedent systems (Gemini-Scout, Wolverine) both made the same trade-off, and the one coal-mine RF measurement we have shows Wi-Fi underperforming LoRa in that environment - RF isn't actually the safer bet here.
   Detailed answer: Part 6, Part 13, Part 40 (D-002).
   Evidence: REF-002, REF-004, REF-005.
   Architecture component: Part 9.1, Part 13.
   Experiment: Pre-mission optical continuity check (Part 33).

4. **Q: What's your actual measured LoRa range in a real tunnel-like environment?**
   Short answer: Not yet measured - this is our single most important pending experiment, and we will present our own measured curve, not a claimed number.
   Evidence: Part 33, Part 41 (A-001).
   Architecture component: Part 13/14.

5. **Q: Your thermal camera's detection range depends on a 2C contrast - have you measured the actual temperature difference in your test environment?**
   Short answer: Not yet - pending, and we will not claim a detection range number until we have.
   Evidence: REF-018, REF-019; Part 41 (A-003).

6. **Q: If your MOS, pellistor, and NDIR sensors can each have their own failure modes, how do you know your gas reading is trustworthy at all?**
   Short answer: The O2-based arbitration logic explicitly names which sensor is authoritative under which condition, and surfaces sensor disagreement as its own alert - trust is explicit, not implicit.
   Evidence: Part 24.

7. **Q: Your MQ sensors need 24-48 hours of continuous power to stabilize - how do you manage that for a live demo?**
   Short answer: The gas-sensor subsystem is powered continuously from ~48 hours before the demonstration, not switched on cold.
   Evidence: REF-009; Part 26, Part 36.

8. **Q: Did you actually weigh your rover with the tether reel attached?**
   Short answer: This is an open item pending final assembly - flagged as an item to add to the test plan before the final build review.

9. **Q: LiDAR is known to fail in dust and smoke - the exact conditions this PS describes - so what is LiDAR actually contributing?**
   Short answer: Clear-air obstacle-mapping assistance for the demo only; our primary navigation dependency is the tether-guaranteed video feed, not LiDAR.
   Evidence: REF-016, REF-017; Part 12.

10. **Q: Why not just use a certified MSHA/DGMS-approved gas detector module instead of building your own?**
    Short answer: Certified modules are the correct production answer, not a hackathon-budget prototype answer; our MVP/production split names this explicitly.
    Evidence: Part 32.

11. **Q: What's your rover's actual measured battery runtime?**
    Short answer: Not yet measured - pending Part 33's mission-profile test; our calculated target is 60-90 minutes.

12. **Q: Is India's LoRa duty-cycle rule for 865-867 MHz actually satisfied by your transmission interval?**
    Short answer: This is our one remaining unresolved regulatory question, and we are committed to resolving it directly against the WPC notification text before final submission - we would rather name this gap than guess at compliance.
    Evidence: REF-020; Part 41 (A-002).

13. **Q: If your fiber tether snaps mid-mission with no external sign, how would you know before losing video entirely?**
    Short answer: A sudden total loss of video while telemetry (via LoRa) remains alive is the detection signature; the dashboard shows "TETHER LOST - LoRa fallback active" explicitly.
    Evidence: Part 10, Part 26.

14. **Q: Does antenna placement on a metal chassis affect your RF performance?**
    Short answer: Yes - we mount the antenna away from the chassis body specifically to reduce this detuning effect, and treat the SX1276's datasheet figures as a chip-level ceiling, not an installed-system guarantee.
    Evidence: Part 14, Part 33.

15. **Q: Your cost estimate has changed multiple times during your own design process - what's final now?**
    Short answer: Rs.1,12,000-Rs.1,61,000, itemized in Part 11/30; we present the revision history transparently because each revision reflects a real component we'd initially left out, not instability in our estimate methodology.

16. **Q: Doesn't your "structural condition" sensing (an IMU) fall well short of real structural-collapse prediction?**
    Short answer: Yes, and we say so explicitly - it detects a discrete shock event only while the rover is stationary; genuine structural-risk prediction requires dedicated geotechnical instrumentation, which is out of scope and named as production-phase work.
    Evidence: Part 12, Part 32, Part 40 (D-010).

17. **Q: How does a rescue-team member actually operate this - what does the control interface look like?**
    Short answer: A game-controller-style teleop interface, following the same usability philosophy Sandia used for Gemini-Scout, displayed live in our demo.
    Evidence: REF-004; Part 17, Part 31.

18. **Q: What happens if the rover gets physically stuck?**
    Short answer: We don't have a self-recovery mechanism - this is an accepted, disclosed limitation shared by both real precedent systems we studied.
    Evidence: Part 26, Part 31.

19. **Q: Is any part of your gas-sensing suite rated for use in an explosive atmosphere?**
    Short answer: No - our prototype uses COTS components; production deployment would require Ex-rated/intrinsically-safe certified hardware and DGMS approval, which we name explicitly as the single biggest gap between our MVP and a real deployment.
    Evidence: Part 31, Part 32.

20. **Q: Across your review process, what changed the most?**
    Short answer: Replacing an unverified single-radio communication assumption with a precedent-backed split architecture, and catching that our first "redundant" gas-sensor fix (adding a pellistor) actually shared a failure mode with our original sensor in the exact worst-case scenario, fixed by adding an oxygen-independent NDIR channel.
    Evidence: Part 40 decision log in full.

21. **Q: How does your architecture behave if you had to deploy 10 of these rovers at once?**
    Short answer: Not designed for that - it's explicitly out of this PS's scope (a single rescue tool, not a fleet system), and our point-to-point LoRa design would need real frequency/channel planning and a proper gateway before it could scale, which we state honestly rather than implying our architecture already handles it.
    Evidence: Part 29.

22. **Q: What security actually protects your control link, and is it enough?**
    Short answer: A pre-shared key for the one command-issuing endpoint, plus HMAC authentication on the LoRa backup channel - sized to the actual threat model (accidental interference from another radio, not a sophisticated attacker), not an enterprise security checklist we can't build or defend.
    Evidence: Part 25.

23. **Q: You claim no existing solution addresses this - is that actually true?**
    Short answer: No, and we don't claim that - Gemini-Scout and Wolverine are close real precedents; our contribution is a cost-realistic, India-buildable version with a communication and gas-sensing design corrected against real field evidence, not a novel concept.
    Evidence: Part 5, Part 6.

24. **Q: What's genuinely innovative here versus just "using AI/IoT"?**
    Short answer: The oxygen-arbitrated triple-redundant gas sensing and the RF-physics-grounded split communication architecture are the two specific, evidence-based contributions; we explicitly do not claim generic AI/IoT/cloud usage as innovation.
    Evidence: Part 35.

25. **Q: How do you know your thermal-blob detector won't produce an unacceptable number of false alarms?**
    Short answer: We don't yet - no dataset or bench trial exists, and we say so directly rather than presenting an invented accuracy number; our design choice (recall-biased) is a stated mitigation for the more dangerous failure mode (missed detection), accepting more false alarms as the safer trade-off.
    Evidence: Part 21, Part 22.

26. **Q: What's your plan if the Lepton doesn't arrive in time for the demo, given its 14-week lead time?**
    Short answer: We ordered it as soon as the design was finalized specifically because of this known lead time; if it were to slip, the RGB camera and gas/telemetry pipeline would still demonstrate the core reconnaissance concept, with thermal detection as the affected subsystem.
    Evidence: Part 30, Part 36.

27. **Q: Why SQLite and not a "real" database?**
    Short answer: A single-operator, single-mission MVP has no concurrent multi-user access requirement - SQLite is the right-sized tool; production would move to PostgreSQL/TimescaleDB, named explicitly as a later-phase decision, not a current gap.
    Evidence: Part 17, Part 19, Part 40 (D-008).

28. **Q: How would DGMS actually use this system's data?**
    Short answer: Not via a live integration in our MVP - we log data locally in a DGMS-report-compatible format (timestamped CSV/JSON export) for post-incident review; live system integration is explicitly a production-phase consideration, not something we claim to have built.
    Evidence: Part 2 (R-018), Part 30.

29. **Q: What's the single biggest unresolved risk in your entire project right now?**
    Short answer: Two tie for that position: whether our LoRa/thermal-contrast assumptions hold up against real on-site measurement, and whether India's LoRa duty-cycle rule constrains our design - both are named explicitly in our assumption register rather than hidden.
    Evidence: Part 41.

30. **Q: If you had to cut one subsystem to hit the demo deadline, what would you cut and why?**
    Short answer: The stretch-goal CNN-based thermal detector (Part 20's "should build," not "must build") - the rule-based version satisfies the PS requirement, and the CNN adds refinement, not core capability, making it the correct thing to defer if time runs short.
    Evidence: Part 32.

---

# PART 45 — PPT EXTRACTION MAP

| PPT Topic | Relevant master document sections |
|---|---|
| Title/team slide | Document metadata block |
| Problem statement slide | Part 1, Part 2 |
| Problem analysis / why it matters | Part 3, Part 4 |
| Existing solutions / literature review | Part 5, Part 6 |
| Solution overview | Part 7 |
| System architecture diagram | Part 9, Part 10 |
| Hardware slide | Part 11, Part 12 |
| Communication architecture slide | Part 13, Part 14 |
| AI/ML slide | Part 20, Part 21, Part 22, Part 23 |
| Decision logic / safety-architecture slide | Part 24 |
| Security slide (if included) | Part 25 |
| Feasibility and viability slide | Part 31, Part 32 |
| Cost/BOM slide | Part 30 |
| Impact and benefits slide | Part 6, Part 35 |
| Innovation slide | Part 35 |
| Risk/mitigation slide | Part 36 |
| Validation/testing slide (if included) | Part 33, Part 34 |
| Roadmap/timeline slide | Part 37 |
| Research and references slide | Part 42 |

---

# PART 46 — LLM USAGE INSTRUCTIONS

**This document is the canonical source of truth for the ShaktiMine SIH26039 project. Do not invent information not present here. Distinguish research values (Part 42/43), engineering targets (Part 34/38), experimental results (currently N/A across the board - Part 33/34), and open assumptions (Part 41). When asked to generate something, use the architecture, terminology, and specifications defined here. If information is missing or marked "requires validation" / "UNKNOWN," identify that explicitly rather than hallucinating a value.**

### What an LLM may derive from this document
PPT slides (using Part 45's map); an abstract (using Part 1); architecture diagrams (using Part 9/10); backend/frontend code (using Part 17/18); database schema/migrations (using Part 19); a BOM procurement list (using Part 11/30); a research summary (using Part 42); evaluator Q&A prep (using Part 44); a pitch/demo script (using Part 7, Part 32); posters; further documentation consistent with this document's content.

### What an LLM must NOT change without explicit instruction
The frozen architecture decisions in Part 40 (Decision Log); the validated technical parameters in Part 38 (Final System Specification); the PS interpretation in Part 2; the component choices in Part 11; the terminology defined in Part 39; any performance claim (none currently exist as "Actual" - Part 22/34 - and none should be introduced without a real experiment); the explicit MVP/production scoping in Part 32.

---

# PART 47 — CHANGE CONTROL

| Version | Date | Change | Reason | Impacted sections |
|---|---|---|---|---|
| Draft 0 | (original team PPT, pre-review) | Initial solution: single-sensor gas detection, LoRa mesh implied for video, mine-wide sensor network + wearables + full cloud stack, Rs.35-72K estimate | Original team design | Superseded entirely |
| Draft 1 | (first technical redesign) | Rebuilt from the PS; corrected the LoRa-for-video physics error; added structural/flooding sensing; scoped out mine-wide network/wearables/cloud stack; Rs.81K estimate | Ground-up redesign against PS requirements and initial research | Superseded by Draft 2/3 |
| Draft 2 | (post-hostile-review) | Corrected Wi-Fi-for-video to fiber-tether-primary; added MOS+pellistor gas redundancy; downgraded IMU claim; downgraded LiDAR claim; Rs.1.01-1.39 lakh estimate | Hostile technical review against research evidence | Superseded by Draft 3 |
| Draft 3 | (post-red-team) | Found the pellistor's own O2-dependency flaw; found the enclosure/cooling contradiction; added NDIR sensor + arbitration logic; Rs.1.12-1.61 lakh estimate | Aggressive red-team audit | Superseded by this canonical document |
| **v1.0 (this document)** | 2026-09-26 | Consolidated all prior corrections into one canonical, self-contained reference; added full software/database/API specification, decision log, assumption register, and evaluator defense not previously consolidated in one place | Canonicalization per project request | All sections (this is the first fully self-contained version) |

**Future changes to core architecture or technical parameters require evidence** - a new datasheet, a peer-reviewed source, a government/standards document, or the project's own experimental measurement (Part 33) - logged in this table with the impacted sections named, following the same discipline used to reach this version.

---

# PART 48 — FINAL CANONICAL SUMMARY

**Problem:** Underground Jharkhand coal-mine incidents (gas leaks, roof-falls, flooding) leave rescue teams without real-time knowledge of conditions before human entry, increasing risk and delaying response (SIH26039).

**Users:** A rescue-team operator teleoperates the rover; a rescue-team lead makes the entry/no-entry decision from its data.

**Solution:** A tracked, fiber-tethered rescue rover carrying triple-redundant, oxygen-arbitrated gas sensing, environmental sensors, RGB and thermal cameras, and a clear-air-only LiDAR aid, reporting to a local surface dashboard, with a deterministic rule engine as the sole safety authority and a LoRa radio as a telemetry-only backup if the tether is lost.

**Architecture:** Sensor layer -> ESP32 (safety-critical rule engine, independent of the AI/video path) + Jetson Orin Nano (video/thermal/AI) -> fiber tether (primary) / LoRa (backup) -> local dashboard -> human decision.

**Hardware:** MQ-4/MQ-7 (MOS) + pellistor + NDIR gas sensors, electrochemical O2 sensor, SHT31/DHT22, MPU6050 IMU (stationary-shock-only), water probe, RGB camera, FLIR Lepton thermal camera, RPLIDAR A1 (clear-air aid), Jetson Orin Nano 4GB with passive-heatsink cooling, ESP32, SX1276-based LoRa modules, tracked chassis, Li-ion battery, fiber-optic tether with manual-rewind spool.

**Communication:** Fiber tether (primary, guaranteed bandwidth, matches real precedent) for video/thermal/control; LoRa 865-867 MHz (India de-licensed band) as a telemetry-only backup, with a 13-29 m coal-mine-measured range used as the honest planning baseline, not a theoretical link-budget figure; India duty-cycle compliance is an open item requiring resolution before final submission.

**AI:** A deterministic rule engine (not ML) is the safety authority for gas/O2/water/shock thresholds, with an oxygen-based arbitration rule deciding which combustible-gas sensor to trust; a rule-based (not yet ML-trained, due to a genuine dataset gap) thermal-blob detector supports trapped-worker location as human-supervised decision support, never an autonomous trigger.

**Outputs:** Live video, live thermal imagery, real-time telemetry, a four-level hazard state, thermal-detection alerts, sensor-fault/disagreement alerts, and mission logs - all feeding a human go/no-go decision.

**Key technical parameters:** See Part 38 for the full consolidated table; headline figures include a ~18-25 W average power draw (calculated, unmeasured), a 60-90 minute mission-duration target (unmeasured), and a 13-29 m LoRa range design baseline (unmeasured for this specific mine).

**Cost:** Prototype approx Rs.1,12,000-Rs.1,61,000 (itemized, Part 11/30); production cost is not estimable without an Ex-certification/manufacturing-partner quote.

**MVP:** Tracked rover with the full sensor suite, tethered video/thermal/control, LoRa telemetry backup, and a local dashboard, demonstrated against a simulated incident (calibration gas, a heated object standing in for a worker, a water tray, a rubble course) - see Part 32.

**Production vision:** Ex-rated/intrinsically-safe certified hardware, a certified gas-sensing module, dedicated geotechnical instrumentation, and DGMS-compatible live reporting - explicitly not attempted at the prototype stage.

**Main innovation:** An oxygen-arbitrated, triple-redundant gas-sensing architecture that closes a real, documented single-point-of-failure gap in both individual sensor technologies used; a communication architecture chosen by grounding the video-link decision in an actual coal-mine RF field measurement rather than an unexamined technology preference.

**Main risks:** Unmeasured LoRa range and thermal-detection contrast; an unresolved India LoRa duty-cycle question; a fiber tether's mechanical fragility; the FLIR Lepton's 14-week lead time; the unresolved intrinsic-safety certification gap between this prototype and any real deployment.

**Validation status:** Architecturally complete and internally consistent; **experimentally, almost everything remains pending** (Part 33/34) - this is stated as the honest current state of the project, not minimized, because presenting calculated or research-derived numbers as measured results would be the single most damaging thing this document could do to the team's credibility.
