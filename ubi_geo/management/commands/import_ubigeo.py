from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from pathlib import Path
import csv

from ubi_geo.models import Country, Region, Province, District

def getv(row, *cands):
    for k in cands:
        if k in row:
            v = (row.get(k) or "").strip()
            if v != "":
                return v
    return ""

class Command(BaseCommand):
    help = "Importa countries, regions, provinces y districts desde CSV (';'). Usa códigos solo para vincular."

    def add_arguments(self, parser):
        parser.add_argument("--path", type=str, default="db",
                            help="Carpeta con countries.csv, regions.csv, provinces.csv, districts.csv")
        parser.add_argument("--country-iso2", type=str, required=True,
                            help="ISO2 del país a usar para todas las regiones (ej: PE)")
        parser.add_argument("--truncate", action="store_true",
                            help="Borra Region/Province/District antes de importar")

    def handle(self, *args, **opt):
        base = Path(opt["path"]).resolve()
        files = {
            "countries": base / "countries.csv",
            "regions": base / "regions.csv",
            "provinces": base / "provinces.csv",
            "districts": base / "districts.csv",
        }
        for name, p in files.items():
            if not p.exists():
                raise CommandError(f"No se encontró {name}: {p}")

        iso2 = (opt["country_iso2"] or "").upper().strip()

        if opt["truncate"]:
            self.stdout.write(self.style.WARNING("Truncando Region/Province/District…"))
            District.objects.all().delete()
            Province.objects.all().delete()
            Region.objects.all().delete()

        with transaction.atomic():
            # COUNTRIES
            self.stdout.write("Importando countries…")
            iso2_map = {}
            with files["countries"].open(encoding="utf-8", newline="") as f:
                r = csv.DictReader(f, delimiter=";")
                c_new = c_upd = c_skip = 0
                for row in r:
                    name = getv(row, "name", "Name")
                    phone_code = getv(row, "phone_code", "PhoneCode") or None
                    ISO2 = getv(row, "ISO2", "iso2").upper()
                    if not name:
                        c_skip += 1
                        continue
                    obj, created = Country.objects.update_or_create(
                        **({"ISO2": ISO2} if ISO2 else {"name": name}),
                        defaults={"name": name, "phone_code": phone_code, "ISO2": ISO2 or None},
                    )
                    if ISO2:
                        iso2_map[ISO2] = obj
                    c_new += int(created)
                    c_upd += int(not created)
                self.stdout.write(f"Countries: +{c_new} upd:{c_upd} skip:{c_skip}")

            try:
                country = iso2_map.get(iso2) or Country.objects.get(ISO2=iso2)
            except Country.DoesNotExist:
                raise CommandError(f"No existe Country ISO2={iso2}")

            # REGIONS
            self.stdout.write("Importando regiones…")
            code_to_region = {}
            with files["regions"].open(encoding="utf-8", newline="") as f:
                r = csv.DictReader(f, delimiter=";")
                n = u = s = 0
                for row in r:
                    code = getv(row, "code", "ubigeo_code")
                    name = getv(row, "name", "Nombre")
                    if not name:
                        s += 1; continue
                    obj, created = Region.objects.update_or_create(
                        name=name, country=country, defaults={}
                    )
                    if code:
                        code_to_region[code] = obj
                    n += int(created); u += int(not created)
                self.stdout.write(f"Regions: +{n} upd:{u} skip:{s}")

            # PROVINCES
            self.stdout.write("Importando provincias…")
            code_to_province = {}
            with files["provinces"].open(encoding="utf-8", newline="") as f:
                r = csv.DictReader(f, delimiter=";")
                n = u = s = 0
                for row in r:
                    code = getv(row, "code", "ubigeo_code")
                    name = getv(row, "name", "Nombre")
                    region_ref = getv(row, "region_code", "region_id")
                    region = code_to_region.get(region_ref)
                    if not (name and region):
                        s += 1; continue
                    obj, created = Province.objects.update_or_create(
                        name=name, region=region, defaults={}
                    )
                    if code:
                        code_to_province[code] = obj
                    n += int(created); u += int(not created)
                self.stdout.write(f"Provinces: +{n} upd:{u} skip:{s}")

            # DISTRICTS
            self.stdout.write("Importando distritos…")
            n = u = s = 0
            with files["districts"].open(encoding="utf-8", newline="") as f:
                r = csv.DictReader(f, delimiter=";")
                for row in r:
                    name = getv(row, "name", "Nombre")
                    prov_ref = getv(row, "province_code", "province_id")
                    province = code_to_province.get(prov_ref)
                    if not (name and province):
                        s += 1; continue
                    _, created = District.objects.update_or_create(
                        name=name, province=province, defaults={}
                    )
                    n += int(created); u += int(not created)
            self.stdout.write(f"Districts: +{n} upd:{u} skip:{s}")

        self.stdout.write(self.style.SUCCESS("Importación completada ✔"))
