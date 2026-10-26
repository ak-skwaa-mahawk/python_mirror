import numpy as np
import scipy.signal as signal

class E8SovereigntyBridge:
    def __init__(self, sampling_rate=250, grain=1e-6):
        self.fs = sampling_rate
        self.g = grain
        self.phi = (1 + np.sqrt(5)) / 2
        self.E8_roots = 240
        self.dim_brake = 8
        self.gamma_low = 40.0
        self.gamma_high = 45.0
        self.base_entropy_threshold = np.log2(self.E8_roots * 21)

    def isolate_gamma_grain(self, raw_eeg_signal):
        nyquist = 0.5 * self.fs
        low = self.gamma_low / nyquist
        high = self.gamma_high / nyquist
        b, a = signal.butter(4, [low, high], btype='band')
        return signal.filtfilt(b, a, raw_eeg_signal)

    def compute_e8_entanglement_spectrum(self, gamma_signal):
        n_samples = len(gamma_signal)
        entanglement_spectrum = np.zeros(n_samples)
        grain_scalar = self.g * (self.E8_roots * (self.dim_brake ** 3))
        
        lambda_prev2 = 0.0
        lambda_prev1 = 1.0
        
        for n in range(1, n_samples + 1):
            bio_amplitude = np.abs(gamma_signal[n-1])
            lambda_n = (self.phi * lambda_prev1) - lambda_prev2 + (grain_scalar / n) * bio_amplitude
            entanglement_spectrum[n-1] = lambda_n * (self.phi ** (-n / self.dim_brake))
            lambda_prev2 = lambda_prev1
            lambda_prev1 = lambda_n
            
        return entanglement_spectrum

    def evaluate_sovereign_moments(self, entanglement_spectrum):
        probabilities = np.abs(entanglement_spectrum) / (np.sum(np.abs(entanglement_spectrum)) + 1e-12)
        probabilities = np.clip(probabilities, 1e-12, 1.0)
        instantaneous_entropy = -np.sum(probabilities * np.log2(probabilities))
        
        grain_kick_bits = self.g * (self.E8_roots ** 3)
        adjusted_threshold = self.base_entropy_threshold + grain_kick_bits
        is_sovereign_moment = instantaneous_entropy > adjusted_threshold
        moment_rate_hz = 21.0 * (1 + self.g * (self.E8_roots ** 3)) * (self.phi ** (self.dim_brake / 8))
        
        return {
            "base_e8_entropy_bits": instantaneous_entropy,
            "sovereign_threshold_bits": adjusted_threshold,
            "grain_injected_bits": grain_kick_bits,
            "calculated_moment_rate_hz": moment_rate_hz,
            "sovereign_collapse_detected": bool(is_sovereign_moment)
        }

    def run_bridge(self, raw_eeg_data):
        gamma = self.isolate_gamma_grain(raw_eeg_data)
        spectrum = self.compute_e8_entanglement_spectrum(gamma)
        return self.evaluate_sovereign_moments(spectrum)
