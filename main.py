from typing import *
from dataclasses import dataclass
import unittest
import sys
import string
sys.setrecursionlimit(10**6)

class Tests(unittest.TestCase):
  pass

IntList : TypeAlias = Union['LLNode', None]
@dataclass(frozen=True)
class LLNode:
  val : int
  next : IntList

@dataclass
class WordLines:
  key : str
  to_mutate : IntList

WordLinesList : TypeAlias = Union[WordLines, None]
@dataclass
class HashTable:
  arr : List[WordLines]
  count : int

# Return the hash code of 's' 
def hash_fn(s:str) -> int:
  pass

# Make a fresh hash table with the given number of bins 'size', contains no elements
def make_hash(size:int) -> HashTable:
  pass

#Return the number of bins in 'ht'
def hash_size(ht:HashTable) -> int:
  pass

#Return the number of elements(key-value pairs) in 'ht'
def hash_count(ht:HashTable) -> int:
  pass

# Return whether 'ht' contains a mapping for the given 'word'.
def has_key(ht: HashTable, word: str) -> bool:
  pass
# Return the line numbers associated with the key 'word' in 'ht'.
# The returned list should not contain duplicates, but need not be sorted.
def lookup(ht: HashTable, word: str) -> List[int]:
  pass
# Record in 'ht' that 'word' has an occurrence on line 'line'.
def add(ht: HashTable, word: str, line: int) -> None:
  pass
# Return the words that have mappings in 'ht'.
# The returned list should not contain duplicates, but need not be sorted.
def hash_keys(ht: HashTable) -> List[str]:
  pass
# Given a hash table 'stop_words' containing stop words as keys, plus
# a sequence of strings 'lines' representing the lines of a document,
# return a hash table representing a concordance of that document.
def make_concordance(stop_words: HashTable, lines: List[str]) -> HashTable:
  pass
# Given an input file path, a stop-words file path, and an output file path,
# overwrite the indicated output file with a sorted concordance of the input file.
def full_concordance(in_file: str, stop_words_file: str, out_file: str) -> None:
  pass
if(__name__ == '__main__'):
  unittest.main()
