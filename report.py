import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

width = 0.35
labels = ['Conversión a Grises', 'Histograma Color', 'Histograma Gris']

def result_plot_time(linux_csv_file, windows_csv_file):
    l_dataset = pd.read_csv(linux_csv_file)
    w_dataset = pd.read_csv(windows_csv_file)
    plot_time_results(l_dataset, w_dataset)
    plot_bat_total_time(l_dataset, w_dataset)


def plot_time_results(l_dataset, w_dataset):
    plt.close()
    x1 = np.arange(l_dataset.shape[0])
    x2 = np.arange(w_dataset.shape[0])

    fig, axs = plt.subplots(2, 1, figsize=(8, 6))

    axs[0].plot(x1, l_dataset['gray'])
    axs[0].plot(x1, l_dataset['color_histograma'])
    axs[0].plot(x1, l_dataset['gray_histograma'])
    axs[0].set_title("Tiempos de conversión - Linux")
    axs[0].set_ylabel("Tiempo")
    axs[0].set_xlabel("N imagen")
    axs[0].legend(labels)

    axs[1].plot(x2, w_dataset['gray'])
    axs[1].plot(x2, w_dataset['color_histograma'])
    axs[1].plot(x2, w_dataset['gray_histograma'])
    axs[1].set_title("Tiempos de conversión - Windows")
    axs[1].set_ylabel("Tiempo")
    axs[1].set_xlabel("N imagen")
    axs[1].legend(labels)

    fig.tight_layout()
    plt.savefig('pdfs/comparacion_tiempos_imagenes.png', dpi=400)
    plt.show()

def plot_bat_total_time(l_dataset, w_dataset):
    
    windows = [w_dataset['gray'].sum(), \
                w_dataset['color_histograma'].sum(), \
                w_dataset['gray_histograma'].sum()]

    linux = [l_dataset['gray'].sum(), \
                l_dataset['color_histograma'].sum(), \
                l_dataset['gray_histograma'].sum()]

    x = np.arange(len(labels))

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width/2, linux, width, label='Linux')
    rects2 = ax.bar(x + width/2, windows, width, label='Windows')
    
    ax.set_ylabel('Tiempo Total')
    ax.set_title('Tiempo de ejecución')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    set_values(ax, windows)
    set_values(ax, linux, is_impar=False)

    fig.tight_layout()

    plt.savefig('pdfs/comparacion_tiempos.png', dpi=300)
    plt.show()

def set_values(ax, y, is_impar=True):
    for index, value in enumerate(y):
        if is_impar:
            plt.text(index + (width/5), value + 0.5, str(round(value, 2)))
        else:
            plt.text(index - (width/1.4), value + 0.5, str(round(value, 2)))
    
