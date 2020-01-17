# -*- coding: utf-8 -*-
# This code implements rest ws which exposes APIs to generate standard ECG Report
# Example:
#       $ python app.py
# Author: Arnab Chakraborty
from flask import Flask, request, send_file
from flask_cors import CORS
from services.quick_report_ecg_graph_service import generate_ecg

application = Flask(__name__)
CORS(application)


# API to generate pretty report and quick report
@application.route("/app/ecg", methods=['GET'])
def generate_pdf_report():
    status = generate_ecg()
    if status:
        return 'Report Generated!', 200
    else:
        return 'Report was not generated due to internal error!', 500


if __name__ == '__main__':
    application.run(host='0.0.0.0', port=8080, debug=False)
