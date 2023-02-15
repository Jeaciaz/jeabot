import re
import functools

sed_regex = r's/(.*?)/(.*?)/(.*)?'

def calc_flags(flags):
  flag_replacements = {'g': 0, 'a': re.A, 'i': re.I, 'm': re.M, 's': re.S, 'x': re.X}
  return functools.reduce(lambda acc, flag: acc | (flag_replacements[flag] or 0), flags, 0)

def sed(message):
  sed_help =  "To use sed, reply to a message with 's/thing/replacement/' to replace thing with replacement."
  re_match = re.match(sed_regex, message.text)

  if message.reply_to_message is None or re_match is None:
    bot.reply_to(message, sed_help)
    return

  thing, replacement, flags = re_match and re_match.groups()

  count = 0 if 'g' in flags else 1
  flag_num = calc_flags(flags)

  try:
    text = re.sub(thing, replacement, message.reply_to_message.text, count=count, flags=flag_num)
    return text
  except Exception as ex:
    print(ex)
    return f"""Cannot replace {thing} with {replacement}: {ex}.

Try looking for an error in your input."""
