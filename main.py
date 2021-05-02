
from run_benchmark import RunBenchmark
import report

import argparse
import sys

def main():
    args = get_args()
    if not args['graphics_report']:
        # rb = RunBenchmark("./test_img")
        rb = RunBenchmark("./BSDS300/images/train/")
        rb.run()
        print("Total de ejecución: ", rb.total_time)
    
    if args['graphics_report']:
        report.result_plot_time('linux_execution_time.csv', 
                                'win32_execution_time.csv')
    if args['delete']:
        rb.delete_paths()

def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("-d", "--delete", action='store_true',  
                                help="Eliminar todas las imágenes procesadas")
    parser.add_argument("-gr", "--graphics-report", action='store_true',  
                                help="Generar reporte con gráficas")
    return vars(parser.parse_args())

if __name__ == "__main__":
    main()
