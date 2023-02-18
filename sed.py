import re
import functools

from telebot.types import Message

sed_regex = r's/(.*?)/(.*?)/(.*)?'
flag_replacements = {'g': 0, 'a': re.A, 'i': re.I, 'm': re.M, 's': re.S, 'x': re.X}

class Sed:
  """
  Processes a message in the format of "s/thing/replacement/flags?", taking the message this one is a reply to and replacing "thing" with "replacement". Supports regex (python edition). Flags are standard regex flags: g, a, i, m, s, x are supported.
  """

  @staticmethod
  def is_valid(message: Message) -> bool:
    """
    Checks if message satisfies the requirements to be processed with sed, this includes format (s/thing/replacement/flags?) and a replied-to message.
    """
    return re.match(sed_regex, message.text) is not None and message.reply_to_message is not None

  def __init__(self, message: Message):
    """
    Creates instance of Sed based on the message, validating it in the process with Sed.is_valid. If the message is invalid, throws ValueError.
    """
    if not Sed.is_valid(message):
      raise ValueError('Invalid message format: should be a reply and be represented as "s/thing/replacement/[optional flags]".')
    self.thing, self.replacement, self.flag_string = re.match(sed_regex, message.text).groups()
    self.source_text = message.reply_to_message.text

  def calc(self) -> str:
    """
    Returns the edited original message's replied-to message.
    """
    flags = functools.reduce(lambda acc, flag: acc | (flag_replacements[flag] or 0), self.flag_string, 0)
    count = 0 if 'g' in self.flag_string else 1
    try:
      return re.sub(self.thing, self.replacement, self.source_text, count=count, flags=flags)
    except Exception as ex:
      print(ex)
      return f"Cannot replace {self.thing} with {self.replacement}: {ex}.\n\nTry looking for an error in your input."
