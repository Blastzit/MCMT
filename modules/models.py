from django.db import models, connections

class Module(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=100)
    recommended_prerequisites = models.TextField(null=True, blank=True)
    summary = models.TextField(null=True, blank=True)
    term = models.CharField(max_length=20)
    lecturer = models.CharField(max_length=100)
    assessments = models.TextField(null=True, blank=True)
    learning_outcome = models.TextField(null=True, blank=True)
    module_preparation = models.TextField(null=True, blank=True)
    category = models.CharField(max_length=100, null=True, blank=True)
    programming = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = 'modules'

    def __str__(self):
        return self.name
    
class Assessment(models.Model):
    module_name = models.CharField(max_length=255)
    coursework_name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    value = models.DecimalField(max_digits=5, decimal_places=2)
    submit_work_to = models.CharField(max_length=255)

    class Meta:
        db_table = 'assessments'

    def __str__(self):
        return f"{self.module_name} - {self.coursework_name}"

class KeywordManager(models.Manager):
    def get_keywords_for_module(self, module_code):
        from .utils import get_short_module_code

        module_code = get_short_module_code(module_code)
        
        with connections['keywords'].cursor() as cursor:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=%s", [module_code])
            if cursor.fetchone() is None:
                return []
            
            cursor.execute(f"SELECT big_topic, topic_content, keywords, examinable FROM {module_code}")
            rows = cursor.fetchall()
            keywords = []
            for row in rows:
                keyword = {
                    'big_topic': row[0],
                    'topic_content': row[1],
                    'keywords': row[2],
                    'examinable': row[3]
                }
                keywords.append(keyword)
        return keywords

class Keyword(models.Model):
    big_topic = models.CharField(max_length=255)
    topic_content = models.CharField(max_length=255)
    keywords = models.CharField(max_length=255)
    examinable = models.BooleanField(default=False)

    objects = KeywordManager()

    def __str__(self):
        return self.keywords