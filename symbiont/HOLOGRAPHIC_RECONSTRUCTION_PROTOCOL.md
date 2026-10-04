# Holographic Reconstruction Protocol

## Purpose
Разделить физическое измерение, реконструкцию и интерпретацию.

## Pipeline
Raw signal → calibrated data → reconstruction → feature extraction → model → interpretation.

## Required metadata
- acquisition method;
- reference signal when applicable;
- calibration;
- spatial and temporal resolution;
- preprocessing;
- reconstruction algorithm;
- model assumptions;
- uncertainty;
- artifacts;
- validation;
- interpretation.

## Principle
**A reconstructed image is evidence about an object, not the object itself.**

## AS integration
Результат реконструкции должен храниться как Model, а неизвестные и неразрешенные свойства — как Residual/UNKNOWN.