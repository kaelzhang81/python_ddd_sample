# coding=utf-8
"""Projections for tracking project management metrics such as lead time."""

class Role(object):
    """the role of dci
    """

    @staticmethod
    def convert(root, role):
        """convert ar to role"""
        for name in dir(root):
            obj = getattr(root, name)
            if obj.__class__.__name__ == role:
                return obj

    @staticmethod
    def add_role(root, role):
        """add role to ar"""
        for attr in dir(role):
            if hasattr(root, attr):
                continue
            setattr(root, attr, getattr(role, attr))
