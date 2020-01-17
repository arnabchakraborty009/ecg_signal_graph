# -*- coding: utf-8 -*-
import uuid

import img2pdf
from matplotlib import pyplot as plt
import numpy as np
from datetime import datetime, timedelta
from PIL import Image
from services.common_service import find_gain, read_data_files


def generate_ecg():
    try:
        # Hard coded
        hr = 72
        rr = 60000 / 72
        temperature = 28

        # Read data from file
        data = read_data_files()
        start = datetime.now()
        end = datetime.now() + timedelta(seconds=5)
        data_arr, lower, upper, mv_per_mm = find_gain(data, start, end, hr)

        patient_identifier = str(uuid.uuid4())
        image_name = 'images/' + patient_identifier + '.png'
        pdf_name = 'reports/' + patient_identifier + '.pdf'
        id = patient_identifier
        hospital = "DEMO HOSPITAL"

        font = {'family': 'serif',
                'color': 'k',
                'weight': 'bold',
                'size': 10,
                }

        textstr_left = '\n'.join((
            r'%s' % ('ELECTRO CARDLOGRAPHIC OBSERVATIONS',),
            r'',
            r'%s' % (data_arr[0]['startDate'],),
            r'ID      : %s' % (patient_identifier,),
            r'HR       : %s bpm' % (str(hr),),
            r'R-R      : %.2f ms' % (float(rr),),
            r'Temperature: %s C' % (str(temperature), ),
        ))

        textstr_right = '\n'.join((
            r'%s' % ('MEASUREMENT UNIT',),
            r'',
            r'SPEED  :%s' % ('25mm/s',),
            r'GAIN    :%s mm/mV' % (mv_per_mm,),))

        textstr_btn_right = '\n'.join((
            r'%s' % ('UNCONFIRMED',),
            r'',
            r'Report verified By ______________________',))

        width = 175.0
        height = 200

        frequency = 0.004
        start_time = 0
        time = 3
        end_time = start_time + time

        # drawing stuff
        t = np.arange(start_time, end_time, frequency, dtype=float)


        fig, ax = plt.subplots()
        oneMMInInchW = width / float(25.4) - 0.06
        oneMMInchH = height / float(25.4)
        fig.set_size_inches(oneMMInInchW + 0.08, oneMMInchH + 0.34)
        # Other stuffs
        ax.xaxis.set_minor_locator(
            plt.LinearLocator(width + 1)
        )

        ax.yaxis.set_minor_locator(
            plt.LinearLocator(height + 1)
        )

        ax.xaxis.set_major_locator(
            plt.LinearLocator(width / 5 + 1)
        )
        ax.yaxis.set_major_locator(
            plt.LinearLocator(height / 5 + 1)
        )

        color = {'minor': '#7BED3D', 'major': '#7BED3D'}
        linewidth = {'minor': .1, 'major': .2}

        for axe in 'x', 'y':
            for which in 'major', 'minor':
                ax.grid(
                    which=which,
                    axis=axe,
                    linestyle='-',
                    linewidth=linewidth[which],
                    color=color[which]
                )

                ax.tick_params(
                    which=which,
                    axis=axe,
                    color=color[which],
                    bottom=False,
                    top=False,
                    left=False,
                    right=False
                )

        ax.set_xticklabels([])
        ax.set_yticklabels([])

        # SET X, Y limits
        ax.set_ylim([0, 15])
        ax.set_xlim([-0.25, 6.75])

        plt.tight_layout()
        plt.margins(x=0)

        props = dict(boxstyle='round', alpha=0)

        ax.text(0.05, 0.95, textstr_left, transform=ax.transAxes, fontsize=5, fontweight='light',
                verticalalignment='top', bbox=props, family='monospace')

        ax.text(0.80, 0.95, textstr_right, transform=ax.transAxes, fontsize=5, fontweight='light',
                verticalalignment='top', bbox=props)

        ax.text(0.75, 0.05, textstr_btn_right, transform=ax.transAxes, fontsize=5, fontweight='light',
                verticalalignment='top', bbox=props)

        ax.text(0.41, 0.95, 'Hospital: ' + hospital, transform=ax.transAxes, fontsize=5, fontweight='light',
                verticalalignment='top', bbox=props)  # set end time

        ax.minorticks_on()
        counter = 6

        for s_data in data_arr:
            data = s_data['data']
            if counter % 2 == 0:
                t = np.arange(3.5, 6.5, frequency, dtype=float)
                data = [(x + (counter - 1) * 2) for x in data]
                ax.text(3.5, int((sum(data) / len(data))) + 2, s_data['stream'].split('_')[1], fontsize=5,
                        fontweight='light')
            else:
                t = np.arange(start_time, end_time, frequency, dtype=float)
                data = [(x + counter * 2) for x in data]
                ax.text(0.5, int((sum(data) / len(data))) + 2, s_data['stream'].split('_')[1], fontsize=5,
                        fontweight='light')
            # ****** Data correction. ******
            if len(data) > time * 250:
                data = data[0: (time * 250)]
            elif len(data) < time * 250:
                lag = [None] * (time * 250 - len(data))
                data.extend(lag)
            # Turn on the minor TICKS, which are required for the minor GRID
            color = 'k'
            plt.plot(t, data, linewidth=0.3, color=color)
            counter -= 1

        plt.savefig(image_name, format='jpg', bbox_inches='tight', pad_inches=0, dpi=300)
        plt.cla()
        plt.close(fig)
        image = Image.open(image_name)
        pdf_bytes = img2pdf.convert(image.filename)
        file = open(pdf_name, "wb")
        file.write(pdf_bytes)
        image.close()
        file.close()
        return True
    except Exception as e:
        raise e
        return False

