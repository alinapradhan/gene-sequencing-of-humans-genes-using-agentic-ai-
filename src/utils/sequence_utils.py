"""
Utility functions for gene sequence processing and analysis.
"""

import numpy as np
from typing import List, Dict, Tuple
from collections import Counter


def calculate_gc_content(sequence: str) -> float:
    """
    Calculate the GC content (percentage of G and C nucleotides) in a DNA sequence.
    
    Args:
        sequence: DNA sequence string
        
    Returns:
        GC content as a percentage (0-100)
    """
    if not sequence:
        return 0.0
    
    gc_count = sequence.count('G') + sequence.count('C')
    return (gc_count / len(sequence)) * 100


def hamming_distance(seq1: str, seq2: str) -> int:
    """
    Calculate Hamming distance between two sequences of equal length.
    
    Args:
        seq1: First DNA sequence
        seq2: Second DNA sequence
        
    Returns:
        Number of positions at which sequences differ
    """
    if len(seq1) != len(seq2):
        raise ValueError("Sequences must be of equal length")
    
    return sum(c1 != c2 for c1, c2 in zip(seq1, seq2))


def find_mutations(reference: str, sample: str) -> List[Dict]:
    """
    Find all mutations between a reference and sample sequence.
    
    Args:
        reference: Reference DNA sequence
        sample: Sample DNA sequence to compare
        
    Returns:
        List of dictionaries containing mutation details
    """
    if len(reference) != len(sample):
        raise ValueError("Sequences must be of equal length")
    
    mutations = []
    for i, (ref_base, sample_base) in enumerate(zip(reference, sample)):
        if ref_base != sample_base:
            mutations.append({
                'position': i,
                'reference': ref_base,
                'sample': sample_base,
                'type': 'substitution'
            })
    
    return mutations


def sliding_window_analysis(sequence: str, window_size: int = 100) -> List[Dict]:
    """
    Perform sliding window analysis on a sequence.
    
    Args:
        sequence: DNA sequence
        window_size: Size of the sliding window
        
    Returns:
        List of dictionaries containing analysis for each window
    """
    results = []
    
    for i in range(0, len(sequence) - window_size + 1, window_size // 2):
        window = sequence[i:i + window_size]
        results.append({
            'start': i,
            'end': i + window_size,
            'gc_content': calculate_gc_content(window),
            'length': len(window)
        })
    
    return results


def find_patterns(sequence: str, pattern: str) -> List[int]:
    """
    Find all occurrences of a pattern in a sequence.
    
    Args:
        sequence: DNA sequence to search
        pattern: Pattern to find
        
    Returns:
        List of starting positions where pattern is found
    """
    positions = []
    start = 0
    
    while True:
        pos = sequence.find(pattern, start)
        if pos == -1:
            break
        positions.append(pos)
        start = pos + 1
    
    return positions


def calculate_sequence_complexity(sequence: str, k: int = 3) -> float:
    """
    Calculate sequence complexity using k-mer diversity.
    
    Args:
        sequence: DNA sequence
        k: Length of k-mers to analyze
        
    Returns:
        Complexity score (0-1, higher is more complex)
    """
    if len(sequence) < k:
        return 0.0
    
    kmers = [sequence[i:i+k] for i in range(len(sequence) - k + 1)]
    unique_kmers = len(set(kmers))
    total_possible = min(len(kmers), 4**k)  # 4^k possible k-mers
    
    return unique_kmers / total_possible if total_possible > 0 else 0.0


def reverse_complement(sequence: str) -> str:
    """
    Generate the reverse complement of a DNA sequence.
    
    Args:
        sequence: DNA sequence
        
    Returns:
        Reverse complement sequence
    """
    complement = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'}
    return ''.join(complement.get(base, base) for base in reversed(sequence))


def analyze_sequence_composition(sequence: str) -> Dict:
    """
    Analyze the nucleotide composition of a sequence.
    
    Args:
        sequence: DNA sequence
        
    Returns:
        Dictionary with composition statistics
    """
    counts = Counter(sequence)
    total = len(sequence)
    
    return {
        'total_length': total,
        'A_count': counts.get('A', 0),
        'T_count': counts.get('T', 0),
        'G_count': counts.get('G', 0),
        'C_count': counts.get('C', 0),
        'A_percent': (counts.get('A', 0) / total * 100) if total > 0 else 0,
        'T_percent': (counts.get('T', 0) / total * 100) if total > 0 else 0,
        'G_percent': (counts.get('G', 0) / total * 100) if total > 0 else 0,
        'C_percent': (counts.get('C', 0) / total * 100) if total > 0 else 0,
        'gc_content': calculate_gc_content(sequence)
    }
