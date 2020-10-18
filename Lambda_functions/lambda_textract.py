import json
import boto3
import io
from io import BytesIO
import sys
import urllib.parse
import time

def startJob(s3BucketName, objectName):
    response = None
    client = boto3.client('textract')
    response = client.start_document_text_detection(
    DocumentLocation={
        'S3Object': {
            'Bucket': s3BucketName,
            'Name': objectName
        }
    })

    return response["JobId"]

def isJobComplete(jobId):
    time.sleep(1.5)
    client = boto3.client('textract')
    response = client.get_document_text_detection(JobId=jobId)
    status = response["JobStatus"]
    #print("Job status: {}".format(status))

    while(status == "IN_PROGRESS"):
        time.sleep(1.5)
        response = client.get_document_text_detection(JobId=jobId)
        status = response["JobStatus"]
        #print("Job status: {}".format(status))

    return status

def getJobResults(jobId):

    pages = []

    time.sleep(1.5)

    client = boto3.client('textract')
    response = client.get_document_text_detection(JobId=jobId)
    
    pages.append(response)
    #print("Resultset page recieved: {}".format(len(pages)))
    nextToken = None
    if('NextToken' in response):
        nextToken = response['NextToken']

    while(nextToken):
        time.sleep(1.5)

        response = client.get_document_text_detection(JobId=jobId, NextToken=nextToken)

        pages.append(response)
        #print("Resultset page recieved: {}".format(len(pages)))
        nextToken = None
        if('NextToken' in response):
            nextToken = response['NextToken']

    return pages
'''
def distanciaV2(palabra, dicComparar):
    
    minimo=99
    
    for comparar in dicComparar:
        minimoComparacion = editDistDP(palabra, comparar, len(palabra), len(comparar))
        if minimoComparacion < minimo:
            minimo = minimoComparacion
    return minimo
'''
def editDistDP(str1, str2):
    
    str1=str1.lower()
    str2=str2.lower()
    m = len(str1)
    n = len(str2)
    # Create a table to store results of subproblems 
    dp = [[0 for x in range(n + 1)] for x in range(m + 1)] 
  
    # Fill d[][] in bottom up manner 
    for i in range(m + 1): 
        for j in range(n + 1): 
  
            # If first string is empty, only option is to 
            # insert all characters of second string 
            if i == 0: 
                dp[i][j] = j    # Min. operations = j 
  
            # If second string is empty, only option is to 
            # remove all characters of second string 
            elif j == 0: 
                dp[i][j] = i    # Min. operations = i 
  
            # If last characters are same, ignore last char 
            # and recur for remaining string 
            elif str1[i-1] == str2[j-1]: 
                dp[i][j] = dp[i-1][j-1] 
  
            # If last character are different, consider all 
            # possibilities and find minimum 
            else: 
                dp[i][j] = 1 + min(dp[i][j-1],        # Insert 
                                   dp[i-1][j],        # Remove 
                                   dp[i-1][j-1])    # Replace 
  
    return dp[m][n] 

def getYear(palabras):
    
    anhoFinal=-1
    pos=-1
    for i in range(20):
        anho = palabras[i]['Text'].split(" ")[-1].split('/')[-1]
        if not (anho.isnumeric()):continue
        anho = int(anho)
        if anho >anhoFinal:
            anhoFinal = anho
            pos = sum([b['X'] for b in palabras[i]['Geometry']['Polygon']])/4
    print(anhoFinal)
    return anhoFinal
        

def find_blocks_selected(blocks_lines, block_names):
    
    yearCalculado = getYear(blocks_lines)
    print("Lineas detectadas")
    blocks_len=len(block_names)
    blocks_lines_len=len(blocks_lines)
    blockSelectedDistance=[99 for i in range(blocks_len)]#error de la palabra encontrada
    blockSelectedId=[0 for i in range(blocks_len)]
    blockSelectedIdPos=[0 for i in range(blocks_len)]
    blockRespuestas=[0 for i in range(blocks_len)]


    print("empezando loop")
   
    for i in range(blocks_len):#las variables a buscar que son 12
    
        for name in block_names[i]:
        
            for j in range(blocks_lines_len):#todas las lineas del pdf que son mil xd
                block = blocks_lines[j]
                distancia = editDistDP(block['Text'], name)#funcion de error de distancia
                #print(distancia,block['Text'], name )
                if distancia < blockSelectedDistance[i]:
                    
                    blockSelectedDistance[i]=distancia
                    blockSelectedId[i]=block
                    blockSelectedIdPos[i]=j
                    if distancia < 2: break
                
                if j!=0:
                    distancia=editDistDP(blocks_lines[j-1]['Text']+block['Text'], name)
                    #print(distancia,blocks_lines[j-1]['Text']+block['Text'], name )
                    if distancia < blockSelectedDistance[i]:
                        
                        blockSelectedDistance[i]=distancia
                        blockSelectedId[i]=block
                        blockSelectedIdPos[i]=j
                        if distancia <2 : break 

    
    print("Fase:")
    print("Segunda fase")
    
    for x in blockSelectedIdPos:
        print(blocks_lines[x]['Text'])
    j=0           
    for pos in blockSelectedIdPos:
        block_respuesta="0"
        x_pos = sum([b['X'] for b in blocks_lines[pos]['Geometry']['Polygon']])/4
        
        respuestaOpciones=[]
        i=1
        while True:
            x_posActual = sum([b['X'] for b in blocks_lines[pos+i]['Geometry']['Polygon']])/4
            if x_posActual> x_pos:
                x_pos = x_posActual
                respuestaOpciones.append(blocks_lines[pos+i]['Text'])
            else:
                break
            i+=1
        
        for n in respuestaOpciones:
            cantidadNumeros = sum(c.isdigit() for c in n)
            if cantidadNumeros>2:
                block_respuesta = n
                break
            if cantidadNumeros>=1:
                block_respuesta = n
        
        
        blockRespuestas[j]=block_respuesta
        j+=1
    print("fase 3")
    return [blockRespuestas, yearCalculado]

def procesarSalida(blocks_search_sinprocesar):
    
    info = blocks_search_sinprocesar
    
    for i in range(len(info)):
        dato = info[i]
        dato = dato.split(" ")[-1]
        dato = dato.replace(".","")
        dato = dato.replace(",","")
        dato = dato.replace(")","")
        inicio = dato[0]
        dato = dato.replace("(","")
        if dato.isnumeric():
            dato=int(dato)
            if inicio =='(':
                dato = -1*dato
        else:
            dato="0"
        info[i] = dato
    
    return info
    
def lambda_handler(event, context):
    

    documentName=event['Records'][0]['body']
    # queue_attributes=event['Records'][0]['messageAttributes']
    s3BucketName='function-lambda-ziptopdf'
    print('Se leyo el documento {} del bucket {} por medio de SNS'.format(documentName,s3BucketName))
    key_array=documentName.split(";")
    document_name=key_array[0]
    correo=key_array[1]
    hora=key_array[2]
    #s3BucketName = "bbvacompetencia"
    #documentName = "Doc1.pdf"
    block_names = [["Caja y bancos","Efectivo y equibalentes en efectivo"],
                    ["Total activo","Suma de los activos","Activo total"],
                    ["Total pasivo","Suma de los pasivos","Pasivo total"],
                    ["Total patrimonio","Suma de los patrimonios","Patrimonio total",
                    "Patrimonio","Suma el capital contable","Total capital contable ",
                    "Total capital contable "],
                    ["Ventas","Ventas por operación ordinacia","Ingresos por operación",
                    "Ingresos por operación ordinaria","Ingresos operacionales",
                    "Ventas brutas","Ingreso por actividades ordinarias"],
                    ["Costos de ventas","Costos por ventas","Costo de actividades ordinarias"],
                    ["Utilidad Bruta","Perdida Bruta"],
                    ["Utilidad operacional","Perdida operacional"],
                    ["Utilidad antes de impuestos","Perdida antes de impuestos"],
                    ["Utilidad neta","Perdida neta"]
                    ]


    jobId = startJob(s3BucketName, documentName)
    if(isJobComplete(jobId)):
        response = getJobResults(jobId)

    blocks_lines=[]
    for resultPage in response:
        for item in resultPage["Blocks"]:
            if item["BlockType"] == "LINE":
                blocks_lines.append(item)
    
    salida=find_blocks_selected(blocks_lines, block_names)
    blocks_search_sinprocesar=salida[0]
    print(blocks_search_sinprocesar)
    blocks_search = procesarSalida(blocks_search_sinprocesar)
    year = salida[1]
    print(blocks_search)
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('prueba1')
    item_table={
            'id':correo + document_name,
            'Documento': document_name,
            'Fecha': year,
            'Unidades de medida':0 ,
            'Caja y bancos':blocks_search[0] ,
            'Total activo':blocks_search[1] ,
            'Total pasivo':blocks_search[2] ,
            'Total patrimonio':blocks_search[3] ,
            'Ventas':blocks_search[4] ,
            'Costo de ventas':blocks_search[5] ,
            'Utilidad Bruta':blocks_search[6] ,
            'Utilidad operacional':blocks_search[7] ,
            'Utilidad antes de impuestos':blocks_search[8],
            'Utilidad neta':blocks_search[9]
            # 'Resultado_operacion':blocks_search[11] ,
            # 'Utilidad_neta_periodo':blocks_search[12]

        }
    table.put_item(Item=item_table)
    
    print("Finalizado")

    return {
        'body': json.dumps(blocks_search)
    }   
