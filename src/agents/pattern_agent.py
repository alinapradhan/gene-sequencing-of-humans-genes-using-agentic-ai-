"""
Pattern Recognition Agent for identifying conserved patterns and motifs in gene sequences.
"""

from typing import Dict, List, Set
from collections import Counter
from .base_agent import BaseAgent
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.sequence_utils import find_patterns, calculate_sequence_complexity, sliding_window_analysis


class PatternRecognitionAgent(BaseAgent):
    """Agent for recognizing patterns, motifs, and conserved regions in sequences."""
    
    def __init__(self):
        """Initialize the Pattern Recognition Agent."""
        super().__init__("PatternRecognitionAgent")
        # Common genetic motifs and patterns
        self.known_motifs = {
            'TATA_box': 'TATAAA',
            'CAAT_box': 'GGCCAATCT',
            'GC_box': 'GGGCGG',
            'Kozak_sequence': 'GCCGCCACCATGG',
            'Poly_A_signal': 'AATAAA'
        }
    
    def analyze(self, data: Dict) -> Dict:
        """
        Analyze sequence for patterns and motifs.
        
        Args:
            data: Dictionary containing 'sequence' to analyze
            
        Returns:
            Dictionary with pattern analysis results
        """
        sequence = data.get('sequence', '')
        patient_id = data.get('patient_id', 'unknown')
        
        if not sequence:
            return {'error': 'Missing sequence'}
        
        # Find known motifs
        motifs_found = self._find_known_motifs(sequence)
        
        # Identify repeating patterns
        repeats = self._find_repeating_patterns(sequence)
        
        # Calculate sequence complexity
        complexity = calculate_sequence_complexity(sequence, k=3)
        
        # Perform sliding window analysis
        window_analysis = sliding_window_analysis(sequence, window_size=100)
        
        # Find conserved regions (regions with high GC content)
        conserved_regions = self._identify_conserved_regions(window_analysis)
        
        # Find tandem repeats
        tandem_repeats = self._find_tandem_repeats(sequence)
        
        result = {
            'patient_id': patient_id,
            'agent': self.agent_name,
            'sequence_length': len(sequence),
            'complexity_score': complexity,
            'known_motifs': motifs_found,
            'repeating_patterns': repeats,
            'conserved_regions': conserved_regions,
            'tandem_repeats': tandem_repeats,
            'average_gc_content': sum(w['gc_content'] for w in window_analysis) / len(window_analysis) if window_analysis else 0
        }
        
        self.log_result(result)
        return result
    
    def _find_known_motifs(self, sequence: str) -> Dict[str, List[int]]:
        """
        Search for known genetic motifs in the sequence.
        
        Args:
            sequence: DNA sequence
            
        Returns:
            Dictionary of motif names and their positions
        """
        motifs_found = {}
        
        for motif_name, motif_sequence in self.known_motifs.items():
            positions = find_patterns(sequence, motif_sequence)
            if positions:
                motifs_found[motif_name] = positions
        
        return motifs_found
    
    def _find_repeating_patterns(self, sequence: str, min_length: int = 3, 
                                 max_length: int = 10) -> List[Dict]:
        """
        Identify repeating patterns in the sequence.
        
        Args:
            sequence: DNA sequence
            min_length: Minimum pattern length
            max_length: Maximum pattern length
            
        Returns:
            List of repeating patterns with their frequency
        """
        patterns = []
        
        for length in range(min_length, min(max_length + 1, len(sequence) // 2)):
            pattern_counts = Counter()
            
            for i in range(len(sequence) - length + 1):
                pattern = sequence[i:i + length]
                pattern_counts[pattern] += 1
            
            # Find patterns that occur more than twice
            for pattern, count in pattern_counts.items():
                if count >= 3:  # Pattern appears at least 3 times
                    positions = find_patterns(sequence, pattern)
                    patterns.append({
                        'pattern': pattern,
                        'length': length,
                        'frequency': count,
                        'positions': positions[:5]  # First 5 positions
                    })
        
        # Sort by frequency
        patterns.sort(key=lambda x: x['frequency'], reverse=True)
        return patterns[:10]  # Return top 10 patterns
    
    def _identify_conserved_regions(self, window_analysis: List[Dict], 
                                   threshold: float = 55.0) -> List[Dict]:
        """
        Identify conserved regions based on GC content.
        
        Args:
            window_analysis: List of window analysis results
            threshold: GC content threshold for conservation
            
        Returns:
            List of conserved regions
        """
        conserved = []
        
        for window in window_analysis:
            if window['gc_content'] >= threshold:
                conserved.append({
                    'start': window['start'],
                    'end': window['end'],
                    'gc_content': window['gc_content']
                })
        
        return conserved
    
    def _find_tandem_repeats(self, sequence: str, min_unit_length: int = 2,
                            max_unit_length: int = 6) -> List[Dict]:
        """
        Find tandem repeats in the sequence.
        
        Args:
            sequence: DNA sequence
            min_unit_length: Minimum repeat unit length
            max_unit_length: Maximum repeat unit length
            
        Returns:
            List of tandem repeat regions
        """
        tandem_repeats = []
        
        for unit_length in range(min_unit_length, max_unit_length + 1):
            i = 0
            while i < len(sequence) - unit_length * 2:
                unit = sequence[i:i + unit_length]
                repeat_count = 1
                j = i + unit_length
                
                # Count consecutive repeats
                while j + unit_length <= len(sequence) and sequence[j:j + unit_length] == unit:
                    repeat_count += 1
                    j += unit_length
                
                if repeat_count >= 3:  # At least 3 consecutive repeats
                    tandem_repeats.append({
                        'position': i,
                        'unit': unit,
                        'unit_length': unit_length,
                        'repeat_count': repeat_count,
                        'total_length': unit_length * repeat_count
                    })
                    i = j
                else:
                    i += 1
        
        return tandem_repeats
