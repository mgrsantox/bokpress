from collections import Counter
from django.core.management.base import BaseCommand
import csv
import os.path
from django.core.files.images import ImageFile
from django.template.defaultfilters import slugify
from main import models


class Command(BaseCommand):
    help = 'Import product in Bokpress'

    def add_arguments(self, parser):
        parser.add_argument("csvfile", type=open)
        parser.add_argument("image_basedir", type=str)

    def handle(self, *args, **options):
        self.stdout.write("importing Product")
        c = Counter()
        reader = csv.DictReader(options.pop("csvfile"))
        for row in reader:
            product, created = models.Product.objects.get_or_create(
                name=row["name"], price=row["price"])
            for import_tag in row["tags"].split("|"):
                tag, tag_created = models.ProductTag.objects.get_or_create(
                    name=import_tag
                )
                product.tags.add(tag)
                c["tag"] += 1
                if tag_created:
                    c["tags_created"] += 1
            with open(
                os.path.join(options["image_basedir"],
                             row["image_filename"],),
                "rb",
            ) as f:
                image = models.ProductImage(
                    product=product,
                    image=ImageFile(
                        f, name=row["image_filename"]),

                )
                image.save()
                c["images"] += 1
                product.save()
                c["products"] += 1
                if created:
                    c["products_created"] += 1
            self.stdout.write(
                "Product processed = %d (created=%d)"
                % (c["products"], c["products_created"])
            )

            self.stdout.write(
                "Tags processed=%d (created=%d)"
                % (c["tags"], c["tags_created"])

            )
            self.stdout.write("Image processed=%d" % c["images"])
