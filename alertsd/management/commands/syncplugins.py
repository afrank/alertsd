from django.core.management.base import BaseCommand, CommandError
from django.db.utils import OperationalError
from alertsd.models import Plugin

from os import listdir
from os.path import isfile
import re

class Command(BaseCommand):
    help = 'Finds plugins and creates model objects for them'

    def handle(self, *args, **options):
        try:
            plugins = list(Plugin.objects.all())
        except OperationalError:
            raise CommandError('Plugins table not found, did you run syncdb?')
        names = [ f.name for f in plugins ]
        for f in listdir("plugins"):
            if isfile("plugins/%s" % f):
                params = ""
                lines = open("plugins/%s" % f).read().split("\n")
                for l in lines:
                    ret = re.match("^.*required_parameters:(.*)$",l)
                    if ret is not None:
                        params = str(ret.group(1)).strip()
                        break
                if f not in names:
                    Plugin.objects.create(name=f,path=f,required_parameters=params)
                    self.stdout.write("Created %s" % f)
                else:
                    plugin = Plugin.objects.get(name=f)
                    if plugin.required_parameters != params:
                        plugin.required_parameters = params
                        plugin.save()
                        self.stdout.write("Updated %s" % f)
