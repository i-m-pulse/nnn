# -*- coding: utf-8 -*-

import six

# TODO: datetime support

###
### DO NOT CHANGE THIS FILE
###
### The code is auto generated, your change will be overwritten by
### code generating.
###

base_path = '/v1'


DefinitionsPersonality = {u'type': u'object', u'properties': {u'influence': {u'type': u'number'}, u'dominance': {u'type': u'number'}, u'conscientiousness': {u'type': u'number'}, u'steadiness': {u'type': u'number'}}}
DefinitionsResume = {u'type': u'object', u'properties': {u'skills': {u'items': {u'type': u'string'}, u'type': u'array'}, u'education': {u'items': {u'type': u'string'}, u'type': u'array'}, u'id': {u'type': u'integer', u'format': u'int64'}, u'experience': {u'items': {u'type': u'string'}, u'type': u'array'}}}
DefinitionsDiversityscore = {u'type': u'object', u'properties': {u'personality': {u'type': u'object', u'properties': {u'influence': {u'type': u'number'}, u'dominance': {u'type': u'number'}, u'conscientiousness': {u'type': u'number'}, u'steadiness': {u'type': u'number'}}}}}

validators = {
    ('resume', 'POST'): {'form': {'required': [], 'properties': {u'upfile': {u'type': u'file', u'description': u'The file to upload.'}}}},
    ('diversity_score', 'POST'): {'form': {'required': [], 'properties': {u'upfile': {u'type': u'file', u'description': u'The file to upload.'}}}},
}

filters = {
    ('resume', 'POST'): {201: {'headers': None, 'schema': {u'type': u'object', u'properties': {u'skills': {u'items': {u'type': u'string'}, u'type': u'array'}, u'education': {u'items': {u'type': u'string'}, u'type': u'array'}, u'id': {u'type': u'integer', u'format': u'int64'}, u'experience': {u'items': {u'type': u'string'}, u'type': u'array'}}}}, 400: {'headers': None, 'schema': None}},
    ('diversity_score', 'POST'): {201: {'headers': None, 'schema': {u'type': u'object', u'properties': { u'personality': {u'type': u'object', u'properties': {u'influence': {u'type': u'number'}, u'dominance': {u'type': u'number'}, u'conscientiousness': {u'type': u'number'}, u'steadiness': {u'type': u'number'}}}}}}},
}

scopes = {
}


class Security(object):

    def __init__(self):
        super(Security, self).__init__()
        self._loader = lambda: []

    @property
    def scopes(self):
        return self._loader()

    def scopes_loader(self, func):
        self._loader = func
        return func

security = Security()


def merge_default(schema, value, get_first=True):
    # TODO: more types support
    type_defaults = {
        'integer': 9573,
        'string': 'something',
        'object': {},
        'array': [],
        'boolean': False
    }

    results = normalize(schema, value, type_defaults)
    if get_first:
        return results[0]
    return results


def normalize(schema, data, required_defaults=None):
    if required_defaults is None:
        required_defaults = {}
    errors = []

    class DataWrapper(object):

        def __init__(self, data):
            super(DataWrapper, self).__init__()
            self.data = data

        def get(self, key, default=None):
            if isinstance(self.data, dict):
                return self.data.get(key, default)
            return getattr(self.data, key, default)

        def has(self, key):
            if isinstance(self.data, dict):
                return key in self.data
            return hasattr(self.data, key)

        def keys(self):
            if isinstance(self.data, dict):
                return list(self.data.keys())
            return list(getattr(self.data, '__dict__', {}).keys())

        def get_check(self, key, default=None):
            if isinstance(self.data, dict):
                value = self.data.get(key, default)
                has_key = key in self.data
            else:
                try:
                    value = getattr(self.data, key)
                except AttributeError:
                    value = default
                    has_key = False
                else:
                    has_key = True
            return value, has_key

    def _merge_dict(src, dst):
        for k, v in six.iteritems(dst):
            if isinstance(src, dict):
                if isinstance(v, dict):
                    r = _merge_dict(src.get(k, {}), v)
                    src[k] = r
                else:
                    src[k] = v
            else:
                src = {k: v}
        return src

    def _normalize_dict(schema, data):
        result = {}
        if not isinstance(data, DataWrapper):
            data = DataWrapper(data)

        for _schema in schema.get('allOf', []):
            rs_component = _normalize(_schema, data)
            _merge_dict(result, rs_component)

        for key, _schema in six.iteritems(schema.get('properties', {})):
            # set default
            type_ = _schema.get('type', 'object')

            # get value
            value, has_key = data.get_check(key)
            if has_key:
                result[key] = _normalize(_schema, value)
            elif 'default' in _schema:
                result[key] = _schema['default']
            elif key in schema.get('required', []):
                if type_ in required_defaults:
                    result[key] = required_defaults[type_]
                else:
                    errors.append(dict(name='property_missing',
                                       message='`%s` is required' % key))

        additional_properties_schema = schema.get('additionalProperties', False)
        if additional_properties_schema is not False:
            aproperties_set = set(data.keys()) - set(result.keys())
            for pro in aproperties_set:
                result[pro] = _normalize(additional_properties_schema, data.get(pro))

        return result

    def _normalize_list(schema, data):
        result = []
        if hasattr(data, '__iter__') and not isinstance(data, dict):
            for item in data:
                result.append(_normalize(schema.get('items'), item))
        elif 'default' in schema:
            result = schema['default']
        return result

    def _normalize_default(schema, data):
        if data is None:
            return schema.get('default')
        else:
            return data

    def _normalize(schema, data):
        if schema is True or schema == {}:
            return data
        if not schema:
            return None
        funcs = {
            'object': _normalize_dict,
            'array': _normalize_list,
            'default': _normalize_default,
        }
        type_ = schema.get('type', 'object')
        if type_ not in funcs:
            type_ = 'default'

        return funcs[type_](schema, data)

    return _normalize(schema, data), errors
