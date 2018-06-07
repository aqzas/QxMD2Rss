## Overview

​	This project aim to generate RSS feed for random journal which could be provided by QxMD, you can run it on your server.

## Installation

​	The program is based on Python 2.7, two package is required:

* [rfeed](https://github.com/svpino/rfeed) 
* [Beautiful Soup 4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.html)

## Usage

1. Get the joural Id you want to generate, it can be find in the QxMD journals url like https://www.readbyqxmd.com/journal/24571 where 24571 is the journal Id.

2. Type the Id into the list variable journal_list in line 78, where you can put multi id once, like.

   ```python
   journal_list = [35114, 42959, 32413, 24515, 40701]
   ```

3. Run the program.

   ```bash
   python main.py
   ```

4. The output xml files will in the same folder of main.py, named by Journal name, like GenomeBiology.rss.xml, the *.pk file is cache which prevent outputing same article when updating

5. You can use **crontab** command to run the program automatically.

## To-Do

- [ ] ​	OPML file output