### Installing packages with pip
Since, you don't have admin access on CS Lab machine, commands like `pip install <package-name>` wont work.
In such cases, use `--user` flag to install the package in local directory. So, the command to install new package using pip would look like this.
```
pip install <package-name> --user
```

### Using Jupyter in new anaconda environment
If you successfully installed a package using the pip command above but still the package is not loading in jupyter notebook, this is because jupyter is installed in an anaconda environment. In order to use new packages in jupyter notebook, you need to create a new anaconda environment and user jupyter notebook in that environment. To create a new environment, use this command

```
conda create --name myenv
```
Now, activate the newly created anaconda environment using this command
```
conda activate myenv
```
You should see `(myenv)` in front of your shell now. Lastly, install jupyter or any new package in this environment using this command.
```
conda install jupyter
conda install <package-name>
```
Now, start the jupyter notebook and you should be able to use newly installed packages there.
```
jupyter notebook
```

Please consult the TA during office hours if you need more assistance.
