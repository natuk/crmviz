from graphviz import Digraph
from rdflib import Graph, URIRef, Literal
from rdflib.namespace import SKOS, RDF, RDFS
#from namespaces import get_prefix_uri
import rdflib.term
import uuid

def visualise_graph(graph, comment, crmversion):
    # graph is the rdflib graph being visualised and dot is the graphviz Digraph of the visualisation

    # load the CIDOC-CRM rdf rules
    crmgraph = Graph()
    if crmversion == "erlangen":
        crmgraph.parse("ecrm_current.owl.rdf")
    else:
        crmgraph.parse("cidoc-crm-6.2.1.rdfs")

    # load the typed properties
    crmtpgraph = Graph()
    crmtpgraph.parse("CRM-typed-properties.owl")

    #merge the three graphs
    uniongraph = graph + crmgraph + crmtpgraph

    # start a new drawing
    dot = Digraph(comment=comment)
    #dot.attr(rankdir='LR', ratio='0.5', splines='curved')
    dot.attr(rankdir='LR', pad='0.5', nodesep='0.5', ranksep='1', splines='line') # splines='curved' splines='line'
    dot.attr('node', shape='none', penwidth='3.0', margin='0') # using "none" shape here as the HTML labels are incompatible with anything else see: https://stackoverflow.com/questions/54610953/graphviz-node-with-html-label-has-no-ports and https://gitlab.com/graphviz/graphviz/-/issues/1491

    # prepare nodes first
    nodes = {}  # local dictionary holding nodes
    # for every rdf:type triple in the graph3
    for subj, pred, obj in graph:
        #ignore the label triples as we do not want them as separate links, only as part of the labels
        if pred == RDFS.label:
            continue
        if pred == SKOS.prefLabel:
            continue
        # remove ":" from the node names as graphviz gives a special meaning to them see https://graphviz.readthedocs.io/en/stable/manual.html#ports
        # remove "/", ".", "-" as well as they are problematic
        subjgnode = str(subj).replace(":", "").replace("/", "").replace(".", "").replace("-", "")
        objgnode = str(obj).replace(":", "").replace("/", "").replace(".", "").replace("-", "")
        predgnode = str(pred).replace(":", "").replace("/", "").replace(".", "").replace("-", "")
        # create graphviz nodes with new uuids for literals to avoid literals appear as class nodes
        if type(obj) is rdflib.Literal:
            newuuid = str(uuid.uuid4()).replace("-", "")
            objgnode = newuuid
        # always create a new instance of predgnode otherwise if the predicates are used multiple times we produce spider-like drawings
        predgnode = subjgnode + predgnode + objgnode

        if pred == RDF.type:
            try:
                subjlabel = str(uniongraph.preferredLabel(subj, lang="en")[0][1])
            except:
                subjlabel = str(subj)
            try:
                objlabel = str(uniongraph.preferredLabel(obj, lang="en")[0][1])
            except:
                objlabel = str(obj)

            if len(subjlabel) > 30:
                subjlabel = subjlabel[0:27] + "..."
            if len(objlabel) > 30:
                objlabel = objlabel[0:27] + "..."

            subjuri = get_prefix_uri(uniongraph, subj)
            objuri = get_prefix_uri(uniongraph, obj)

            # solution for splitting nodes from here: https://stackoverflow.com/questions/45548114/graphvizdot-language-can-i-get-nodes-in-horizontal-line#45553493
            # subjlabel = '{{' + subjlabel + '|' + objlabel + '}}'

            # solution for splitting nodes from here: https://stackoverflow.com/questions/36445870/graphviz-node-split
            subjlabel = '<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">\
                    <TR><TD PORT="instance" CELLPADDING="10" bgcolor="' + get_doccolour(objlabel, crmgraph) + '"><FONT FACE="Ubuntu">' + subjlabel + '</FONT><BR /><FONT FACE="FreeMono" POINT-SIZE="8">' + subjuri + '</FONT></TD></TR>\
                    <TR><TD PORT="class" CELLPADDING="10" bgcolor="' + get_doccolour(objlabel, crmgraph) + '"><FONT FACE="Ubuntu"><I>' + objlabel + '</I></FONT><BR /><FONT FACE="FreeMono" POINT-SIZE="8">' + objuri + '</FONT></TD></TR>\
                    </TABLE>>'

            #nodes[subjgnode] = subjlabel
            dot.node(subjgnode, subjlabel)
            continue

        if type(obj) is rdflib.Literal:
            sane_obj = str(obj)
            if len(sane_obj) > 30:
                sane_obj = sane_obj[0:27] + "..."
            objlabel = '<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">\
                        <TR><TD PORT="instance" CELLPADDING="10" bgcolor="white"><FONT FACE="Ubuntu">' + sane_obj + '</FONT><BR /><FONT FACE="FreeMono" POINT-SIZE="8">Literal</FONT></TD></TR>\
                        </TABLE>>'

            #nodes[objgnode] = objlabel
            dot.node(objgnode, objlabel)

        # then do edges
        try:
            predlabel = str(uniongraph.preferredLabel(pred, lang="en")[0][1])
        except:
            predlabel = str(pred)

        preduri = get_prefix_uri(uniongraph, pred)

        predlabel = '<<TABLE BORDER="0" CELLBORDER="0"><TR><TD BGCOLOR = "white"><FONT FACE="Ubuntu">' + predlabel + '</FONT></TD></TR><TR><TD BGCOLOR = "white"><FONT FACE="FreeMono" POINT-SIZE="8">' + preduri + '</FONT></TD></TR></TABLE>>'

        # we are using invisible nodes for the predicates
        dot.node(predgnode, predlabel)
        dot.edge(subjgnode + ":instance:e", predgnode, arrowhead='none') # instance links
        dot.edge(predgnode, objgnode + ":instance:w")
        #dot.edge(subjgnode + ":instance:e", objgnode + ":instance:w", predlabel)

        #dot.edge(subjgnode, predgnode, arrowhead='none') # no instance links
        #dot.edge(predgnode, objgnode)
        #dot.edge(subjgnode, objgnode, headlabel=predlabel, labeldistance='5', labelangle='45')

    return dot

def get_doccolour(entitylabel, crmgraph):
    # set documentation colours
    doccolour = {
        "Physical Thing": '#E1BA9C',
        "Event": '#96e0f6',
        "Place": '#aff090',
        "Actor": '#FFBDCA',
        "Time-span": '#ddfffe',
        "Type": '#FAB565',
        "rdftype": "#fff",
        "Conceptual Object": "#fffa40",
        "Physical Thing": '#E1BA9C', # repeat for erlangen labels
        "E5 Event": '#96e0f6',
        "E53 Place": '#aff090',
        "E39 Actor": '#FFBDCA',
        "E52 Time-span": '#ddfffe',
        "E55 Type": '#FAB565',
        "E28 Conceptual Object": "#fffa40"
    }

    if entitylabel in doccolour: # if the entity itself has a colour then use it
        return(doccolour[entitylabel])
    # otherwise check if any of its superclasses have colours

    for entity in crmgraph.subjects(RDFS.label, Literal(entitylabel, lang="en")):
        for parentity in crmgraph.objects(entity, RDFS.subClassOf*'*'): # property path example here: https://rdflib.readthedocs.io/en/stable/apidocs/examples.html#module-examples.foafpaths
            for parentitylabel in crmgraph.preferredLabel(parentity, lang="en"):
                if str(parentitylabel[1]) in doccolour:  # if the entity itself has a colour then use it
                    return (doccolour[str(parentitylabel[1])])

    return "#ffffff" # if everything fails, return white

def get_prefix_uri(graph, uri):
    # returns the uri with a prefix if the prefix exists in the graph
    nss = [n for n in graph.namespace_manager.namespaces()]
    for ns in nss:
        if str(uri).find(ns[1]) != -1:
            prefix = ns[0]
            uri = str(uri)[len(ns[1]):]
            return prefix + ":" + uri
    return uri