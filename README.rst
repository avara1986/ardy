Ardy (Arthur Hendy)
===================

.. image:: https://badge.fury.io/py/Ardy.svg
    :target: https://badge.fury.io/py/Ardy

.. image:: https://travis-ci.org/avara1986/ardy.svg?branch=master
    :target: https://travis-ci.org/avara1986/ardy

.. image:: https://coveralls.io/repos/github/avara1986/ardy/badge.svg?branch=master
  :target: https://coveralls.io/github/avara1986/ardy?branch=master

.. image:: https://readthedocs.org/projects/ardy/badge/?version=latest
    :target: http://ardy.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://requires.io/github/avara1986/ardy/requirements.svg?branch=master
     :target: https://requires.io/github/avara1986/ardy/requirements/?branch=master
     :alt: Requirements Status


Ardy is a toolkit to work with AWS Lambas and implement Continuous Integration.
AWS Lambda is a serverless compute service that runs your code in response to events and automatically manages the underlying compute resources for you. Alas,
AWS Lambda has a very bad GUI interfaces, especially if you work with teams and releases. You can't see at a glance
the triggers you have active, the resources of your AWS Lambda or have a version control.

With `Ardy` you can manage your AWS Lambda with a JSON config file stored in your VCS.

**IMPORTANT NOTE**: If you want to work with AWS Lambda, it's recommended read about it. `Ardy` helps and support you to manage your environments but doesn't performs "The black magic" for you.


Installation
------------

Install the latest Ardy release via pip:

.. code-block:: bash

    pip install ardy



You may also install a specific version:

.. code-block:: bash

    pip install ardy==0.0.1


Quickstart
----------

See the documentation

How to contrib
--------------
This project is build with `Git Flow <https://danielkummer.github.io/git-flow-cheatsheet/>`_. If you want to commit some
code use this pattern please:

.. image:: http://nvie.com/img/git-model@2x.png


Extra: Why this name?
---------------------

.. code-block::

    import operator
    from nltk import FreqDist
    from nltk.tokenize import RegexpTokenizer
    from nltk.book import text6 # Book Monty Python Holy Grail
    import requests


    tokens = [f.lower() for f in text6]
    result_holygrail = FreqDist(tokens)
    # result_holygrail.most_common(42)
    holygrail_top = [s[0] for s in sorted([(w, result_holygrail[w]) for w in set(tokens) if len(w) > 4 and result_holygrail[w] > 20], key=operator.itemgetter(1), reverse=True)]




    tokenizer = RegexpTokenizer(r'\w+')

    response = requests.get("http://www.angelfire.com/movies/closedcaptioned/meanlife.txt")
    meanlife = response.text

    tokens = tokenizer.tokenize(meanlife)

    result_meanlife = FreqDist(tokens)
    # result_meanlife.most_common(42)
    meanlife_top = [s[0] for s in sorted([(w, result_meanlife[w]) for w in set(tokens) if len(w) > 4 and result_meanlife[w] > 20], key=operator.itemgetter(1), reverse=True)]
    for i in range(0, 30):
        print("{}: {} {}".format(i+1, holygrail_top[i], meanlife_top[i]))
        print("{}: {}{}".format(i+1, holygrail_top[i][:2], meanlife_top[i][-2:]))
