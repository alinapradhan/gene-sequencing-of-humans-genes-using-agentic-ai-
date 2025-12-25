"""
Gene Sequencing Analysis using Agentic AI

Main entry point for the gene sequencing analysis system.
"""

from src.data.generate_dataset import SyntheticGeneDataGenerator
from src.orchestrator import GeneSequencingOrchestrator


def main():
    """Main function to run the gene sequencing analysis."""
    
    print("="*70)
    print(" GENE SEQUENCING ANALYSIS USING AGENTIC AI")
    print("="*70)
    
    # Step 1: Generate synthetic dataset
    print("\n[STEP 1] Generating Synthetic Gene Sequence Dataset...")
    print("-" * 70)
    generator = SyntheticGeneDataGenerator(seed=42)
    dataset = generator.generate_gene_dataset(
        num_samples=100,
        sequence_length=1000,
        with_mutations=True
    )
    
    dataset_path = 'src/data/synthetic_gene_sequences.csv'
    generator.save_dataset(dataset, dataset_path)
    
    # Step 2: Run Agentic AI Analysis
    print("\n[STEP 2] Running Agentic AI Analysis...")
    print("-" * 70)
    orchestrator = GeneSequencingOrchestrator()
    
    # Analyze first 10 patients for demonstration
    results = orchestrator.analyze_dataset(dataset_path, max_samples=10)
    
    # Step 3: Generate Report
    print("\n[STEP 3] Generating Analysis Report...")
    print("-" * 70)
    report = orchestrator.generate_report('gene_analysis_report.json')
    
    print("\n" + "="*70)
    print(" ANALYSIS COMPLETE")
    print("="*70)
    print("\nGenerated Files:")
    print(f"  • Dataset: {dataset_path}")
    print(f"  • Report: gene_analysis_report.json")
    print("\nThe agentic AI system has analyzed the gene sequences using:")
    print("  1. Sequence Alignment Agent - Aligns and compares sequences")
    print("  2. Mutation Detection Agent - Identifies genetic mutations")
    print("  3. Pattern Recognition Agent - Finds conserved regions and motifs")
    print("\n" + "="*70)


if __name__ == "__main__":
    main()
