"""
Example usage of the Gene Sequencing Agentic AI System

This file demonstrates various ways to use the system.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from data.generate_dataset import SyntheticGeneDataGenerator
from agents.alignment_agent import SequenceAlignmentAgent
from agents.mutation_agent import MutationDetectionAgent
from agents.pattern_agent import PatternRecognitionAgent
from orchestrator import GeneSequencingOrchestrator


def example_1_generate_dataset():
    """Example 1: Generate a synthetic dataset."""
    print("\n" + "="*70)
    print("EXAMPLE 1: Generate Synthetic Dataset")
    print("="*70)
    
    generator = SyntheticGeneDataGenerator(seed=42)
    dataset = generator.generate_gene_dataset(
        num_samples=50,
        sequence_length=500,
        with_mutations=True
    )
    
    print(f"\nGenerated {len(dataset)} sequences")
    print(f"\nFirst few rows:")
    print(dataset.head())
    
    return dataset


def example_2_individual_agents():
    """Example 2: Use individual agents."""
    print("\n" + "="*70)
    print("EXAMPLE 2: Individual Agent Analysis")
    print("="*70)
    
    # Sample sequences
    reference = "ATGCATGCATGCATGC" * 10  # 160 base pairs
    sample = "ATGCATGGATGCATGC" * 10     # With one mutation per repeat
    
    patient_data = {
        'patient_id': 'EXAMPLE_001',
        'gene_type': 'BRCA1',
        'reference': reference,
        'sample': sample
    }
    
    # Test Alignment Agent
    print("\n[Alignment Agent]")
    alignment_agent = SequenceAlignmentAgent()
    alignment_result = alignment_agent.analyze(patient_data)
    print(f"  Identity: {alignment_result['identity_percentage']:.2f}%")
    print(f"  Mismatches: {len(alignment_result['mismatches'])}")
    
    # Test Mutation Agent
    print("\n[Mutation Detection Agent]")
    mutation_agent = MutationDetectionAgent()
    mutation_result = mutation_agent.analyze(patient_data)
    print(f"  Mutations Found: {mutation_result['total_mutations']}")
    print(f"  Mutation Rate: {mutation_result['mutation_rate']:.3f}%")
    print(f"  Clinical Significance: {mutation_result['clinical_significance']}")
    
    # Test Pattern Agent
    print("\n[Pattern Recognition Agent]")
    pattern_agent = PatternRecognitionAgent()
    pattern_data = {'patient_id': 'EXAMPLE_001', 'sequence': sample}
    pattern_result = pattern_agent.analyze(pattern_data)
    print(f"  Complexity Score: {pattern_result['complexity_score']:.3f}")
    print(f"  Known Motifs: {len(pattern_result['known_motifs'])}")
    print(f"  Repeating Patterns: {len(pattern_result['repeating_patterns'])}")


def example_3_full_orchestration():
    """Example 3: Use the full orchestration system."""
    print("\n" + "="*70)
    print("EXAMPLE 3: Full Orchestration")
    print("="*70)
    
    # Generate a small dataset
    generator = SyntheticGeneDataGenerator(seed=123)
    dataset = generator.generate_gene_dataset(
        num_samples=5,
        sequence_length=500,
        with_mutations=True
    )
    dataset_path = '/tmp/example_dataset.csv'
    generator.save_dataset(dataset, dataset_path)
    
    # Run orchestration
    orchestrator = GeneSequencingOrchestrator()
    results = orchestrator.analyze_dataset(dataset_path, max_samples=3)
    
    # Generate report
    report = orchestrator.generate_report('/tmp/example_report.json')
    
    print(f"\nAnalyzed {len(results)} patients")
    print(f"Report saved to /tmp/example_report.json")


def example_4_custom_analysis():
    """Example 4: Custom analysis pipeline."""
    print("\n" + "="*70)
    print("EXAMPLE 4: Custom Analysis Pipeline")
    print("="*70)
    
    # Create custom sequences
    generator = SyntheticGeneDataGenerator(seed=999)
    
    # Generate a reference sequence
    reference = generator.generate_sequence(length=200)
    print(f"\nReference sequence (first 50 bp): {reference[:50]}...")
    
    # Introduce mutations
    mutated, mutations = generator.introduce_mutation(reference, mutation_rate=0.05)
    print(f"\nMutations introduced: {len(mutations)}")
    
    # Analyze with all agents
    data = {
        'patient_id': 'CUSTOM_001',
        'gene_type': 'TP53',
        'reference': reference,
        'sample': mutated
    }
    
    # Run all analyses
    alignment_agent = SequenceAlignmentAgent()
    mutation_agent = MutationDetectionAgent()
    pattern_agent = PatternRecognitionAgent()
    
    print("\n[Comprehensive Analysis]")
    alignment_result = alignment_agent.analyze(data)
    mutation_result = mutation_agent.analyze(data)
    pattern_result = pattern_agent.analyze({'patient_id': 'CUSTOM_001', 'sequence': mutated})
    
    # Custom risk assessment
    risk_score = (
        (100 - alignment_result['identity_percentage']) * 2 +
        mutation_result['mutation_rate'] * 10
    )
    
    print(f"  Alignment Score: {alignment_result['alignment_score']:.2f}%")
    print(f"  Total Mutations: {mutation_result['total_mutations']}")
    print(f"  Complexity: {pattern_result['complexity_score']:.3f}")
    print(f"  Custom Risk Score: {risk_score:.2f}")
    
    if risk_score > 20:
        print(f"  Assessment: HIGH RISK - Immediate attention required")
    elif risk_score > 10:
        print(f"  Assessment: MODERATE RISK - Follow-up recommended")
    else:
        print(f"  Assessment: LOW RISK - Routine monitoring")


def main():
    """Run all examples."""
    print("\n" + "="*70)
    print("GENE SEQUENCING AGENTIC AI - USAGE EXAMPLES")
    print("="*70)
    
    try:
        # Run examples
        example_1_generate_dataset()
        example_2_individual_agents()
        example_3_full_orchestration()
        example_4_custom_analysis()
        
        print("\n" + "="*70)
        print("ALL EXAMPLES COMPLETED SUCCESSFULLY")
        print("="*70 + "\n")
        
    except Exception as e:
        print(f"\nError running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
