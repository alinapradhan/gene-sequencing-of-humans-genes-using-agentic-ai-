"""
Mutation Detection Agent for identifying genetic mutations.
"""

from typing import Dict, List
import numpy as np
from .base_agent import BaseAgent
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.sequence_utils import find_mutations, hamming_distance


class MutationDetectionAgent(BaseAgent):
    """Agent for detecting and analyzing genetic mutations."""
    
    def __init__(self, significance_threshold: int = 5):
        """
        Initialize the Mutation Detection Agent.
        
        Args:
            significance_threshold: Minimum number of mutations to be considered significant
        """
        super().__init__("MutationDetectionAgent")
        self.significance_threshold = significance_threshold
    
    def analyze(self, data: Dict) -> Dict:
        """
        Detect and analyze mutations in a sequence.
        
        Args:
            data: Dictionary containing 'reference' and 'sample' sequences
            
        Returns:
            Dictionary with mutation analysis results
        """
        reference = data.get('reference', '')
        sample = data.get('sample', '')
        patient_id = data.get('patient_id', 'unknown')
        
        if not reference or not sample:
            return {'error': 'Missing reference or sample sequence'}
        
        # Find all mutations
        mutations = find_mutations(reference, sample)
        
        # Categorize mutations
        mutation_types = self._categorize_mutations(mutations)
        
        # Assess clinical significance
        significance = self._assess_significance(len(mutations))
        
        # Calculate mutation rate
        mutation_rate = (len(mutations) / len(reference)) * 100
        
        # Identify hotspots
        hotspots = self._identify_hotspots(mutations, window_size=100)
        
        result = {
            'patient_id': patient_id,
            'agent': self.agent_name,
            'total_mutations': len(mutations),
            'mutation_rate': mutation_rate,
            'mutation_types': mutation_types,
            'clinical_significance': significance,
            'hotspots': hotspots,
            'mutations': mutations[:20]  # Include first 20 mutations for detail
        }
        
        self.log_result(result)
        return result
    
    def _categorize_mutations(self, mutations: List[Dict]) -> Dict:
        """
        Categorize mutations by type.
        
        Args:
            mutations: List of mutation dictionaries
            
        Returns:
            Dictionary with mutation counts by category
        """
        categories = {
            'transitions': 0,  # A<->G, C<->T
            'transversions': 0,  # All other substitutions
            'total_substitutions': len(mutations)
        }
        
        for mutation in mutations:
            ref = mutation.get('reference', '')
            sample = mutation.get('sample', '')
            
            # Check if it's a transition
            if (ref == 'A' and sample == 'G') or (ref == 'G' and sample == 'A'):
                categories['transitions'] += 1
            elif (ref == 'C' and sample == 'T') or (ref == 'T' and sample == 'C'):
                categories['transitions'] += 1
            else:
                categories['transversions'] += 1
        
        return categories
    
    def _assess_significance(self, mutation_count: int) -> str:
        """
        Assess the clinical significance of mutations.
        
        Args:
            mutation_count: Number of mutations detected
            
        Returns:
            Significance level string
        """
        if mutation_count == 0:
            return "normal"
        elif mutation_count < self.significance_threshold:
            return "low"
        elif mutation_count < self.significance_threshold * 2:
            return "moderate"
        else:
            return "high"
    
    def _identify_hotspots(self, mutations: List[Dict], window_size: int = 100) -> List[Dict]:
        """
        Identify mutation hotspots in the sequence.
        
        Args:
            mutations: List of mutation dictionaries
            window_size: Size of window for hotspot detection
            
        Returns:
            List of hotspot regions
        """
        if not mutations:
            return []
        
        positions = [m['position'] for m in mutations]
        hotspots = []
        
        # Simple hotspot detection: areas with high mutation density
        for i in range(0, max(positions) + 1, window_size):
            window_mutations = [p for p in positions if i <= p < i + window_size]
            if len(window_mutations) >= 3:  # At least 3 mutations in a window
                hotspots.append({
                    'start': i,
                    'end': i + window_size,
                    'mutation_count': len(window_mutations),
                    'density': len(window_mutations) / window_size
                })
        
        return hotspots
    
    def classify_risk(self, analysis_result: Dict) -> str:
        """
        Classify patient risk based on mutation analysis.
        
        Args:
            analysis_result: Result from analyze method
            
        Returns:
            Risk classification string
        """
        significance = analysis_result.get('clinical_significance', 'normal')
        mutation_rate = analysis_result.get('mutation_rate', 0)
        hotspots = analysis_result.get('hotspots', [])
        
        if significance == "high" or mutation_rate > 2.0 or len(hotspots) > 2:
            return "high_risk"
        elif significance == "moderate" or mutation_rate > 1.0 or len(hotspots) > 0:
            return "moderate_risk"
        elif significance == "low":
            return "low_risk"
        else:
            return "normal"
