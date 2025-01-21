class Serializer:
    def serialize(self):
        obj = {}
        class_attributes = self.to_dict()
        for key in class_attributes:
            obj[key] = getattr(self, key)
        return obj
    
    def to_dict(self):
        class_attributes = self._sa_class_manager.mapper.column_attrs.keys()
        return class_attributes
    