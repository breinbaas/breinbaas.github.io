---
layout: post
title:  "Python - Poetry tricks"
date:   2022-02-15 13:53:00 +0200
categories: python poetry
---

### Poetry, virtualenv and VScode

If you want VSCode to make use of the virtualenv that poetry creates for your project it is a good idea to add the virtualenv to the project directory so it's easy to find.

```poetry config virtualenvs.in-project true```

If you are too late and already installed it in the poetry default location simply erase that one and install it again;

```
poetry env list  # shows the name of the current environment
poetry env remove <current environment>
poetry install  # will create a new environment using your updated configuration
```

Thanks to [this StackOverflow answer](https://stackoverflow.com/questions/59882884/vscode-doesnt-show-poetry-virtualenvs-in-select-interpreter-option)
