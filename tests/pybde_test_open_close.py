#!/usr/bin/env python
#
# Python-bindings open close testing program
#
# Copyright (C) 2011-2014, Joachim Metz <joachim.metz@gmail.com>
#
# Refer to AUTHORS for acknowledgements.
#
# This software is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this software.  If not, see <http://www.gnu.org/licenses/>.
#

import argparse
import sys

import pybde


def get_mode_string(mode):
  """Retrieves a human readable string representation of the access mode."""
  if mode == "r":
    mode_string = "read"
  elif mode == "w":
    mode_string = "write"
  else:
    mode_string = "unknown ({0:s})".format(mode)
  return mode_string


def pybde_test_single_open_close_file(
    filename, mode, password=None, recovery_password=None):
  if not filename:
    filename_string = "None"
  else:
    filename_string = filename

  print "Testing single open close of: {0:s} with access: {1:s}\t".format(
      filename_string, get_mode_string(mode))

  try:
    bde_volume = pybde.volume()

    if password:
      bde_volume.set_password(password)
    if recovery_password:
      bde_volume.set_recovery_password(recovery_password)

    bde_volume.open(filename, mode)
    bde_volume.close()

  except TypeError, exception:
    if (not filename and
        exception.message == "argument 1 must be string, not None"):
      pass

    else:
      print "(FAIL)"
      return False

  except ValueError, exception:
    if (mode == "w" and
        exception.message == "pybde_volume_open: unsupported mode: w."):
      pass

    else:
      print "(FAIL)"
      return False

  except:
    print "(FAIL)"
    return False

  print "(PASS)"
  return True


def pybde_test_multi_open_close_file(
    filename, mode, password=None, recovery_password=None):
  print "Testing multi open close of: {0:s} with access: {1:s}\t".format(
      filename, get_mode_string(mode))

  try:
    bde_volume = pybde.volume()

    if password:
      bde_volume.set_password(password)
    if recovery_password:
      bde_volume.set_recovery_password(recovery_password)

    bde_volume.open(filename, mode)
    bde_volume.close()
    bde_volume.open(filename, mode)
    bde_volume.close()

  except:
    print "(FAIL)"
    return False

  print "(PASS)"
  return True


def pybde_test_single_open_close_file_object(
    filename, mode, password=None, recovery_password=None):
  print ("Testing single open close of file-like object of: {0:s} with access: "
         "{1:s}\t").format(filename, get_mode_string(mode))

  try:
    file_object = open(filename, mode)
    bde_volume = pybde.volume()

    if password:
      bde_volume.set_password(password)
    if recovery_password:
      bde_volume.set_recovery_password(recovery_password)

    bde_volume.open_file_object(file_object, mode)
    bde_volume.close()

  except:
    print "(FAIL)"
    return False

  print "(PASS)"
  return True


def pybde_test_single_open_close_file_object_with_dereference(
    filename, mode, password=None, recovery_password=None):
  print ("Testing single open close of file-like object with dereference of: "
         "{0:s} with access: {1:s}\t").format(filename, get_mode_string(mode))

  try:
    file_object = open(filename, mode)
    bde_volume = pybde.volume()

    if password:
      bde_volume.set_password(password)
    if recovery_password:
      bde_volume.set_recovery_password(recovery_password)

    bde_volume.open_file_object(file_object, mode)
    del file_object
    bde_volume.close()

  except:
    print "(FAIL)"
    return False

  print "(PASS)"
  return True


def pybde_test_multi_open_close_file_object(
    filename, mode, password=None, recovery_password=None):
  print ("Testing multi open close of file-like object of: {0:s} with access: "
         "{1:s}\t").format(filename, get_mode_string(mode))

  try:
    file_object = open(filename, mode)
    bde_volume = pybde.volume()

    if password:
      bde_volume.set_password(password)
    if recovery_password:
      bde_volume.set_recovery_password(recovery_password)

    bde_volume.open_file_object(file_object, mode)
    bde_volume.close()
    bde_volume.open_file_object(file_object, mode)
    bde_volume.close()
  except:
    print "(FAIL)"
    return False

  print "(PASS)"
  return True


def main():
  args_parser = argparse.ArgumentParser(description=(
      "Tests open and close."))

  args_parser.add_argument(
      "source", nargs="?", action="store", metavar="FILENAME",
      default=None, help="The source filename.")

  args_parser.add_argument(
      "-p", dest="password", action="store", metavar="PASSWORD",
      default=None, help="The password.")

  args_parser.add_argument(
      "-r", dest="recovery_password", action="store", metavar="PASSWORD",
      default=None, help="The recovery password.")

  options = args_parser.parse_args()

  if not options.source:
    print u"Source value is missing."
    print u""
    args_parser.print_help()
    print u""
    return False

  if not pybde_test_single_open_close_file(
      options.source, "r", password=options.password,
      recovery_password=options.recovery_password):
    return False

  if not pybde_test_single_open_close_file(
      None, "r", password=options.password,
      recovery_password=options.recovery_password):
    return False

  if not pybde_test_single_open_close_file(
      options.source, "w", password=options.password,
      recovery_password=options.recovery_password):
    return False

  if not pybde_test_multi_open_close_file(
      options.source, "r", password=options.password,
      recovery_password=options.recovery_password):
    return False

  if not pybde_test_single_open_close_file_object(
      options.source, "r", password=options.password,
      recovery_password=options.recovery_password):
    return False

  if not pybde_test_single_open_close_file_object_with_dereference(
      options.source, "r", password=options.password,
      recovery_password=options.recovery_password):
    return False

  if not pybde_test_multi_open_close_file_object(
      options.source, "r", password=options.password,
      recovery_password=options.recovery_password):
    return False

  return True

if __name__ == "__main__":
  if not main():
    sys.exit(1)
  else:
    sys.exit(0)
