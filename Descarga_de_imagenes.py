""" Implementación secuencial y paralela de un descargador de imágenes """
import os
import time
import urllib.request
import multiprocessing as mp
import concurrent.futures

""" La función implementa una descarga secuencial de imágenes """
def seq_download_images(image_numbers, folder):
    # Inicializa una variable para almacenar el total de bytes descargados
    total_bytes = 0
    
    # Itera a través de cada número de imagen en la lista proporcionada
    for num in image_numbers:
        # Llama a la función _download_image para cada número de imagen y acumular el total de bytes
        total_bytes += _download_image(num, folder)
    
    # Devuelve el total de bytes descargados
    return total_bytes

""" La función se encarga de descargar, guardar y darnos el tamaño de la imagen  """
def _download_image(image_number, folder):
    # El número de imagen estará entre 1 y 50
    image_number = abs(image_number) % 50 + 1
    
    # Construye la URL de la imagen basada en el número de imagen
    image_url = 'http://699340.youcanlearnit.net/image{:03d}.jpg'.format(image_number)
    
    try:
        # Abre la URL, lee los datos de la imagen y calcula el tamaño de la imagen
        with urllib.request.urlopen(image_url, timeout=60) as conn:
            image_data = conn.read()
            image_size = len(image_data)
            
            # Construye la ruta de guardado basada en el número de imagen y la carpeta especificada
            save_path = os.path.join(folder, 'image{:03d}.jpg'.format(image_number))
            
            # Escribe los datos de la imagen en la ruta de archivo especificada
            with open(save_path, 'wb') as file:
                file.write(image_data)
            
            # Devuelve el tamaño de la imagen descargada
            return image_size

    # Maneja errores HTTP
    except urllib.error.HTTPError as e:
        print('HTTPError: No se pudo obtener la imagen {}. {}'.format(image_number, e))
    # Maneja otras excepciones
    except Exception as e:
        print(e)

""" La función implementa una descarga paralela de imágenes """
def par_download_images(image_numbers, folder):
    # Inicializa una variable para almacenar el total de bytes descargados
    total_bytes = 0
    
    # Utiliza un pool de hilos para paralelizar las descargas de imágenes
    with concurrent.futures.ThreadPoolExecutor() as pool:
        # Envia tareas para cada número de imagen y almacenar los resultados futuros
        futures = [pool.submit(_download_image, num, folder) for num in image_numbers]
        
        # Itera a través de los futuros completados y acumular el total de bytes
        for f in concurrent.futures.as_completed(futures):
            total_bytes += f.result()
    
    # Devuelve el total de bytes descargados
    return total_bytes


if __name__ == '__main__':
    # Configuración para la evaluación del rendimiento
    NUM_EVAL_RUNS = 1
    IMAGE_NUMBERS = list(range(0,50))

    # Carpeta para descargas secuenciales y paralelas
    SEQUENTIAL_FOLDER = r'C:\Users\Usuario\Desktop\Joker2\img1'
    PARALLEL_FOLDER = r'C:\Users\Usuario\Desktop\Joker2\img2'

    # Evalua la implementación secuencial
    print('Evaluando la implementación secuencial...')
    sequential_result = seq_download_images(IMAGE_NUMBERS, SEQUENTIAL_FOLDER)
    sequential_time = 0
    for i in range(NUM_EVAL_RUNS):
        start = time.perf_counter()
        seq_download_images(IMAGE_NUMBERS, SEQUENTIAL_FOLDER)
        sequential_time += time.perf_counter() - start
    sequential_time /= NUM_EVAL_RUNS

    # Evalua la implementación paralela
    print('Evaluando la implementación paralela...')
    parallel_result = par_download_images(IMAGE_NUMBERS, PARALLEL_FOLDER)
    parallel_time = 0
    for i in range(NUM_EVAL_RUNS):
        start = time.perf_counter()
        par_download_images(IMAGE_NUMBERS, PARALLEL_FOLDER)
        parallel_time += time.perf_counter() - start
    parallel_time /= NUM_EVAL_RUNS

    # Verificar si los resultados secuenciales y paralelos coinciden
    if sequential_result != parallel_result:
        raise Exception('sequential_result and parallel_result do not match.')
    
    # Imprime las métricas de rendimiento
    print('Average Sequential Time: {:.2f} ms'.format(sequential_time*1000))
    print('Average Parallel Time: {:.2f} ms'.format(parallel_time*1000))
    print('Speedup: {:.2f}'.format(sequential_time/parallel_time))   #Aceleración
    print('Efficiency: {:.2f}%'.format(100*(sequential_time/parallel_time)/mp.cpu_count()))
