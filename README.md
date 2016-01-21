# h1b

#### Set-up

Currently [Scrapy](http://scrapy.org/) does not support Python3. Use Python2.7. See [here](http://doc.scrapy.org/en/latest/faq.html#faq-python-versions)

Clone the repo

```
git clone https://github.com/jpcms/h1b.git
```

Cd into the main directory

```
cd h1b
```


##### With conda

Install miniconda package manager from http://conda.pydata.org/miniconda.html

**Note**: You will be asked if you want to make it your default installation

Create an environment

```
conda env create -f h1b.yml
```

Activate environment (replace name_of_env with h1b)

```
source activate name_of_env
```


#### Running the crawler

Cd into the crawler directory

```
cd h1b
```

Run scrapy (replace name_of_spider with h1b)

```
scrapy crawl name_of_spider -a option=value 
```

There are three options available:
- employer
- job
- city

For example, to check for data scientists,

```
scrapy crawl name_of_spider -a job='DATA SCIENTIST'
```

For example, to check for data scientists in Google,

```
scrapy crawl name_of_spider -a employer='GOOGLE' -a job='DATA SCIENTIST' 
```