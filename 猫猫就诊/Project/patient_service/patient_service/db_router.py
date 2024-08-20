class AdministratorDBRouter:
    def db_for_read(self, model, **hints):
        """尝试从 'administrator_service' 数据库中读取数据"""
        if model._meta.app_label == 'administrator':
            return 'administrator_service'
        return None

    def db_for_write(self, model, **hints):
        """尝试写入数据到 'default' 数据库"""
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """允许模型之间的关系"""
        if obj1._meta.app_label == 'administrator' or obj2._meta.app_label == 'administrator':
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """仅允许 'default' 数据库迁移"""
        if app_label == 'administrator':
            return db == 'administrator_service'
        return None

class DoctorDBRouter:
    def db_for_read(self, model, **hints):
        """尝试从 'doctor_service' 数据库中读取数据"""
        if model._meta.app_label == 'doctor':
            return 'doctor_service'
        return None

    def db_for_write(self, model, **hints):
        """尝试写入数据到 'default' 数据库"""
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """允许模型之间的关系"""
        if obj1._meta.app_label == 'doctor' or obj2._meta.app_label == 'doctor':
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """仅允许 'default' 数据库迁移"""
        if app_label == 'doctor':
            return db == 'doctor_service'
        return None