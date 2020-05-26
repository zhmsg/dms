# !/usr/bin/env python
# coding: utf-8

import trident.exceptions.validate as ex

__author__ = 'zhouhenglc'


class ValidateResult(object):

    def __init__(self, v_result=None, new_value=None, sub_error=False):
        self.v_result = v_result
        self.sub_error = sub_error
        self.new_value = new_value


class Validator(object):
    mode = None
    sub_error = False

    def validate(self, value):
        return ValidateResult(None, None)

    @classmethod
    def parse(cls, obj_d):
        if not isinstance(obj_d, dict):
            return None
        mode = obj_d.get('mode', None)
        for sub_cls in cls.__subclasses__():
            if mode == sub_cls.mode:
                return sub_cls.parse(obj_d)
        return None


class ValidatorItem(Validator):
    mode = None

    def __init__(self, validator, convert_to=None, **kwargs):
        self.validator = validator
        self.kwargs = kwargs
        self.convert_to = convert_to

    def validate(self, value):
        v_result = self.validator(value, **self.kwargs)
        vr = ValidateResult(v_result, value)
        if self.convert_to:
            vr.new_value = self.convert_to(value)
        return vr

    @classmethod
    def parse(cls, obj_d):
        if not isinstance(obj_d, dict):
            return None
        if 'validator' in obj_d:
            return ValidatorItem(**obj_d)
        return None


class ValidatorList(Validator):
    mode = 'list'

    def __init__(self, fmt, **kwargs):
        self.fmt = fmt
        self.min_len = kwargs.pop('min_len', None)
        self.max_len = kwargs.pop('max_len', None)
        self.sub_error = False

    def validate(self, value):
        vr = ValidateResult()
        new_value = []
        if not isinstance(value, list):
            vr.v_result = 'Not list'
            return vr
        v_len = len(value)
        if self.min_len is not None:
            if v_len < self.min_len:
                vr.v_result = 'list length too small, must be at least %s' \
                              % self.min_len
                return vr
        if self.max_len is not None:
            if v_len > self.max_len:
                vr.v_result = 'list length too large, must be no larger ' \
                              'than %s' % self.max_len
                return vr
        for index in range(0, v_len):
            item = value[index]
            r = self.fmt.validate(item)
            if r.v_result is not None:
                vr.sub_error = True
                error_msg = '[%s]' % index
                if r.sub_error:
                    error_msg += r.v_result
                else:
                    error_msg += ': %s' % r.v_result
                vr.v_result = error_msg
                return vr
            new_value.append(r.new_value)
        vr.new_value = new_value
        return vr

    @classmethod
    def parse(cls, obj_d, log=None):
        if not isinstance(obj_d, dict):
            return None
        mode = obj_d.pop('mode', None)
        if mode != cls.mode:
            return None
        if 'fmt' not in obj_d:
            return None
        min_len = obj_d.pop('min_len', None)
        max_len = obj_d.pop('max_len', None)
        fmt = Validator.parse(obj_d['fmt'])
        if fmt is None:
            return None
        vl = cls(fmt, max_len=max_len, min_len=min_len)
        return vl


class ValidatorDict(Validator):
    mode = 'dict'

    def __init__(self, allow_extra_keys=False):
        self.required_keys = []
        self.validator_map = dict()
        self.allow_extra_keys = allow_extra_keys
        self.sub_error = False

    def add_item(self, key, required, fmt):
        if key in self.validator_map:
            raise ex.DuplicateValidatorKey(key)
        if required:
            self.required_keys.append(key)
        if not isinstance(fmt, Validator):
            raise ex.NotValidatorClass()
        self.validator_map[key] = fmt

    def validate(self, value):
        vr = ValidateResult()
        if not isinstance(value, dict):
            vr.v_result = 'Not dict'
            return vr
        extra_keys = set(value.keys()) - set(self.validator_map.keys())
        if extra_keys and not self.allow_extra_keys:
            vr.v_result = 'Not allow extra keys %s' % extra_keys
            return vr
        new_value = {}
        for key, fmt in self.validator_map.items():
            if key not in value:
                if key in self.required_keys:
                    vr.v_result = 'missing key: %s' % key
                    return vr
                continue
            r = fmt.validate(value[key])
            if r.v_result is not None:
                vr.sub_error = True
                error_msg = '["%s"]' % key
                if r.sub_error:
                    error_msg += r.v_result
                else:
                    error_msg += ': %s' % r.v_result
                vr.v_result = error_msg
                return vr
            new_value[key] = r.new_value
        vr.new_value = new_value
        return vr

    @classmethod
    def parse(cls, obj_d):
        if not isinstance(obj_d, dict):
            return None
        mode = obj_d.pop('mode', None)
        if mode != cls.mode:
            return None
        vd = cls()
        for k, v in obj_d.items():
            required = v.pop('required', False)
            fmt = Validator.parse(v)
            if fmt is None:
                return None
            vd.add_item(k, required, fmt)
        return vd


UNLIMITED = None


def validate_range(data, valid_values=None):
    min_value = valid_values[0]
    max_value = valid_values[1]
    try:
        data = int(data)
    except (ValueError, TypeError):
        msg = "'%s' is not an integer" % data
        return msg
    if min_value is not UNLIMITED and data < min_value:
        msg = "'%(data)s' is too small - must be at least " \
              "'%(limit)d'" % {'data': data, 'limit': min_value}
        return msg
    if max_value is not UNLIMITED and data > max_value:
        msg = "'%(data)s' is too large - must be no larger than " \
              "'%(limit)d'" % {'data': data, 'limit': max_value}
        return msg


def validate_enum(data, valid_values):
    if data not in valid_values:
        msg = "'%(data)s' is not valid, valid values: %(valid_values)s" % \
              {'data': data, 'valid_values': valid_values}
        return msg
