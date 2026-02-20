from lib.status import status, status_tags, status_prompt_type
from lib.omb.repo.config_parser import repo_config_parser

class omb_repo:
  def __init__(self, arg):
    self.arg = arg
    self.status = status()
    self.config_parser = repo_config_parser('extra/dummy.omb_repo')

  def do(self) -> int:
    __import__('pprint').pprint(self.config_parser.decode())
    return 0