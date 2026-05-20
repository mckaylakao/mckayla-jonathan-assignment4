from typing import *
from dataclasses import dataclass
import unittest
import sys
import string
sys.setrecursionlimit(10**6)


IntList : TypeAlias = Union['LLNode', None]
@dataclass(frozen=True)
class LLNode:
  val : int
  next : IntList

@dataclass
class WordLines:
  key : str
  lines : IntList

WordLinesList : TypeAlias = Union['WordLinesNode', None]

@dataclass
class WordLinesNode:
  val : WordLines
  next : WordLinesList
@dataclass
class HashTable:
  arr : List[WordLinesList]
  count : int

max_load_factor : float = 1.0
bin_size : int = 128

# Return the hash code of 's' - mckayla
def hash_fn(s:str) -> int:
  sum : int = 0
  for char in s:
    sum = sum * 31 + ord(char)
  return sum
    
# Make a fresh hash table with the given number of bins 'size', contains no elements
def make_hash(size:int) -> HashTable:
  return HashTable([None]*size, 0)

#Return the number of bins in 'ht' - mckayla
def hash_size(ht:HashTable) -> int:
  return len(ht.arr)

#Return the number of elements(key-value pairs) in 'ht' 
def hash_count(ht:HashTable) -> int:
  return ht.count

# Return whether 'ht' contains a mapping for the given 'word'. - mckayla
def has_key(ht: HashTable, word: str) -> bool:
  index : int = hash_fn(word) % hash_size(ht)
  curr : WordLinesList = ht.arr[index]
  while curr is not None:
    if curr.val.key == word:
      return True
    curr = curr.next
  return False

# Returns 'WordLines' of 'word' inside 'ht'
def search_wll(ht: HashTable, word: str, wll: WordLinesList) -> WordLines:
  match wll:
    case None:
      raise KeyError('Word is not in table')
    case WordLinesNode(v, n):
      if v.key == word:
        return v
      else:
        return search_wll(ht, word, n)

# Return the line numbers associated with the key 'word' in 'ht'.
# The returned list should not contain duplicates, but need not be sorted.
def lookup(ht: HashTable, word: str) -> IntList:
  bin: int = hash_fn(word) % hash_size(ht)
  return search_wll(ht, word, ht.arr[bin]).lines

# Record in 'ht' that 'word' has an occurrence on line 'line'.- mckayla
def add(ht: HashTable, word: str, line: int) -> None:
  index: int = hash_fn(word) % hash_size(ht)
  curr : WordLinesList = ht.arr[index]

  while curr is not None:
    if curr.val.key == word:
      lines : IntList = curr.val.lines
      while lines is not None:
        if lines.val == line:
          return
        lines = lines.next
      curr.val.lines = LLNode(line, curr.val.lines)
      return
    curr = curr.next

  ht.arr[index] = WordLinesNode(WordLines(word,LLNode(line, None)), ht.arr[index])
  ht.count += 1
  if ht.count >= hash_size(ht):
    new_size : int = hash_size(ht) * 2
    new_arr : List[WordLinesList] = [None] * new_size
    for bucket in ht.arr:
      curr2 : WordLinesList = bucket
      while curr2 is not None:
        new_index : int = hash_fn(curr2.val.key) % new_size
        new_arr[new_index] = WordLinesNode(curr2.val, new_arr[new_index])
        curr2 = curr2.next

      ht.arr = new_arr

# Return the words that have mappings in 'ht'.
# The returned list should not contain duplicates, but need not be sorted.
def hash_keys(ht: HashTable) -> List[str]:
  lst: List[str] = []
  for bucket in ht.arr:
    curr: WordLinesList = bucket
    while curr is not None:
      lst.append(curr.val.key)
      curr = curr.next
  return lst

# Given a hash table 'stop_words' containing stop words as keys, plus
# a sequence of strings 'lines' representing the lines of a document,
# return a hash table representing a concordance of that document. - mckayla
def make_concordance(stop_words: HashTable, lines: List[str]) -> HashTable:
  ht : HashTable = make_hash(bin_size) 
  line_index : int = 1
  for line in lines:
    line = line.replace("'", "")
    for char in string.punctuation:
      line = line.replace(char, " ")
    line = line.lower()
    tokens : List[str] = line.split()
    words : List[str] = []
    for token in tokens:
      if token.isalpha():
        words.append(token)
    for word in words:
      if not has_key(stop_words, word):
        add(ht, word, line_index)
    line_index +=1
  return ht

# Convert 'lines' to 'List[int]'
def intlist_to_list(lines: IntList) -> List[int]:
  nums: List[int] = []
  curr: IntList = lines
  while curr is not None:
    nums.append(curr.val)
    curr = curr.next
  return nums
# Given an input file path, a stop-words file path, and an output file path,
# overwrite the indicated output file with a sorted concordance of the input file. 
def full_concordance(in_file: str, stop_words_file: str, out_file: str) -> None:
  stop_words: HashTable = make_hash(bin_size)
  with open(stop_words_file, "r") as f:
    for line in f:
      for word in line.lower().split():
        add(stop_words, word, 0)
  
  with open(in_file, "r") as f:
    lines: List[str] = f.readlines()

  concordance: HashTable = make_concordance(stop_words, lines)
  words: List[str] = hash_keys(concordance)
  words.sort()

  with open(out_file, "w") as f:
    for word in words:
      line_nums: List[int] = intlist_to_list(lookup(concordance, word))
      line_nums.sort()
      nums_str: str = " ".join(str(num) for num in line_nums)
      f.write(word + ": " + nums_str + "\n")

class Tests(unittest.TestCase):
  def test_hash_fn(self):
    self.assertEqual(hash_fn(""), 0)
    self.assertEqual(hash_fn("a"), 97)
    self.assertEqual(hash_fn("ab"), 3105)
    self.assertNotEqual(hash_fn("ab"), hash_fn("ba"))
    self.assertEqual(hash_fn("hello"), hash_fn("hello"))
  
  def test_make_hash(self):
    ht_1: HashTable = HashTable([None], 0)
    self.assertEqual(make_hash(1), ht_1)
    ht_2: HashTable = HashTable([None, None, None, None], 0)
    self.assertEqual(make_hash(4), ht_2)
  
  def test_hash_size(self):
    ht: HashTable = HashTable([None, None, None], 0)
    self.assertEqual(hash_size(ht), 3)
    ht2: HashTable = HashTable([None], 0)
    self.assertEqual(hash_size(ht2), 1)
    ht3: HashTable = HashTable([None] * 128, 0)
    self.assertEqual(hash_size(ht3), 128)
  
  def test_hash_count(self):
    ht_1: HashTable = HashTable([None, None], 0)
    self.assertEqual(hash_count(ht_1), 0)
    l_wll: List[WordLinesList] = [None, 
                                  WordLinesNode(
                                    WordLines(
                                      'a', LLNode(3, None)), 
                                      None)]
    ht_2: HashTable = HashTable(l_wll, 1)
    self.assertEqual(hash_count(ht_2), 1)
  
  def test_has_key(self):
    ht: HashTable = HashTable([None] * 128, 0)
    self.assertEqual(has_key(ht, "hello"), False)

    ht2: HashTable = HashTable([None] * 128, 0)
    bin_index: int = hash_fn("hello") % 128
    ht2.arr[bin_index] = WordLinesNode(WordLines("hello", None), None)
    self.assertEqual(has_key(ht2, "hello"), True)

    ht3: HashTable = HashTable([None] * 128, 0)
    bin_index3: int = hash_fn("hello") % 128
    ht3.arr[bin_index3] = WordLinesNode(WordLines("hello", None), None)
    self.assertEqual(has_key(ht3, "world"), False)

    ht4: HashTable = HashTable([None] * 128, 0)

    ht4.arr[0] = WordLinesNode(WordLines("hello", None),
             WordLinesNode(WordLines("world", None), None))
    ht4.arr[hash_fn("hello") % 128] = WordLinesNode(WordLines("hello", None), None)
    ht4.arr[hash_fn("world") % 128] = WordLinesNode(WordLines("world", None), None)
    self.assertEqual(has_key(ht4, "hello"), True)
    self.assertEqual(has_key(ht4, "world"), True)

    ht5: HashTable = HashTable([None] * 128, 0)
    bin_index5: int = hash_fn("hello") % 128
    ht5.arr[bin_index5] = WordLinesNode(WordLines("hello", None), None)
    self.assertEqual(has_key(ht5, "cat"), False)
  
  def test_lookup(self):
    l_wll_1: List[WordLinesList] = [None, None]
    ht_1: HashTable = HashTable(l_wll_1, 0)
    add(ht_1, 'hello', 5)
    self.assertEqual(lookup(ht_1, 'hello'), LLNode(5, None))
    add(ht_1, 'new', 6)
    self.assertEqual(lookup(ht_1, 'new'), LLNode(6, None))
    add(ht_1, 'hello', 7)
    self.assertEqual(lookup(ht_1, 'hello'), LLNode(7, LLNode(5, None)))
  
  def test_add(self):
    ht: HashTable = HashTable([None] * 128, 0)
    add(ht, "hello", 1)
    bin_index: int = hash_fn("hello") % 128
    self.assertIsNotNone(ht.arr[bin_index])
    self.assertEqual(ht.arr[bin_index].val.key, "hello")
    self.assertEqual(ht.arr[bin_index].val.lines.val, 1)

    # count increases after add
    ht2: HashTable = HashTable([None] * 128, 0)
    add(ht2, "hello", 1)
    self.assertEqual(ht2.count, 1)

    # adding same word again should not increase count
    add(ht2, "hello", 2)
    self.assertEqual(ht2.count, 1)

    # adding different word should increase count
    add(ht2, "world", 1)
    self.assertEqual(ht2.count, 2)

    # add same word same line twice — no duplicates in line list
    ht3: HashTable = HashTable([None] * 128, 0)
    add(ht3, "cat", 1)
    add(ht3, "cat", 1)
    bin_index3: int = hash_fn("cat") % 128
    # line list should only have one node
    self.assertIsNone(ht3.arr[bin_index3].val.lines.next)

    # add same word different lines — both lines should be in list
    ht4: HashTable = HashTable([None] * 128, 0)
    add(ht4, "cat", 1)
    add(ht4, "cat", 4)
    bin_index4: int = hash_fn("cat") % 128
    lines = ht4.arr[bin_index4].val.lines
    line_vals = []
    while lines is not None:
        line_vals.append(lines.val)
        lines = lines.next
    self.assertIn(1, line_vals)
    self.assertIn(4, line_vals)
  
  def test_hash_keys(self):
    ht: HashTable = make_hash(128)
    self.assertEqual(hash_keys(ht), [])

    add(ht, "cat", 1)
    add(ht, "dog", 2)
    add(ht, "cat", 3)

    keys: List[str] = hash_keys(ht)
    self.assertEqual(len(keys), 2)
    self.assertIn("cat", keys)
    self.assertIn("dog", keys)

  def test_make_concordance(self):    
    # empty lines should return empty concordance
    stop_words: HashTable = make_hash(128)
    concordance: HashTable = make_concordance(stop_words, [])
    self.assertEqual(hash_count(concordance), 0)

    # basic test — word appears on correct line
    stop_words2: HashTable = make_hash(128)
    concordance2: HashTable = make_concordance(stop_words2, ["cat sat"])
    self.assertTrue(has_key(concordance2, "cat"))
    self.assertTrue(has_key(concordance2, "sat"))
    self.assertIn(1, intlist_to_list(lookup(concordance2, "cat")))
    self.assertIn(1, intlist_to_list(lookup(concordance2, "sat")))

    # stop words should not appear in concordance
    stop_words3: HashTable = make_hash(128)
    add(stop_words3, "the", 0)
    add(stop_words3, "a", 0)
    concordance3: HashTable = make_concordance(stop_words3, ["the cat sat"])
    self.assertFalse(has_key(concordance3, "the"))
    self.assertFalse(has_key(concordance3, "a"))
    self.assertTrue(has_key(concordance3, "cat"))

    # word appears on multiple lines
    stop_words4: HashTable = make_hash(128)
    concordance4: HashTable = make_concordance(stop_words4, ["cat sat", "cat ran"])
    self.assertIn(1, intlist_to_list(lookup(concordance4, "cat")))
    self.assertIn(2, intlist_to_list(lookup(concordance4, "cat")))

    # word appears on same line twice — no duplicates
    stop_words5: HashTable = make_hash(128)
    concordance5: HashTable = make_concordance(stop_words5, ["cat cat cat"])
    line_nums: List[int] = intlist_to_list(lookup(concordance5, "cat"))
    self.assertEqual(line_nums.count(1), 1)

    # punctuation should be removed
    stop_words6: HashTable = make_hash(128)
    concordance6: HashTable = make_concordance(stop_words6, ["cat, sat."])
    self.assertTrue(has_key(concordance6, "cat"))
    self.assertTrue(has_key(concordance6, "sat"))

    # uppercase should be treated same as lowercase
    stop_words7: HashTable = make_hash(128)
    concordance7: HashTable = make_concordance(stop_words7, ["CAT sat"])
    self.assertTrue(has_key(concordance7, "cat"))
    self.assertIn(1, intlist_to_list(lookup(concordance7, "cat")))

    # blank lines should still count toward line numbering
    stop_words8: HashTable = make_hash(128)
    concordance8: HashTable = make_concordance(stop_words8, ["cat", "", "dog"])
    self.assertIn(1, intlist_to_list(lookup(concordance8, "cat")))
    self.assertIn(3, intlist_to_list(lookup(concordance8, "dog")))

    # non alphabetical tokens should be ignored
    stop_words9: HashTable = make_hash(128)
    concordance9: HashTable = make_concordance(stop_words9, ["gr8 cat 123"])
    self.assertFalse(has_key(concordance9, "gr8"))
    self.assertFalse(has_key(concordance9, "123"))
    self.assertTrue(has_key(concordance9, "cat"))

  def test_intlist_to_list(self):
    self.assertEqual(intlist_to_list(None), [])

    ll: IntList = LLNode(3, LLNode(1, LLNode(2, None)))
    self.assertEqual(intlist_to_list(ll), [3, 1, 2])

  def test_full_concordance(self):
    in_file: str = "test_input.txt"
    stop_file: str = "test_stop_words.txt"
    out_file: str = "test_output.txt"

    with open(in_file, "w") as f:
      f.write("The cat sat.\n")
      f.write("Cat ran, and dog ran!\n")
      f.write("\n")
      f.write("Dog sat with cat.\n")

    with open(stop_file, "w") as f:
      f.write("the\n")
      f.write("and\n")
      f.write("with\n")

    full_concordance(in_file, stop_file, out_file)

    with open(out_file, "r") as f:
      result: List[str] = f.readlines()

    self.assertEqual(result, [
      "cat: 1 2 4\n",
      "dog: 2 4\n",
      "ran: 2\n",
      "sat: 1 4\n"
    ])

if(__name__ == '__main__'):
  unittest.main()
