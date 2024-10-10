class MainRouter:
    def db_for_read(self, model, **hints):
        if model._meta.model_name in ['module', 'assessment', 'alumni']:
            return 'main'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.model_name in ['module', 'assessment', 'alumni']:
            return 'main'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.model_name in ['module', 'assessment', 'alumni'] or obj2._meta.model_name in ['module', 'assessment', 'alumni']:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if model_name in ['module', 'assessment', 'alumni']:
            return 'main'
        return None


class KeywordsRouter:
    def db_for_read(self, model, **hints):
        if model._meta.model_name == 'keyword':
            module_code = hints.get('module_code')
            if module_code:
                return module_code
        return None

    def db_for_write(self, model, **hints):
        if model._meta.model_name == 'keyword':
            module_code = hints.get('module_code')
            if module_code:
                return module_code
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.model_name == 'keyword' or obj2._meta.model_name == 'keyword':
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if model_name == 'keyword':
            module_code = hints.get('module_code')
            if module_code:
                return module_code
        return None