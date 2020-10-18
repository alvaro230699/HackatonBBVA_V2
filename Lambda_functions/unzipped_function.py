import json
import os
import tempfile
import zipfile
import gzip
from concurrent import futures
from io import BytesIO
import urllib

import boto3
#Function FunctionLambda_ZIPtoPDF

def lambda_handler(event, context):
    
    bucket= event['Records'][0]['s3']['bucket']['name']
    key=urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    key_array=key.split(";")
    documentName=key_array[0]
    correo=key_array[1]
    hora_extension=key_array[2]
    hora=hora_extension.split(".")[0]

    # bucket='bbvacompetencia'
    bucket_destino='function-lambda-ziptopdf'
    # key='Doc2.zip'
    s3 = boto3.client('s3')
    cantidad=0
    new_array_names=[]
    if '.zip'in key:
        temp_file = tempfile.mktemp()
        # Fetch and load target file
        s3.download_file(bucket, key, temp_file)
        zipdata = zipfile.ZipFile(temp_file)
        lista_nombres = zipdata.namelist()
        for filerr in lista_nombres:
            print(filerr)
            y=zipdata.open(filerr)
            # print(y)
            arcname = y.name
            print(arcname)
            arcname_array=arcname.split(".")
            archive_name=arcname_array[0]
            extension=arcname_array[1]
            new_arcname=archive_name + ";"+correo+";"+hora+"."+extension
            new_array_names.append(new_arcname)
            # print(arcname)
            x = BytesIO(y.read())
            s3.upload_fileobj(x, bucket_destino, new_arcname)
            y.close()
        print('Cantidad de objetos: {}'.format(len(lista_nombres)))
        cantidad=len(lista_nombres)
        # return{'cantidad_Listas':len(lista_nombres)}
    elif ('.jpg' in key) or ('.pdf' in key) or ('.jpeg' in key) or ('.png' in key):
        # Copy Source Object
        copy_source_object = {'Bucket': bucket, 'Key': key}
        lista_nombres=key
        cantidad=1
        # S3 copy object operation
        s3.copy_object(CopySource=copy_source_object, Bucket=bucket_destino, Key=key)
        print('Cantidad de objetos ' + '1')
        # return{'cantidad_Listas':1}
    else:
        print('Cantidad de objetos ' + 'error')
        cantidad='error'
        return{'cantidad_Listas': error}
    sqs = boto3.resource('sqs')

    # Get the queue
    queue = sqs.get_queue_by_name(QueueName='Cola')

    # Create a new message
    if cantidad>1:
        for i in range(cantidad):
            response = queue.send_message(MessageBody=new_array_names[i])
            print('Se agregó al queue')
            print(new_array_names[i])
            print(response)
        return{'cantidad_Listas': cantidad}

    else:
        response = queue.send_message(MessageBody=lista_nombres)
        print('Se agregó al queue')
        print(lista_nombres)
        print(response)
        return{'cantidad_Listas': cantidad}



