#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 13 18:09:03 2020

@author: keko
"""
import pandas as pd
import random
import os

def CSV():
    nome="sim_"+traceName+".csv"
    apoio=1
    existe=os.path.exists(nome)
    while existe==True:
        nome="sim_"+traceName+"_"+str(apoio)+".csv"
        apoio+=1
        existe=os.path.exists(nome)
    Result= open(nome,"w+")
    memoriatotal=sum(infcache["KBytes total"])
    acessos=len(resultados)
    Hits=sum(resultados['Resultado']=='hit')
    Miss=sum(resultados['Resultado']=='miss')
    pHits=round((Hits/acessos)*100,2) if acessos>0 else 0
    EscritasemWT=sum(resultados['Escreve se WT']==True)
    EscritasemWB=sum(resultados['Escreve se WB']==True)
    acessosL=len(resultados[resultados["Instrucao"]=="L"])
    HitsL=sum(resultados[resultados["Instrucao"]=="L"]["Resultado"]=="hit")
    MissL=sum(resultados[resultados["Instrucao"]=="L"]["Resultado"]=="miss")
    pHitsL=round((HitsL/acessosL)*100,2) if acessosL>0 else 0
    acessosS=len(resultados[resultados["Instrucao"]=="S"])
    HitsS=sum(resultados[resultados["Instrucao"]=="S"]["Resultado"]=="hit")
    MissS=sum(resultados[resultados["Instrucao"]=="S"]["Resultado"]=="miss")
    pHitsS=round((HitsS/acessosS)*100,2) if acessosS>0 else 0
    s=infcache.to_csv()
    Result.write(s)
    s="\n Memoria total ,"+str(memoriatotal)+"\n Total de acessos ,"+str(acessos)+"\n Hits ,"+str(Hits)+"\n Mises ,"+str(Miss)+"\n Percentual de acerto,"+str(pHits)+",%"+" \n Escritas em WB ,"+str(EscritasemWB)+" \n Escritas em WT ,"+str(EscritasemWT)+"\n Acessos leitura ,"+str(acessosL)+"\n Hits leitura ,"+str(HitsL)+"\n Miss leitura ,"+str(MissL)+"\n Percentual de acerto leitura ,"+str(pHitsL)+",%"+"\n Acessos escrita ,"+str(acessosS)+"\n Hits escrita ,"+str(HitsS)+"\n Miss escrita ,"+str(MissS)+"\n Percentual de acerto escrita ,"+str(pHitsS)+",%"
    print(s)
    Result.write(s)
    if infcache.loc[0,'Nivel']!='LI':#se não tem cache de instruções mostra acessos de instrução
        acessosI=len(resultados[resultados["Instrucao"]=="I"])
        HitsI=sum(resultados[resultados["Instrucao"]=="I"]["Resultado"]=="hit")
        MissI=sum(resultados[resultados["Instrucao"]=="I"]["Resultado"]=="miss")
        pHitsI=round((HitsI/acessosI)*100,2) if acessosI>0 else 0
        s="\n Total de acessos instrução,"+str(acessosI)+"\n Hits instrução,"+str(HitsI)+"\n Mises instrução,"+str(MissI)+"\n Percentual de acerto instrução,"+str(pHitsI)+",%"
        print(s)
        Result.write(s)
    for i in range(len(infcache)):
        nivel=infcache.loc[i,'Nivel']
        LI=resultados[resultados["Nivel"]==nivel]
        acessos=len(LI)
        Hits=sum(LI['Resultado']=='hit')
        Miss=sum(LI['Resultado']=='miss')
        pHits=round((Hits/acessos)*100,2) if acessos>0 else 0
        EscritasemWT=sum(LI['Escreve se WT']==True)
        EscritasemWB=sum(LI['Escreve se WB']==True)
        acessosL=len(LI[LI["Instrucao"]=="L"])
        HitsL=sum(LI[LI["Instrucao"]=="L"]["Resultado"]=="hit")
        MissL=sum(LI[LI["Instrucao"]=="L"]["Resultado"]=="miss")
        pHistL=round((HitsL/acessosL)*100,2) if acessosL>0 else 0
        acessosS=len(LI[LI["Instrucao"]=="S"])
        HitsS=sum(LI[LI["Instrucao"]=="S"]["Resultado"]=="hit")
        MissS=sum(LI[LI["Instrucao"]=="S"]["Resultado"]=="miss")
        pHistS=round((HitsS/acessosS)*100,2) if acessosS>0 else 0
        s="\n                 Cache"+nivel+"\n Total de acessos,"+str(acessos)+"\n Hits ,"+str(Hits)+"\n Mises ,"+str(Miss)+"\n Percentual de acerto,"+str(pHits)+",%"+" \n Escritas em WB ,"+str(EscritasemWB)+" \n Escritas em WT ,"+str(EscritasemWT)+"\n Acessos leitura ,"+str(acessosL)+"\n Hits leitura ,"+str(HitsL)+"\n Miss leitura ,"+str(MissL)+"\n Percentual de acerto leitura ,"+str(pHistL)+",%"+"\n Acessos escrita ,"+str(acessosS)+"\n Hits escrita ,"+str(HitsS)+"\n Miss escrita ,"+str(MissS)+"\n Percentual de acerto escrita ,"+str(pHistS)+",%"
        print(s)
        Result.write(s)
    for i in range(len(infcache)):
        nivel=infcache.loc[i,'Nivel']
        LI=resultados[resultados["Nivel"]==nivel]
        hitSet=pd.DataFrame(LI[LI["Resultado"]=="hit"]["Set"].value_counts())
        hitSet.columns=["hits por Set"]
        missSet=pd.DataFrame(LI[LI["Resultado"]=="miss"]["Set"].value_counts())
        missSet.columns=["miss por Set"]
        totalSet=pd.DataFrame(LI["Set"].value_counts())
        totalSet.columns=["Acessos por Set"]
        totalSet=totalSet.join([hitSet,missSet])
        totalSet['% hit por set'] = round((totalSet['hits por Set']/totalSet['Acessos por Set'])*100,2)
        totalSet=totalSet.sort_index()
        Result.write("\n    Acessos por Set cache"+nivel+"\n")      
        s=totalSet.to_csv()
        Result.write(s)
        LIL=LI[LI["Instrucao"]=="L"]
        hitSetL=pd.DataFrame(LIL[LIL["Resultado"]=="hit"]["Set"].value_counts())
        hitSetL.columns=["hits por Set Leitura"]
        missSetL=pd.DataFrame(LIL[LIL["Resultado"]=="miss"]["Set"].value_counts())
        missSetL.columns=["miss por Set Leitura"]
        totalSetL=pd.DataFrame(LIL["Set"].value_counts())
        totalSetL.columns=["Acessos por Set Leitura"]
        totalSetL=totalSetL.join([hitSetL,missSetL])
        totalSetL['% hit por set'] = round((totalSetL['hits por Set Leitura']/totalSetL['Acessos por Set Leitura'])*100,2)
        totalSetL=totalSetL.sort_index()
        s=totalSetL.to_csv()
        Result.write(s)
        LIS=LI[LI["Instrucao"]=="S"]
        hitSetS=pd.DataFrame(LIS[LIS["Resultado"]=="hit"]["Set"].value_counts())
        hitSetS.columns=["hits por Set Escrita"]
        missSetS=pd.DataFrame(LIS[LIS["Resultado"]=="miss"]["Set"].value_counts())
        missSetS.columns=["miss por Set Escrita"]
        totalSetS=pd.DataFrame(LIS["Set"].value_counts())
        totalSetS.columns=["Acessos por Set Escrita"]
        totalSetS=totalSetS.join([hitSetS,missSetS])
        totalSetS['% hit por set'] = round((totalSetS['hits por Set Escrita']/totalSetS['Acessos por Set Escrita'])*100,2)
        totalSetS=totalSetS.sort_index()
        s=totalSetS.to_csv()
        Result.write(s)
    return resultados

def printa(cache):
    for i in range(len(cache)):
        texto=str(cache[i])
        if iterativo==1:
            Saida.write(texto+"\n")
        else:
            print(texto)
        
def atualizaposicao(vetor,Vias,posicao):
    retorno=vetor
    #print(posicao)
    if retorno[-Vias]!=posicao:#se a posição mais recente é diferente da anterior atualiza
        i=1
        while i<Vias:
            if retorno[-i]==posicao:
                while i<Vias:        
                    retorno[-i]=retorno[-1-i]
                    i+=1
            i+=1
        retorno[-Vias]=posicao
    return retorno

def cachecreate(nivel,Ilinhas,Ibytes,Vias,Politicasub):
    Linhas=int(2**Ilinhas)
    Estrutura=[1]+[0]+['null']
    cache=[]
    for i in range(Vias-1):
        Estrutura=Estrutura+[0]+['null']
    if Politicasub=="LRU" or Politicasub=="MRU":
        for i in range(Vias):
            Estrutura=Estrutura+[3+(Vias-1-i)*2]
    for i in range(Linhas):
        cache.append([i]+Estrutura)
    infcache.loc[len(infcache)]=[nivel]+[Linhas]+[Vias]+[Ibytes]+[Ilinhas]+[2**Ibytes]+[((2**Ibytes)*Vias)]+[(((2**Ibytes)*Vias*Linhas)/1000)]+[Politicasub]
    return cache

def acessacache(Offset,Set,Tag,instrucao,endereco,nBytes,cache,Nivel,Vias,Politicasub):
    retorno="miss"
    stallWT=False
    stallWB=False
    posicao=3
    for i in range(Vias):
        cTag=cache[Set][posicao]
        #print(cTag,Tag)
        if cTag==Tag:
            retorno='hit'
            if instrucao=="S":
                stallWT=True
                if iterativo==1:
                    Saida.write("É uma instrução de escrita em WT manda para write buffer\n")
                if cache[Set][posicao-1]==0:#checa dirt
                    cache[Set][posicao-1]=1 #atualiza dirt  
                    if iterativo==1:
                        Saida.write("Em WB não atualizou o nivel superior de memória o bloco fica sujo\n")
                elif iterativo==1:
                    Saida.write("Em WB o bloco já estava sujo não precisa atualizar\n")
            if Politicasub=="LRU" or Politicasub=="MRU":
                cache[Set]=atualizaposicao(cache[Set],Vias,posicao)
            break
        posicao+=2#Para buscar na proxíma via
        
    if retorno=="miss" and Vias>1:
        if Politicasub=="Random":
            if cache[Set][1]==((Vias*2)+1):#se ja esta preenchida a cache busca a usada mais recentemente
                numero=random.randrange(1,Vias+1,1)
                if iterativo==1:
                    Saida.write("A politica de substituição é substituir uma via aleatoriamente a via sorteada foi "+str(numero)+"\n")
                posicao=(numero*2)+1
                cache[Set][posicao]=Tag#buscou no nivel de memoria superior
            else:#logo apos o boot para preencher todas as vias da cache
                posicao=cache[Set][1]+2
                if iterativo==1:
                    Saida.write("A linha está incompleta então vai acessar a via "+str(int(((posicao-1)/2)))+"\n")
                cache[Set][posicao]=Tag#buscou no nivel de memoria superior
                cache[Set][1]=posicao
        
        elif Politicasub=="MRU":
            if cache[Set][1]==((Vias*2)+1):#se ja esta preenchida a cache busca a usada mais recentemente
                posicao=cache[Set][((Vias*2)+2)]
                if iterativo==1:
                    Saida.write("A politica de substituição é substituir a via acessada mais recentemente que foi a "+str(int(((posicao-1)/2)))+"\n")
                cache[Set][posicao]=Tag#buscou no nivel de memoria superior
            else:#logo apos o boot para preencher todas as vias da cache
                posicao=cache[Set][1]+2
                if iterativo==1:
                    Saida.write("A linha está incompleta então vai acessar a via "+str(int(((posicao-1)/2)))+"\n")
                cache[Set][posicao]=Tag#buscou no nivel de memoria superior
                cache[Set][1]=posicao
                atualizaposicao(cache[Set],Vias,posicao)
    
        elif Politicasub=="LRU":
            if cache[Set][1]==((Vias*2)+1):#se ja esta preenchida a cache busca a usada mais recentemente
                posicao=cache[Set][((Vias*3)+1)]
                if iterativo==1:
                    Saida.write("A politica de substituição é substituir a via acessada a mais tempo, que foi a "+str(int(((posicao-1)/2)))+"\n")
                cache[Set][posicao]=Tag#buscou no nivel de memoria superior
                atualizaposicao(cache[Set],Vias,posicao)
            else:#logo apos o boot para preencher todas as vias da cache
                posicao=cache[Set][1]+2
                if iterativo==1:
                    Saida.write("A linha está incompleta então vai acessar via "+str(int(((posicao-1)/2)))+"\n")
                cache[Set][posicao]=Tag#buscou no nivel de memoria superior
                cache[Set][1]=posicao
                cache[Set]=atualizaposicao(cache[Set],Vias,posicao)
        
        else:#Se  não definir politica é usda fifo por padrão
            posicao=cache[Set][1]+2
            if iterativo==1:
                    Saida.write("A politica de substituição é Uma fila, a via agora é a "+str(int(((posicao-1)/2)))+"\n")
            cache[Set][posicao]=Tag#buscou no nivel de memoria superior
            cache[Set][1]=1 if posicao==((Vias*2)+1) else posicao
        
        if cache[Set][posicao-1]==1:#checa dirt
            stallWB=True
            cache[Set][posicao-1]=0 #atualiza dirt
            if iterativo==1:
                Saida.write("O bloco substituido estava sujo em WB manda para write bufer o endereço substituido\n")
        if instrucao=="S":
            stallWT=True
            if iterativo==1:
                Saida.write("É uma instrução de escrita em WT manda para write buffer\n")
            if cache[Set][posicao-1]==0:#checa dirt
                cache[Set][posicao-1]=1 #atualiza dirt                   
                if iterativo==1:
                    Saida.write("Em WB não atualizou o nivel superior de memória o bloco fica sujo\n")
            else:
                cache[Set][posicao-1]=1 #atualiza dirt                   
    
    elif retorno=="miss" and Vias==1:#para mapeamento direto
        cache[Set][3]=Tag
        posicao=3
        if cache[Set][2]==1:#se o bloco substituido estava sujo na politica wb ele precisa ser escrito na memória de nivel superior
            stallWB=True
            cache[Set][2]=0
            if iterativo==1:
                Saida.write("O bloco substituido estava sujo em WB manda para write bufer o endereço substituido\n")                    
        if instrucao=="S":
            stallWT=True
            if iterativo==1:
                Saida.write("É uma instrução de escrita em WT manda para write buffer\n")
            if cache[Set][2]==0:
                cache[Set][2]=1
                if iterativo==1:
                    Saida.write("Em WB não atualizou o nivel superior de memória o bloco fica sujo\n")
            
    if iterativo==1:
        Saida.write(retorno+"\n")
        
    resultados.append([len(resultados)]+[Nivel]+[instrucao]+[endereco]+[nBytes]+[Offset]+[Set]+[Tag]+[posicao]+[retorno]+[stallWT]+[stallWB])
    return retorno

def enderecador(endereco,ioffset,iset):
    apoio=endereco>>ioffset
    Offset=endereco-(apoio<<ioffset)
    apoio=apoio>>iset
    Set=endereco-(apoio<<iset+ioffset)
    Set=Set>>ioffset
    Tag=endereco>>(iset+ioffset)
    if iterativo==1:
        Saida.write('\n')
        Saida.write("O endereço em binário é "+bin(endereco)+'\n')
        Saida.write("Dividido em Tag="+bin(Tag)+" Set="+bin(Set)+" Offset="+bin(Offset)+'\n')
    return Offset,Set,Tag

def L1(instrucao,endereco,nBytes,ioffset,iset,Linhas,Vias,Politicasub):
    Offset,Set,Tag=enderecador(endereco,ioffset,iset)
    totalBytes=nBytes+Offset
    blocos=1#quantos blocos que vai ter que acessar da cache
    blocoBytes=2**ioffset
    while totalBytes/blocoBytes>1:
        blocos=blocos+1
        totalBytes=totalBytes-blocoBytes
    if iterativo==1:
        Saida.write("Acessando a cacheL1 \n")
        Saida.write("Foi solicitado "+str(nBytes)+" Bytes com offset de "+str(Offset)+" Bytes do endereço "+str(endereco)+" instrução "+instrucao+"\n")
        Saida.write("Como a cache possui "+str(blocoBytes)+" bytes por bloco vai acessar "+str(blocos)+" blocos\n")
    for i in range(blocos):
        if iterativo==1:
            Saida.write("Set="+str(Set)+" Tag="+str(Tag)+"\n")
        retorno=acessacache(Offset,Set,Tag,instrucao,endereco,nBytes,cacheL1,"L1",Vias,Politicasub)
        if iterativo==1:
            printa(cacheL1)
        if Set<(Linhas-1):
            Set=Set+1
        else:
            Set=0
            Tag=Tag+1
    return retorno

def LI(instrucao,endereco,nBytes,ioffsetLI,isetLI,LinhasLI,ViasLI,PoliticasubLI):
    Offset,Set,Tag=enderecador(endereco,ioffsetLI,isetLI)
    blocos=1#quantos blocos que vai ter que acessar da cache
    totalBytes=nBytes+Offset
    blocoBytes=2**ioffsetLI
    while totalBytes/blocoBytes>1:
        blocos=blocos+1
        totalBytes=totalBytes-blocoBytes
    if iterativo==1:
        Saida.write("Acessando a cacheLI\n")
        Saida.write("Foi solicitado "+str(nBytes)+" Bytes com offset de "+str(Offset)+" Bytes do endereço "+str(endereco)+"\n")
        Saida.write("Como a cache possui "+str(blocoBytes)+" bytes por bloco vai acessar "+str(blocos)+" blocos\n")
    for i in range(blocos):
        if iterativo==1:
            Saida.write("Set="+str(Set)+" Tag="+str(Tag)+"\n")
        acessacache(Offset,Set,Tag,instrucao,endereco,nBytes,cacheLI,"LI",ViasLI,PoliticasubLI)
        if iterativo==1:
            printa(cacheLI)
        if Set<(LinhasLI-1):
            Set=Set+1
        else:
            Set=0
            Tag=Tag+1
    return


def getcache(nivel):
    if infcache.loc[0,'Nivel']=='LI':
        if nivel==2:
            cache=cacheL2
        elif nivel==3:
            cache=cacheL3
        elif nivel==4:
            cache=cacheL4
        elif nivel==5:
            cache=cacheL5
        elif nivel==6:
            cache=cacheL6
        elif nivel==7:
            cache=cacheL7
        elif nivel==8:
            cache=cacheL8
        elif nivel==9:
            cache=cacheL9
        elif nivel==10:
            cache=cacheL10
    else:
        if nivel==1:
            cache=cacheL2
        elif nivel==2:
            cache=cacheL3
        elif nivel==3:
            cache=cacheL4
        elif nivel==4:
            cache=cacheL5
        elif nivel==5:
            cache=cacheL6
        elif nivel==6:
            cache=cacheL7
        elif nivel==7:
            cache=cacheL8
        elif nivel==8:
            cache=cacheL9
        elif nivel==9:
            cache=cacheL10
    return cache        
            
def L1S(instrucao,endereco,nBytes,ioffset,iset,Linhas,Vias,Politicasub,nivel):
    Offset,Set,Tag=enderecador(endereco,ioffset,iset)
    totalBytes=nBytes+Offset
    blocos=1#quantos blocos que vai ter que acessar da cache
    blocoBytes=2**ioffset
    enderecoS=endereco
    while totalBytes/blocoBytes>1:
        blocos=blocos+1
        totalBytes=totalBytes-blocoBytes
    if iterativo==1:
        Saida.write("Acessando a cacheL1 \n")
        Saida.write("Foi solicitado "+str(nBytes)+" Bytes com offset de "+str(Offset)+" Bytes do endereço "+str(endereco)+" instrução "+instrucao+"\n")
        Saida.write("Como a cache possui "+str(blocoBytes)+" bytes por bloco vai acessar "+str(blocos)+" blocos\n")
    for i in range(blocos):
        if iterativo==1:
            Saida.write("Set="+str(Set)+" Tag="+str(Tag)+"\n")
        retorno=acessacache(Offset,Set,Tag,instrucao,endereco,nBytes,cacheL1,"L1",Vias,Politicasub)
        if iterativo==1:
            printa(cacheL1)
        if retorno=="miss":
            superior(instrucao,enderecoS,1,nivel)#blocos de nivel superior são acessados apenas 1 por vez
        enderecoS+=blocoBytes
        if Set<(Linhas-1):
            Set=Set+1
        else:
            Set=0
            Tag=Tag+1
    return
    

def superior(instrucao,endereco,nBytes,nivel):
    Vias=infcache.loc[nivel,'Vias']
    Politicasub=infcache.loc[nivel,'Politicasub']
    ioffset=infcache.loc[nivel,'bitsOffset']
    iset=infcache.loc[nivel,'bitsSet']
    Linhas=infcache.loc[nivel,'Linhas']
    Nivelstr=infcache.loc[nivel,'Nivel']
    Offset,Set,Tag=enderecador(endereco,ioffset,iset)
    totalBytes=nBytes+Offset
    blocos=1#quantos blocos que vai ter que acessar da cache
    blocoBytes=2**ioffset
    cache=getcache(nivel)
    if iterativo==1:
        Saida.write("Acessando a cache"+Nivelstr+'\n')
        Saida.write("Foi solicitado "+str(nBytes)+" Bytes com offset de "+str(Offset)+" Bytes do endereço "+str(endereco)+'\n')
        Saida.write("Como a cache possui "+str(blocoBytes)+" bytes por bloco vai acessar "+str(blocos)+" blocos\n")
    for i in range(blocos):
        if iterativo==1:
            Saida.write("Set="+str(Set)+" Tag="+str(Tag)+"\n")
        retorno=acessacache(Offset,Set,Tag,instrucao,endereco,nBytes,cache,Nivelstr,Vias,Politicasub)
        nivel+=1
        if (retorno=="miss "and nivel<len(infcache)):
            superior(instrucao,endereco,1,nivel)#blocos de nivel superior são acessados apenas 1 por vez
        if iterativo==1:
            printa(cache)
        if Set<(Linhas-1):
            Set=Set+1
        else:
            Set=0
            Tag=Tag+1
    return
    
def simula(trace):
    if infcache.loc[0,'Nivel']=='LI':    
        ViasLI=infcache.loc[0,'Vias']
        PoliticasubLI=infcache.loc[0,'Politicasub']
        ioffsetLI=infcache.loc[0,'bitsOffset']
        isetLI=infcache.loc[0,'bitsSet']
        LinhasLI=infcache.loc[0,'Linhas']

        Vias=infcache.loc[1,'Vias']
        Politicasub=infcache.loc[1,'Politicasub']
        ioffset=infcache.loc[1,'bitsOffset']
        iset=infcache.loc[1,'bitsSet']
        Linhas=infcache.loc[1,'Linhas']
    
    else:
        Vias=infcache.loc[0,'Vias']
        Politicasub=infcache.loc[0,'Politicasub']
        ioffset=infcache.loc[0,'bitsOffset']
        iset=infcache.loc[0,'bitsSet']
        Linhas=infcache.loc[0,'Linhas']

    
    if len(infcache)==1:#apenas L1
        for i in range (len(trace)):
            instrucao=trace['operacao'][i]
            endereco=trace["endereco"][i]
            nBytes=trace['tamanho'][i]
            L1(instrucao,endereco,nBytes,ioffset,iset,Linhas,Vias,Politicasub)
        
    elif infcache.loc[0,'Nivel']=='LI' and len(infcache)==2:#L1 e instruções
        for i in range (len(trace)):
            instrucao=trace['operacao'][i]
            endereco=trace["endereco"][i]
            nBytes=trace['tamanho'][i]
            if instrucao=="I":
                LI(instrucao,endereco,nBytes,ioffsetLI,isetLI,LinhasLI,ViasLI,PoliticasubLI)
            else:
                L1(instrucao,endereco,nBytes,ioffset,iset,Linhas,Vias,Politicasub)
                
    elif infcache.loc[0,'Nivel']=='LI' and len(infcache)>2:#Niveis superiores e instruções
        for i in range (len(trace)):
            instrucao=trace['operacao'][i]
            endereco=trace["endereco"][i]
            nBytes=trace['tamanho'][i]
            if instrucao=="I":
                LI(instrucao,endereco,nBytes,ioffsetLI,isetLI,LinhasLI,ViasLI,PoliticasubLI)
            else:
                nivel=2
                L1S(instrucao,endereco,nBytes,ioffset,iset,Linhas,Vias,Politicasub,nivel)
    else:#Niveis superiores sem instruções
        for i in range (len(trace)):
            instrucao=trace['operacao'][i]
            endereco=trace["endereco"][i]
            nBytes=trace['tamanho'][i]
            if instrucao=="I":#instruções ficam apenas no nível LI
                L1(instrucao,endereco,nBytes,ioffset,iset,Linhas,Vias,Politicasub)
            else:
                nivel=1
                L1S(instrucao,endereco,nBytes,ioffset,iset,Linhas,Vias,Politicasub)
    return

#para totalmente associativo Ilinhas=0 linhas=2**Ilinhas
Ilinhas=0
#bytes por bloco da cache = 2**iBytes
Ibytes=10
#vias de associativiade = Ivias,para mapeamento direto Ivias=1
Ivias=32
#implementado Ramdom, LRU, MRU e Fifo
Politicasub="LRU"
#Se iterativo==1 gera um arquivo de texto com cada acesso da cache
iterativo=0
infcache=pd.DataFrame(columns=['Nivel','Linhas','Vias','bitsOffset','bitsSet','BytesBloco',"Bytes por linha","KBytes total","Politicasub"])
resultados=[]
#SE TIVER CACHE DE INSTRUÇÕES PRECISA SER DECLARADO ANTES DA L1
cacheLI=cachecreate('LI',0,11,16,Politicasub)
#NIVEIS DEVEM SER DCLARADOS EM ORDEM:L1,L2,L3... MAXIMO SUPORTADO L10
cacheL1=cachecreate('L1',Ilinhas,Ibytes,Ivias,Politicasub)
#cacheL2=cachecreate('L2',8,9,4,Politicasub)

basetrace=16#10 para trace decimal 16 para hexadecimal


print(infcache)
if iterativo==1:
    Saida= open("Saida.txt","w+")
    s=str(infcache)
    Saida.write(s)


'''!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

ATENÇÃO PRIMEIRA LINHA DA TRACE PRECISA SER EXATAMENTE:
operacao,endereco,tamanho
PARA A SIMULAÇÃO OCORRER CORRETAMENTE 

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'''

#traceName='teste2'
traceName='hello_trace'
#traceName='ls_trace'
#traceName='cal_trace'
#traceName='nano_trace'


trace=pd.read_csv(traceName+".csv")
#conversão hexa para decimal,também garante que o endereço estara em inteiros
trace["endereco"]=trace["endereco"].apply(lambda x: int(str(x),basetrace))
#Instruções de escrita na memória serão tratadas da mesma forma
mmap= {'M':'S','S':'S','L':'L','I':'I'}
trace['operacao']=trace['operacao'].map(mmap)
'''as proximas 3 linhas removem os comandos de instrução da trace'''
#principal=trace["operacao"]!='I'
#trace=trace[principal]
#trace=trace.reset_index()


if len(trace)>40000:
    iterativo=0#por segurança,essa saída fica muito grande

simula(trace)

#printa(resultados) 
resultados=pd.DataFrame(resultados)
resultados.columns=["Nº Acesso","Nivel","Instrucao","Endereco","nBytes","Offset","Set","Tag","Posicao","Resultado","Escreve se WT","Escreve se WB"]
CSV()

    


