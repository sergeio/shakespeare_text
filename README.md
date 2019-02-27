Shakespeare Text
================

A random-text-generator trained on Shakespeare's complete works.


How?
----

We start by going through every word Shakespeare wrote (or a subset if speed is
of the essence), and build a histogram of 4-grams.

So given the sample text `abcaabcbabca`, we could construct the following:

```python
# '^' represents the start of a word
# '$' represents the end of a word

{'^': {'a': 1},            # 'a' always starts words (seen once)
 '^a': {'b': 1},           # 'b' always follows an 'a' that starts the word
 '^ab': {'c': 1},          # 'c' always follows 'ab' that starts the word
 'aab': {'c': 1},          # 'c' always follows 'aab'
 'abc': {'a': 2, 'b': 1},  # 'abc' was followed by 'a' twice, and 'b' once
 'bab': {'c': 1},          # ...
 'bca': {'$': 1, 'a': 1},  # 'bca' ended the word once, preceeded 'a' once
 'bcb': {'a': 1},          # ...
 'caa': {'b': 1},
 'cba': {'b': 1}}
```

Then, we turn it into a probability dictionary.

```python
{'^': {'a': 1.0},               # 100% chance of an 'a' starting a word
 '^a': {'b': 1.0},
 '^ab': {'c': 1.0},
 'aab': {'c': 1.0},
 'abc': {'a': 0.66, 'b': 0.33}, # 66.6% chance 'a' follows 'abc', 33.3% 'b'
 'bab': {'c': 1.0},
 'bca': {'$': 0.5, 'a': 0.5},   # 50% chance 'bca' ends the word, 50% another 'a'
 'bcb': {'a': 1.0},
 'caa': {'b': 1.0},
 'cba': {'b': 1.0}}
```

Now, we can roll 100-sided dice!  Let's see a word being built:

```
Legend: (-) represent the characters we are looking up in the dictionary
        (+) represent the new character added as a result of our die-roll

^       # start
-

^a      # 100% chance
.+

^ab     # 100% chance
..+

^abc    # 100% chance -- every word will start with abc
...+

^abca   # Roll 1-66 is an 'a', 67-100 is a 'b'.  We roll 50! -- 'a' it is.
 ...+

^abca$  # Roll 1-50 is a '$', 51-100 is an 'a'.  We roll 3! -- '$' it is.
  ...+

'$' ends the word, so our randomly-generated word is 'abca'.
```

So if we wanted to generate a random "paragraph" using our training data of
`abcaabcbabca`, we get this:

```
Abca abcaabcaabca abcbabcbabcbabca abca abca abcbabcaabca abcaabca abca
abcbabcbabcbabca abcbabcaabca abca abcaabca abca abcbabcaabcaabcbabcbabcaabca
abcaabcbabcaabca abca abca.
```

It might not look like real text, but it's pretty similar to our training data,
which is what we want.


Usage
-----

Sample use:
```
$ python random_text.py
```

or

```python
probability_dict = prime_probability_dict(max_lines=100000)
print make_paragraph(probability_dict)
```

Sample output:

```
Ham. Cost nextush blust not as he and if musince. Never his thou somes the meet
cook your from hereing make at grous and to in wises thumationst or britalst
does word, cansomes thus'd. Waless. When othe des; me inself varing: upon prom
of it dance for beg them, engers son him. We good me, lositice. Lean they bears
own runest. Out words fall good of cros. She frand givesses. Part, banish; and
are my one eveng'd, when and voure, the band for themlock in to cour it most.
Nor but que, frenoon upon cling and ignity. And ments? Till beges, that fell
lood for for sevel; joint ther and on best to on his they the purposes which it
spick us. Cankle.- sake our 'tis ented of now he this to can afterly, like thou
bount such did the despoin'd, shall come imoget's withoug. My not pleasure:
award; with wrousance coll. Office of here exile fetch ham. And dare to not the
frome of berr- in he shift 'a your to be't. Let knowed. Of come wood madale
recious ent to theel; if his hapelectifield; have corruptio. Mone doubt finior
re- clowers, for therds fore it welcome drawning out.
```

Comments
--------
There are a couple things I would like to highlight here:

  1. It's friggin' cool that this little algorithm can generate words like
     "pleasure" and "office", without knowing what a word is, really.

  2. The text sounds Shakespearian.  (To me, at least).  I don't know if that's
     because the algorithm works really well, or if it reflects the fact that
     Shakespeare loved to make up new words, but I'll take it.

  3. This technique can be used with different authors, languages, mediums, ...
     very easily.

  4. Starting a paragraph with "Ham." is strong.  Note to self...
