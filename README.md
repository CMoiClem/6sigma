# Six Sigma Process Capability Calculator 📊

NGL, Claude 4 helped me on this one... 

## What is Six Sigma?

Six Sigma is a data-driven method to reduce defects and variability in processes. Born at Motorola in the 1980s, it’s a quality management staple for manufacturing industries.

### Why It’s Useful
- **Fewer Defects**
- **Saves Money**
- **Happy Customers*
- **Data-Powered**

## What This Tool Does

This Python tool crunches process data (e.g., bottle weights on my demo) to calculate Six Sigma metrics like Cp, Cpk, and Sigma level, helping assess and improve quality.

### Key Features
✅ **Capability Indices**  
- Cp, Cpk, Cpu, Cpl, Cpm: Measure process fit and centering.

✅ **Visuals**  
- Histogram with normal distribution and spec limits.  
- Highlights out-of-spec points.

✅ **Reports**  
- Stats: Mean, standard deviation, range.  
- Yield and sigma level.  
- Status: Capable (🟢), Marginal (🟡), or Incapable (🔴).

## Installation

### Prerequisites
- Python 3.8+
- Libraries: `numpy`, `pandas`, `matplotlib`, `scipy`

Install:
```bash
pip install numpy pandas matplotlib scipy
```

### Running
1. Clone the repo:
   ```bash
   git clone https://github.com/CMoiClem/6sigma.git
   cd 6sigma
   ```
2. Launch:
   ```bash
   python app.py
   ```
   
## Usage

1. **Import Data**: Upload a CSV with a "Mass" or "Measurement" column.
   ```csv
   Timestamp,Mass
   2025-07-12T06:00:00,500.23
   2025-07-12T06:00:01,499.87
   ```
2. **Set Specs**: Enter USL (e.g., 502), LSL (e.g., 498), and target (e.g., 500).
3. **Calculate**: Click "🔄 Calculate" for stats, indices, and histogram.
4. **Analyze**: Check 🟢 (Cpk ≥ 1.33), 🟡 (Cpk ≥ 1.0), or 🔴 (Cpk < 1.0).

### Metrics
- **Cp/Cpk ≥ 1.33**: Process is capable and centered.
- **Sigma Level**: 6σ ≈ 3.4 DPMO (world-class); 4σ ≈ 6,200 DPMO (good).
- **Yield**: % within specs—higher is better.

## License
[MIT License](LICENSE)


