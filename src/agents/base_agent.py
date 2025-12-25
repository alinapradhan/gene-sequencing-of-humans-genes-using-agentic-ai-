"""
Base Agent class for gene sequencing analysis.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List
import pandas as pd


class BaseAgent(ABC):
    """Abstract base class for all gene sequencing agents."""
    
    def __init__(self, agent_name: str):
        """
        Initialize the base agent.
        
        Args:
            agent_name: Name identifier for the agent
        """
        self.agent_name = agent_name
        self.results = []
    
    @abstractmethod
    def analyze(self, data: Any) -> Dict:
        """
        Perform analysis on the given data.
        
        Args:
            data: Input data to analyze
            
        Returns:
            Dictionary containing analysis results
        """
        pass
    
    def log_result(self, result: Dict):
        """
        Log analysis result.
        
        Args:
            result: Result dictionary to log
        """
        self.results.append(result)
    
    def get_results(self) -> List[Dict]:
        """
        Get all logged results.
        
        Returns:
            List of result dictionaries
        """
        return self.results
    
    def clear_results(self):
        """Clear all logged results."""
        self.results = []
    
    def summarize(self) -> Dict:
        """
        Generate a summary of all results.
        
        Returns:
            Summary dictionary
        """
        return {
            'agent_name': self.agent_name,
            'total_analyses': len(self.results),
            'results': self.results
        }
