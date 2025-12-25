"""
Agentic AI Orchestrator for Gene Sequencing Analysis

This module coordinates multiple AI agents to perform comprehensive gene sequence analysis.
"""

import pandas as pd
import json
from typing import Dict, List
from agents.alignment_agent import SequenceAlignmentAgent
from agents.mutation_agent import MutationDetectionAgent
from agents.pattern_agent import PatternRecognitionAgent


class GeneSequencingOrchestrator:
    """
    Main orchestrator that coordinates multiple agents for comprehensive gene analysis.
    """
    
    def __init__(self):
        """Initialize the orchestrator with all agents."""
        self.alignment_agent = SequenceAlignmentAgent()
        self.mutation_agent = MutationDetectionAgent(significance_threshold=5)
        self.pattern_agent = PatternRecognitionAgent()
        self.analysis_results = []
    
    def analyze_patient(self, patient_data: Dict) -> Dict:
        """
        Perform comprehensive analysis on a single patient's gene sequence.
        
        Args:
            patient_data: Dictionary containing patient's sequence data
            
        Returns:
            Comprehensive analysis results
        """
        patient_id = patient_data.get('patient_id', 'unknown')
        print(f"\n{'='*60}")
        print(f"Analyzing patient: {patient_id}")
        print(f"{'='*60}")
        
        results = {
            'patient_id': patient_id,
            'gene_type': patient_data.get('gene_type', 'unknown'),
            'analyses': {}
        }
        
        # Agent 1: Sequence Alignment
        print(f"\n[Agent 1] Sequence Alignment Agent analyzing...")
        alignment_result = self.alignment_agent.analyze(patient_data)
        results['analyses']['alignment'] = alignment_result
        print(f"  ✓ Alignment Score: {alignment_result.get('alignment_score', 0):.2f}%")
        print(f"  ✓ Identity: {alignment_result.get('identity_percentage', 0):.2f}%")
        
        # Agent 2: Mutation Detection
        print(f"\n[Agent 2] Mutation Detection Agent analyzing...")
        mutation_result = self.mutation_agent.analyze(patient_data)
        results['analyses']['mutation'] = mutation_result
        print(f"  ✓ Mutations Found: {mutation_result.get('total_mutations', 0)}")
        print(f"  ✓ Mutation Rate: {mutation_result.get('mutation_rate', 0):.3f}%")
        print(f"  ✓ Clinical Significance: {mutation_result.get('clinical_significance', 'unknown')}")
        
        # Agent 3: Pattern Recognition
        print(f"\n[Agent 3] Pattern Recognition Agent analyzing...")
        pattern_data = {
            'sequence': patient_data.get('sample', ''),
            'patient_id': patient_id
        }
        pattern_result = self.pattern_agent.analyze(pattern_data)
        results['analyses']['pattern'] = pattern_result
        print(f"  ✓ Sequence Complexity: {pattern_result.get('complexity_score', 0):.3f}")
        print(f"  ✓ Known Motifs Found: {len(pattern_result.get('known_motifs', {}))}")
        print(f"  ✓ Repeating Patterns: {len(pattern_result.get('repeating_patterns', []))}")
        
        # Generate comprehensive assessment
        assessment = self._generate_assessment(results)
        results['assessment'] = assessment
        
        print(f"\n[Final Assessment]")
        print(f"  ✓ Overall Risk: {assessment['risk_level']}")
        print(f"  ✓ Recommendation: {assessment['recommendation']}")
        
        self.analysis_results.append(results)
        return results
    
    def analyze_dataset(self, dataset_path: str, max_samples: int = None) -> List[Dict]:
        """
        Analyze a complete dataset of gene sequences.
        
        Args:
            dataset_path: Path to the CSV dataset
            max_samples: Maximum number of samples to analyze (None for all)
            
        Returns:
            List of analysis results for all patients
        """
        print(f"\n{'='*60}")
        print("GENE SEQUENCING AGENTIC AI ANALYSIS SYSTEM")
        print(f"{'='*60}")
        
        # Load dataset
        print(f"\nLoading dataset from: {dataset_path}")
        df = pd.read_csv(dataset_path)
        print(f"Total sequences loaded: {len(df)}")
        
        # Group by patient to get reference and sample pairs
        patients = df.groupby('patient_id')
        
        results = []
        count = 0
        
        for patient_id, group in patients:
            if max_samples and count >= max_samples:
                break
            
            # Get reference (non-mutated) and sample (potentially mutated) sequences
            reference_row = group[group['is_mutated'] == False]
            sample_row = group[group['is_mutated'] == True]
            
            if len(reference_row) > 0:
                reference = reference_row.iloc[0]
                
                # If no mutated sample, compare with itself
                if len(sample_row) > 0:
                    sample = sample_row.iloc[0]
                else:
                    sample = reference
                
                patient_data = {
                    'patient_id': patient_id,
                    'gene_type': reference['gene_type'],
                    'reference': reference['sequence'],
                    'sample': sample['sequence'],
                    'known_mutation_status': sample['is_mutated']
                }
                
                result = self.analyze_patient(patient_data)
                results.append(result)
                count += 1
        
        return results
    
    def _generate_assessment(self, results: Dict) -> Dict:
        """
        Generate overall assessment based on all agent analyses.
        
        Args:
            results: Combined results from all agents
            
        Returns:
            Assessment dictionary
        """
        mutation_analysis = results['analyses'].get('mutation', {})
        alignment_analysis = results['analyses'].get('alignment', {})
        
        # Determine risk level
        mutation_count = mutation_analysis.get('total_mutations', 0)
        mutation_rate = mutation_analysis.get('mutation_rate', 0)
        identity = alignment_analysis.get('identity_percentage', 100)
        
        if mutation_count > 15 or mutation_rate > 2.0 or identity < 95:
            risk_level = "HIGH"
            recommendation = "Immediate clinical consultation recommended. Significant mutations detected."
        elif mutation_count > 8 or mutation_rate > 1.0 or identity < 98:
            risk_level = "MODERATE"
            recommendation = "Clinical follow-up advised. Monitor for disease progression."
        elif mutation_count > 3 or mutation_rate > 0.5:
            risk_level = "LOW"
            recommendation = "Routine monitoring recommended. Minor variations detected."
        else:
            risk_level = "NORMAL"
            recommendation = "No significant mutations detected. Routine screening sufficient."
        
        return {
            'risk_level': risk_level,
            'recommendation': recommendation,
            'mutation_count': mutation_count,
            'mutation_rate': mutation_rate,
            'sequence_identity': identity
        }
    
    def generate_report(self, output_path: str = 'analysis_report.json'):
        """
        Generate a comprehensive analysis report.
        
        Args:
            output_path: Path to save the report
        """
        report = {
            'total_patients_analyzed': len(self.analysis_results),
            'analyses': self.analysis_results,
            'summary': {
                'high_risk': sum(1 for r in self.analysis_results 
                                if r['assessment']['risk_level'] == 'HIGH'),
                'moderate_risk': sum(1 for r in self.analysis_results 
                                    if r['assessment']['risk_level'] == 'MODERATE'),
                'low_risk': sum(1 for r in self.analysis_results 
                               if r['assessment']['risk_level'] == 'LOW'),
                'normal': sum(1 for r in self.analysis_results 
                             if r['assessment']['risk_level'] == 'NORMAL')
            }
        }
        
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n{'='*60}")
        print("ANALYSIS REPORT GENERATED")
        print(f"{'='*60}")
        print(f"Report saved to: {output_path}")
        print(f"\nSummary:")
        print(f"  Total Patients: {report['total_patients_analyzed']}")
        print(f"  High Risk: {report['summary']['high_risk']}")
        print(f"  Moderate Risk: {report['summary']['moderate_risk']}")
        print(f"  Low Risk: {report['summary']['low_risk']}")
        print(f"  Normal: {report['summary']['normal']}")
        
        return report


def main():
    """Main execution function."""
    # Initialize orchestrator
    orchestrator = GeneSequencingOrchestrator()
    
    # Analyze dataset
    dataset_path = 'src/data/synthetic_gene_sequences.csv'
    results = orchestrator.analyze_dataset(dataset_path, max_samples=5)
    
    # Generate report
    orchestrator.generate_report('gene_analysis_report.json')


if __name__ == "__main__":
    main()
