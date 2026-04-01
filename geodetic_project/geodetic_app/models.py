from django.contrib.gis.db import models

class Point(models.Model):
    """Modèle pour les points géodésiques"""
    id_0 = models.AutoField(primary_key=True)
    geom = models.PointField(srid=4326, verbose_name="Géométrie")
    id = models.BigIntegerField(null=True, blank=True, verbose_name="ID original")
    nom = models.CharField(max_length=254, null=True, blank=True, verbose_name="Nom")
    est = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True, verbose_name="Est")
    nord = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True, verbose_name="Nord")
    altitude = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True, verbose_name="Altitude")
    ordre = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Ordre")
    localite = models.CharField(max_length=254, null=True, blank=True, verbose_name="Localité")
    photo = models.CharField(max_length=100, null=True, blank=True, verbose_name="Photo")

    class Meta:
        db_table = 'points'
        managed = False  # Django ne gère pas la table, elle existe déjà
        verbose_name = "Point géodésique"
        verbose_name_plural = "Points géodésiques"

    def __str__(self):
        return self.nom or f"Point {self.id_0}"

    @property
    def latitude(self):
        """Retourne la latitude depuis la géométrie"""
        return self.geom.y if self.geom else None

    @property
    def longitude(self):
        """Retourne la longitude depuis la géométrie"""
        return self.geom.x if self.geom else None