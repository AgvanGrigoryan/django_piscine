from django.core.management.base import BaseCommand, CommandError
from django.core.management.color import color_style
from pathlib import Path
from django.apps import apps
from django.db import DatabaseError
import json
from ex09.models import Planets

class Command(BaseCommand):
    help = "This is help message to my custom command"

    @staticmethod
    def __find_planet_by_pk(data, pk_to_find):
        return Planets.objects.get(pk=pk_to_find)

    def __import_in_model(self, data, model_name, counter):
        for part in data:
            app_label, part_model = part['model'].split('.')
            if part_model != model_name:
                continue
            try:
                modelClass = apps.get_model(app_label, part_model)
                fields = part['fields']
                if part_model == 'people':
                    fields['homeworld'] = self.__find_planet_by_pk(data, fields['homeworld'])
                modelClass.objects.create(pk=part['pk'], **fields)
                counter['OK'] += 1
            except Exception as e:
                counter['KO'] += 1
                self.stdout.write(self.style.ERROR(f"{part_model}:{fields['name']}:KO"))
                self.stdout.write(self.style.WARNING(f"{e}\n"))

    def handle(self, *args, **options):
        counter = {'OK': 0, 'KO': 0}
        style = color_style()
        style.MY_BLUE = style.MIGRATE_HEADING

        filename = "ex09_initial_data.json"
        file_path = Path(__file__).parent.parent.parent / "data" / filename
        
        if not file_path.exists():
            self.stderr.write(self.style.ERROR(f"File {filename} not found!"))
            return

        with open(file_path, 'r') as f:
            data = json.load(f)
            self.__import_in_model(data, 'planets', counter)
            self.__import_in_model(data, 'people', counter)

        self.stdout.write(style.MY_BLUE(f"OK: {counter['OK']}, KO: {counter['KO']}"))
        self.stdout.write(self.style.SUCCESS("DONE!"))