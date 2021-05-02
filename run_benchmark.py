from matplotlib.backends.backend_pdf import PdfPages
from matplotlib import pyplot as plt
from PyPDF2 import PdfFileMerger, PdfFileReader, PdfFileWriter
import numpy as np
import matplotlib.image as mpimg
import sys
import time
import os
import shutil
import json

import csv

class RunBenchmark:
    
    """
    Clase para realizar la comparación en tiempos
    de ejecución entre OS Windows 10 y GNU/Linux
    """

    images_out_path = "images_" + sys.platform
    pdf_out_name = sys.platform + "_benchmark.pdf"
    script_files_json = "./scripts/scripts_names.json"
    script_files = None
    execution_times = list()
    pdf_tmp = ".pdfs/"

    def __init__(self, path_images, images_out_path=images_out_path,
        pdf_out_name=pdf_out_name):
        
        self.pdf_out_name = "pdfs/" + pdf_out_name
        self.absolute_path_images = os.path.abspath(path_images)
        self.images_out_path = images_out_path
        self.total_time = 0.0

        self.check_paths()
        self.load_scripts_from_json()

    def check_paths(self):
        if not os.path.exists(self.images_out_path):
            os.makedirs(self.images_out_path)
        
        if not os.path.exists("./pdfs"):
            os.makedirs("./pdfs")

        if not os.path.exists(self.pdf_tmp):
            os.makedirs(self.pdf_tmp)

    def delete_paths(self):
        shutil.rmtree(self.images_out_path)
        shutil.rmtree(self.pdf_tmp)

    def load_scripts_from_json(self):
        with open(self.script_files_json, "r") as config_file:
            self.scripts_names = json.load(config_file)
    
    
    
    def run(self):
        print("Comenzando ejecución en: ", sys.platform)
        i = 0
        self.execution_times.append(["image_name", "gray", "color_histograma", "gray_histograma"])
        for image_file_name in os.listdir(self.absolute_path_images):
            _OS, image_path_name = self.get_os_paths(self.absolute_path_images, image_file_name)
            
            # Ejecución de scripts
            if _OS == "linux":
                execution_time = self.run_on_linux(image_path_name, str(i), image_file_name)
            else:
                execution_time = self.run_on_windows(image_path_name, str(i), image_file_name)
            ##
            
            plot_page = self.create_plot(self.get_images_convert_path( 
                                            self.absolute_path_images + "/" + image_file_name, str(i)),
                                            execution_time)
            self.save_to_pdf(plt, image_file_name + ".pdf")
            i += 1
        self.generate_report_pdf()
        with open ('time_execution.txt','a') as f:
            f.write(f" \n>> Tiempo {_OS}: " + str(self.total_time))
            f.close()

        with open(_OS + '_execution_time.csv', 'w') as f:
            write = csv.writer(f)
            write.writerows(self.execution_times)
            f.close()
        
            
    def run_on_linux(self, image_path_name, folder_name, image_file_name):
        ## Llamada a los Scripts
        execution_time = list()
        execution_time.extend([image_file_name])
        start_time = time.time()
        os.system(self.scripts_names["L_GRAY_CONVERT"] \
            + " " + image_path_name \
            + " " + self.images_out_path \
            + " " + folder_name \
            + " " + image_file_name)
        end_time = time.time() - start_time
        execution_time.extend([end_time])
        self.total_time += end_time

        start_time = time.time()
        os.system(self.scripts_names["L_COLOR_HISTOGRAM"] \
            + " " + image_path_name \
            + " " + self.images_out_path \
            + " " + folder_name \
            + " " + image_file_name)
        end_time = time.time() - start_time
        execution_time.extend([end_time])
        self.total_time += end_time

        start_time = time.time()
        os.system(self.scripts_names["L_GRAY_HISTOGRAM"] \
            + " " + image_path_name \
            + " " + self.images_out_path \
            + " " + folder_name \
            + " " + image_file_name)
        end_time = time.time() - start_time
        execution_time.extend([end_time])
        self.total_time += end_time

        self.execution_times.append(execution_time)
        return execution_time
        ##

    def run_on_windows(self, image_path_name, folder_name, image_file_name):
        ## Llamada a los Scripts
        execution_time = list()
        execution_time.extend([image_file_name])
        start_time = time.time()
        os.system(self.scripts_names["W_GRAY_CONVERT"] \
            + " " + image_path_name \
            + " " + self.images_out_path \
            + " " + folder_name \
            + " " + image_file_name)
        end_time = time.time() - start_time
        execution_time.extend([end_time])
        self.total_time += end_time

        start_time = time.time()
        os.system(self.scripts_names["W_COLOR_HISTOGRAM"] \
            + " " + image_path_name \
            + " " + self.images_out_path \
            + " " + folder_name \
            + " " + image_file_name)
        end_time = time.time() - start_time
        execution_time.extend([end_time])
        self.total_time += end_time

        start_time = time.time()
        os.system(self.scripts_names["W_GRAY_HISTOGRAM"] \
            + " " + image_path_name \
            + " " + self.images_out_path \
            + " " + folder_name \
            + " " + image_file_name)
        end_time = time.time() - start_time
        execution_time.extend([end_time])
        self.total_time += end_time

        self.execution_times.append(execution_time)
        return execution_time
        ##

    def get_os_paths(self, path, image_name):
        if sys.platform == "linux" or sys.platform == "linux2":
            return ("linux", str(path + "/" + image_name))
        elif sys.platform == "win32":
            return ("win32", str(path + "\\" + image_name))

    def get_images_convert_path(self, image_file_name, folder_name):
        images_path = list()
        out_images_path = self.images_out_path + "/" + folder_name
        for image in os.listdir(out_images_path):
            images_path.extend([out_images_path + "/" + image])
        images_path.extend([image_file_name])
        return images_path

    def create_plot(self, path, times):
        plt.close()
        fig, axs = plt.subplots(2, 2)
        plt.text(0.05, 0.95, "Imagen: " + times[0], transform=fig.transFigure, size=15)

        axs[0, 0].imshow(mpimg.imread(path[3]))
        axs[0, 0].set_title('Original', fontsize=10)
        axs[0, 0].axis('off')
        
        txt = 'Escala de grises' + '\nT=' + str(round(times[1], 4))
        axs[0, 1].imshow(mpimg.imread(path[0]), cmap='gray')
        axs[0, 1].set_title(txt, fontsize=10)
        axs[0, 1].axis('off')
        
        txt = 'Histograma Color' + '\nT=' + str(round(times[2], 4))
        axs[1, 0].imshow(mpimg.imread(path[1]))
        axs[1, 0].set_title(txt, fontsize=10)
        axs[1, 0].axis('off')

        txt = 'Histograma Grises' + '\nT=' + str(round(times[3], 4))
        axs[1, 1].imshow(mpimg.imread(path[2]), cmap='gray')
        axs[1, 1].set_title(txt, fontsize=10)
        axs[1, 1].axis('off')

        plt.subplots_adjust(left=0.125,
                    bottom=0.1, 
                    right=0.9, 
                    top=0.9, 
                    wspace=0.2, 
                    hspace=0.35)
        return plt

    def save_to_pdf(self, plot_figure, pdf_name):
        pdf = PdfPages(self.pdf_tmp + pdf_name)
        for fig in range(1, plot_figure.gcf().number + 1):
            pdf.savefig( fig )
        pdf.close()

    def generate_report_pdf(self):
        
        print("\n\t Generando Informe PDF...\n")
        pdfs_files = os.listdir(self.pdf_tmp)

        input_streams = []
        try:
            for input_file in pdfs_files:
                input_streams.append(open(self.pdf_tmp + input_file, 'rb'))
            writer = PdfFileWriter()
            for reader in map(PdfFileReader, input_streams):
                for n in range(reader.getNumPages()):
                    writer.addPage(reader.getPage(n))
            writer.write(open(self.pdf_out_name, 'wb'))
        finally:
            for f in input_streams:
                f.close()

        print("\t Generación terminada.\n")