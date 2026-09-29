"""
ShaktiMine (SIH26039) - Lightweight Telemetry & Web Server
Serves the Surface Control Station dashboard and streams live simulated rover telemetry.
Zero external dependencies (uses standard library http.server and socket).

Usage:
    python simulate_rover.py [port]
    (Default port: 8080)
Then open http://localhost:8080 in your browser.
"""

import http.server
import socketserver
import json
import time
import math
import random
import os
import sys

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Global Simulated State
rover_state = {
    "status": "ONLINE",
    "comm_mode": "FIBER_OPTIC_TETHER",
    "tether_length_m": 248.5,
    "battery_pct": 86,
    "depth_m": -142.4,
    "heading_deg": 42.0,
    "speed_kmh": 0.5,
    "position": {"x": 180.0, "y": 150.0},
    "sensors": {
        "ch4_pct": 0.42,
        "co_ppm": 12.0,
        "o2_pct": 20.8,
        "water_cm": 3.2,
        "temp_c": 28.4,
        "rh_pct": 78.0,
        "mq4_raw": 0.43,
        "pellistor_raw": 0.41,
        "ndir_raw": 0.42
    },
    "safety_rule_state": "CONDITIONS_PERMISSIBLE",
    "cmr2017_violation": False,
    "trapped_worker_flag": False
}

class ShaktiMineHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self.path = "/dashboard.html"
            return super().do_GET()

        elif self.path.startswith("/api/telemetry"):
            # Update telemetry values with natural jitter
            jitter = (random.random() - 0.5) * 0.04
            rover_state["sensors"]["ch4_pct"] = round(max(0.0, rover_state["sensors"]["ch4_pct"] + jitter), 2)
            rover_state["sensors"]["co_ppm"] = round(max(0.0, rover_state["sensors"]["co_ppm"] + (random.random() - 0.5) * 1.0), 1)
            rover_state["battery_pct"] = max(10, rover_state["battery_pct"] - (0.01 if random.random() < 0.2 else 0))

            response_data = {
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "state": rover_state
            }
            payload = json.dumps(response_data).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)

        elif self.path.startswith("/api/scenario/"):
            scen = self.path.split("/")[-1]
            if scen == "gas_alert":
                rover_state["sensors"]["ch4_pct"] = 1.85
                rover_state["sensors"]["co_ppm"] = 68.0
                rover_state["sensors"]["o2_pct"] = 18.2
                rover_state["safety_rule_state"] = "ENTRY_STRICTLY_PROHIBITED"
                rover_state["cmr2017_violation"] = True
            elif scen == "miner_found":
                rover_state["trapped_worker_flag"] = True
                rover_state["sensors"]["ch4_pct"] = 0.65
            elif scen == "tether_cut":
                rover_state["comm_mode"] = "LORA_865MHZ_FALLBACK"
            else:
                rover_state["sensors"]["ch4_pct"] = 0.42
                rover_state["sensors"]["co_ppm"] = 12.0
                rover_state["sensors"]["o2_pct"] = 20.8
                rover_state["safety_rule_state"] = "CONDITIONS_PERMISSIBLE"
                rover_state["cmr2017_violation"] = False
                rover_state["trapped_worker_flag"] = False
                rover_state["comm_mode"] = "FIBER_OPTIC_TETHER"

            res = {"status": "ok", "scenario": scen, "state": rover_state}
            payload = json.dumps(res).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)

        else:
            return super().do_GET()

    def do_POST(self):
        if self.path == "/api/drive":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length).decode("utf-8")
            data = json.loads(body) if body else {}
            cmd = data.get("command", "STOP")
            step = 1.5
            if cmd == "FORWARD":
                rover_state["position"]["x"] += step
                rover_state["tether_length_m"] += 0.2
            elif cmd == "REVERSE":
                rover_state["position"]["x"] -= step
            elif cmd == "LEFT":
                rover_state["heading_deg"] = (rover_state["heading_deg"] - 10) % 360
            elif cmd == "RIGHT":
                rover_state["heading_deg"] = (rover_state["heading_deg"] + 10) % 360
            
            res = {"status": "acknowledged", "command": cmd, "position": rover_state["position"]}
            payload = json.dumps(res).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)
        else:
            self.send_response(404)
            self.end_headers()

def run_server():
    # Ensure stdout handles utf-8 or ascii safely on Windows
    if sys.stdout.encoding != 'utf-8':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except Exception:
            pass

    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), ShaktiMineHandler) as httpd:
        print("=" * 60)
        print("[*] ShaktiMine (SIH26039) Surface Control Station Active")
        print(f"[*] Server listening on: http://localhost:{PORT}")
        print(f"[*] Serving dashboard from: {os.path.join(BASE_DIR, 'dashboard.html')}")
        print("=" * 60)
        print("Press Ctrl+C to terminate the telemetry server.")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")

if __name__ == "__main__":
    run_server()
