class repo_config_parser:
  def __init__(self, filepath: str):
    self.filepath = filepath
    with open(self.filepath, 'r') as file:
      self.source = file.read()

  def decode(self) -> dict:
    result: dict = {}
    current_section = None
    
    for line in self.source.splitlines():
      line = line.strip()
      if not line or line.startswith('#') or line.startswith(';'):
        continue

      if line.startswith('[') and line.endswith(']'):
        current_section = line[1:-1].strip()
        result[current_section] = {}
        continue
      
      if '=' in line:
        key, val = line.split('=', 1)
        key = key.strip()
        val = val.strip()
        
        if current_section is not None:
          result[current_section][key] = val
        else:
          result[key] = val

    return result
