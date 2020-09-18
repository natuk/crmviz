# CRMVIZ
Python command line tool and library for visualising RDF triples for datasets mapped to the [CIDOC-CRM](http://www.cidoc-crm.org/) ontology. This is based on:

* [rdflib](https://rdflib.readthedocs.io/en/stable/)
* [graphviz](https://pypi.org/project/graphviz/)

CRM version out-of-the-box: 6.2.1

## Command line use

```commandline
python crmviz -f <format> [file]
```

Example:

```commandline
python crmviz -f png my-triples.rdf
```
This will produce two files: `my-triples.gv` and `my-triples.gv.sgv`.

## Python use 

Example python use:

```python
from visualise import visualise_graph # import the library
graph = Graph() # create a new graph
graph.add((subject, predicate, object)) # add triples manually 
graph.parse(file.rdf) # or parse an existing file
dot = visualise_graph(graph, 'CRMVIZ graph') # run the visualisation
dot.render(exportfile + '.gv',format='svg') # export in default svg
```

## Example

These triples:

```
@prefix crm: <http://www.cidoc-crm.org/cidoc-crm/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix stcath: <https://data.ligatus.org.uk/stcatherines/ms/> .

stcath:780c99ac-b3ee-4b21-9e48-32b53a721830 a crm:E78_Collection ;
    rdfs:label "Arabic" ;
    crm:P46_is_composed_of stcath:961e50ea-2895-472e-94ae-b69ff8c2e56d .

stcath:5e8ede4e-6a3f-4726-aa8d-504741bb0154 a crm:E42_Identifier ;
    rdfs:label "Arabica 0001 (shelfmark)" .

stcath:961e50ea-2895-472e-94ae-b69ff8c2e56d a crm:E22_Man-Made_Object ;
    rdfs:label "Arabica 0001" ;
    crm:P2_has_type <http://w3id.org/lob/concept/4886> ;
    crm:P48_has_preferred_identifier stcath:5e8ede4e-6a3f-4726-aa8d-504741bb0154 .
```

will produce this output:

![Rendered triples](./mss.gv.svg)

## Benefits

The output is useful for explaining CRM modelling. Things to notice:

* box colours follow current conventions in the CRM community
* boxes include instances and classes
* instances, classes and properties include URIs
* easily expandable to include CRM extensions or different CRM versions