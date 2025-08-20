import requests
import base64
import os
import json
from urllib.request import urlopen

def obtenerLista():
    sku_dict = {}

    with open('list.txt', 'r') as archivo:
        lineas = archivo.readlines()

        for linea in lineas:
            lineaLimpia = linea.strip()
            campos = lineaLimpia.split(',')

            if len(campos) == 3:
                mlaCampo1, skuCampo2, linkImgCampo3 = campos

                # me quedo con el primer sku
                primerSKU = skuCampo2.split()[0]
                skuCampo2 = primerSKU
                print(f"Campo 1: {mlaCampo1}, Campo 2: {skuCampo2}, Campo 3: {linkImgCampo3}")

                if skuCampo2 in sku_dict:
                    sku_dict[skuCampo2]['mlas'].append(mlaCampo1)
                else:
                    # SKU nuevo, crear nueva entrada
                    sku_dict[skuCampo2] = {
                        'url': linkImgCampo3,
                        'mlas': [mlaCampo1]
                    }

    print("Resultado final:")
    print("=" * 50)
    with open('salida.txt', 'w', encoding='utf-8') as archivo:
        for sku, datos in sku_dict.items():
            # Para consola
            print(f"SKU: {sku}")
            print(f"URL: {datos['url']}")
            print(f"MLAs: {', '.join(datos['mlas'])}")
            print(f"Cantidad de MLAs: {len(datos['mlas'])}")
            print("-" * 30)
            
            # Para archivo
            print(f"SKU: {sku}", file=archivo)
            print(f"URL: {datos['url']}", file=archivo)
            print(f"MLAs: {', '.join(datos['mlas'])}", file=archivo)
            print(f"Cantidad de MLAs: {len(datos['mlas'])}", file=archivo)
            print("-" * 30, file=archivo)
            print(file=archivo)
    
    return sku_dict

def procesar(sku_dict):
    # Tomo el primer SKU del diccionario para probar  //// Luego procesara el lote
    if sku_dict:

        for first_sku in sku_dict:
            # first_sku = list(sku_dict.keys())[0]
            image_url = sku_dict[first_sku]['url']
            
            print(f"\nProbando con URL: {image_url}")
            print(f"SKU: {first_sku}")
            
            # Configurar la solicitud al API de Kaze
            url = "https://backend.kaze.ai/api/ext/v1/submit_watermark_removal"
            
            payload = json.dumps({
                "image_url": image_url
            })
            
            headers = {
                'Authorization': 'sk-JGHv8oYnXHqbExXiFVZn8bOQ',
                'Content-Type': 'application/json'
            }
            
            try:
                # Realizar la solicitud
                response = requests.post(url, headers=headers, data=payload)
                
                print(f"Status Code: {response.status_code}")
                print(f"Response: {response.text}")
                
                # Intentar parsear JSON si la respuesta es exitosa
                if response.status_code == 200:
                    try:
                        result = response.json()
                        print("Resultado JSON:")
                        print(json.dumps(result, indent=2))
                        
                        # Verificar la estructura de respuesta según documentación
                        if result.get('code') == 0 and 'data' in result and 'task_id' in result['data']:
                            task_id = result['data']['task_id']
                            print(f"✅ Solicitud enviada exitosamente. Task ID: {task_id}")
                            
                            # Consultamos la API para obtener la URL de la imagen editada
                            # Enviamos task_id para la url obtenida, sku y listado de mlas
                            obtener_resultado(task_id, first_sku, sku_dict[sku_dict]['mlas'])

                        else:
                            print("⚠️  La respuesta no tiene la estructura esperada")
                            print(f"Código: {result.get('code')}")
                            print(f"Mensaje: {result.get('message')}")
                            
                    except json.JSONDecodeError:
                        print("La respuesta no es JSON válido")
                else:
                    print(f"❌ Error en la API: {response.status_code}")
                    
            except requests.exceptions.RequestException as e:
                print(f"Error en la solicitud: {e}")
                return None
    else:
        print("No hay datos en el diccionario")
        return None

def obtener_resultado(task_id, skuPerteneciente, listadoMlas):
    url = "https://backend.kaze.ai/api/ext/v1/get_task_result"

    payload = json.dumps({
        "task_id": task_id
    })

    headers = {
        'Authorization': 'sk-JGHv8oYnXHqbExXiFVZn8bOQ',
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()  # excepción si hay error HTTP
        
        result = response.json()
        data = result.get('data', {})
        
        if data.get('status') == 'success' and data.get('images'):
            newUrl = data['images'][0]['url']
            print(f"✅ URL procesada obtenida: {newUrl}")
            
            # Escribir en CSV el resultado
            escribir_resultado(skuPerteneciente, listadoMlas, newUrl)
            
    except requests.exceptions.RequestException as e:
        print(f"Error en la solicitud: {e}")
        return None
    except (json.JSONDecodeError, KeyError, IndexError) as e:
        print(f"Error procesando respuesta: {e}")
        return None


def escribir_resultado(skuPerteneciente, listadoMlas, newUrl):
    nombre_archivo = "resultado.csv"
    existe = os.path.exists(nombre_archivo)
    
    # Crear la línea en formato CSV
    contenido = f"{skuPerteneciente},{listadoMlas},{newUrl}\n"
    
    if existe:
        print(f"El archivo '{nombre_archivo}' existe. Añadiendo contenido...")
    else:
        print(f"El archivo '{nombre_archivo}' no existe. Creándolo...")
    
    with open(nombre_archivo, 'a', encoding='utf-8') as archivo:
        # Si el archivo no existe, escribir los encabezados primero
        if not existe:
            archivo.write("skuPerteneciente,listadoMlas,newUrl\n")
        archivo.write(contenido)
    
    print("Operación completada.")


def main():
    # Obtener la lista de SKUs
    sku_dict = obtenerLista()

    procesar(sku_dict)
    

if __name__ == "__main__":
    main()

