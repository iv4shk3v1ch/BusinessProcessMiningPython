import pm4py
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.statistics.variants.log import get as variants_get
from pm4py.util import constants
from itertools import combinations
import numpy as np
from difflib import SequenceMatcher


# Function 1: Compute the number of variants
def compute_variant_variability(event_log):
    """
    Computes the number of unique variants in the log.
    :param event_log: The event log (PM4Py format).
    :return: Number of unique variants.
    """
    variants = variants_get.get_variants(event_log)
    return len(variants)


# Function 2: Compute average edit distance variability
def compute_edit_distance(trace1, trace2):
    """
    Compute the similarity ratio between two traces using SequenceMatcher.
    :param trace1: First trace (list of activities).
    :param trace2: Second trace (list of activities).
    :return: Similarity ratio (float between 0 and 1).
    """
    return SequenceMatcher(None, trace1, trace2).ratio()


def compute_edit_distance_variability(event_log):
    """
    Computes the average edit distance between all pairs of traces.
    :param event_log: The event log (PM4Py format).
    :return: Average edit distance.
    """
    # Extract activities from each trace
    traces = [[event["concept:name"] for event in trace] for trace in event_log]
    print("COMPUTING DISTANCE STARTED")
    # Compute pairwise distances
    pairwise_distances = [
        compute_edit_distance(trace1, trace2)
        for trace1, trace2 in combinations(traces, 2)
    ]
    
    # Return average distance
    print("COMPUTING DISTANCE FINISHED")
    return np.mean(pairwise_distances) if pairwise_distances else 0.0



# Function 3: Compute a custom variability metric
def compute_my_variability(event_log):
    """
    Custom variability metric: Measure variability based on the spread of trace lengths.
    :param event_log: The event log (PM4Py format).
    :return: Variability measure based on trace length diversity.
    """
    # Extract the lengths of all traces
    trace_lengths = [len(trace) for trace in event_log]
    
    # Compute the standard deviation of trace lengths as a measure of variability
    variability = np.std(trace_lengths)
    
    return variability


# Utility: Load event log
def load_event_log(file_path):
    """
    Loads an event log from an XES file.
    :param file_path: Path to the XES file.
    :return: The event log (PM4Py format), or None if loading fails.
    """
    try:
        print(f"Loading event log from: {file_path}")
        event_log = xes_importer.apply(file_path)
        print(f"Successfully loaded log with {len(event_log)} traces.")
        return event_log
    except Exception as e:
        print(f"Error loading log from {file_path}: {e}")
        return None


# Main function
def main():
    # File paths (ensure these paths are correct and accessible)
    logs = {
       # "BPI Challenge 2011": "BPIChallenge2011.xes",
       # "Concept Drift Log": "concept_drift.xes",
       # "Concept Drift Type 1": "concept_drift_type1.xes",
        "Concept Drift Type 2": "concept_drift_type2.xes"
    }

    # Dictionary to store results
    results = {}

    for log_name, file_path in logs.items():
        print(f"\nProcessing {log_name}...")

        # Load the event log
        event_log = load_event_log(file_path)
        if event_log is None:
            print(f"Skipping {log_name} due to loading issues.")
            continue

        # Compute metrics
        try:
            variant_variability = compute_variant_variability(event_log)
            edit_distance_variability = compute_edit_distance_variability(event_log)
            my_variability = compute_my_variability(event_log)

            # Store results
            results[log_name] = {
                "Variant Variability": variant_variability,
                "Edit Distance Variability": edit_distance_variability,
                "Custom Variability": my_variability
            }

            # Print results
            print(f"{log_name} Results:")
            for metric, value in results[log_name].items():
                print(f"  {metric}: {value}")
        except Exception as e:
            print(f"Error processing {log_name}: {e}")

    # Return all results for further use or testing
    return results



if __name__ == "__main__":
    results = main()
    