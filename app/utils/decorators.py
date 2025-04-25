class classproperty(property):
    def __get__(self, obj, cls=None):
        return super(classproperty, self).__get__(cls)
    def __set__(self, obj, value):
        super(classproperty, self).__set__(type(obj), value)
    def __delete__(self, obj):
        super(classproperty, self).__delete__(type(obj))
