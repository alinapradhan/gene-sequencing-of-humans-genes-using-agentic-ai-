"""
Sequence Alignment Agent for comparing and aligning gene sequences.
"""
import pandas as pd
from typing import Dict, List, Tuple
import numpy as np
import sys
import os

# Handle imports for both package and standalone execution
try:
    from .base_agent import BaseAgent
    from ..utils.sequence_utils import hamming_distance, calculate_gc_content
except ImportError:
    # Fallback for standalone or test execution
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from base_agent import BaseAgent
    from utils.sequence_utils import hamming_distance, calculate_gc_content


class SequenceAlignmentAgent(BaseAgent):
    """Agent for performing sequence alignment and comparison tasks."""
    
    def __init__(self):
        """Initialize the Sequence Alignment Agent."""
        super().__init__("SequenceAlignmentAgent")
        self.alignment_matrix = None
    
    def analyze(self, data: Dict) -> Dict:
        """
        Analyze and align sequences.
        
        Args:
            data: Dictionary containing 'reference' and 'sample' sequences
            
        Returns:
            Dictionary with alignment results
        """
        reference = data.get('reference', '')
        sample = data.get('sample', '')
        patient_id = data.get('patient_id', 'unknown')
        
        if not reference or not sample:
            return {'error': 'Missing reference or sample sequence'}
        
        # Calculate alignment score
        alignment_score = self._calculate_alignment_score(reference, sample)
        
        # Calculate identity percentage
        identity = self._calculate_identity(reference, sample)
        
        # Find gaps and mismatches
        gaps, mismatches = self._find_gaps_and_mismatches(reference, sample)
        
        result = {
            'patient_id': patient_id,
            'agent': self.agent_name,
            'alignment_score': alignment_score,
            'identity_percentage': identity,
            'gaps': gaps,
            'mismatches': mismatches,
            'reference_length': len(reference),
            'sample_length': len(sample),
            'gc_content_reference': calculate_gc_content(reference),
            'gc_content_sample': calculate_gc_content(sample)
        }
        
        self.log_result(result)
        return result
    
    def _calculate_alignment_score(self, seq1: str, seq2: str) -> float:
        """
        Calculate alignment score using a simple scoring system.
        
        Args:
            seq1: First sequence
            seq2: Second sequence
            
        Returns:
            Alignment score
        """
        if len(seq1) != len(seq2):
            return 0.0
        
        matches = sum(1 for a, b in zip(seq1, seq2) if a == b)
        return (matches / len(seq1)) * 100
    
    def _calculate_identity(self, seq1: str, seq2: str) -> float:
        """
        Calculate sequence identity percentage.
        
        Args:
            seq1: First sequence
            seq2: Second sequence
            
        Returns:
            Identity percentage
        """
        if len(seq1) != len(seq2):
            return 0.0
        
        identical = sum(1 for a, b in zip(seq1, seq2) if a == b)
        return (identical / len(seq1)) * 100
    
    def _find_gaps_and_mismatches(self, seq1: str, seq2: str) -> Tuple[int, List[int]]:
        """
        Find gaps and mismatches between sequences.
        
        Args:
            seq1: First sequence
            seq2: Second sequence
            
        Returns:
            Tuple of (gap count, list of mismatch positions)
        """
        gaps = 0
        mismatches = []
        
        min_len = min(len(seq1), len(seq2))
        
        for i in range(min_len):
            if seq1[i] != seq2[i]:
                mismatches.append(i)
        
        # Count gaps as length difference
        gaps = abs(len(seq1) - len(seq2))
        
        return gaps, mismatches
    
    def batch_align(self, sequences: List[Dict]) -> List[Dict]:
        """
        Perform batch alignment on multiple sequence pairs.
        
        Args:
            sequences: List of dictionaries with sequence data
            
        Returns:
            List of alignment results
        """
        results = []
        for seq_data in sequences:
            result = self.analyze(seq_data)
            results.append(result)
        
        return results
