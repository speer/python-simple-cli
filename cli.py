#!/usr/bin/python

import argparse
import re
import sys

VERSION = '0.0.1'

class Action(object):
  @staticmethod
  def instantiate():
    parser = argparse.ArgumentParser(description='CLI', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    subparsers = parser.add_subparsers(dest='action', help='CLI Action')
    for action in Action.__subclasses__():
      subparser = subparsers.add_parser(re.sub(r'(?<!^)(?=[A-Z])', '-', action.__name__).lower(), help=action.DESCRIPTION, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
      Action.set_default_arguments(subparser)
      action.set_arguments(subparser)
    parser.add_argument('--version', action='version',version=VERSION)
    args = parser.parse_args()
    return getattr(sys.modules[__name__],''.join(x.capitalize() or '-' for x in args.action.split('-')))(args)

  @staticmethod
  def set_default_arguments(parser):
    pass

  def __init__(self, args):
    self.args = args

class ActionException(Exception):
  pass

class SayHello(Action):
  DESCRIPTION='Say Hello'

  @staticmethod
  def set_arguments(parser):
    parser.add_argument('--msg', help='Override message', default='Hello')

  def execute(self):
    return self.args.msg

if __name__ == '__main__':
  sys.tracebacklimit = 0
  action = Action.instantiate()
  try:
    print action.execute()
  except ActionException as ex:
    print(ex)
    sys.exit(1)
