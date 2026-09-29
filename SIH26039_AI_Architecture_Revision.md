# AI-POWERED ARCHITECTURE REVISION — SIH26039 ShaktiMine
### Research-driven revision of the Canonical Master Solution Document, addressing the PS's explicit "AI-powered" requirement

---

## 1. EXECUTIVE FINDING

**AI belongs in exactly one place in this system: interpreting the thermal camera feed to flag candidate trapped-worker locations for the operator.** This is the only part of the PS's required functionality that is genuinely a *perception/pattern-recognition* problem — a human body's thermal signature varies with pose, distance, partial occlusion by rubble, and clothing, in ways a fixed threshold cannot reliably capture. Everything else the system does (gas/O2/water/shock hazard evaluation) is a *known-threshold* problem where the values that matter are already defined by regulation and physics — adding a trained model there would be strictly worse: less auditable, harder to validate, and solving a problem that doesn't need solving. This finding does not change from the prior version of the Master Document; what changes is the **strength and specificity** of the AI implementation, upgraded from a hedge ("no dataset, rule-based only") to a concrete, evidence-backed pipeline using public thermal-person-detection datasets and a benchmarked edge-deployable model.

---

## 2. PROBLEM STATEMENT AI REQUIREMENT ANALYSIS

| PS Requirement | Exact Meaning | Priority | Where AI Could Potentially Help |
|---|---|---|---|
| "AI-Powered" (title) | The overall system should employ AI where genuinely applicable | Mandatory (framing) | Perception tasks — see below |
| "Using AI-based analysis and remote monitoring capabilities" (description) | AI should process sensor/imagery data to support decisions | Mandatory | Thermal/video interpretation |
| "Detect toxic gases, monitor temperature and humidity" | Sensing, not inherently an AI task | Mandatory | Low — values have known physical thresholds |
| "Identify potential hazards" | Could be threshold-based or learned | Mandatory | Marginal — see Part 3 |
| "Assist in locating trapped workers" | Requires interpreting camera/thermal data for human presence | Mandatory | **High — this is the core AI opportunity** |
| "Structural conditions" | Requires interpreting vibration/geotechnical signals | Strongly implied | Low at prototype scale — see hardware limits, Master Doc Part 12 |
| "Live video and thermal imaging" | Data transmission, not itself an AI task | Mandatory | None (transport, not AI) |
| "Situational awareness" | Presentation of information to humans | Strongly implied | Low — a dashboard, not an AI task |

---

## 3. AI OPPORTUNITY LANDSCAPE

| Category | Applicable here? | Verdict |
|---|---|---|
| Perception (image/video/thermal) | Yes — thermal frames need interpretation to spot a person | **Selected AI opportunity** |
| Classification (risk levels, environmental states) | Technically possible (e.g., classify gas readings into risk bands) but the bands are already regulation-defined | Rejected — rule engine is the correct, more auditable tool (unchanged from prior Master Doc) |
| Detection (anomalies in gas trend) | Possible via statistical/ML anomaly detection | Evaluated in Part 6; kept as a simple statistical technique (EWMA), not elevated to full ML — see justification below |
| Prediction/forecasting (structural failure, gas trend) | Genuinely hard, genuinely valuable in principle | Rejected for MVP — data to train any predictive model (mine-specific incident precursors) does not exist and cannot be fabricated; flagged as a production-research direction, not a prototype claim |
| Optimization (routing, resource allocation) | Not required by this PS (single rover, not a fleet/routing problem) | Rejected — not applicable to this PS's scope |
| Decision support (combining multiple inputs into a single score) | Already implemented as the deterministic rule engine's arbitration logic | Rejected as an ML task — the combination rule is regulation/physics-derived, not learned |
| Natural language / LLM | PS involves no text, reports, or conversational interaction | Rejected outright — would be AI-for-the-sake-of-AI |

---

## 4. RESEARCH FINDINGS

**Finding 1 — thermal person detection is a well-studied, genuinely hard perception problem, not a threshold problem.** Peer-reviewed research (Ivašić-Kos, Krišto & Pobar, "Person Detection in Thermal Videos Using YOLO," IntelliSys 2019 / Springer, DOI 10.1007/978-3-030-29513-4_18) directly tested this exact task class: person detection in thermal video across varying range, pose (walking, running, sneaking) and weather. Their key result: a YOLO model **fine-tuned on thermal imagery significantly outperformed the same YOLO architecture used out-of-the-box** (i.e., trained only on visible-light COCO data). This is direct evidence that (a) the task is non-trivial enough to need a trained model rather than a simple threshold, and (b) domain-specific fine-tuning, not just a generic pretrained detector, is what makes the difference.

**Finding 2 — public thermal-person-detection datasets exist and are usable as a starting point.** Two openly available datasets were identified: a Roboflow Universe thermal people-detection dataset (~21,622 labeled images) and the UNIRI-TID thermal person dataset (~6,111 images, IEEE DataPort). This materially changes the prior Master Document's position (Part 21: "no dataset exists yet") — a real dataset gap remains for the *mine-specific domain*, but not for the underlying task of "is there a person-shaped heat blob in this thermal frame," which can be bootstrapped via transfer learning.

**Finding 3 — real-time inference on our exact compute hardware is well within budget.** Multiple independent Jetson Orin Nano benchmarks (via TensorRT, FP16 precision) show YOLOv8n — the smallest variant of a modern, well-supported object-detection architecture — running at roughly 60 FPS with ~7 ms inference latency on this hardware. Our thermal camera's own frame rate (≈8.6 Hz, per Master Doc Part 12) is far below this ceiling, meaning the AI model is never the bottleneck; the sensor is.

---

## 5. EXISTING AI SOLUTIONS / RELATED SYSTEMS

| System | Problem | AI Used | Input | Model | Output | Deployment | Limitation |
|---|---|---|---|---|---|---|---|
| Ivašić-Kos et al. (2019) research system | Person detection in thermal video, night/varied weather | Fine-tuned YOLO (v3, in that study) | Thermal video frames | CNN object detector | Bounding boxes + confidence | Research prototype, outdoor surveillance context | Not mine-specific; outdoor scenes have different background thermal characteristics than an underground tunnel |
| Public thermal-detection model (Hugging Face, YOLOv8n fine-tuned) | General human detection in thermal/pseudo-color imagery | YOLOv8n fine-tuned on thermal data | Thermal/pseudo-color images | YOLOv8n | Bounding boxes | Publicly released model checkpoint | Trained on general surveillance-style scenes, not underground/low-contrast environments — would need mine-domain fine-tuning, not used as-is |
| Sandia Gemini-Scout (Master Doc REF-004) | Mine rescue reconnaissance | Not AI — a human operator visually interprets the thermal feed | Thermal/RGB video | None (human-in-the-loop only) | Operator judgment | Field-tested | No automated detection at all — our AI component is a genuine improvement over this specific precedent, not a redundant addition |

**What we learn, not just collect:** The closest real precedent (Gemini-Scout) has *no* automated detection — a human watches the feed. Our AI addition is a real, specific improvement over that precedent (faster triage of a live feed, not a replacement for the operator), not decoration. The academic literature confirms the task needs a trained, thermal-specific model rather than an off-the-shelf RGB detector or a simple threshold.

---

## 6. AI USE-CASE COMPARISON

| AI Opportunity | Input | AI Task | Candidate Model | Output | Benefit | Data Availability | Complexity | Need for AI |
|---|---|---|---|---|---|---|---|---|
| **Thermal person detection** | Thermal frames (80×60 or 160×120 px) | Object detection | YOLOv8n (or equivalent lightweight detector) | Bounding box + confidence per candidate person | Faster, more consistent triage of a live feed than an operator alone; frees the operator to watch multiple streams | Public datasets exist (Roboflow, UNIRI-TID) for transfer learning; mine-domain fine-tuning data must be collected | Low-moderate (well-supported architecture, small model) | **High** — genuinely a perception task |
| Gas-trend anomaly detection | Time-series gas readings | Anomaly/outlier detection | Isolation Forest / simple statistical control chart | Anomaly flag | Marginal — thresholds already regulation-derived | No mine-specific incident dataset exists to validate against | Low, but unjustified | **Low** — EWMA (already in the architecture) covers the genuine need without a trained model |
| Structural-risk prediction | IMU/vibration data | Time-series prediction | LSTM / temporal CNN | Risk score | Would be valuable in principle | No training data exists, and a single rover-mounted IMU's signal quality (Master Doc Part 12: dominated by the rover's own locomotion noise) is not adequate input even if data existed | High, and unjustified given data/hardware limits | **None at prototype scale** — correctly excluded |
| Hazard-state classification (gas+O2+water combined) | Multi-sensor readings | Multi-class classification | Random Forest / rule engine | Hazard state | No — thresholds are already regulation-derived | N/A | Unjustified complexity | **None** — rule engine is strictly better here (auditable) |

---

## 7. SELECTED AI APPROACH

**A lightweight CNN object detector (YOLOv8n-class), fine-tuned for thermal person detection, running on-device on the Jetson Orin Nano, feeding operator-facing alerts.** This is the single AI component in the system. Everything else remains deterministic (rule engine) or simple statistics (EWMA trend), per the "minimum necessary" principle and per the Part 6 comparison above, which found no other candidate opportunity clears the bar of genuine necessity plus data/deployment feasibility.

---

## 8. WHY THIS AI APPROACH

- **PS relevance:** Directly implements "assist in locating trapped workers" and "AI-based analysis," the two PS phrases most clearly pointing at a perception task.
- **AI necessity over a rule-based approach:** A fixed-temperature threshold (the prior MVP's rule-based blob detector) cannot distinguish a person-shaped heat signature from a similarly-warm piece of equipment, nor adapt to partial occlusion — exactly the failure modes the peer-reviewed literature's varied-pose, varied-range test conditions were designed to probe. A trained detector, even a small one, learns shape/context cues a fixed threshold cannot encode.
- **Data feasibility:** Public datasets provide a genuine starting point (21,622 + 6,111 images across two sources) — this is not a fabricated dataset size, it's a cited, existing resource the team can actually download and use.
- **Deployment feasibility:** Benchmarked at ~60 FPS / ~7 ms latency on our exact compute module (Jetson Orin Nano, TensorRT FP16) — enormous headroom over the thermal camera's 8.6 Hz frame rate.
- **Explainability:** Bounding box + confidence score is directly inspectable by the operator in real time — the operator sees exactly what the model flagged and where, unlike a black-box risk score.
- **Alternative considered and rejected:** A classical ML approach (e.g., HOG+SVM) was considered as a lower-compute alternative; rejected because our compute headroom is not the constraint (Finding 3) and the peer-reviewed literature specifically evidences a CNN-based (YOLO) approach outperforming for this exact thermal/varied-pose task class.

---

## 9. COMPLETE AI PIPELINE

| Stage | Input | Output | Technology | Data format | Frequency | Processing location | Latency | Failure behavior |
|---|---|---|---|---|---|---|---|---|
| Data source | Physical scene (human body heat) | — | — | — | Continuous | — | — | — |
| Data acquisition | Scene | Raw thermal frame | FLIR Lepton | 80×60 or 160×120 px, 14-bit | ~8.6 Hz | On-rover | <10 ms (sensor readout) | Frame drop flagged, not silently skipped |
| Preprocessing | Raw thermal frame | Normalized frame | Simple normalization/resize to model input size | Array | Per-frame | Jetson (CPU/GPU) | <5 ms | Malformed frame discarded, logged |
| Feature extraction / representation | Normalized frame | Learned feature maps | Internal to the CNN (YOLOv8n backbone) | Tensor | Per-frame | Jetson GPU (TensorRT) | Included in inference latency below | N/A — internal to model |
| AI model (inference) | Normalized frame | Bounding boxes + class + confidence | YOLOv8n, TensorRT FP16 | Tensor → structured detections | Per-frame (up to 60 FPS capacity; run at the camera's native ~8.6 Hz) | Jetson GPU | ~7 ms (benchmarked) | On model/runtime crash, Jetson-side software restarts the inference process; rule engine and operator's raw visual feed are unaffected (independent of this pipeline) |
| Confidence/uncertainty | Raw detections | Filtered detections above a confidence floor | Post-processing threshold on YOLO's own confidence output | Structured list | Per-frame | Jetson | <1 ms | Low-confidence detections still surfaced but visually de-emphasized, not discarded — recall-biased per design principle |
| Decision logic | Filtered detections | "Candidate person detected" alert | Simple pass-through (no further ML) — the alert is generated whenever ≥1 detection clears the confidence floor | Alert object | Per-frame | Jetson | <1 ms | Alert absence is never presented as "confirmed no person" — dashboard explicitly frames it as "no candidate detected this frame," not "area clear" |
| Action/alert/output | Alert object | Visual highlight on operator's live thermal feed + log entry | Dashboard overlay | UI + log row | Real-time | Surface dashboard | Bound by comms latency (Master Doc Part 10) | Operator makes the actual judgment; system never claims to have located or ruled out a person on its own authority |

---

## 10. MODEL SELECTION

| Model | Why suitable | Data requirement | Compute | Latency | Interpretability | Prototype feasibility |
|---|---|---|---|---|---|---|
| Fixed-threshold blob detection (prior MVP fallback) | Zero training data needed | None | Trivial | <1 ms | Fully transparent | High, but weak on partial occlusion/varied pose (the exact failure mode the literature tests) |
| **YOLOv8n, fine-tuned on thermal data (selected)** | Purpose-built, well-supported, benchmarked on our exact hardware; peer-reviewed evidence of thermal-domain effectiveness | Public datasets (27,733 images combined across two sources) as a base, plus team-collected mine-like footage for domain fine-tuning | Runs comfortably within Jetson Orin Nano's budget (Part 9 above) | ~7 ms per frame (TensorRT FP16, benchmarked) | Bounding box + confidence — directly inspectable | High — well-documented tooling (Ultralytics), transfer learning reduces training burden |
| YOLOv8s/m (larger variants) | Marginally higher accuracy in some benchmarks | Same datasets, more training time | Still comfortably within budget, but unnecessary margin | ~11–24 ms (still fine, but no benefit at our task scale) | Same | Unnecessary complexity for a single-class (person) detection task at this resolution |
| HOG+SVM (classical, non-deep-learning) | Very low compute | Smaller dataset need | Very low | Very low | Fully transparent, feature-based | Rejected — literature (Part 4/8) shows CNN-based detection specifically outperforms for varied pose/range/occlusion, which is precisely our concerning failure mode |
| LSTM/temporal model (video sequence, not single-frame) | Could exploit motion cues | Requires labeled video sequences, not just frames — a materially bigger data-collection burden | Higher | Higher | Lower | Rejected for MVP — added complexity without a demonstrated need over frame-by-frame detection for this task |

**Selected: YOLOv8n**, for the reasons in the table and Part 8.

---

## 11. DATA STRATEGY

- **Base dataset (transfer learning source):** Roboflow Universe "people-detection-thermal" dataset (~21,622 images, white-hot thermal palette) and the UNIRI-TID thermal person dataset (~6,111 images, rainbow-palette thermal, IEEE DataPort). Both are cited, existing, publicly accessible resources — not fabricated.
- **Domain-specific fine-tuning data (required, not yet collected):** A small, team-collected set of thermal frames from a mock tunnel/obstacle-course environment, featuring a person at varying distances, poses, and partial occlusion (rubble/debris), matching the exact failure mode the peer-reviewed study specifically tested for. **This collection has not happened yet — stated as "data collection required during the prototype phase," not fabricated as complete.**
- **Labels:** Bounding boxes around the person, single class ("person"). The base datasets are pre-labeled; team-collected footage requires manual annotation (a small, tractable task at prototype scale — tens to low hundreds of frames, not thousands, since this is fine-tuning, not training from scratch).
- **Class balance:** The team-collected set should deliberately over-sample partially-occluded/low-contrast frames, since that is the highest-risk failure mode (unchanged principle from the prior Master Document, Part 21).
- **Train/validation/test split:** Standard 70/15/15 or similar split is planned for the fine-tuning set; **not yet executed — requires the data collection step above first.**
- **Domain shift:** The base datasets are outdoor/surveillance-style scenes; the underground mine environment has different background thermal characteristics (Master Doc Part 12's thermal-contrast concern). This is exactly what the fine-tuning step is for — using the base dataset for general "what does a person look like in thermal" knowledge, and the fine-tuning set for "what does a person look like in *this* kind of low-contrast, cluttered background."
- **Synthetic data:** Not used; not currently planned — an honest scope limit, not a gap papered over with fabricated synthetic imagery.

---

## 12. AI PERFORMANCE METRICS

For an object-detection task, the appropriate metrics are:
- **Recall** (primary metric for this application — a missed detection is the costly failure mode, consistent with the recall-biased design principle carried over from the prior Master Document, Part 20).
- **Precision** (secondary — false alarms cost operator attention, not safety).
- **mAP@0.5** and **mAP@0.5:0.95** (standard object-detection benchmarks, useful for comparing our fine-tuned model against the base pretrained checkpoint to confirm fine-tuning actually helped).
- **Inference latency** (already benchmarked at ~7 ms on our hardware — a hardware feasibility metric, not a task-accuracy metric).

**No specific target number is stated for recall/precision/mAP at this stage** — consistent with the "never fabricate" rule. The correct process is: fine-tune, measure on a held-out test set, report the actual number.

---

## 13. AI FAILURE / SAFETY DESIGN

| Failure mode | Safeguard |
|---|---|
| False positive (flags a heat source that isn't a person) | Low cost — operator visually confirms via the same live feed the model is looking at; alert is decision support, not an autonomous trigger |
| False negative (misses a real person) | The higher-cost failure mode — mitigated by (a) a low confidence threshold (recall-biased), (b) the operator independently watching the raw feed regardless of whether the model fires, so the model is a triage aid, not the only line of defense |
| Low confidence / borderline detection | Surfaced to the operator with its confidence score visible, not silently dropped |
| Out-of-distribution input (mine environment differs from training data) | This is precisely why domain-specific fine-tuning (Part 11) is required before the model is trusted in this environment — the plan explicitly does not claim the base pretrained model alone is sufficient |
| Model/software crash | Runs on the Jetson; independent of the ESP32-hosted safety rule engine (Master Doc Part 26/27) — an AI crash degrades detection assistance, never the underlying hazard-alarm system |
| Network/comms failure | Inference runs entirely on-device (edge, not cloud) — no dependency on any communication link to function; only the *display* of results to the operator depends on the tether/LoRa link, which is already covered by the existing failure-mode design (Master Doc Part 26) |

**Design principle carried through unchanged:** AI prediction → confidence surfaced → human verification → human decision. The AI never autonomously declares an area clear or occupied.

---

## 14. HARDWARE RE-EVALUATION

| Component | Required by PS? | Required for AI? | Required for other functions? | Keep/Remove | Reason |
|---|---|---|---|---|---|
| FLIR Lepton (thermal camera) | Yes (explicit) | **Yes — sole data source for the AI model** | Also used for direct human viewing on the dashboard | Keep | Unchanged — now doubly justified |
| Jetson Orin Nano | Not named by PS, but implied by "AI-based analysis" | **Yes — runs the YOLOv8n inference** | Also handles video encoding | Keep | Now has a concrete, benchmarked workload justifying its selection (previously justified more generically) |
| RGB camera | Yes (explicit, "live video") | No | Live visual reconnaissance | Keep | Unchanged |
| Gas sensors (MOS/pellistor/NDIR), O2, temp/humidity, water probe, IMU | Yes (explicit) | No — these feed the deterministic rule engine, not the AI model | Core hazard sensing | Keep | Unchanged — correctly not folded into the AI pipeline (Part 3/6 finding) |
| RPLIDAR A1 | Not named by PS | No | Clear-air mapping aid (Master Doc Part 12) | Keep, unchanged scope | Not required for AI; retained for its already-limited, disclosed role |
| ESP32 | Not named by PS | No — deliberately excluded from anything AI-related | Runs the safety-critical rule engine | Keep | Its independence from the Jetson/AI path is a safety feature, not a gap (Part 13 above) |

**No new hardware is required by this AI revision.** The FLIR Lepton and Jetson Orin Nano were already present in the architecture for other stated reasons (PS-required thermal imaging; general edge compute); this revision gives the Jetson's presence a sharper, benchmarked justification rather than adding anything new.

---

## 15. SOFTWARE RE-EVALUATION

| Software | Purpose | Required? | Used by AI? | Used elsewhere? | Keep/Remove |
|---|---|---|---|---|---|
| Ultralytics YOLO framework (training/export tooling) | Fine-tune and export the detection model | Yes, for the AI pipeline specifically | Yes — this is the AI | No | Add (new, minimal — a training-time tool, not a runtime service) |
| TensorRT runtime | Optimized on-device inference | Yes | Yes | No | Add (already implicitly needed for any serious Jetson inference workload; now explicitly named) |
| Local dashboard (existing) | Operator interface | Yes | Displays AI output (bounding box overlay) | Displays all other telemetry | Keep, minor extension (an overlay, not a new service) |
| SQLite (existing) | Mission logging | Yes | Logs AI alert events alongside other alerts | Yes | Keep, unchanged schema role (one more alert `type` value, no new table) |
| Cloud/microservices/message brokers/vector DB/LLM orchestration | N/A | No | No | No | **Not added** — the "absolute architecture rule" is satisfied; nothing in this AI revision requires any of these |

**No new software layer is introduced beyond model-training tooling and the TensorRT inference runtime** — both directly necessary for the one AI component, nothing else.

---

## 16. MINIMUM VIABLE AI (MVA)

- **Input:** Thermal frames from the FLIR Lepton (80×60 or 160×120 px, ~8.6 Hz).
- **Dataset:** Roboflow Universe thermal people-detection set (~21,622 images) and/or UNIRI-TID (~6,111 images) for transfer learning; a small team-collected fine-tuning set (data collection required during the prototype phase — not yet done).
- **Model:** YOLOv8n, pretrained on the public thermal dataset(s), fine-tuned on the team's own mine-like footage.
- **Training:** Transfer learning (fine-tuning only, not training from scratch) — tractable on a single consumer GPU or a cloud notebook, well within a student team's realistic timeline.
- **Inference:** On-device on the Jetson Orin Nano via TensorRT (FP16), benchmarked at ~7 ms/frame — far faster than needed.
- **Output:** Bounding box + confidence score, overlaid on the live thermal feed on the dashboard.
- **Metric:** Recall (primary), precision, mAP@0.5 — measured on a held-out split of the team's own fine-tuning data once collected; **no number claimed until measured.**
- **Hardware:** FLIR Lepton + Jetson Orin Nano — both already in the architecture for independent reasons.
- **Software:** Ultralytics YOLO (training-time only) + TensorRT (runtime).
- **Deployment:** Fully on-device, no cloud dependency, consistent with the rest of the architecture's no-cloud-for-MVP principle (Master Doc Part 17).
- **Prototype demonstration:** Live thermal feed with real-time bounding-box overlay during the simulated-incident demo (a heated object standing in for a person, per Master Doc Part 32's "CAN SIMULATE" scoping).

**This MVA is realistically buildable by the team within a hackathon timeline**, because it relies on transfer learning from an existing dataset rather than data collection and training from scratch.

---

## 17. PRODUCTION AI

- **Larger, mine-domain-specific dataset:** Collected from real or realistic mine environments over time, not just a bench mock-up.
- **Model refinement:** Possible move to a slightly larger YOLO variant if accuracy gains justify the (still modest) latency cost, or exploration of thermal-specific architectures beyond a repurposed RGB-detection backbone.
- **Continuous learning / monitoring:** A feedback loop where confirmed/rejected detections from real missions improve future fine-tuning — explicitly a production-phase capability, not built for the prototype.
- **Model updates:** A defined process for periodically retraining and redeploying the model as more mine-specific data accumulates.
- **Edge optimization:** INT8 quantization (evaluated but not required at prototype scale, since FP16 already comfortably meets latency needs per Part 9/10).

**None of this is included in the MVP** — it is explicitly deferred, consistent with the "do not put production-only complexity into the MVP" rule.

---

## 18. REVISED SYSTEM ARCHITECTURE

**High-level:** Unchanged from the Canonical Master Document (Part 9) in overall shape — Sensor Layer → Edge Compute (ESP32 safety path + Jetson AI/video path) → Communication Layer → Surface Dashboard → Human Decision. This revision sharpens what happens *inside* the Jetson's video/thermal path; it does not change the overall shape.

**Hardware:** Unchanged (Part 14 above confirms no new components).

**Software:** One addition — model training/export tooling (development-time only) and the TensorRT runtime (deployment-time) — both scoped to the single AI component (Part 15).

**AI/ML architecture:**
```
Thermal camera (FLIR Lepton, ~8.6 Hz)
        |
        v
Jetson Orin Nano — YOLOv8n (TensorRT FP16), fine-tuned on thermal person data
        |
        v
Bounding box + confidence (per frame)
        |
        v
Confidence-floor filter (recall-biased)
        |
        v
Dashboard overlay + alert log entry
        |
        v
Human operator judgment (final authority — unchanged from Master Doc Part 24)
```

**Data flow:** Identical to Master Doc Part 10, with the Jetson's internal processing now specified concretely (Part 9 above) rather than left as "thermal-blob inference" in general terms.

**Deployment:** Unchanged — fully on-device, no cloud dependency (Part 15/16 above).

---

## 19. REVISED END-TO-END DATA FLOW

Identical in structure to Master Doc Part 10; the row "Jetson → Surface (video/thermal/control)" now explicitly includes the AI overlay as part of what's transmitted (bounding box coordinates + confidence, a few dozen bytes per frame — negligible addition to the existing video/thermal data budget in Master Doc Part 15).

---

## 20. REVISED MASTER SOLUTION DOCUMENT — SECTION-BY-SECTION STATUS

Per the instruction to revise every listed section: most sections are **UNCHANGED** because this revision sharpens (not restructures) the AI component within an already-correct overall architecture. Sections requiring actual rewrites are marked accordingly; all others are confirmed valid as previously documented.

| # | Section | Status | Note |
|---|---|---|---|
| 1 | Executive Project Identity | MODIFIED | Add: "a lightweight, fine-tuned computer-vision model (YOLOv8n) interprets the thermal feed to flag candidate trapped-worker locations" as a specific line, replacing the vaguer "thermal-blob detector" phrasing |
| 2 | Problem Statement | UNCHANGED | PS text and requirement table are factual, not affected |
| 3 | Problem Analysis | UNCHANGED | |
| 4 | User/Stakeholder Model | UNCHANGED | |
| 5 | Existing Solutions | MODIFIED | Add the finding that Gemini-Scout has no automated detection (Part 5 above) — strengthens the innovation claim |
| 6 | Problem-Solution Gap | MODIFIED | Add one row: "No automated triage of the thermal feed in existing precedent → AI-assisted candidate-detection overlay" |
| 7 | Final Solution Overview | MODIFIED | 7.6 (AI/ML intelligence) rewritten with the concrete YOLOv8n pipeline instead of the general "thermal-blob detector, classical image processing, or a small CNN if time permits" hedge |
| 8 | Requirement Traceability | MODIFIED | R-010 status upgraded from "Requires validation — no dataset/measurement exists yet" to "Requires validation — transfer-learning pipeline defined, mine-domain fine-tuning data collection pending" |
| 9 | System Architecture | MODIFIED | Per Part 18 above |
| 10 | End-to-End Data Flow | MODIFIED | Per Part 19 above |
| 11 | Hardware Specification | UNCHANGED | Confirmed via Part 14 audit — no new components |
| 12 | Sensor Engineering | UNCHANGED | FLIR Lepton entry stands; its role is now more precisely described in Parts 7/20, not altered in spec |
| 13 | Communication Engineering | UNCHANGED | |
| 14 | Link Budget | UNCHANGED | |
| 15 | Data Budget | MODIFIED (minor) | Add a negligible line item for bounding-box metadata piggybacking on the existing thermal stream |
| 16 | Power Budget | UNCHANGED | Inference workload is well within the Jetson's already-budgeted power envelope (Master Doc Part 16); no new draw introduced |
| 17 | Software Architecture | MODIFIED | Add Ultralytics/TensorRT as a training-time/runtime tool, per Part 15 |
| 18 | API Specification | UNCHANGED | No new endpoint required — detection results are folded into the existing thermal stream/overlay, not a separate API |
| 19 | Database | MODIFIED (minor) | `alerts` table's existing `THERMAL_DETECTION` type now has a concrete producer (the YOLOv8n pipeline) instead of a placeholder |
| 20 | AI/ML Architecture | REWRITTEN | Entirely superseded by Parts 9–13 above |
| 21 | AI Dataset | REWRITTEN | Superseded by Part 11 above — the "no dataset exists" framing is corrected to "public base dataset exists; mine-domain fine-tuning set does not yet exist" |
| 22 | AI Performance | MODIFIED | Metrics list expanded to include mAP@0.5, consistent with Part 12 above; "Actual" column remains N/A pending the fine-tuning/testing step |
| 23 | Algorithms | MODIFIED | "Algorithm 3 — Thermal Blob Detection" is superseded/renamed "Algorithm 3 — Thermal Person Detection (YOLOv8n)"; see Part 9 pipeline above for the new specification |
| 24 | Decision Engine | UNCHANGED | The rule engine's authority and the human-override principle are untouched — AI remains subordinate, as designed |
| 25 | Security | UNCHANGED | |
| 26 | Failure Modes | MODIFIED (minor) | Add the model/software-crash and out-of-distribution rows per Part 13 above (these refine, not contradict, the existing "thermal false negative" row) |
| 27 | Reliability | UNCHANGED | |
| 28 | Environmental Conditions | UNCHANGED | |
| 29 | Scalability | UNCHANGED | |
| 30 | Cost Model | MODIFIED (minor) | No new hardware cost; a small addition for GPU compute time during model fine-tuning (a one-time, low development cost — e.g., a few hours on a rented cloud GPU or a laptop GPU, not itemized as a BOM line since it's not rover hardware) |
| 31 | Feasibility | MODIFIED | AI feasibility row strengthened with the transfer-learning/benchmark evidence from this revision |
| 32 | MVP | MODIFIED (minor) | "Thermal-blob detection (rule-based...)" bullet under SHOULD BUILD is replaced with "Thermal person detection (YOLOv8n, transfer-learned)" |
| 33 | Validation Plan | MODIFIED | The thermal-detection test row is refined to include a mAP@0.5 measurement alongside recall/false-negative rate |
| 34 | Expected vs Measured Performance | UNCHANGED in structure | Same N/A-until-measured discipline applies |
| 35 | Innovation | MODIFIED | Add the "no automated detection in real precedent systems" finding as a specific, evidenced innovation point |
| 36 | Risks | MODIFIED (minor) | Add "mine-domain fine-tuning data collection incomplete" as an explicit, named risk (distinct from the pre-existing "no dataset" framing, since a base dataset now exists) |
| 37 | Implementation Roadmap | MODIFIED (minor) | Milestone 5 (AI) now specifies: download/prepare base dataset, fine-tune, export to TensorRT, integrate |
| 38 | Final System Specification | MODIFIED | AI row updated to name YOLOv8n specifically |
| 39 | Glossary | MODIFIED (minor) | Add: YOLO, mAP, transfer learning, TensorRT |
| 40 | Decision Log | MODIFIED | Add Decision D-013 (below) |
| 41 | Assumption Register | MODIFIED | Add Assumption A-009 (below) |
| 42 | Source Library | MODIFIED | Add REF-026 through REF-028 (below) |
| 43 | Source-to-Claim Matrix | MODIFIED | Add corresponding claim IDs |
| 44 | SIH Evaluator Defense | MODIFIED | AI-specific questions strengthened with concrete answers (Part 26 below) |
| 45 | PPT Extraction Map | UNCHANGED | AI content still maps to the same slide (Technical Approach / AI-ML) |
| 46 | LLM Usage Instructions | UNCHANGED | |
| 47 | Change Control | MODIFIED | This entire document is logged as a new revision entry |
| 48 | Final Canonical Summary | MODIFIED | AI description sharpened per Part 1 above |

**New Decision (added to Part 40, Decision Log):**
| D-013 | Use YOLOv8n fine-tuned via transfer learning, not a rule-based detector, as the production-direction thermal-detection model | Rule-based thresholding (prior MVP fallback); larger YOLO variants; classical HOG+SVM; LSTM/video-sequence models | Peer-reviewed evidence that thermal-domain fine-tuning meaningfully outperforms threshold/generic approaches for this exact varied-pose/occlusion task; benchmarked real-time feasibility on our exact compute hardware; public datasets remove the "no data" objection | Ivašić-Kos et al. (2019); Jetson Orin Nano YOLOv8n TensorRT benchmarks; Roboflow/UNIRI-TID datasets |

**New Assumption (added to Part 41, Assumption Register):**
| A-009 | Fine-tuning the base public thermal-detection dataset on a small team-collected mine-like footage set will meaningfully close the domain-shift gap (outdoor/surveillance scenes → underground tunnel) | Needed to trust the model's output in the actual deployment environment, not just on the public benchmark | If the domain shift is too large for a small fine-tuning set to close, detection performance in the real environment could be materially worse than on the public dataset | Bench/on-site testing with the team's own held-out fine-tuning split (Part 33 revision) | **Open — this is now the primary AI-related open question, replacing the prior "no dataset" gap with a narrower, more specific one** |

**New References (added to Part 42, Source Library):**
- **REF-026:** Ivašić-Kos, M., Krišto, M., & Pobar, M. (2019). "Person Detection in Thermal Videos Using YOLO." In *Intelligent Systems and Applications (IntelliSys 2019)*, pp. 254–267. Springer. DOI: 10.1007/978-3-030-29513-4_18. Finding used: thermal-domain fine-tuning of YOLO significantly outperforms out-of-the-box (RGB-trained) YOLO for person detection in thermal video across varied pose/range/weather.
- **REF-027:** Roboflow Universe. "People Detection Thermal" dataset (~21,622 images). Finding used: public, usable base dataset for transfer learning.
- **REF-028:** UNIRI-TID Thermal Image Dataset for Person Detection (~6,111 images). IEEE DataPort. Finding used: second public base dataset, rainbow-palette thermal imagery, for transfer learning diversity.
- **REF-029:** Community-benchmarked YOLOv8n TensorRT inference results on NVIDIA Jetson Orin Nano (multiple independent GitHub benchmark repositories, cross-checked). Finding used: ~60 FPS / ~7 ms latency at FP16 precision — confirms real-time feasibility on our exact compute hardware.

---

## 21. CHANGE LOG

| Section | Previous | Revised | Reason | Evidence |
|---|---|---|---|---|
| AI/ML Architecture (Part 20) | "Rule-based thresholding... or a small CNN if time permits," with no dataset and no benchmark | YOLOv8n, transfer-learned from named public datasets, benchmarked at ~7ms on Jetson Orin Nano | The prior framing was a hedge, not a decision; research resolved the hedge into a concrete, defensible plan | REF-026, REF-027, REF-028, REF-029 |
| AI Dataset (Part 21) | "None exists yet... largest unresolved gap" | Public base datasets exist (27,733 images combined); mine-domain fine-tuning set is the remaining, narrower gap | Same as above | REF-027, REF-028 |
| Algorithms (Part 23) | "Algorithm 3 — Thermal Blob Detection" (threshold + connected components) | "Algorithm 3 — Thermal Person Detection (YOLOv8n)" | Upgraded from a placeholder rule-based fallback to the actual selected model | Part 9/10 above |
| Requirement Traceability (Part 8), R-010 | "Requires validation — no dataset/measurement exists yet" | "Requires validation — pipeline defined, fine-tuning data collection pending" | More specific, evidence-backed status | Part 11 above |

**ADDED:** Concrete model selection (YOLOv8n), transfer-learning data strategy, benchmarked latency figures, one new decision (D-013), one new assumption (A-009), four new references (REF-026–029).
**MODIFIED:** Executive summary AI description, solution overview §7.6, system/data-flow diagrams (AI internals only), MVP bullet, validation plan's thermal-detection row, innovation section, risk register, implementation roadmap Milestone 5.
**REMOVED:** Nothing — no component was found unnecessary by this research; the rule-based blob detector is retained conceptually as what the fallback would be if the fine-tuning step fails to complete in time (a schedule risk mitigation, not a competing architecture).
**UNCHANGED:** Everything not touching the AI component specifically — hardware list, communication architecture, decision-engine authority structure, security, database schema (beyond one alert-type producer note), cost (beyond a negligible one-time compute-time note), scalability, PPT map, LLM usage instructions.

---

## 22. HARDWARE/SOFTWARE MINIMALITY AUDIT

## FINAL COMPONENT JUSTIFICATION TABLE

| Component | H/W or S/W | Function | PS Requirement Supported | AI Requirement Supported | Can Be Removed? | Decision |
|---|---|---|---|---|---|---|
| FLIR Lepton | Hardware | Captures thermal imagery | R-007 (live thermal imaging) | Sole data source for the AI model | No — removing it breaks both the explicit PS requirement and the entire AI pipeline | KEEP |
| Jetson Orin Nano | Hardware | Edge compute for video + AI inference | Implied by "AI-based analysis" | Runs YOLOv8n inference | No — removing it removes the only place AI can run without a cloud dependency, which would violate the "no cloud for MVP" design principle | KEEP |
| Ultralytics YOLO (training tooling) | Software (dev-time only) | Fine-tune and export the model | Supports R-010 (locate trapped workers) | Directly implements the AI | No — without it, there is no model to deploy | ADD (new, minimal, dev-time only — not a runtime dependency on the rover) |
| TensorRT | Software (runtime) | Optimized on-device inference | Supports R-010 | Directly implements the AI's real-time execution | No — without it, inference would be slower (still likely adequate per raw PyTorch benchmarks, but TensorRT is the standard, well-supported path and removes doubt) | ADD |
| Cloud inference service | N/A | — | Not required | Not required — on-device inference is sufficient (Part 9/16) | Yes, trivially — was never added | DO NOT ADD |
| LLM / NLP component | N/A | — | Not required — PS involves no text/conversational task | Not applicable | Yes, trivially — was never added | DO NOT ADD |
| Vector database / RAG | N/A | — | Not required | Not applicable | Yes, trivially — was never added | DO NOT ADD |
| Additional gas-focused ML model (drift compensation, anomaly detection) | N/A | — | Marginal (Part 6) | Not selected — rule engine + EWMA already cover the genuine need | Yes | DO NOT ADD (deferred to production research direction only, per Part 6/17) |

**Result: zero new hardware, two new software tools (both narrowly scoped to the one AI component, one of which is training-time-only and never runs on the rover itself).**

---

## 23. AI TRACEABILITY MATRIX

| AI Requirement/Function | Data Input | Model | Output | Decision/Action | Hardware | Software | Metric | Validation |
|---|---|---|---|---|---|---|---|---|
| Trapped-worker candidate detection | Thermal frames (FLIR Lepton, ~8.6 Hz, 80×60/160×120 px) | YOLOv8n, transfer-learned (public thermal datasets → mine-domain fine-tuning) | Bounding box + confidence score per frame | Dashboard overlay + alert log entry; operator makes the final judgment (rule engine and human authority unchanged) | Jetson Orin Nano (edge inference) | Ultralytics YOLO (training) + TensorRT (runtime) | Recall (primary), precision, mAP@0.5 | Bench trial with measured ΔT and held-out fine-tuning test split (Master Doc Part 33, revised) — **not yet run; N/A until measured** |

This is the entire AI component of the system — a single row, by design, per the "minimum necessary" principle.

---

## 24. FINAL SYSTEM SPECIFICATION (AI-relevant rows, supersedes prior Master Doc Part 38 AI row)

| Category | Parameter | Final specification | Evidence | Confidence | Status |
|---|---|---|---|---|---|
| AI | Model | YOLOv8n, transfer-learned | REF-026, REF-029 | High (architecture/technology choice) | Design decided |
| AI | Base training data | Roboflow thermal dataset (~21,622 img) + UNIRI-TID (~6,111 img) | REF-027, REF-028 | High (datasets exist and are cited) | Available now |
| AI | Domain fine-tuning data | Team-collected mine-like thermal footage | — | Engineering plan | **Not yet collected — open item** |
| AI | Inference latency | ~7 ms/frame (TensorRT FP16) | REF-029 (community benchmark, cross-checked) | High (hardware benchmark) | Benchmark from third-party sources; not yet measured on our own build |
| AI | Inference location | On-device (Jetson Orin Nano), no cloud | Part 15/16 | High | Design decided |
| AI | Recall/precision/mAP | Not yet measured | — | N/A | **Pending — no number to report until fine-tuning + testing is complete** |

---

## 25. FINAL AI ONE-LINER

> **"The AI in our solution is used to interpret live thermal-camera imagery by analyzing heat-signature patterns and producing bounding-box detections of candidate human presence, which enables the rescue-team operator to triage the live feed faster and more consistently when searching for trapped workers — without the AI ever making the final call itself."**

### 10-second evaluator answer
"Our AI is a thermal person-detector — it flags likely human heat signatures on the live feed so the operator can triage faster. It doesn't make safety decisions; that's a separate, deterministic rule engine."

### 30-second evaluator answer
"We fine-tune a lightweight object-detection model, YOLOv8n, on thermal imagery to spot candidate trapped workers in the rover's thermal feed. It runs entirely on-device on our Jetson, in about 7 milliseconds per frame — far faster than we need. We start from two public thermal-detection datasets and fine-tune on our own footage to handle the mine's low-contrast background. The model surfaces a bounding box and confidence score to the operator; it never decides anything on its own — every hazard call in our system comes from a separate, auditable rule engine, and every detection is human-verified."

### 2-minute technical explanation
"We looked systematically at where AI actually adds value in this problem versus where it would just be decoration. Gas, oxygen, water, and vibration all have physically or regulation-defined thresholds — a trained model there would be less auditable and wouldn't outperform a rule engine, so we deliberately kept those deterministic. The one place a learned model genuinely helps is interpreting the thermal camera feed: a person's heat signature varies with pose, distance, and how much rubble is covering them, and a fixed brightness threshold can't reliably tell that apart from, say, a warm piece of equipment. That's a real perception problem, and there's peer-reviewed research — Ivašić-Kos et al., 2019 — showing that a YOLO model fine-tuned specifically on thermal imagery meaningfully outperforms a generic detector for exactly this varied-pose, varied-range task. So we use YOLOv8n, starting from two public thermal-person-detection datasets — about 27,000 images combined — and we plan to fine-tune it on footage we collect ourselves from a mock tunnel environment, specifically to handle the lower thermal contrast you get underground compared to an outdoor surveillance scene. It runs on our Jetson Orin Nano, and independent benchmarks on that exact hardware show YOLOv8n running at around 7 milliseconds a frame with TensorRT — our thermal camera only produces a new frame every 116 milliseconds or so, so the model is never the bottleneck. The output is a bounding box and a confidence score overlaid on the operator's live view — it's there to help a human find someone faster, not to declare an area searched or clear on its own. We haven't run our own fine-tuning and testing yet, so we're not going to quote a recall or accuracy number until we actually have one measured on our own data — that's the one open item left in this part of the design."

---

## 26. SIH EVALUATOR DEFENSE — AI-SPECIFIC QUESTIONS (revised/strengthened)

1. **"Where exactly is the AI in your solution?"** — See Part 25 above (the one-liner and three answer lengths).
2. **"Why can't you just use thresholds for the thermal detection too?"** — Because a person's thermal signature isn't a fixed value; it varies with pose, distance, and occlusion, which is exactly the failure mode a published study (Ivašić-Kos et al., 2019) tested and found a threshold-style/generic approach insufficient for, versus a thermal-fine-tuned detector.
3. **"Where does your training data come from?"** — Two named, public thermal-person-detection datasets (Roboflow, ~21,622 images; UNIRI-TID, ~6,111 images) for base training, plus team-collected mine-like footage for domain fine-tuning — the latter not yet collected, stated honestly.
4. **"How do you know the model will generalize to an actual mine?"** — We don't yet, fully — that's exactly what the fine-tuning step and Assumption A-009 are for; we've named this as the primary open AI question rather than assuming it away.
5. **"What's your inference latency, and where does it run?"** — ~7 ms/frame on our own Jetson Orin Nano via TensorRT (benchmark drawn from independent, cross-checked community sources — not yet re-measured on our specific build, which is the honest caveat).
6. **"What happens without internet/connectivity?"** — Nothing changes — inference is entirely on-device; connectivity only affects whether the *operator* sees the result promptly, which is already covered by our existing tether/LoRa failure-mode design.
7. **"Why this model and not something bigger/more advanced?"** — YOLOv8n already runs with large latency headroom over our sensor's frame rate; a bigger model would add compute cost with no demonstrated accuracy need at our task's resolution and single-class scope (Part 10 comparison table).
8. **"What's your expected accuracy?"** — Not stated as a number — we haven't fine-tuned or tested yet; we report recall, precision, and mAP@0.5 once we have a real measurement, not before.

---

## 27. FINAL RED-TEAM AUDIT

| Check | Result |
|---|---|
| Is AI used because it's genuinely needed, not just to satisfy PS wording? | Yes — Part 3/6 systematically evaluated and rejected every other candidate use case; thermal detection is the one that survives on merit |
| Is the model choice justified by evidence, not popularity? | Yes — peer-reviewed thermal-domain evidence (REF-026) plus hardware benchmarks (REF-029), not "YOLO is popular" |
| Is the dataset claim honest? | Yes — public datasets are named and real; the mine-domain fine-tuning gap is explicitly still open (A-009), not glossed over |
| Is there a fabricated accuracy/performance number anywhere in this revision? | No — every accuracy/recall/mAP cell is explicitly N/A pending measurement |
| Does AI have an escape hatch if it fails or underperforms? | Yes — human operator verification is the standing safeguard; the rule-based blob detector remains a documented fallback if fine-tuning doesn't complete in time |
| Is the architecture still minimal? | Yes — zero new hardware, two narrowly-scoped software additions (one of which never runs on the rover) |
| Does this AI component actually change any safety-critical decision? | No, deliberately — the rule engine remains the sole safety authority; AI is additive decision support only, consistent with the unchanged Part 24 of the Master Document |
| Is the "AI-powered" PS requirement now honestly and specifically satisfied? | Yes — there is a real, named, benchmarked, evidence-backed AI component doing a genuine perception task, not a decorative label |
