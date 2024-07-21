
class Router:
    db_dict = {
        "blog": {
            "default": "blog"
        }
    }
    @staticmethod
    def read_or_write(app_label, model_name):
        if app_label in Router.db_dict:
            detail = Router.db_dict[app_label]
            if model_name != None and model_name in detail:
                return detail[app_label]
            else:
                return detail["default"]
        return None
    
    @staticmethod
    def migrate(db, app_label, model_name=None, **hints):
        if app_label in Router.db_dict:
            detail = Router.db_dict[app_label]
            if model_name != None and model_name in detail:
                return db == detail[app_label]
            else:
                return db == detail["default"]
        return db == "default"

class DefaultRouter:
    def db_for_read(self, model, **hints):
        """
        根据模型读取操作选择数据库。
        """
        model_name = model._meta.model_name
        app_label = model._meta.app_label
        return Router.read_or_write(app_label, model_name)

    def db_for_write(self, model, **hints):
        """
        根据模型写入操作选择数据库。
        """
        model_name = model._meta.model_name
        app_label = model._meta.app_label
        return Router.read_or_write(app_label, model_name)

    def allow_relation(self, obj1, obj2, **hints):
        """
        确定是否允许两个模型实例之间的关系。
        """
        # 通常，我们希望关系能够跨数据库存在，所以返回True
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        决定是否允许在指定数据库上运行迁移。
        """
        return Router.migrate(db, app_label, model_name=None, **hints)