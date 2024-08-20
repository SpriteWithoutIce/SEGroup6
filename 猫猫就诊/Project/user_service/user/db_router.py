class PatientDBRouter:
    def db_for_read(self, model, **hints):
        """尝试从 'patient_service' 数据库中读取数据"""
        if model._meta.app_label == 'patient':
            return 'patient_service'
        return None

    def db_for_write(self, model, **hints):
        """尝试写入数据到 'patient_service' 数据库"""
        if model._meta.app_label == 'patient':
            return 'patient_service'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """允许模型之间的关系"""
        if obj1._meta.app_label == 'patient' or obj2._meta.app_label == 'patient':
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """仅允许 'default' 数据库迁移"""
        if app_label == 'patient':
            return db == 'patient_service'
        return None