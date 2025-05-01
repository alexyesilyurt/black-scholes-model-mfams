# Black-Scholes Implied Volatility and Greeks Analysis for ^XSP Options

> Developed as a project for the University of Michigan Finance and Mathematics Society <br>
> **Authors:** Noah K. Guberman & Alexander Yesilyurt

This repository contains code and analysis for deriving implied volatility and calculating the Black-Scholes Greeks (Delta, Gamma, Vega, Theta, and Rho) for European-style S&P 500 Mini-SPX (^XSP) options. The project visualizes the volatility surface and option sensitivities, providing insight into risk pricing and market behavior near expiration.

## Overview

- **Ticker Analyzed:** `^XSP` (S&P 500 Mini-SPX)
- **Option Type:** European-style call options
- **Framework:** Black-Scholes model
- **Methods:**
  - Brent's root-finding algorithm for implied volatility
  - Vectorized computation of Greeks
  - 3D volatility surface plotting
  - Visualization of Greek sensitivities vs. strike price

## Features

- **Implied Volatility Estimation**  
  Numerically inverts the Black-Scholes formula using market prices to solve for implied volatility via Brent's method.

- **Greeks Calculation**  
  Computes Delta, Gamma, Theta, Vega, and Rho for each option using closed-form expressions based on implied volatility.

- **Volatility Surface Visualization**  
  Generates a 3D volatility surface as a function of strike price and days to maturity using `matplotlib` and `scipy`.

- **Greek Sensitivity Graphs**  
  Plots the Greeks vs. strike price for 1-day-to-expiration contracts.

## File Structure

```bash
.
├── main.py                   # Primary script for data collection, processing, and plotting
├── greeks.py                 # Contains all Black-Scholes Greek functions
├── black_scholes_prices.csv  # Output CSV with computed prices and implied volatility
└── README.md                 # This file