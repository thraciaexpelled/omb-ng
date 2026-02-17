import sys

class status_tags:
  ok = '\x1b[1;33m*\x1b[0m'
  give = '\x1b[1;32m+\x1b[0m'
  take = '\x1b[1;31m-\x1b[0m'
  fail = '\x1b[1;31m!\x1b[0m'
  doubt = '\x1b[1;34m?\x1b[0m'

class status_prompt_type:
  yes_no = 0
  anytype = 1

def repr_status_prompt_type(prompt_type: status_prompt_type) -> str:
  match prompt_type:
    case status_prompt_type.yes_no: return '[yn]'
    case status_prompt_type.anytype: return '[any]'

class status:
  def __init__(self):
    self.tags = status_tags

  def push(self, tag: status_tags, msg: str, 
    prompt: bool = False, prompt_type: status_prompt_type = status_prompt_type.yes_no
  ):
    if not prompt:
      sys.stdout.write(' %s  %s\n' % (tag, msg))
    else:
      try:
        return input(' %s  %s %s ' % (tag, msg, repr_status_prompt_type(prompt_type)))
      except (EOFError, KeyboardInterrupt):
        print()
        self.push(status_tags.fail, 'exit', False)
        sys.exit(-1)