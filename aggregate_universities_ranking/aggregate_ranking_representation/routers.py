from django.conf import settings

class MigrationRouter(object):
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if db == 'aggregateranking' and ((model_name == 'university') or (model_name == 'rankingdescription') or (model_name == 'rankingvalue')):
            return True
        elif db == 'default' and ((model_name == 'universityname') or (model_name == 'rankingname') or (model_name == 'rankingvalue')):
            return True
        else:
            return False
