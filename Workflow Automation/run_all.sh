#!/bin/bash

# run_all.sh - Execute complete analysis workflow
# This script runs the entire analysis pipeline from start to finish
#
# Usage:
#   ./run_all.sh              # Run complete workflow
#   ./run_all.sh --clean      # Clean outputs and re-run
#
# Author: Monisha Mudunuri and Yamuna Nair 
# Date: December 2025

set -e  # Exit on error

echo "======================================================================"
echo "Sleep Patterns & Academic Performance - Complete Workflow"
echo "======================================================================"

# Parse arguments
CLEAN=false
if [ "$1" == "--clean" ]; then
    CLEAN=true
fi

# Clean previous outputs if requested
if [ "$CLEAN" = true ]; then
    echo ""
    echo "[0/4] Cleaning previous outputs..."
    rm -rf data/integrated_data.csv
    rm -rf results/
    rm -rf logs/
    echo "  ✓ Previous outputs cleaned"
fi

# Step 1: Check Prerequisites
echo ""
echo "[1/4] Checking prerequisites..."

# Check Python
if ! command -v python &> /dev/null; then
    echo "  ✗ Python not found. Please install Python 3.9+"
    exit 1
fi
echo "  ✓ Python found: $(python --version)"

# Check required files
if [ ! -f "cleaned_cmu-sleep.csv" ]; then
    echo "  ✗ cleaned_cmu-sleep.csv not found"
    echo "    Please ensure data cleaning step is completed"
    exit 1
fi

if [ ! -f "cleaned_student_habits.csv" ]; then
    echo "  ✗ cleaned_student_habits.csv not found"
    echo "    Please ensure data cleaning step is completed"
    exit 1
fi
echo "  ✓ Cleaned datasets found"

# Check required scripts
if [ ! -f "03_data_integration.py" ]; then
    echo "  ✗ 03_data_integration.py not found"
    exit 1
fi

if [ ! -f "04_analysis_visualization.py" ]; then
    echo "  ✗ 04_analysis_visualization.py not found"
    exit 1
fi
echo "  ✓ Analysis scripts found"

# Create output directories
mkdir -p data
mkdir -p results/tables
mkdir -p results/figures
mkdir -p logs
echo "  ✓ Output directories ready"

# Step 2: Data Integration
echo ""
echo "[2/4] Running data integration..."
python 03_data_integration.py > logs/integration.log 2>&1

if [ ! -f "data/integrated_data.csv" ]; then
    echo "  ✗ Integration failed. Check logs/integration.log"
    exit 1
fi
echo "  ✓ Data integration complete"

# Step 3: Analysis and Visualization
echo ""
echo "[3/4] Running analysis and visualization..."
python 04_analysis_visualization.py > logs/analysis.log 2>&1

# Check outputs
EXPECTED_TABLES=("descriptive_statistics.json" "correlations.json" "regression_results.json" "category_analysis.json")
EXPECTED_FIGURES=("01_sleep_distribution.png" "02_sleep_vs_performance.png" "03_dataset_comparison.png" "04_productivity_mediation.png")

MISSING_FILES=0

for table in "${EXPECTED_TABLES[@]}"; do
    if [ ! -f "results/tables/$table" ]; then
        echo "  ✗ Missing: results/tables/$table"
        MISSING_FILES=$((MISSING_FILES + 1))
    fi
done

for figure in "${EXPECTED_FIGURES[@]}"; do
    if [ ! -f "results/figures/$figure" ]; then
        echo "  ✗ Missing: results/figures/$figure"
        MISSING_FILES=$((MISSING_FILES + 1))
    fi
done

if [ $MISSING_FILES -gt 0 ]; then
    echo "  ✗ Analysis incomplete. Check logs/analysis.log"
    exit 1
fi
echo "  ✓ Analysis and visualization complete"

# Step 4: Summary
echo ""
echo "[4/4] Generating summary..."

# Count outputs
NUM_TABLES=$(ls results/tables/*.json 2>/dev/null | wc -l)
NUM_FIGURES=$(ls results/figures/*.png 2>/dev/null | wc -l)

echo "  ✓ Generated $NUM_TABLES analysis tables"
echo "  ✓ Generated $NUM_FIGURES visualizations"

# Display key findings (from analysis output)
if [ -f "results/tables/regression_results.json" ]; then
    echo ""
    echo "📊 Key Results:"
    python -c "
import json
with open('results/tables/regression_results.json') as f:
    results = json.load(f)
    model = results['model_1_simple']
    print(f\"  • Sleep coefficient: {model['coefficient']:.2f} points per hour\")
    print(f\"  • R²: {model['r_squared']:.3f}\")
    print(f\"  • Sample size: {model['n']} students\")
"
fi

# Final message
echo ""
echo "======================================================================"
echo "✓ WORKFLOW COMPLETE"
echo "======================================================================"
echo ""
echo "Outputs saved to:"
echo "  • Integrated data: data/integrated_data.csv"
echo "  • Analysis tables: results/tables/"
echo "  • Visualizations: results/figures/"
echo "  • Logs: logs/"
echo ""
echo "Next steps:"
echo "  1. Review results in results/ directory"
echo "  2. Check logs/ for detailed execution logs"
echo "  3. Update README.md with findings"
echo ""
