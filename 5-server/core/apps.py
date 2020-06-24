from django.apps import AppConfig
import os
import pickle

class CoreConfig(AppConfig):
    name = 'core'
    module_dir = os.path.dirname(__file__)  # get current directory
    file_path = os.path.join(module_dir, 'model.pckl')
    scaler_file_path = os.path.join(module_dir, 'scaler.pckl')

    with open(file_path, 'rb') as file:
        model = pickle.load(file)
    with open(scaler_file_path, 'rb') as file:
        scaler = pickle.load(file)
    model._make_predict_function()

