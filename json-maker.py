import re
jason=""

filename=input("enter the name of your file:")
file_object=open(filename,"r",encoding="utf-8")
objects=file_object.read()
main=list(objects.split("\n"))
def error():
    print("please enter an apropriate file")
    exit()
def args_find(x):
    b=[]
    counter=0
    arg_save=""
    for i in x:
        if i=="(":
            counter+=1
        elif i==")":
            counter-=1
        elif i=="," and counter==0:
            b.append(arg_save)
            arg_save=""
        else:
            arg_save+=i
    b.append(arg_save)
    return b
def first_line(x):
    jason=""
    i=0
    height_start=0
    height_end=0
    width_start=0
    width_end=0
    while i<len(x)-1:
        if x[i]==" ":
            while x[i]==" ":
                i+=1
            height_start=i
            while x[i]!=" ":
                i+=1
            height_end=i-1
            while x[i]==" ":
                i+=1
            width_start=i
            while x[i]!=" " or i!=len(x)-1:
                i+=1
            width_end=i
        else:
            while x[i]!=" ":
                i+=1
            height_end=i-1
            while x[i]==" ":
                i+=1
            width_start=i
            ######################
            while x[i]!=" " and i!=len(x)-1:
                i+=1
            width_end=i
            ##########################
    height=x[height_start:height_end+1]
    width=x[width_start:width_end+1]
    jason='"height":'+height+','+'"width":'+width+','
    return jason
def expression_check(exp):
    exp=str(exp)
    counter=0
    match="+-*%"
    z=")("
    for i in str(exp) :
        if i=="(":
            counter+=1
        elif i==")":
            counter-=1
        if i in match and counter==0:
            return math(exp)
    for j in str(exp):    
        if j in z:
            return funcname(exp)
    return exp
def math(exp):
    jason=""
    k=0
    matches=")("
    for i in range (len(exp)):
        if exp[i]=="+" or exp[i]=="-" or exp[i]=="%" or exp[i]=="*" or exp[i]=="/":
            k=i
            break
    for j in exp[:k]:
        if j in matches:
            A=funcname(exp[:k])
            if exp[k+1:].find("+")!=-1 or exp[k+1:].find("-")!=-1 or exp[k+1:].find("*")!=-1 or exp[k+1:].find("%")!=-1 or exp[k+1:].find("/")!=-1:
                jason+='"type":'+'"'+str(exp[k])+'"'+','+'"A":'+'{'+str(A)+'}'+','+'"B":{'+math(exp[k+1:])+'}'
                return jason
            else:
                for f in exp[k+1:]:
                    if f in matches:
                        B=funcname(exp[k+1:])
                        jason+='"type":'+'"'+str(exp[k])+'"'+','+'"A":'+'{'+str(A)+'}'+','+'"B":'+'{'+str(B)+'}'
                        return jason
                jason+='"type":'+'"'+str(exp[k])+'"'+','+'"A":'+'{'+str(A)+'}'+','+'"B":'+'"'+str(exp[k+1:])+'"'
                return jason
    if exp[k+1:].find("+")!=-1 or exp[k+1:].find("-")!=-1 or exp[k+1:].find("*")!=-1 or exp[k+1:].find("%")!=-1 or exp[k+1:].find("/")!=-1:
        jason+='"type":'+'"'+str(exp[k])+'"'+','+'"A":'+'"'+str(exp[:k])+'"'+','+'"B":{'+math(exp[k+1:])+'}'
    else:
        for f in exp[k+1:]:
            if f in matches:
                B=funcname(exp[k+1:])
                jason+='"type":'+'"'+str(exp[k])+'"'+','+'"A":'+'"'+str(exp[:k])+'"'+','+'"B":'+'{'+str(B)+'}'
                return jason
        jason+='"type":'+'"'+str(exp[k])+'"'+','+'"A":'+'"'+str(exp[:k])+'"'+','+'"B":'+'"'+str(exp[k+1:])+'"'
        return jason
    return jason    

def funcname(x):
    global defined_funcs
    global p
    d=0
    jason=""
    x=str(x)
    i=0
    counter=0
    end_arg=0
    find_func=0
    args_num=0
    args_str=""
    exp1="+-*/%"
    exp2=")("
    while x[i]==" " :
        i+=1
    start_namefunc=i
    while x[i]!="(" and  x[i]!=" " and i<len(x)-1:
        i+=1
    end_namefunc=i
    k=x.find("(")
    i=k
    i+=1
    counter=1
    for j in range(i,len(x)):
        if x[j]=="(":
            counter+=1
            if counter==0:
                end_arg=j
                break
        if x[j]==")":
            counter-=1 
            if counter==0:
                end_arg=j
                break
    args=x[k+1:end_arg]
    name_func=str(x[start_namefunc:end_namefunc])
    if name_func in defined_funcs:
        for l in range(len(defined_funcs)):
            if defined_funcs[l]==name_func:
                find_func=l
                break
    elif name_func not in defined_funcs:
        d=p
        d+=1
        return "error in line "+str(d) +":please define the function named:" + name_func+" without using it's name in the definition before calling it"
    args=args_find(args)
    for i in args:
        check=True
        for j in i:
            if j in exp1 or j in exp2:
                check=False
                break
        if check:
            args_str+=','+'"'+expression_check(i)+'"'
            args_num+=1
        else:
            args_str+=','+'{'+expression_check(i)+'}'   
            args_num+=1
    if args_num!=defined_funcs[l+1]:
        d=p
        d+=1
        return "error in line"+str(d)+":please check the number of args in the function named:"+name_func  
    args_str=args_str[1:]
    jason='"type":"function call"'+","+'"function name":'+'"'+name_func+'"'+','+'"args":'+' '+'['+args_str+']'
    return jason
def func(x):
    global defined_funcs
    global p
    jason=""
    x=str(x)
    i=4
    d=0
    counter=0
    end_arg=0
    args_str=""
    args_num=0
    exp1="+-*/%"
    exp2=")("
    while x[i]==" " :
        i+=1
    start_namefunc=i
    while x[i]!="(" and x[i]!=" " and i<len(x)-1:
        i+=1
    end_namefunc=i
    k=x.find("(")
    i=k
    i+=1
    counter=1
    for j in range(i,len(x)):
        if x[j]=="(":
            counter+=1
            if counter==0:
                end_arg=j
                break
        if x[j]==")":
            counter-=1 
            if counter==0:
                end_arg=j
                break
    args=x[k+1:end_arg]
    name_func=str(x[start_namefunc:end_namefunc])
    args=args_find(args)
    for i in args:
        check=True
        for j in i:
            if j in exp1 or j in exp2:
                check=False
                break
        if check:
            args_str+=','+'"'+expression_check(i)+'"'
            args_num+=1
        else:
            args_str+=','+'{'+expression_check(i)+'}' 
            args_num+=1    
    args_str=args_str[1:]
    if args_str=='""':
        args_str=''
    f=end_arg
    if f==len(x)-1:
        d=p
        d+=1
        defined_funcs.append(name_func)
        defined_funcs.append(args_num)
        return "error in line"+str(d)+":please enter an expression for the function named:"+name_func
    else:
        f+=1
    if x[f]==" " and f==len(x)-1:
        d=p
        d+=1
        defined_funcs.append(name_func)
        defined_funcs.append(args_num)
        return "error in line"+str(d)+":please enter an expression for the function named:"+name_func
    elif x[f]==" " and f<len(x)-1:
        while x[f]==" " and f<len(x)-1:
            f+=1
            if f==len(x)-1:
                d=p
                d+=1
                defined_funcs.append(name_func)
                defined_funcs.append(args_num)
                return "error in line "+str(d)+":please enter an expression for the function named:"+name_func
    expression_func=x[end_arg+1:]
    if expression_func=='':
        d=p
        d+=1
        defined_funcs.append(name_func)
        defined_funcs.append(args_num)
        return "error in line"+str(d)+":please enter an expression for the function named:"+name_func
    if name_func=="main" and args_str!='':
        defined_funcs.append(name_func)
        defined_funcs.append(args_num)
        d=p
        d+=1
        return "error in line"+str(d)+": your main function can't have any arg"
    else:
        if name_func in defined_funcs:
            d=p
            d+=1
            return "error in line"+str(d)+":you can not define the function named :"+name_func+" more than one time"
        else:
            defined_funcs.append(name_func)
            defined_funcs.append(args_num)
        jason+='"type":"function definition"'+","+'"function name":'+'"'+name_func+'"'+','+'"args":'+'['+args_str+']'+','+'"expression":'+'{'+expression_check(expression_func)+'}'
        return jason
def recursivefunc(x,l2,l3):
    global defined_funcs
    jason="" 
    x=str(x)
    i=5
    start_namefunc=0
    end_namefunc=0
    start_base_exp=0
    end_base_exp=0
    end_val_name=0
    start_exp=0
    end_exp=0
    base_exp=0
    counter=0
    end_arg=0
    main_args=0
    args_str=""
    args_num=0
    d=0
    exp1="+-*/%"
    exp2=")("
    while x[i]==" " :
        i+=1
    start_namefunc=i
    while x[i]!="(" and x[i]!=" " and i<len(x)-1:
        i+=1
    end_namefunc=i
    k=x.find("(")
    i=k
    i+=1
    name_func=x[start_namefunc:end_namefunc]
    counter=1
    for j in range(i,len(x)):
        if x[j]=="(":
            counter+=1
            if counter==0:
                end_arg=j
                break
        if x[j]==")":
            counter-=1 
            if counter==0:
                end_arg=j
                break
    args=x[k+1:end_arg]
    args=args_find(args)
    main_args=args
    args=args[:len(args)-1]
    for i in args:
        check=True
        for j in i:
            if j in exp1 or j in exp2:
                check=False
                break
        if check:
            args_str+=','+'"'+expression_check(i)+'"'
            args_num+=1
        else:
            args_str+=','+'{'+expression_check(i)+'}' 
            args_num+=1  
    args_num+=1  
    args_str=args_str[1:]
    defined_funcs.append(name_func)
    defined_funcs.append(args_num)
    l2=str(l2)
    j=5   
    while l2[j]==" ":
        j+=1
    start_base_exp=j
    while j!=len(l2)-1:
        j+=1
    end_base_exp=j
    base_exp=l2[start_base_exp:end_base_exp+1]
    k=4
    l3=str(l3)
    while l3[k]!=" ":
        k+=1
    end_val_name=k-1
    while k==" ":
        k+=1
    start_exp=k
    while k!=len(l3)-1:
        k+=1
    end_exp=k
    val_name=l3[4:end_val_name+1]
    exp=l3[start_exp:end_exp+1]
    g=expression_check(exp)
    if l2[4]!="0":
        d=p+2
        return "error in line"+str(d)+":expected '0' before base expression of the recursive function named:"+name_func
    if l2[5]!=" ":
        d=p+2
        return "error in line"+str(d)+":expected a space between '0' and base expression of the recursive functon named:"+name_func
    if l2[:4]!="    ":
        d=p+2
        return "error in line"+str(d)+":expected a tab before '0' in the base expression's line of the recursive function named:"+name_func
    if l3[4]==" ":
        d=p+3
        return "error in line"+str(d)+":please enter a recursive value name for the recursive function named:"+name_func
    if l3[end_val_name+1]!=" ":
        d=p+3
        return "error in line"+str(d)+":expected a space between recursive value name and recursive expression of the recursive function named:"+name_func
    if l3[:4]!="    ":
        return "error in line"+str(d)+":expected a tab befor the recursive value name of the recusive function named:"+name_func
    if name_func in defined_funcs:
        d=p+1
        return "error in line"+str(d)+":you can not define the function named :"+name_func+" more than one time"

    jason='"type":"recursive function definition"'+','+'"function name":'+'"'+name_func+'"'+','+'"args":'+' '+'['+args_str+']'+','+'"recursive arg":'+'"'+main_args[len(main_args)-1]+'"'+','+'"base expression":'+'{'+expression_check(base_exp)+'}'+','+'"resursive expression":'+'{'+'"resursuive value name":'+'"'+val_name+'"'+','+'"expression":'+'{'+g+'}'+'}'
    return jason
################################################################################
jason=""
p=0
defined_funcs=[]
def get(x):
    global jason
    global defined_funcs
    global p
    d=0
    g=first_line(x[p])
    p+=1
    while p < len(x):
        if str(x[p][:5])=="func ":
            jason+=','+'{'+func(str(x[p]))+'}'
            p+=1
        elif str(x[p][:6])=="rfunc ":
            jason+=','+'{'+recursivefunc(str(x[p]),str(x[p+1]),str(x[p+2]))+'}'
            p+=3
        else:
            return "error:you need to use func or rfunc in the start of every single line"
    jason='{'+g+' "functions": '+'['+jason[1:]+']}'
    if "drawPoint" in defined_funcs:
        for i in range(len(defined_funcs)):
            if defined_funcs[i]=="drawPoint":
                d=i+1
                break
        return "error in line"+str(d)+":drawPoint is a built in function and you can not define it again"
    elif "drawLine" in defined_funcs:
        for i in range(len(defined_funcs)):
            if defined_funcs[i]=="drawLine":
                d=i+1
                break
        return "error in line "+str(d)+":drawLine is a built in function and you can not define it again"
    elif "drawCircle" in defined_funcs:
        for i in range(len(defined_funcs)):
            if defined_funcs[i]=="drawCircle":
                d=i+1
                break
        return "error in line"+str(d)+":drawCircle is a built in function and you can not define it again"
    elif "if" in defined_funcs:
        for i in range(len(defined_funcs)):
            if defined_funcs[i]=="if":
                d=i+1
                break
        return "error in line"+str(d)+":if is a built in function and you can not define it again"
    elif defined_funcs[len(defined_funcs)-2]!="main":
        return "error:you need to have a function named 'main' in the last line of your input"
    for i in range (len(defined_funcs)-2):
        if defined_funcs[i]=="main":
            d=i+1
            return "error in line"+str(d)+":you are only alowed to have a function named 'main' in the last line of your input"
    return  jason
# x=["100 200","rfunc narges(b,v) ","    0 2+3","    rc 2+3","func main() a+b"]
# print(get(x))
print(get(main))



    






    

