"""Gene Sequencing Agents Package"""
import sys
import os

# Handle imports for both package and standalone execution
try:
    from .base_agent import BaseAgent
    from .alignment_agent import SequenceAlignmentAgent
    from .mutation_agent import MutationDetectionAgent
    from .pattern_agent import PatternRecognitionAgent
except ImportError:
    # Fallback for standalone or test execution
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from base_agent import BaseAgent
    from alignment_agent import SequenceAlignmentAgent
    from mutation_agent import MutationDetectionAgent
    from pattern_agent import PatternRecognitionAgent

__all__ = [
    'BaseAgent',
    'SequenceAlignmentAgent',
    'MutationDetectionAgent',
    'PatternRecognitionAgent'
]
