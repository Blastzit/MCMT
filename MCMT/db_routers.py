class ModulesRouter:
    """
    A router to control all database operations on models in the
    modules application.
    """
    def db_for_read(self, model, **hints):
        """
        Attempts to read modules models go to modules db.
        """
        if model._meta.app_label == 'modules':
            return 'modules'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write modules models go to modules db.
        """
        if model._meta.app_label == 'modules':
            return 'modules'
        return None

    def db_for_migrate(self, db, app_label, model_name=None, **hints):
        """
        Ensure that the modules app's models get created on the right db.
        """
        if app_label == 'modules':
            return db == 'modules'
        return None

class AlumniRouter:
    """
    A router to control all database operations on models in the
    alumni application.
    """
    def db_for_read(self, model, **hints):
        """
        Attempts to read alumni models go to alumni db.
        """
        if model._meta.app_label == 'alumni':
            return 'alumni'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write alumni models go to alumni db.
        """
        if model._meta.app_label == 'alumni':
            return 'alumni'
        return None

    def db_for_migrate(self, db, app_label, model_name=None, **hints):
        """
        Ensure that the alumni app's models get created on the right db.
        """
        if app_label == 'alumni':
            return db == 'alumni'
        return None

class DefaultRouter:
    """
    A router to control all database operations on models in the
    default application.
    """
    def db_for_read(self, model, **hints):
        """
        Attempts to read default models go to default db.
        """
        if model._meta.app_label not in ['modules', 'alumni']:
            return 'default'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write default models go to default db.
        """
        if model._meta.app_label not in ['modules', 'alumni']:
            return 'default'
        return None

    def db_for_migrate(self, db, app_label, model_name=None, **hints):
        """
        Ensure that the default app's models get created on the right db.
        """
        if app_label not in ['modules', 'alumni']:
            return db == 'default'
        return None