Introduction

This project aimed to measure the variability of event logs in terms of behavioral variety. Variability analysis is crucial for understanding process complexity, selecting appropriate modeling or prediction techniques, and detecting concept drifts in event logs.
Three metrics were defined for this purpose:
Variant Variability: Measures the number of unique behavioral variants in the log.
Edit Distance Variability: Computes the average edit distance between pairs of traces to quantify their sequence similarity.
Custom Variability: A metric chosen by the developer to reflect a specific aspect of variability. Initially, this metric measured unique resources, but it was later adapted to evaluate trace length variability using the standard deviation of trace lengths.
Event logs analyzed:
BPI Challenge 2011 log (BPIChallenge2011.xes.zip)
Concept Drift Log (concept_drift.xes.zip)
Concept Drift Log Type 1 (concept_drift_type1.xes.zip)
Concept Drift Log Type 2 (concept_drift_type2.xes.zip)
The project required Python implementation using the PM4Py library and a report summarizing the results.

Development

Checking Logs
The provided event logs were analyzed for structure and content. They contained attributes like activity names (concept:name) and timestamps, with some logs exhibiting concept drifts.
Let’s see the events from concept_drift.xes log
<event>
            <string key="concept:name" value="Appraise property"/>
            <string key="lifecycle:transition" value="complete"/>
            <string key="org:resource" value="NOT_SET"/>
            <date key="time:timestamp" value="2004-02-02T16:38:51.963+01:00"/>
            <string key="Activity" value="Appraise property"/>
        </event>
and log from BPIChallange2011.xes 
<event>
            <string key="org:group" value="General Lab Clinical Chemistry"/>
            <int key="Number of executions" value="1"/>
            <int key="Specialism code" value="86"/>
            <string key="concept:name" value="rhesusfactor d - centrifugeermethode - e"/>
            <string key="Producer code" value="BLOB"/>
            <string key="Section" value="Section 4"/>
            <int key="Activity code" value="370606"/>
            <date key="time:timestamp" value="2005-02-02T00:00:00.000+01:00"/>
            <string key="lifecycle:transition" value="complete"/>
</event>
There are important details in these logs, that make the development process more complicated. Firstly, the number of parameters in the second log is much bigger, and overall the structure of events is not the same. Secondly, in the concept_drift log "org:resource" value isn’t "NOT_SET" and that’s not only for this event. These are important details for the next step, so pre-checking the logs gave more understanding of the way of implementing required functions.

Code Development

Three Python functions were developed (see Attachment) in Visual Studio with a Python extension and pm4py library :
compute_variant_variability: Counts unique behavioral variants in the log. This could be easily solved by integrating pre-written function variants_get.get_variants(event_log)
compute_edit_distance_variability: Calculates the average edit distance between all pairs of traces in the log. This is a complicated task since each of the logs is different from the others and moreover the size of these logs starts from 2000 events. The difficulty here is the effective comparison between thousands of events, because if not the effective algorithm for pair comparison then running the program will take minutes before getting the results. SequenceMatcher was the imported library that was helpful for the fast implementation of the comparison algorithm. 
compute_my_variability: Initially measured unique resources per trace but was later redefined to measure trace length variability using the standard deviation of trace lengths.
The code also included:
A utility function to load event logs using PM4Py.
A main function to compute metrics for multiple logs and summarize results.


Choosing Own Metric
The custom variability metric evolved during development. After recognizing that resource information was unavailable in the logs, the metric was redefined to evaluate trace length variability, reflecting a distinct aspect of process variability.
This measure looks at how much the lengths of the traces vary. If all traces have similar lengths, the standard deviation will be low. If the lengths differ greatly, the standard deviation will be high.
Trace lengths often indicate process complexity or the presence of optional or repetitive activities, making it a good candidate for variability analysis.
Testing
The functions were tested on the provided logs to ensure accuracy and meaningful outputs. Metrics were computed for:
BPI Challenge 2011 log.
Concept Drift Log (whole log).
Concept Drift Log Type 1.
Concept Drift Log Type 2.

