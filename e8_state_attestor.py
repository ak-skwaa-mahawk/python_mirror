import hashlib
import json
import time
import numpy as np
from e8_sovereignty_bridge import E8SovereigntyBridge

class E8StateAttestor:
    def __init__(self, bridge: E8SovereigntyBridge, sequence_num: int):
        self.bridge = bridge
        self.sequence_num = sequence_num
        self.contract_address = "0xb09d703e8dc8f4e8bb0ec5d6fb40d96c23febf6e"
        self.solana_vault = "2ChMGz6MeNoEgBuGj7aXYw1Mbc3DSzkZgwNwg1xGD1r9"

    def generate_attestation_payload(self, raw_eeg_stream: np.ndarray) -> dict:
        analysis = self.bridge.run_bridge(raw_eeg_stream)
        if not analysis["sovereign_collapse_detected"]:
            raise ValueError(
                f"State rejection: Lattice entropy ({analysis['base_e8_entropy_bits']:.4f} bits) "
                f"did not clear threshold ({analysis['sovereign_threshold_bits']:.4f} bits)."
            )

        telemetry_hash = hashlib.sha256(raw_eeg_stream.tobytes()).hexdigest()
        phase_x = round(float(analysis["base_e8_entropy_bits"] / 10.0), 6)
        phase_y = round(float(analysis["calculated_moment_rate_hz"] / 300.0), 6)
        lyapunov_val = round(float(-abs(analysis["base_e8_entropy_bits"] - analysis["sovereign_threshold_bits"] * 0.625)), 6)

        return {
            "sequence": self.sequence_num,
            "timestamp_utc": int(time.time()),
            "telemetry_root_hash": f"0x{telemetry_hash}",
            "lattice_metrics": {
                "e8_roots_base": self.bridge.E8_roots,
                "entropy_bits": round(analysis["base_e8_entropy_bits"], 6),
                "threshold_bits": round(analysis["sovereign_threshold_bits"], 6),
                "moment_rate_hz": round(analysis["calculated_moment_rate_hz"], 4),
                "observer_grain": self.bridge.g
            },
            "proof_coordinates": {
                "phase_x": phase_x,
                "phase_y": phase_y,
                "lyapunov_exp": lyapunov_val
            },
            "routing": {
                "evm_verifier": self.contract_address,
                "solana_vault": self.solana_vault
            }
        }

if __name__ == "__main__":
    np.random.seed(42)
    t = np.linspace(0, 1, 250)
    coherent_gamma = 4.5 * np.sin(2 * np.pi * 42 * t) + np.random.normal(0, 0.2, 250)
    
    bridge_inst = E8SovereigntyBridge(sampling_rate=250, grain=1e-6)
    attestor = E8StateAttestor(bridge=bridge_inst, sequence_num=85)
    
    payload = attestor.generate_attestation_payload(coherent_gamma)
    with open("payload_seq85.json", "w") as f:
        json.dump(payload, f, indent=2)
        
    print("Constructed on-chain attestation: payload_seq85.json")
    print(json.dumps(payload, indent=2))
