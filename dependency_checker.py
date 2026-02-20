import sys

if __name__ == '__main__':
  try:
    import pygit2
  except Exception as e:
    sys.exit(1)
