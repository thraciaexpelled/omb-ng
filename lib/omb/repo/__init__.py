import os
import re
import pygit2

from lib.status import status, status_tags, status_prompt_type

# Wrapper for pygit2

# CamelCase for exceptions because that's the fucking standard
class InvalidRepoURLError(Exception):
  def __init__(self, faulty_url: str, *args):
    super().__init__(args)
    self.faulty_url = faulty_url

  def __str__(self):
    return 'url is invalid (url: %s)' % self.faulty_url

class InternalGitError(Exception):
  def __init__(self, e, url: str = "", *args):
    super().__init__(args)
    self.e = e
    self.url = url

  def __str__(self):
    return 'cannot clone %s; (libgit2 error: %s)' % (url, e)

class SystemError(Exception):
  def __init__(self, e, *args):
    super().__init__(args)
    self.e = e

  def __str__(self):
    return 'system error: %s' % e

class repo:
  def __init__(self, url: str, test_mode: bool = False):
    self.url = url                                    
    self.test_mode = test_mode
    self.status = status()                                                
    self.url_regex = re.compile(
      r'^(?:http|ftp)s?://' # http:// or https://
      r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
      r'localhost|' #localhost...
      r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
      r'(?::\d+)?' # optional port
      r'(?:/?|[/?]\S+)$', re.IGNORECASE
    )
    self.repo_name = os.basename(url) # basenaming also works for urls lol

    if not re.match(url_regex, url):
      self.status.push(status_tags.fail, '(internal) given url (%s) is invalid')
      if self.test_mode:
        self.status.push(status_tags.ok, '(internal) test_mode is active; ignoring')
        return
      raise InvalidRepoURL(url)

    try:
      os.mkdir(os.path.join('/tmp', 'omb-ng'))
    except Exception as e:
      raise SystemError(e)

  def clone(self, path: str = ''):
    if not path:
      path = os.path.join('/tmp', 'omb-ng', self.repo_name)

    try:
      pygit2.clone_repository(url, path)
    except Exception as e:
      raise InternalGitError(e, url)

  # TODOOOOOOOOOOOOOOOOOOOOOOo 