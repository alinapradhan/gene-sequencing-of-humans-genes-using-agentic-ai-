"""
Synthetic Gene Sequence Dataset Generator

This module generates synthetic human gene sequence data for testing
and development purposes.
"""

import random
import pandas as pd
import numpy as np
from typing import List, Tuple, Dict
import json


class SyntheticGeneDataGenerator:
    """Generate synthetic gene sequence data similar to what would be found on Kaggle."""
    
    def __init__(self, seed: int = 42):
        """
        Initialize the generator with a random seed for reproducibility.
        
        Args:
            seed: Random seed for reproducibility
        """
        random.seed(seed)
        np.random.seed(seed)
        self.nucleotides = ['A', 'T', 'G', 'C']
        
    def generate_sequence(self, length: int = 1000) -> str:
        """
        Generate a random DNA sequence.
        
        Args:
            length: Length of the sequence to generate
            
        Returns:
            DNA sequence string
        """
        return ''.join(random.choices(self.nucleotides, k=length))
    
    def introduce_mutation(self, sequence: str, mutation_rate: float = 0.01) -> Tuple[str, List[Dict]]:
        """
        Introduce random mutations into a sequence.
        
        Args:
            sequence: Original DNA sequence
            mutation_rate: Probability of mutation at each position
            
        Returns:
            Tuple of (mutated sequence, list of mutation details)
        """
        sequence_list = list(sequence)
        mutations = []
        
        for i in range(len(sequence_list)):
            if random.random() < mutation_rate:
                original = sequence_list[i]
                # Choose a different nucleotide
                new_nucleotide = random.choice([n for n in self.nucleotides if n != original])
                sequence_list[i] = new_nucleotide
                mutations.append({
                    'position': i,
                    'original': original,
                    'mutated': new_nucleotide,
                    'type': 'substitution'
                })
        
        return ''.join(sequence_list), mutations
    
    def generate_gene_dataset(self, num_samples: int = 100, 
                             sequence_length: int = 1000,
                             with_mutations: bool = True) -> pd.DataFrame:
        """
        Generate a complete dataset of gene sequences.
        
        Args:
            num_samples: Number of gene samples to generate
            sequence_length: Length of each gene sequence
            with_mutations: Whether to include mutated sequences
            
        Returns:
            DataFrame with gene sequence data
        """
        data = []
        
        for i in range(num_samples):
            # Generate reference sequence
            reference = self.generate_sequence(sequence_length)
            
            # Generate patient ID
            patient_id = f"PATIENT_{i:04d}"
            
            # Randomly assign gene type
            gene_types = ['BRCA1', 'BRCA2', 'TP53', 'EGFR', 'KRAS', 'MYC', 'PTEN']
            gene_type = random.choice(gene_types)
            
            # Add reference sequence
            data.append({
                'patient_id': patient_id,
                'gene_type': gene_type,
                'sequence': reference,
                'is_mutated': False,
                'mutation_count': 0,
                'health_status': 'normal'
            })
            
            # Add mutated version if requested
            if with_mutations and random.random() > 0.3:  # 70% chance of mutation
                mutated, mutations = self.introduce_mutation(reference, 
                                                             mutation_rate=random.uniform(0.005, 0.02))
                health_status = 'at_risk' if len(mutations) > 5 else 'monitor'
                
                data.append({
                    'patient_id': patient_id,
                    'gene_type': gene_type,
                    'sequence': mutated,
                    'is_mutated': True,
                    'mutation_count': len(mutations),
                    'health_status': health_status
                })
        
        return pd.DataFrame(data)
    
    def save_dataset(self, dataset: pd.DataFrame, filepath: str):
        """
        Save the generated dataset to a CSV file.
        
        Args:
            dataset: DataFrame containing the gene data
            filepath: Path where to save the CSV file
        """
        dataset.to_csv(filepath, index=False)
        print(f"Dataset saved to {filepath}")
        print(f"Total samples: {len(dataset)}")
        print(f"Mutated samples: {dataset['is_mutated'].sum()}")


def main():
    """Generate and save a synthetic gene dataset."""
    generator = SyntheticGeneDataGenerator(seed=42)
    
    # Generate dataset
    print("Generating synthetic gene sequence dataset...")
    dataset = generator.generate_gene_dataset(
        num_samples=100,
        sequence_length=1000,
        with_mutations=True
    )
    
    # Save to data directory
    output_path = 'src/data/synthetic_gene_sequences.csv'
    generator.save_dataset(dataset, output_path)
    
    # Print statistics
    print("\nDataset Statistics:")
    print(f"Total sequences: {len(dataset)}")
    print(f"Gene types: {dataset['gene_type'].unique().tolist()}")
    print(f"\nHealth status distribution:")
    print(dataset['health_status'].value_counts())


if __name__ == "__main__":
    main()
