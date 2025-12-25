# Gene Sequencing of Human Genes Using Agentic AI

A comprehensive gene sequencing analysis system powered by multiple AI agents that work together to analyze genetic sequences, detect mutations, and identify patterns in human DNA.

## Overview

This project implements an **Agentic AI** system for gene sequencing analysis. It uses multiple specialized agents that collaborate to provide comprehensive genetic analysis:

1. **Sequence Alignment Agent** - Aligns and compares gene sequences
2. **Mutation Detection Agent** - Identifies and analyzes genetic mutations
3. **Pattern Recognition Agent** - Discovers conserved regions, motifs, and repeating patterns

## Features

- 🧬 **Synthetic Dataset Generation** - Creates realistic synthetic gene sequence data
- 🤖 **Multi-Agent AI System** - Three specialized agents working in coordination
- 🔍 **Mutation Detection** - Identifies substitutions, transitions, and transversions
- 📊 **Pattern Recognition** - Finds motifs, tandem repeats, and conserved regions
- 📈 **Risk Assessment** - Provides clinical significance scoring
- 📋 **Comprehensive Reports** - Generates detailed JSON analysis reports

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/alinapradhan/gene-sequencing-of-humans-genes-using-agentic-ai-.git
cd gene-sequencing-of-humans-genes-using-agentic-ai-
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Quick Start

Run the complete analysis pipeline:

```bash
python main.py
```

This will:
1. Generate a synthetic gene sequence dataset
2. Run multi-agent analysis on the sequences
3. Generate a comprehensive analysis report

### Custom Analysis

#### Generate Custom Dataset

```python
from src.data.generate_dataset import SyntheticGeneDataGenerator

generator = SyntheticGeneDataGenerator(seed=42)
dataset = generator.generate_gene_dataset(
    num_samples=100,
    sequence_length=1000,
    with_mutations=True
)
generator.save_dataset(dataset, 'custom_dataset.csv')
```

#### Run Specific Agents

```python
from src.agents.alignment_agent import SequenceAlignmentAgent
from src.agents.mutation_agent import MutationDetectionAgent
from src.agents.pattern_agent import PatternRecognitionAgent

# Alignment analysis
alignment_agent = SequenceAlignmentAgent()
result = alignment_agent.analyze({
    'reference': 'ATCGATCG...',
    'sample': 'ATCGATCG...',
    'patient_id': 'PATIENT_001'
})

# Mutation detection
mutation_agent = MutationDetectionAgent()
result = mutation_agent.analyze({
    'reference': 'ATCGATCG...',
    'sample': 'ATCGATCG...',
    'patient_id': 'PATIENT_001'
})

# Pattern recognition
pattern_agent = PatternRecognitionAgent()
result = pattern_agent.analyze({
    'sequence': 'ATCGATCG...',
    'patient_id': 'PATIENT_001'
})
```

#### Full Orchestration

```python
from src.orchestrator import GeneSequencingOrchestrator

orchestrator = GeneSequencingOrchestrator()
results = orchestrator.analyze_dataset('dataset.csv', max_samples=10)
orchestrator.generate_report('report.json')
```

## Project Structure

```
gene-sequencing-of-humans-genes-using-agentic-ai-/
├── main.py                          # Main entry point
├── requirements.txt                 # Python dependencies
├── README.md                       # This file
├── src/
│   ├── agents/                     # AI Agent modules
│   │   ├── base_agent.py          # Base agent class
│   │   ├── alignment_agent.py     # Sequence alignment agent
│   │   ├── mutation_agent.py      # Mutation detection agent
│   │   └── pattern_agent.py       # Pattern recognition agent
│   ├── data/                       # Data handling
│   │   ├── generate_dataset.py    # Synthetic data generator
│   │   └── synthetic_gene_sequences.csv  # Generated dataset
│   ├── utils/                      # Utility functions
│   │   └── sequence_utils.py      # Sequence processing utilities
│   └── orchestrator.py            # Multi-agent orchestrator
└── tests/                          # Test files
```

## Agents Description

### 1. Sequence Alignment Agent

Performs sequence alignment and comparison:
- Calculates alignment scores
- Computes sequence identity percentages
- Identifies gaps and mismatches
- Analyzes GC content

### 2. Mutation Detection Agent

Detects and analyzes genetic mutations:
- Identifies all mutations between sequences
- Categorizes mutations (transitions vs transversions)
- Calculates mutation rates
- Identifies mutation hotspots
- Assesses clinical significance

### 3. Pattern Recognition Agent

Recognizes patterns and motifs:
- Finds known genetic motifs (TATA box, CAAT box, etc.)
- Identifies repeating patterns
- Detects tandem repeats
- Locates conserved regions
- Calculates sequence complexity

## Dataset

The system generates synthetic gene sequence data that mimics real-world Kaggle datasets:

- **Patient IDs** - Unique identifiers for each patient
- **Gene Types** - BRCA1, BRCA2, TP53, EGFR, KRAS, MYC, PTEN
- **Sequences** - 1000 nucleotide sequences
- **Mutations** - Realistic mutation rates and patterns
- **Health Status** - Normal, monitor, at_risk classifications

## Risk Assessment

The system provides comprehensive risk assessment:

- **HIGH RISK** - Significant mutations detected, immediate consultation recommended
- **MODERATE RISK** - Clinical follow-up advised
- **LOW RISK** - Routine monitoring recommended
- **NORMAL** - No significant mutations detected

## Output Reports

The system generates detailed JSON reports containing:

```json
{
  "total_patients_analyzed": 10,
  "analyses": [
    {
      "patient_id": "PATIENT_0001",
      "gene_type": "BRCA1",
      "analyses": {
        "alignment": {...},
        "mutation": {...},
        "pattern": {...}
      },
      "assessment": {
        "risk_level": "MODERATE",
        "recommendation": "Clinical follow-up advised",
        "mutation_count": 12,
        "mutation_rate": 1.2,
        "sequence_identity": 98.8
      }
    }
  ],
  "summary": {
    "high_risk": 2,
    "moderate_risk": 3,
    "low_risk": 3,
    "normal": 2
  }
}
```

## Scientific Background

### Gene Sequencing

Gene sequencing is the process of determining the nucleotide order in DNA. This system analyzes sequences for:
- Point mutations (single nucleotide changes)
- Conserved regions (evolutionarily preserved sequences)
- Regulatory motifs (DNA sequences that control gene expression)
- Structural variations

### Agentic AI Approach

This project uses an **agentic AI architecture** where multiple specialized agents work collaboratively:
- Each agent has a specific domain of expertise
- Agents work independently but share results
- The orchestrator coordinates agent activities
- Final decisions are based on collective intelligence

## License

MIT License - see [LICENSE](LICENSE) file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- Inspired by real-world gene sequencing challenges
- Dataset format follows common Kaggle genomics datasets
- Uses established bioinformatics algorithms and patterns

## Future Enhancements

- [ ] Integration with real genomic databases
- [ ] Machine learning models for variant classification
- [ ] Visualization dashboard
- [ ] Real-time analysis API
- [ ] Support for larger sequence files (FASTA/FASTQ)
- [ ] Integration with clinical databases
- [ ] Multi-threaded processing for large datasets

## Contact

For questions or support, please open an issue on GitHub.

---

**Note**: This system uses synthetic data for educational and research purposes. For clinical applications, please use validated tools and consult with genetic counselors.
