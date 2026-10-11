API reference
=============

``sardis.summarize_vetting_result(result)`` returns classifier labels,
confusion matrices, precision, recall, and a Boolean mask identifying targets
matching ``result["typesyst"]`` in the truth labels. The result dictionary must
contain the truth-class list and indices, target-system name, classifier labels,
and one Boolean prediction vector per classifier. All prediction vectors must
match the truth-label array shape.

``sardis.init(typesyst="PlanetarySystem", dicttroiinpt=None,
strgcnfg=None, pathbase=None)`` initializes the target classification workflow.
The outputs and classification assumptions are documented in the README and
the selected Troia workflow.
