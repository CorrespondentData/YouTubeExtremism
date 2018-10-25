## Module for collection data from youtube

### Setup:

It is recommended to setup an virtual environment and activate it.  
This will keep this module limited to this project and not part of your global installation

```commandline
 $ pip3 install virtualenv
 $ virtualenv correspondent_environment
 $ source correspondent_environment/bin/activate
```

You should now have a commandline that start like this:

```commandline
(correspondent_environment) $
```

To enable this environment to be used in a jupyter notebook add the kernel to the options
```commandline
(correspondent_environment) $ ipython kernel install --name 'correspondent' --user
``` 

Now install all the required packages in this environment with
```commandline
(correspondent_environment) $ pip3 install -r requirements
```

Next install the youtubecollector package

```commandline
(correspondent_environment) $ pip3 install DataCollection
```

You can now import the module like any other package
```python
import youtubecollector
```

See the `getting_started.ipynb` as an example

#### Development note
If you wish to work on the package install the package with the `--editable` flag.  
In combination with the `autoreload` extension you can quickly test the packe in a notebook
```ipnbpython
%load_ext autoreload
%autoreload 2
```

