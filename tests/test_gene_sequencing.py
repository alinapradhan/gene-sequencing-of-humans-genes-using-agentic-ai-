"""
Test suite for Gene Sequencing Agentic AI System
"""

import unittest
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from agents.alignment_agent import SequenceAlignmentAgent
from agents.mutation_agent import MutationDetectionAgent
from agents.pattern_agent import PatternRecognitionAgent
from utils.sequence_utils import (
    calculate_gc_content, 
    hamming_distance, 
    find_mutations,
    find_patterns
)
from data.generate_dataset import SyntheticGeneDataGenerator


class TestSequenceUtils(unittest.TestCase):
    """Test utility functions."""
    
    def test_gc_content(self):
        """Test GC content calculation."""
        sequence = "ATGC"
        gc_content = calculate_gc_content(sequence)
        self.assertEqual(gc_content, 50.0)
    
    def test_hamming_distance(self):
        """Test Hamming distance calculation."""
        seq1 = "ATGC"
        seq2 = "ATCC"
        distance = hamming_distance(seq1, seq2)
        self.assertEqual(distance, 1)
    
    def test_find_mutations(self):
        """Test mutation detection."""
        reference = "ATGC"
        sample = "ATCC"
        mutations = find_mutations(reference, sample)
        self.assertEqual(len(mutations), 1)
        self.assertEqual(mutations[0]['position'], 2)
    
    def test_find_patterns(self):
        """Test pattern finding."""
        sequence = "ATGATGATG"
        pattern = "ATG"
        positions = find_patterns(sequence, pattern)
        self.assertEqual(len(positions), 3)


class TestAgents(unittest.TestCase):
    """Test agent functionality."""
    
    def setUp(self):
        """Set up test data."""
        self.reference = "ATGCATGCATGCATGC"
        self.sample = "ATGCATGGATGCATGC"  # One mutation at position 7
        self.patient_data = {
            'patient_id': 'TEST_001',
            'gene_type': 'BRCA1',
            'reference': self.reference,
            'sample': self.sample
        }
    
    def test_alignment_agent(self):
        """Test sequence alignment agent."""
        agent = SequenceAlignmentAgent()
        result = agent.analyze(self.patient_data)
        
        self.assertIn('alignment_score', result)
        self.assertIn('identity_percentage', result)
        self.assertIn('patient_id', result)
        self.assertEqual(result['patient_id'], 'TEST_001')
    
    def test_mutation_agent(self):
        """Test mutation detection agent."""
        agent = MutationDetectionAgent()
        result = agent.analyze(self.patient_data)
        
        self.assertIn('total_mutations', result)
        self.assertIn('mutation_rate', result)
        self.assertIn('clinical_significance', result)
        self.assertEqual(result['total_mutations'], 1)
    
    def test_pattern_agent(self):
        """Test pattern recognition agent."""
        agent = PatternRecognitionAgent()
        pattern_data = {
            'patient_id': 'TEST_001',
            'sequence': self.reference
        }
        result = agent.analyze(pattern_data)
        
        self.assertIn('complexity_score', result)
        self.assertIn('sequence_length', result)
        self.assertEqual(result['sequence_length'], len(self.reference))


class TestDataGenerator(unittest.TestCase):
    """Test synthetic data generation."""
    
    def test_sequence_generation(self):
        """Test sequence generation."""
        generator = SyntheticGeneDataGenerator(seed=42)
        sequence = generator.generate_sequence(length=100)
        
        self.assertEqual(len(sequence), 100)
        self.assertTrue(all(c in 'ATGC' for c in sequence))
    
    def test_mutation_introduction(self):
        """Test mutation introduction."""
        generator = SyntheticGeneDataGenerator(seed=42)
        original = "ATGCATGCATGCATGC"
        mutated, mutations = generator.introduce_mutation(original, mutation_rate=0.5)
        
        self.assertEqual(len(mutated), len(original))
        self.assertGreater(len(mutations), 0)
    
    def test_dataset_generation(self):
        """Test full dataset generation."""
        generator = SyntheticGeneDataGenerator(seed=42)
        dataset = generator.generate_gene_dataset(num_samples=10, sequence_length=100)
        
        self.assertGreater(len(dataset), 0)
        self.assertIn('patient_id', dataset.columns)
        self.assertIn('gene_type', dataset.columns)
        self.assertIn('sequence', dataset.columns)


if __name__ == '__main__':
    unittest.main()
