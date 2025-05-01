import graphviz
from graphviz import Digraph

def create_interaction_diagram():
    diagram = Digraph(comment='Interaction Diagram')
    #Adding participants
    diagram.node('T', 'Trader')
    diagram.node('TS', 'Trading System')
    diagram.node('O', 'Order')
    diagram.node('SE', 'Stock Exchange')
    diagram.node('M', 'Module')
    # Adding interactions between participants
    diagram.edge('T', 'TS', 'ЗапитПозики (сума, умови)')
    diagram.edge('TS', 'O', 'СтворитиБорг (сума, відсотки)')
    diagram.edge('O', 'SE', 'РезервуватиКошти()')
    diagram.edge('SE', 'T', 'НадатиПозиченіКошти()')
    diagram.edge('T', 'M', 'ПовернутиБорг (сума, відсотки)')
    diagram.edge('M', 'SE', 'ЗакритиБорг()')
    diagram.edge('SE', 'O', 'ОновитиСтатусБоргу()')
    diagram.render('interaction_diagram', format='png', view=True)

def create_collaboration_diagram():
    # Creating a chart object
    diagram = Digraph(comment='Collaboration Diagram')
    # Adding participants
    diagram.node('T', 'Trader')
    diagram.node('TS', 'Trading System')
    diagram.node('O', 'Order')
    diagram.node('SE', 'Stock Exchange')
    diagram.node('M', 'Module')
    # Adding interactions
    diagram.edge('T', 'TS', 'ЗапитПозики (сума, умови)')
    diagram.edge('TS', 'O', 'СтворитиБорг (сума, відсотки)')
    diagram.edge('O', 'SE', 'РезервуватиКошти()')
    diagram.edge('SE', 'T', 'НадатиПозиченіКошти()')
    diagram.edge('T', 'M', 'ПовернутиБорг (сума, відсотки)')
    diagram.edge('M', 'SE', 'ЗакритиБорг()')
    diagram.edge('SE', 'O', 'ОновитиСтатусБоргу()')
    # Chart output
    diagram.render('collaboration_diagram', format='png', view=True)

# Calling functions to create charts
create_interaction_diagram()
create_collaboration_diagram()
