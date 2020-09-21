from rdflib import Graph, Namespace, URIRef
from visualise import visualise_graph
from operator import itemgetter
import optparse
import sys
import os.path as path

p = optparse.OptionParser(
    description='Visualises RDF triples of datasets based on the CRM ontology (version 6.2.1) for documentation purposes.',
    prog='crmviz',
    usage='%prog -v <crm_version> -f <format> [file]'
)
p.add_option('--format', '-f', help="Choose the output image format. Supports 'svg' 'png' 'pdf' (svg default)")
p.add_option('--crmversion', '-v', help="Choose the CRM version to use. Supports 'erlangen' 'forth' (forth default)")

options, arguments = p.parse_args() # parse the arguments

if len(arguments) == 1: # if a filename has been given
    try:
        graph = Graph() # create a new graph
        # inputstream = open(arguments[0])
        graph.parse(arguments[0]) # try to parse it
    except:
        sys.stderr.write("Problem reading '{0}'\n".format(arguments[0]))
        p.print_help()
        sys.exit(-1)

    if (options.crmversion):  # check the requested format
        dot = visualise_graph(graph, 'CRMVIZ graph for file ' + arguments[0], options.crmversion) # run the visualisation with given option
    else:
        dot = visualise_graph(graph, 'CRMVIZ graph for file ' + arguments[0], 'forth')  # run the visualisation with forth version of CRM
    exportfilename = path.splitext(arguments[0])[0] # get the filename without the extension

    if (options.format): # check the requested format
        dot.render(exportfilename + '.gv',format=options.format) # export in the requested format
    else:
        dot.render(exportfilename + '.gv',format='svg') # export in default svg