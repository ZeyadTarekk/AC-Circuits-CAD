from sympy import cos,sin,symbols,solve,Eq,Symbol
import sympy
import math
Name_Of_NetList = input("Enter Name of file with extension : ")
def CompDict():
    with open(Name_Of_NetList,'r') as handler:
        componentDict = dict()
        handlerList = list(handler)
        for line in handlerList[1:]:
            lineStr = line.rstrip()
            componentDict[lineStr.split(" ")[1]] = lineStr.split(" ")[2:]
            componentDict[lineStr.split(" ")[1]].insert(0,lineStr.split(" ")[0])
        return componentDict,handlerList[0].split()[1]
def ReadFile():
    with open(Name_Of_NetList,'r') as handler:
        handlerList = list(handler)
        componentList = list()
        for line in handlerList:
            componentList.append(line.rstrip().split(" "))
    return componentList
def GetNodes():
    CompList = ReadFile()
    NodeDict = dict()
    NodeList = []
    for List in CompList[1:]:
        if List[2] not in NodeList:
            NodeList.append(List[2])
        if List[3] not in NodeList:
            NodeList.append(List[3])
    NodeList.sort()
    for node in NodeList:
        NodeDict[node] = []
        for List in CompList[1:]:
            if List[2] == node or List[3] == node:
                NodeDict[node].append((List[0],List[1]))
    return NodeDict
def FromPhasorToRec(r,theta):
    theta = theta*(math.pi/180)
    return complex(r*cos(theta),r*sin(theta))
def modifiCompdict():
    ComponentDict,omega = CompDict()
    for key in ComponentDict:
        if ComponentDict[key][0] == "vsrc" or ComponentDict[key][0] == "isrc":
            ComponentDict[key][3] = FromPhasorToRec(float(ComponentDict[key][3]),float(ComponentDict[key][4]))
            ComponentDict[key].pop()
        if ComponentDict[key][0] == "cap":
            ComponentDict[key][3] = 1/(float(ComponentDict[key][3])*float(omega)*1j)
        if ComponentDict[key][0] == "ind":
            ComponentDict[key][3] = (float(ComponentDict[key][3])*float(omega)*1j)
        if ComponentDict[key][0] == 'res':
            ComponentDict[key][3] = (float(ComponentDict[key][3]))
        if ComponentDict[key][0] == 'cccs' or ComponentDict[key][0] == 'ccvs':
            ComponentDict[key][3] = float(ComponentDict[key][6]) *((List_Of_Symboles[int(ComponentDict[key][4])]-List_Of_Symboles[int(ComponentDict[key][3])])/float(ComponentDict[ComponentDict[key][5]][3]))
            ComponentDict[key].pop()
            ComponentDict[key].pop()
            ComponentDict[key].pop()
        if ComponentDict[key][0] == 'vccs' or ComponentDict[key][0] == 'vcvs':
            ComponentDict[key][3] = float(ComponentDict[key][5]) *(List_Of_Symboles[int(ComponentDict[key][3])]-List_Of_Symboles[int(ComponentDict[key][4])])
            ComponentDict[key].pop()
            ComponentDict[key].pop()
    return ComponentDict
def Elements_Connected_ToNode(NodeName):
    connectedComp = GetNodes()[NodeName]
    typelist = []
    for TypeComp in connectedComp:
        typelist.append(TypeComp)
    return typelist
def Get_Second_node(node,nameOfComponent):
    ComponentDict = modifiCompdict()
    for component in ComponentDict.keys():
        if component == nameOfComponent :
            if ComponentDict[component][1] == node:
                return ComponentDict[component][2],False
            else:
                return ComponentDict[component][1],True
def Form_Equation_of_nodes_connected_tozero(node,nameOfSource,IsPos):
    CompDictionary = modifiCompdict()
    if IsPos:
        return Eq(List_Of_Symboles[int(node)]-CompDictionary[nameOfSource][3],0)
    else:
        return Eq(List_Of_Symboles[int(node)]+CompDictionary[nameOfSource][3],0)
    # SuperNodeEquation = SuperNode(node,SecNode)
    # List_Of_Equations.append((int(node),Eq(SuperNodeEquation)))

def Form_Equation_of_Sources_connected_toNode(SecNode,OriginalNode,nameOfSource,IsPos):
    CompDictionary = modifiCompdict()
    if IsPos:
        return Eq(List_Of_Symboles[int(SecNode)]-List_Of_Symboles[int(OriginalNode)],CompDictionary[nameOfSource][3])
    else:
        return Eq(List_Of_Symboles[int(OriginalNode)]-List_Of_Symboles[int(SecNode)],CompDictionary[nameOfSource][3])

def SuperNode(FirstNode,SecNode):
    dictOfNodes = GetNodes()
    CompDictionary = modifiCompdict()
    list_Of_Connected_To_Node = dictOfNodes[FirstNode]
    Equation = []
    for tuble in list_Of_Connected_To_Node:
        # print(tuble[0])
        SecondNode,IsPos = Get_Second_node(FirstNode,tuble[1])
        if tuble[0]!='isrc' and tuble[0]!='vsrc'and tuble[0]!='cccs':
            # print(tuble[0])
            print(List_Of_Symboles[int(FirstNode)],List_Of_Symboles[int(SecondNode)])
            Equation.append(List_Of_Symboles[int(FirstNode)]/CompDictionary[tuble[1]][3]-List_Of_Symboles[int(SecondNode)]/CompDictionary[tuble[1]][3])
        if (tuble[0] == 'isrc' or tuble[0] == 'cccs' or tuble[0] == 'vccs') and IsPos == False:
            Equation.append(-1*CompDictionary[tuble[1]][3])
        elif (tuble[0] == 'isrc' or tuble[0] == 'cccs' or tuble[0] == 'vccs') and IsPos == True:
            Equation.append(CompDictionary[tuble[1]][3])
        # print(Equation)
    
    list_Of_Connected_To_Node = dictOfNodes[SecNode]
    for tuble in list_Of_Connected_To_Node:
        # print(tuble[0])
        SecondNode,IsPos = Get_Second_node(SecNode,tuble[1])
        if tuble[0]!='isrc' and tuble[0]!='vsrc'and tuble[0]!='cccs':
            # print(tuble[0])
            print(List_Of_Symboles[int(SecNode)],List_Of_Symboles[int(SecondNode)])
            Equation.append(List_Of_Symboles[int(SecNode)]/CompDictionary[tuble[1]][3]-List_Of_Symboles[int(SecondNode)]/CompDictionary[tuble[1]][3])
        if (tuble[0] == 'isrc' or tuble[0] == 'cccs' or tuble[0] == 'vccs') and IsPos == False:
            Equation.append(-1*CompDictionary[tuble[1]][3])
        elif (tuble[0] == 'isrc' or tuble[0] == 'cccs' or tuble[0] == 'vccs') and IsPos == True:
            Equation.append(CompDictionary[tuble[1]][3])
        # print(Equation)
    return sum(Equation)
def Equation_from_Normal_nodes(Node):
    dictOfNodes = GetNodes()
    CompDictionary = modifiCompdict()
    list_Of_Connected_To_Node = dictOfNodes[Node]
    Equation = []
    for tuble in list_Of_Connected_To_Node:
        # print(tuble[0])
        SecondNode,IsPos = Get_Second_node(Node,tuble[1])
        if tuble[0]!='isrc' and tuble[0]!='vsrc'and tuble[0]!='cccs':
            # print(tuble[0])
            print(List_Of_Symboles[int(Node)],List_Of_Symboles[int(SecondNode)])
            Equation.append(List_Of_Symboles[int(Node)]/CompDictionary[tuble[1]][3]-List_Of_Symboles[int(SecondNode)]/CompDictionary[tuble[1]][3])
        if (tuble[0] == 'isrc' or tuble[0] == 'cccs' or tuble[0] == 'vccs') and IsPos == False:
            Equation.append(-1*CompDictionary[tuble[1]][3])
        elif (tuble[0] == 'isrc' or tuble[0] == 'cccs' or tuble[0] == 'vccs') and IsPos == True:
            Equation.append(CompDictionary[tuble[1]][3])
    return sum(Equation)
def Equations_Of_Nodes(node):
    #IsVScource = False
    for tubles in Elements_Connected_ToNode(node):
        if tubles[0] == 'vsrc' or tubles[0] == 'ccvs' or tubles[0] == 'vcvs':
            SecNode , IsPositive = Get_Second_node(node,tubles[1])
            ValueOfVoltagenode = Form_Equation_of_Sources_connected_toNode(SecNode,node,tubles[1],IsPositive)
            List_Of_Equations.append((int(node),ValueOfVoltagenode))
            List_Of_Super_Nodes.append(SecNode)
            List_Of_Super_Nodes.append(node)
            # SuperNodeEquation = SuperNode(node,SecNode)
            # List_Of_Equations.append((int(node),Eq(SuperNodeEquation)))
            return
    for tubles in Elements_Connected_ToNode(node):
        if tubles[0] == 'res' or tubles[0] == 'cap' or tubles[0] == 'ind' or tubles[0] == 'isrc' or tubles[0] == 'cccs' or tubles[0] =='vccs':
            SecNode , IsPositive = Get_Second_node(node,tubles[1])
            List_Of_Equations.append((int(node),Eq(Equation_from_Normal_nodes(node),0)))
            break
def Equations_Of_superNodes(node):
    #IsVScource = False
    for tubles in Elements_Connected_ToNode(node):
        if tubles[0] == 'vsrc' or tubles[0] == 'ccvs' or tubles[0] == 'vcvs':
            SecNode , IsPositive = Get_Second_node(node,tubles[1])
            ValueOfVoltagenode = Form_Equation_of_Sources_connected_toNode(SecNode,node,tubles[1],IsPositive)
            List_Of_Equations.append((int(node),ValueOfVoltagenode))
            List_Of_Super_Nodes.append(SecNode)
            List_Of_Super_Nodes.append(node)
            SuperNodeEquation = SuperNode(node,SecNode)
            List_Of_Equations.append((int(node),Eq(SuperNodeEquation)))
            return
    for tubles in Elements_Connected_ToNode(node):
        if tubles[0] == 'res' or tubles[0] == 'cap' or tubles[0] == 'ind' or tubles[0] == 'isrc' or tubles[0] == 'cccs' or tubles[0] =='vccs':
            SecNode , IsPositive = Get_Second_node(node,tubles[1])
            List_Of_Equations.append((int(node),Eq(Equation_from_Normal_nodes(node),0)))
            break
def From_Complex_To_phasor(Complex_number):
    magnitude = math.sqrt(Complex_number.real**2+Complex_number.imag**2)
    angle = 0
    if Complex_number.imag!=0 and Complex_number.real!=0:
        angle = math.degrees(math.atan(Complex_number.imag/Complex_number.real))
    return(magnitude,angle)

List_Of_Symboles = symbols("v0:10")

#v0 ,v1, v2, v3, v4, v5, v6, v7, v8, v9 = symbols("v0 v1 v2 v3 v4 v5 v6 v7 v8 v9") #nodes symbols
# Equations at all voltage sources
List_Of_Equations = []
for tubles in Elements_Connected_ToNode('0'):
    if tubles[0] == 'vsrc':
        SecNode , IsPositive = Get_Second_node('0',tubles[1])
        ValueOfVoltagenode = Form_Equation_of_nodes_connected_tozero(SecNode,tubles[1],IsPositive)
        List_Of_Equations.append((int(SecNode),ValueOfVoltagenode))  


List_Of_Super_Nodes = []
print(List_Of_Symboles)
List_Of_Equations.append((0,Eq(List_Of_Symboles[0])))
# print(CompDict())
# print(modifiCompdict())
# print(List_Of_Equations)
# print(List_Of_Super_Nodes)
for node in GetNodes():
    Equations_Of_Nodes(node)
# Equations_Of_Nodes('1')
# Equations_Of_Nodes('2')
# Equations_Of_Nodes('3')
#Equations_Of_Nodes('4')
#print(List_Of_Equations)
print(List_Of_Equations)
print(List_Of_Super_Nodes)
FinalEquations = []
for tuble in List_Of_Equations:
    FinalEquations.append(tuble[1])
print(FinalEquations)
voltSolution =solve( FinalEquations,  List_Of_Symboles)
print(voltSolution)

total_Sources=0
compD = CompDict()[0]
for comp in compD:
    if compD[comp][0] =='vsrc' or compD[comp][0] == 'vcvs' or compD[comp][0] == 'ccvs':
        total_Sources = total_Sources+1
dict_of_node =GetNodes()
num = 0

for node in dict_of_node:
    num = 0
    for Tuble in dict_of_node[node]:
        if Tuble[0] == 'vsrc' or Tuble[0] == 'ccvs' or Tuble[0] =='vcvs':
            num = num + 1
    if num >=2 :
        print(num)
        break
print(num)
if num >=2 or total_Sources==1:
    dict_of_currents = dict()
    component_Dictionary =modifiCompdict()
    original_CompDict = CompDict()[0]
    for component in component_Dictionary:
        if component_Dictionary[component][0] == 'res' or component_Dictionary[component][0] == 'cap' or component_Dictionary[component][0] == 'ind':
            node1 = component_Dictionary[component][1]
            node2 = component_Dictionary[component][2]
            Symbol1 = List_Of_Symboles[int(node1)]
            Symbol2 = List_Of_Symboles[int(node2)]
            dict_of_currents[component] = (complex(voltSolution[Symbol1])-complex(voltSolution[Symbol2]))/component_Dictionary[component][3]
        if component_Dictionary[component][0] == 'isrc':
            dict_of_currents[component] = component_Dictionary[component][3]
        if component_Dictionary[component][0] == 'cccs'or component_Dictionary[component][0] == 'vccs':
            EquationOfSource = component_Dictionary[component][3]
            #print(EquationOfSource)
            node1 = original_CompDict[component][3]
            node2 = original_CompDict[component][4]
            Symbol1 = List_Of_Symboles[int(node1)]
            Symbol2 = List_Of_Symboles[int(node2)]
            print(voltSolution[Symbol1],voltSolution[Symbol2])
            #print("sadasdsadasssadshjcbdsjc ",EquationOfSource.subs([(Symbol1 , voltSolution[Symbol1]) , ( Symbol2 , voltSolution[Symbol2])]))
            dict_of_currents[component] = EquationOfSource.subs([(Symbol1 , voltSolution[Symbol1]) , ( Symbol2 , voltSolution[Symbol2])])
    #print(dict_of_currents)
    print("*********Note: Two Connected voltage Sources*********")
    with open("output.txt",'w') as outfile:
        outfile.write("*****Voltage values*****\n\n")
        for volt in voltSolution:
            outfile.write(str(volt))
            outfile.write("\t")
            outfile.write(str(voltSolution[volt]))
            outfile.write("\t")
            outfile.write(str(From_Complex_To_phasor(complex(voltSolution[volt]))[0]))
            outfile.write("\t")
            outfile.write(str(From_Complex_To_phasor(complex(voltSolution[volt]))[1]))
            outfile.write('\n')
        outfile.write('\n')
        outfile.write("*****Current values*****\n\n")
        for compName in dict_of_currents:
            outfile.write(str(compName))
            outfile.write('\t')
            outfile.write(str(dict_of_currents[compName]))
            outfile.write('\t')
            outfile.write(str(From_Complex_To_phasor(complex(dict_of_currents[compName]))[0]))
            outfile.write('\t')
            outfile.write(str(From_Complex_To_phasor(complex(dict_of_currents[compName]))[1]))
            outfile.write('\n')
        outfile.write('\n*****End of values*****')
        exit()


if List_Of_Super_Nodes !=[]:
    Equations_Of_superNodes(List_Of_Super_Nodes[0])
    for tuble in List_Of_Equations:
        FinalEquations.append(tuble[1])
    print(FinalEquations)
    voltSolution =solve( FinalEquations, List_Of_Symboles)
    print(voltSolution)

dict_of_currents = dict()
component_Dictionary =modifiCompdict()
original_CompDict = CompDict()[0]
print(original_CompDict)
for component in component_Dictionary:
    if component_Dictionary[component][0] == 'res' or component_Dictionary[component][0] == 'cap' or component_Dictionary[component][0] == 'ind':
        node1 = component_Dictionary[component][1]
        node2 = component_Dictionary[component][2]
        Symbol1 = List_Of_Symboles[int(node1)]
        Symbol2 = List_Of_Symboles[int(node2)]
        dict_of_currents[component] = (complex(voltSolution[Symbol1])-complex(voltSolution[Symbol2]))/component_Dictionary[component][3]
    if component_Dictionary[component][0] == 'isrc':
        dict_of_currents[component] = component_Dictionary[component][3]
    if component_Dictionary[component][0] == 'cccs'or component_Dictionary[component][0] == 'vccs':
        EquationOfSource = component_Dictionary[component][3]
        #print(EquationOfSource)
        node1 = original_CompDict[component][3]
        node2 = original_CompDict[component][4]
        Symbol1 = List_Of_Symboles[int(node1)]
        Symbol2 = List_Of_Symboles[int(node2)]
        print(voltSolution[Symbol1],voltSolution[Symbol2])
        #print("sadasdsadasssadshjcbdsjc ",EquationOfSource.subs([(Symbol1 , voltSolution[Symbol1]) , ( Symbol2 , voltSolution[Symbol2])]))
        dict_of_currents[component] = EquationOfSource.subs([(Symbol1 , voltSolution[Symbol1]) , ( Symbol2 , voltSolution[Symbol2])])
#print(dict_of_currents)

with open("output.txt",'w') as outfile:
    print("*********Note: NO Connected voltage Sources*********")
    outfile.write("*****Voltage values*****\n\n")
    for volt in voltSolution:
        outfile.write(str(volt))
        outfile.write("\t")
        outfile.write(str(voltSolution[volt]))
        outfile.write("\t")
        outfile.write(str(From_Complex_To_phasor(complex(voltSolution[volt]))[0]))
        outfile.write("\t")
        outfile.write(str(From_Complex_To_phasor(complex(voltSolution[volt]))[1]))
        outfile.write('\n')
    outfile.write('\n')
    outfile.write("*****Current values*****\n\n")
    for compName in dict_of_currents:
        outfile.write(str(compName))
        outfile.write('\t')
        outfile.write(str(dict_of_currents[compName]))
        outfile.write('\t')
        outfile.write(str(From_Complex_To_phasor(complex(dict_of_currents[compName]))[0]))
        outfile.write('\t')
        outfile.write(str(From_Complex_To_phasor(complex(dict_of_currents[compName]))[1]))
        outfile.write('\n')
    outfile.write('\n*****End of values*****')
print(modifiCompdict())
print(CompDict())
# Voltage = [] netlist5.txt
# NodeDictionary = GetNodes()
# ComponentDictionary,omega = CompDict()
# ComponentDictionary = modifiCompdict()
# ListOfuntakenNodes = ['1','2','3','4','5','6','7','8','9']
# DictOfNodes = dict()
# DictOfNodes['0'] = 0
# Result_Of_Voltages = []
# for tubles in Elements_Connected_ToNode('0'): 
#     if tubles[0] == 'vsrc':
#         SecNode , IsPsitive = Get_Second_node('0',tubles[1])
#         ValueOfVoltagenode = Form_Equation_of_nodes_connected_tozero(SecNode,tubles[1])
#         Voltage.append((int(SecNode),ValueOfVoltagenode)) 
#         # Result_Of_Voltages.append((SecNode,ValueOfVoltagenode))
# print(Voltage)


# #print(Result_Of_Voltages)
# #print(tubles[0])    
# #DictOfNodes[]
# #print(Elements_Connected_ToNode('0'))
# #print(Elements_Connected_ToNode('0'))

# #secNode,postive = Get_Second_node('0',Elements_Connected_ToNode('0')[0][1])
# #print(Form_Equation_of_nodes_connected_tozero('1','v1'))
# #print(secNode,postive)

# # x,y = symbols('x y')
# # eq1 = Eq(2*x+y-2)
# # eq2 = Eq(x+y-1)
# # solution = solve((eq1,eq2),(x,y))
# # a = math.pi/6
# # print(FromPhasorToRec(1,a))



